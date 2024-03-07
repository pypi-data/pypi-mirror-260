import asyncio
from collections.abc import Callable
from copy import deepcopy

import numpy as np
from arcGisFeatureCache import ArcGisFeatureService
from loguru import logger
from shapely import LineString, MultiLineString, Polygon, STRtree

from kmService.models import KmPunt, KmRaai, KmSubGeocode, KmValueObject, KmVlak
from kmService.uitils.shapleyTools import extend_line


class KmServiceBuilder:
    """
    A builder class for constructing KmService instances.

    Attributes:
        value_objects_dict (dict): A dictionary containing key-value pairs of identifier and KmValueObject.
        _matched (dict): A dictionary containing matched KmPunt and KmRaai objects.
        url (str): The URL for the ArcGIS feature service.
        feature_service (ArcGisFeatureService | None): An instance of ArcGisFeatureService.
        _km_vlakken (list): A list of KmVlak objects.
        _km_raaien (list): A list of KmRaai objects.
        _km_punten (list): A list of KmPunt objects.
        _sub_geocode (list): A list of KmSubGeocode objects.
    """

    def __init__(self):
        self.value_objects_dict: dict[str, KmValueObject] = {}
        self._matched: dict[str, tuple[KmPunt, KmRaai]] = {}
        self.url: str = ""
        self.feature_service: ArcGisFeatureService | None = None
        self._km_vlakken: list[KmVlak] = []
        self._km_raaien: list[KmRaai] = []
        self._km_punten: list[KmPunt] = []
        self._sub_geocode: list[KmSubGeocode] = []

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_transport"]
        return state

    @classmethod
    async def factory(cls, url):
        """
        Factory method to create an instance of KmServiceBuilder.

        Args:
            url (str): The URL for the ArcGIS feature service.

        Returns:
            KmServiceBuilder: An instance of KmServiceBuilder.
        """
        self = KmServiceBuilder()
        self.url = url
        self.feature_service = await ArcGisFeatureService.factory(self.url)
        await self._process()
        return self

    async def _process(self):
        """
        Processes the ArcGIS feature service.
        """
        feature_info = {
            "Kilometerlintvlak": {
                "attributes": ["OBJECTID", "KMLINT", "KMLINT_OMSCHRIJVING"],
                "data_class": KmVlak,
                "data_list": self._km_vlakken,
            },
            "Raai": {
                "attributes": ["OBJECTID", "GEOCODE", "SUBCODE", "HECTOMETER"],
                "data_class": KmRaai,
                "data_list": self._km_raaien,
            },
            "Hectometerpunt (geocode)": {
                "attributes": [
                    "OBJECTID",
                    "GEOCODE",
                    "SUBCODE",
                    "KM_GEOCODE",
                    "KMLINT",
                    "KMLINT_OMSCHRIJVING",
                ],
                "data_class": KmPunt,
                "data_list": self._km_punten,
            },
            "Geocodesubgebied": {
                "attributes": ["OBJECTID", "GEOCODE", "SUBCODE", "NAAM"],
                "data_class": KmSubGeocode,
                "data_list": self._sub_geocode,
            },
        }

        tasks = []
        for feature_type in feature_info.keys():
            tasks.append(
                self._process_features(
                    feature_type,
                    feature_info[feature_type]["data_list"],
                    feature_info[feature_type]["data_class"],
                    feature_info[feature_type]["attributes"],
                )
            )
        await asyncio.gather(*tasks)

        await self.match_all_km_points_km_raai()

    async def _process_features(self, feature_type, data_list, data_class, attributes):
        """
        Processes the features of a specific type.

        Args:
            feature_type (str): The type of feature.
            data_list (list): The list to store the processed data.
            data_class (class): The class of the data.
            attributes (list): The attributes of the feature.
        """

        async def process_feature_item(item):
            _ = [item.attributes.get_value(attr) for attr in attributes]
            data_list.append(data_class(*_, geometry=item.geometry))

        if self.feature_service:
            logger.info(f"process {feature_type} layer")
            await asyncio.gather(
                *[
                    process_feature_item(item)
                    for item in self.feature_service.get_all_features([feature_type])
                ]
            )
        else:
            logger.error("no feature service")

    async def _create_value_object_sub_geocode_km_vlakken(
        self,
    ) -> dict[str, KmValueObject]:
        """
        Creates value objects for sub geocode and km vlakken.

        Returns:
            dict: A dictionary containing key-value pairs of identifier and KmValueObject.
        """

        async def builder(sub_geocode: KmSubGeocode, km_vlak: KmVlak):
            """
            Builds value objects for sub geocode and km vlakken.

            Args:
                sub_geocode (KmSubGeocode): The sub geocode object.
                km_vlak (KmVlak): The km vlak object.

            Returns:
                dict: A dictionary containing key-value pairs of identifier and KmValueObject.
            """
            _ = {}
            if sub_geocode.geometry.intersects(km_vlak.geometry):
                intersection = sub_geocode.geometry.intersection(km_vlak.geometry)
                tester = KmValueObject(intersection, km_vlak, sub_geocode)

                if isinstance(intersection, Polygon):
                    logger.success(f"created sub geocode km lint vlak {tester}")
                    _[
                        f"{sub_geocode.geo_code}_{sub_geocode.sub_code}_{km_vlak.km_lint_naam}"
                    ] = tester

                elif isinstance(intersection, LineString | MultiLineString):
                    logger.info(f"builder returns no polygon: {tester}")
            return _

        tasks = [
            builder(sub_geocode, km_vlak)
            for sub_geocode in self._sub_geocode
            for km_vlak in self._km_vlakken
        ]
        feature_data = await asyncio.gather(*tasks)
        out_dict = {k: v for d in feature_data for k, v in d.items()}

        return out_dict

    @staticmethod
    async def _match_km_punt_with_raai(km_punt_dict: dict, km_raai_dict: dict) -> dict:
        """
        Matches KmPunt objects with KmRaai objects.

        Args:
            km_punt_dict (dict): A dictionary containing KmPunt objects.
            km_raai_dict (dict): A dictionary containing KmRaai objects.

        Returns:
            dict: A dictionary containing matched KmPunt and KmRaai objects.
        """
        km_and_raai_match_dict = {}

        for key, value in km_punt_dict.items():
            # todo make async
            possible_match = []
            try:
                possible_match = km_raai_dict[
                    f"{value[0].geo_code}_{value[0].sub_code}"
                ]
            except KeyError:
                logger.warning(f"no raai for {value[0].geo_code}_{value[0].sub_code}")

            if possible_match is None:
                logger.warning(f"no raai for {value[0].geo_code}_{value[0].sub_code}")
            else:
                for item in value:
                    match_raai = [
                        item2
                        for item2 in possible_match
                        if item2.hectometer == item.hectometer
                    ]
                    assert len(match_raai) <= 1, "should be zero or one result"

                    key = f"{item.geo_code}_{item.sub_code}_{item.km_lint}"
                    if key not in km_and_raai_match_dict:
                        km_and_raai_match_dict[key] = [
                            [item, match_raai[0] if match_raai else None]
                        ]
                    else:
                        km_and_raai_match_dict[key].append(
                            [item, match_raai[0] if match_raai else None]
                        )

        return km_and_raai_match_dict

    @staticmethod
    async def correct_km_raai(km_and_raai_match_dict: dict) -> None:
        """
        Corrects KmRaai objects.

        Args:
            km_and_raai_match_dict (dict): A dictionary containing matched KmPunt and KmRaai objects.
        """

        async def process_item(km, raai):
            if not raai:
                logger.warning(f"no raai for {km}")
            else:
                projected_point = raai.geometry_extended.interpolate(
                    raai.geometry_extended.project(km.geometry)
                )
                dx = km.geometry.x - projected_point.x
                dy = km.geometry.y - projected_point.y

                moved_line = LineString(
                    [(x + dx, y + dy) for x, y in raai.geometry_extended.coords]
                )

                distance = moved_line.distance(raai.geometry_extended)

                raai.geometry_corrected = moved_line
                logger.info(
                    f"km raai {raai} matched and moved to km punt, "
                    f"old distance to line: {round(distance, 3)}, "
                    f"new distance to line: {round(km.geometry.distance(moved_line), 3)}",
                    data={
                        "original_line": raai.geometry_extended,
                        "moved_line": moved_line,
                    },
                )

        tasks = []
        for key, value in km_and_raai_match_dict.items():
            tasks.extend([process_item(km, raai) for km, raai in value])
        await asyncio.gather(*tasks)

    @staticmethod
    async def _create_dict_from_list(items: list, key_function: Callable) -> dict:
        """
        Creates a dictionary from a list of items.

        Args:
            items (list): The list of items.
            key_function (Callable): A function to generate keys.

        Returns:
            dict: A dictionary containing the items.
        """
        result_dict: dict = {}
        for item in items:
            # todo make async
            key = key_function(item)
            if key in result_dict:
                result_dict[key].append(item)
            else:
                result_dict[key] = [item]
        return result_dict

    async def match_all_km_points_km_raai(self):
        """
        Matches all KmPunt objects with KmRaai objects.
        """
        sub_geocode_km_vlakken = (
            await self._create_value_object_sub_geocode_km_vlakken()
        )
        logger.info("Create km punten and raaien dicts")
        km_punt_dict = await self._create_dict_from_list(
            self._km_punten,
            lambda km_punt: f"{km_punt.geo_code}_{km_punt.sub_code}_{km_punt.km_lint}",
        )
        km_raai_dict = await self._create_dict_from_list(
            self._km_raaien, lambda km_raai: f"{km_raai.geo_code}_{km_raai.sub_code}"
        )
        self._matched = await self._match_km_punt_with_raai(km_punt_dict, km_raai_dict)
        await self.correct_km_raai(self._matched)

        # add to value object
        for key, value in self._matched.items():
            if key in sub_geocode_km_vlakken:
                sub_geocode_km_vlakken[key].km_punten = [
                    p[0] for p in value if p[0] is not None
                ]
                sub_geocode_km_vlakken[key].km_raaien = [
                    p[1] for p in value if p[1] is not None
                ]
                sub_geocode_km_vlakken[key].matched = value
            else:
                raise ValueError("no split sub geocodes")  # noqa TRY003

        self.value_objects_dict = sub_geocode_km_vlakken

        # check if no other raai is laying on the km_point, takes way to ling, use tree to get all objects with in 1m, filter on raai.
        temp = []
        temp_2 = {}
        for key, value in self.value_objects_dict.items():
            for item in value.km_raaien:
                temp.append(item)
                temp_2[item.object_id] = item

        # make sure this is done before cutting raaien on sub geocode
        tree = STRtree([record.geometry_corrected for record in temp])
        tree_keys = np.array([record.object_id for record in temp])

        for key, value in self.value_objects_dict.items():
            for item in value.matched:
                if not item[1]:
                    # todo: create tree of all raaien on corrected geometry
                    query = tree.query(
                        item[0].geometry, predicate="dwithin", distance=100
                    )
                    keys = tree_keys.take(query).tolist()
                    tester = [temp_2[item] for item in keys]
                    for _ in tester:
                        if _.hectometer == item[0].hectometer:
                            __ = deepcopy(_)
                            __.geometry_corrected = extend_line(__.geometry, 50)
                            item[1] = __

        # corrected cut on sub geocode polygon
        for key, value in self.value_objects_dict.items():
            for item in value.km_raaien:
                tester = value.geometry.intersection(item.geometry_corrected)
                item.geometry_corrected = tester
