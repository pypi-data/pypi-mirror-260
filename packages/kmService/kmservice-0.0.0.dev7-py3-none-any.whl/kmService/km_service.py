import asyncio
import math
from dataclasses import dataclass

from shapely.geometry import LineString, Point

from kmService.km_service_builder import KmServiceBuilder
from kmService.models import KmRaai, KmValueObject

# todo: massive refactor before production


@dataclass
class KmResponse:
    """
    Data class representing a kilometer response.

    Attributes:
        hm (int, optional): The hectometer value.
        distance (float, optional): The distance value.
        km_lint_naam (str, optional): The kilometer lint name.
        km_lint_omschrijving (str, optional): The kilometer lint description.
        geocode (int, optional): The geocode value.
        geocode_sub (str, optional): The sub geocode value.
        geocode_naam (str, optional): The geocode name.
            xy (Point, optional): The point value.

    """

    hm: float | None = None
    distance: float | None = None
    km_lint_naam: str | None = None
    km_lint_omschrijving: str | None = None
    geocode: int | None = None
    geocode_sub: str | None = None
    geocode_naam: str | None = None
    _raai: KmRaai | None = None
    xy: Point | None = None

    @property
    def km_value_str(self) -> str:
        """
        Computes the kilometer value string.

        Returns:
            str: The kilometer value string.
        """
        if self.distance:
            distance = math.floor(self.distance)
            if distance > 100:
                return f"km {self.hm:.3f} +{distance}"
            else:
                if distance < 10:
                    return f"km {self.hm:.1f}0{distance}"
                else:
                    return f"km {self.hm:.1f}{distance}"
        else:
            return "no km"

    @property
    def raai_geometry(self) -> LineString:
        """
        Retrieves the kilometer Raai geometry.

        Returns:
            LineString: The kilometer Raai geometry.
        """
        if self._raai:
            return self._raai.geometry_corrected
        else:
            return LineString()

    @property
    def raai_hm(self) -> str:
        """
        Retrieves the hectometer string of the kilometer Raai.

        Returns:
            str: The hectometer string of the kilometer Raai.
        """
        if self._raai:
            return self._raai._hectometer_str
        else:
            return "None"


class KmService:
    """
    A service class for calculating kilometers and related features.

    """

    def __init__(self):
        self._value_objects_dict: dict[str, KmValueObject] = {}

    @classmethod
    async def factory(cls):
        """
        Factory method to create an instance of KmService.

        Returns:
            KmService: An instance of KmService.
        """
        self = cls()
        km_service = await KmServiceBuilder.factory(
            "https://maps.prorail.nl/arcgis/rest/services/Referentiesysteem/FeatureServer"
        )
        self._value_objects_dict = km_service.value_objects_dict

        return self

    async def _get_raai(self, point: Point) -> list[KmResponse]:
        """
        Retrieves kilometer responses based on the provided point.

        Args:
            point (Point): The point to calculate kilometer responses for.

        Returns:
            list[KmResponse]: A list of kilometer responses.
        """

        async def process(point_, item_):
            """
            Process the kilometer response for the given point and item.

            Args:
                point_ (Point): The point to check.
                item_ (object): The item containing kilometer information.

            Returns:
                KmResponse: The kilometer response.
            """
            if point_.within(item_.geometry):
                response = KmResponse(
                    km_lint_naam=item_.km_vlak.km_lint_naam,
                    km_lint_omschrijving=item_.km_vlak.km_lint_omschrijving,
                    geocode=int(item_.sub_geocode.geo_code),
                    geocode_sub=item_.sub_geocode.sub_code,
                    geocode_naam=item_.sub_geocode.naam,
                )
                distance_raai_to_point = dict(
                    sorted(
                        {
                            _.geometry_corrected.distance(point): _
                            for _ in item_.km_raaien
                        }.items()
                    )
                )
                first_two = [
                    distance_raai_to_point[k] for k in list(distance_raai_to_point)[:2]
                ]
                if first_two[0].hectometer < first_two[1].hectometer:
                    response._raai = first_two[0]
                    return response
                else:
                    response._raai = first_two[1]
                    return response

        tasks = []
        tasks.extend(
            [process(point, item) for item in self._value_objects_dict.values()]
        )
        result = await asyncio.gather(*tasks)
        return [item for item in result if item is not None]

    async def _get_km_async(self, x: float, y: float):
        """
        Retrieves kilometer responses based on the provided coordinates.

        Args:
            x (float): The x-coordinate.
            y (float): The y-coordinate.

        Returns:
            list[KmResponse]: A list of kilometer responses.
        """

        # todo: add line to raai so we can se measure length

        _ = []
        point = Point(x, y)
        responses = await self._get_raai(point)
        for response in responses:
            projection_point = response.raai_geometry.interpolate(
                response.raai_geometry.project(point)
            )
            if response._raai is not None:
                hm = response._raai.hectometer
            else:
                hm = 0.0

            response.hm = hm

            response.xy = point

            distance = projection_point.distance(point)
            response.distance = distance

            _.append(response)
        return _

    def get_km(self, x: float, y: float):
        """
        Retrieves kilometer responses based on the provided coordinates.

        Args:
            x (float): The x-coordinate.
            y (float): The y-coordinate.

        Returns:
            list[KmResponse]: A list of kilometer responses.
        """
        pass

    def get_km_by(self, point_list: list[list[float]]):
        pass

    #
    # async def get_point(
    #     self, lintnaam: str, km: float, m: int, line_geometry: LineString
    # ):
    #     features = []
    #     features.append(
    #         GeoJsonFeature(
    #             [ShapelyTransform.rd_to_wgs(line_geometry)],
    #             {"type": "input_line_geometry"},
    #         )
    #     )
    #
    #     posible_matches = list(
    #         itertools.chain.from_iterable(
    #             [
    #                 value.km_raaien
    #                 for key, value in self._value_objects_dict.items()
    #                 if key.endswith(lintnaam)
    #             ]
    #         )
    #     )
    #
    #     # Initialize variables to hold the objects before and after the input value
    #     object_before = None
    #     object_after = None
    #     input_value = km
    #     # Iterate through the list of objects
    #
    #     # Initialize variables to hold the minimum differences
    #     min_difference_before = float("inf")
    #     min_difference_after = float("inf")
    #
    #     raai_to_project_from = [obj for obj in posible_matches if obj.hectometer == km][
    #         0
    #     ]
    #     features.append(
    #         GeoJsonFeature(
    #             [ShapelyTransform.rd_to_wgs(raai_to_project_from.geometry_corrected)],
    #             {"type": "raai_to_project_from"},
    #         )
    #     )
    #
    #     # Iterate through the list of objects
    #     for obj in posible_matches:
    #         difference = abs(obj.hectometer - input_value)
    #         if obj.hectometer < input_value and difference < min_difference_before:
    #             min_difference_before = difference
    #             object_before = obj
    #         elif obj.hectometer > input_value and difference < min_difference_after:
    #             min_difference_after = difference
    #             object_after = obj
    #
    #     # Check if objects were found before and/or after the input value
    #     if object_before:
    #         print("Object before:", object_before.hectometer)
    #     else:
    #         print("No object before")
    #
    #     if object_after:
    #         print("Object after:", object_after.hectometer)
    #     else:
    #         print("No object after")
    #     features.append(
    #         GeoJsonFeature(
    #             [ShapelyTransform.rd_to_wgs(object_before.geometry_corrected)],
    #             {"type": "object_before"},
    #         )
    #     )
    #
    #     # Define the reference line
    #     reference_line = raai_to_project_from.geometry_corrected
    #     features.append(
    #         GeoJsonFeature(
    #             [ShapelyTransform.rd_to_wgs(reference_line)], {"type": "reference_line"}
    #         )
    #     )
    #
    #     # Define the target line
    #     target_line = object_after.geometry_corrected
    #     features.append(
    #         GeoJsonFeature(
    #             [ShapelyTransform.rd_to_wgs(target_line)], {"type": "target_line"}
    #         )
    #     )
    #
    #     # Find the nearest points on both lines
    #     nearest_point_on_reference, nearest_point_on_target = nearest_points(
    #         reference_line, target_line
    #     )
    #
    #     # Calculate the vector from the reference line's starting point to the nearest point on the target line
    #     dx_nearest = nearest_point_on_target.coords[0][0] - reference_line.coords[0][0]
    #     dy_nearest = nearest_point_on_target.coords[0][1] - reference_line.coords[0][1]
    #     unit_direction_nearest = np.array([dx_nearest, dy_nearest]) / np.linalg.norm(
    #         [dx_nearest, dy_nearest]
    #     )
    #
    #     # Determine the direction perpendicular to the target line at the nearest point
    #     # perpendicular_dir_nearest = np.array([-dy_nearest, dx_nearest])
    #     # unit_perpendicular_dir_nearest = perpendicular_dir_nearest / np.linalg.norm(
    #     #     perpendicular_dir_nearest
    #     # )
    #
    #     # Define the distance to move the reference line
    #     distance = (
    #         m + 0.001 if m != 0 else m
    #     )  # Adjust it a bit so it is not just under.
    #
    #     # Move the reference line towards the target line
    #     movement_vector_nearest = unit_direction_nearest * distance
    #     moved_reference_line = translate(
    #         reference_line, movement_vector_nearest[0], movement_vector_nearest[1]
    #     )
    #     features.append(
    #         GeoJsonFeature(
    #             [ShapelyTransform.rd_to_wgs(moved_reference_line)],
    #             {"type": "moved_reference_line"},
    #         )
    #     )
    #
    #     print("Original Reference Line:", reference_line)
    #     print("Moved Reference Line:", moved_reference_line)
    #
    #     point = line_geometry.intersection(moved_reference_line)
    #     features.append(
    #         GeoJsonFeature([ShapelyTransform.rd_to_wgs(point)], {"type": "point"})
    #     )
    #
    #     fc = GeoJsonFeatureCollection(features)
    #     tester = dumps(fc)
    #     print(tester)
    #
    #     return point

    # def generate_geojson_output(self) -> str:
    #     """
    #     Generates GeoJSON output based on the data stored in KmService.
    #
    #     Returns:
    #         str: A GeoJSON string representing the data.
    #     """
    #     colors = [
    #         "#1F77B4",
    #         "#AEC7E8",
    #         "#FF7F0E",
    #         "#FFBB78",
    #         "#2CA02C",
    #         "#98DF8A",
    #         "#FF9896",
    #         "#9467BD",
    #         "#C5B0D5",
    #         "#8C564B",
    #         "#C49C94",
    #         "#E377C2",
    #         "#F7B6D2",
    #         "#7F7F7F",
    #         "#C7C7C7",
    #         "#BCBD22",
    #         "#DBDB8D",
    #         "#17BECF",
    #         "#9EDAE5",
    #     ]
    #
    #     features = []
    #     for key, value in self._value_objects_dict.items():
    #         picked_color = random.choice(colors)
    #         features.append(
    #             GeoJsonFeature(
    #                 [ShapelyTransform.rd_to_wgs(value.geometry)],
    #                 {
    #                     "color": picked_color,
    #                     "fill-color": "transparent",
    #                     "fill-opacity": 0.5,
    #                 },
    #             )
    #         )
    #
    #         for item in value.matched:
    #             if not item[1]:
    #                 features.append(
    #                     GeoJsonFeature(
    #                         [ShapelyTransform.rd_to_wgs(item[0].geometry)],
    #                         {"color": "red", "radius": "5px"},
    #                     )
    #                 )  # | item[0].__dict__))
    #             else:
    #                 features.append(
    #                     GeoJsonFeature(
    #                         [ShapelyTransform.rd_to_wgs(item[0].geometry)],
    #                         {"color": picked_color, "radius": "1px"},
    #                     )
    #                 )
    #
    #                 # features.append(GeoJsonFeature([ShapelyTransform.rd_to_wgs(item[1].geometry_extended)], {"color": "#5c5c5c"}))
    #                 features.append(
    #                     GeoJsonFeature(
    #                         [ShapelyTransform.rd_to_wgs(item[1].geometry)],
    #                         {"color": "#c9c9c9"},
    #                     )
    #                 )
    #                 features.append(
    #                     GeoJsonFeature(
    #                         [ShapelyTransform.rd_to_wgs(item[1].geometry_corrected)],
    #                         {"color": picked_color},
    #                     )
    #                 )
    #     _ = dumps(GeoJsonFeatureCollection(features))
    #     with open("output.geojson", "w") as text_file:
    #         text_file.write(_)
    #     return _
    #


def get_km_service() -> KmService:
    """
    Retrieves an instance of KmService using asyncio.

    Returns:
        KmService: An instance of KmService.
    """
    return asyncio.run(KmService.factory())


async def main():
    km_service = await KmService.factory()

    tester = km_service.geojson()
    print(tester)

    _ = [
        [176186.3034, 362277.276],
        [176167.4443, 362276.1518],
        [176290.652, 362255.5943],
        [176267.8789, 362260.7968],
        [176248.7935, 362269.5774],
    ]
    for item in _:
        response = await km_service._get_km_async(item[0], item[1])
        print(response[0].km_value_str)

    print()
    # km_service = await KmServiceBuilder.factory(
    #     "https://maps.prorail.nl/arcgis/rest/services/Referentiesysteem/FeatureServer"
    # )

    #
    # line_geometry = gml_linestring_to_shapely(
    #     "91156.257,395575.682,4.464 91168.873,395588.364,4.432 91176.474,395596.14,4.445 91188.49,395608.862,4.445 91200.222,395621.892,4.491 91210.813,395634.068,4.533 91220.757,395645.905,4.563 91228.634,395655.6,4.607 91241.441,395671.913,4.654 91251.124,395684.733,4.69 91262.942,395700.931,4.7 91270.549,395711.665,4.747 91276.394,395720.207,4.75 91282.57,395729.436,4.774 91292.933,395745.425,4.819 91303.652,395762.766,4.854 91309.927,395773.25,4.882 91316.317,395784.267,4.914 91320.333,395791.379,4.898 91327.674,395804.736,4.969 91334.304,395817.16,4.976 91337.216,395822.819,4.964 91343.448,395835.101,5.004 91348.864,395846.172,5.015 91354.548,395858.099,5.042 91360.109,395870.199,5.05 91369.725,395891.832,5.077 91382.931,395922.667,5.1 91437.481,396052.406,5.281 91451.545,396085.609,5.356 91459.494,396104.064,5.389 91465.459,396117.567,5.402 91471.055,396129.807,5.415 91477.166,396142.804,5.434 91482.817,396154.246,5.448 91490.476,396169.271,5.442 91496.856,396180.799,5.468 91510.335,396204.071,5.488 91521.398,396221.472,5.507 91531.843,396237.018,5.53 91539.565,396247.986,5.539 91548.283,396260.009,5.592 91557.564,396271.965,5.563 91569.123,396286.308,5.606 91581.43,396300.83,5.679 91589.576,396309.894,5.727 91597.224,396318.186,5.723 91605.179,396326.527,5.773 91617.548,396339.031,5.749 91630.165,396351.297,5.966 91644.22,396364.574,5.776 91701.102,396417.399,5.816 91744.942,396457.892,5.877 91836.809,396542.578,5.963 91883.439,396585.743,5.879 91892.934,396594.385,5.852 91970.184,396665.639,5.795 91972.773,396667.906,5.82 92121.68,396805.649,5.748 92330.797,396998.696,5.574 92539.913,397191.743,4.708 92592.711,397240.368,4.502 92636.827,397281.165,4.345 92701.234,397340.554,4.166 92716.74,397354.985,4.134 92817.861,397448.217,3.889 92954.761,397574.642,3.718 92965.198,397584.14,3.711 93014.794,397630.015,3.923 93190.063,397791.745,3.572 93365.331,397953.476,3.788 93395.542,397981.534,3.843 93423.971,398007.8,3.903 93430.992,398014.078,3.912 93438.925,398021.569,3.897 93467.568,398047.815,3.974 93491.619,398070.161,3.989 93532.275,398107.72,4.047 93542.802,398117.318,4.099 93723.773,398284.281,4.697 93904.744,398451.244,4.552 94085.714,398618.206,4.525 94266.685,398785.169,4.459 94538.318,399035.585,3.963 94755.006,399235.498,3.407 94823.658,399298.613,3.148 94829.509,399304.169,3.14 94861.167,399333.442,3.079 94931.446,399398.223,2.882 94938.202,399404.295,2.878 94972.174,399435.975,2.755 95004.06,399465.235,2.626 95023.93,399483.663,2.538 95036.353,399494.949,2.524 95052.496,399509.819,2.496 95058.942,399515.842,2.458 95087.273,399541.897,2.375 95109.057,399562.2,2.305 95115.693,399568.214,2.316 95123.922,399575.921,2.257 95140.638,399591.299,2.216 95151.286,399600.977,2.183 95178.245,399625.894,2.1 95201.522,399647.151,2.025 95282.014,399721.144,1.916 95361.07,399794.089,1.796 95382.737,399814.204,1.819 95402.918,399832.705,1.821 95430.738,399858.373,1.805 95466.927,399891.872,1.881 95476.632,399900.715,1.905 95499.414,399921.859,1.924 95535.115,399954.712,2.01 95581.788,399997.928,2.175 95652.604,400063.097,2.391 95708.842,400115.112,2.496 95888.314,400280.741,2.83 95917.006,400307.396,3.078 95933.222,400322.116,3.002 96002.175,400385.799,2.864 96063.519,400442.332,2.744 96324.093,400682.777,2.581 96584.667,400923.222,2.546 96685.028,401015.554,2.709 96802.749,401124.463,2.417 96974.227,401282.37,2.193 97164.009,401457.458,2.013 97215.729,401505.078,1.987 97226.017,401514.73,1.978 97239.692,401527.221,1.976 97246.269,401533.433,1.966 97292.37,401575.848,1.934 97357.359,401635.811,1.953 97373.67,401650.873,1.981 97383.795,401660.371,1.984 97417.583,401691.386,1.977 97471.193,401740.877,1.933 97484.663,401753.15,1.921 97728.724,401978.24,1.919 97972.784,402203.331,1.868 98242.483,402451.941,1.833 98519.541,402707.62,1.623 98553.372,402739.017,1.65 98590.134,402772.761,1.647 98615.554,402796.232,1.649 98623.711,402803.62,1.671 98639.89,402818.806,1.703 98680.827,402856.293,1.698 98709.704,402883.238,1.727 98719.574,402892.197,1.715 98741.132,402912.011,1.694 98756.045,402926.015,1.718 98776.598,402944.857,1.71 98788.529,402955.964,1.728 98804.489,402970.474,1.739 98921.063,403078.158,1.862 98933.682,403089.654,1.868 99012.204,403162.286,1.929 99053.346,403200.13,1.931 99181.031,403318.034,1.908 99345.719,403469.739,1.951 99510.407,403621.444,1.665 99589.823,403694.469,1.492 99615.075,403717.954,1.46 99633.727,403735.716,1.444 99644.478,403746.153,1.432 99654.354,403755.829,1.416 99674.144,403775.683,1.404 99691.896,403793.911,1.408 99701.841,403804.349,1.418 99721.791,403825.724,1.473 99740.936,403846.889,1.485 99751.185,403858.484,1.503 99768.561,403878.564,1.556 99778.758,403890.565,1.557 99789.09,403902.964,1.603 99798.752,403914.785,1.652 99809.561,403928.19,1.704 99818.988,403940.024,1.716 99829.127,403953.053,1.758 99847.785,403977.452,1.819 99856.285,403988.811,1.899 99872.081,404010.556,2.028 99878.655,404019.731,2.087 99891.974,404038.748,2.175 99907.551,404061.635,2.32 99914.911,404072.683,2.345 99933.625,404101.422,2.498 99965.565,404151.666,2.75 100011.73,404224.849,2.937 100041.069,404270.684,2.966 100059.268,404299.37,2.955 100187.87,404502.904,2.49 100338.559,404741.169,1.783 100359.477,404774.368,1.703 100399.435,404837.413,1.499 100459.559,404932.62,1.191 100466.202,404942.997,1.158 100497.485,404992.674,0.986 100504.453,405003.647,0.938 100509.567,405011.432,0.915 100597.924,405151.338,0.571 100627.811,405198.507,0.448 100633.388,405207.504,0.292 100668.06,405262.246,0.142 100712.484,405332.771,0.082 100775.943,405432.864,0.001 100783.236,405444.523,-0.003 100803.72,405476.761,-0.023 100826.668,405513.093,-0.029 100834.263,405524.963,-0.01 100850.832,405551.461,0.046 100875.643,405590.502,0.102 100957.42,405719.939,0.11 101006.17,405796.895,0.091 101106.468,405955.66,0.378 101143.748,406014.62,0.244 101153.285,406029.999,0.263 101199.173,406102.563,0.178 101207.551,406115.565,0.211 101208.976,406117.822,0.206 101267.918,406211.172,0.178 101279.532,406229.71,0.382 101370.646,406373.769,0.24 101405.385,406428.925,0.258 101483.966,406553.215,0.262 101490.166,406563.159,0.278 101537.558,406637.802,0.359 101553.503,406662.326,0.366 101567.736,406683.707,0.344 101575.635,406695.35,0.339 101584.586,406708.336,0.35 101591.584,406718.297,0.52 101599.915,406729.84,0.51 101606.475,406738.723,0.317 101624.049,406761.927,0.315 101638.558,406780.555,0.358 101647.789,406792.15,0.366 101655.929,406802.162,0.373 101674.028,406824.181,0.388 101688.538,406841.086,0.404 101707.553,406862.653,0.409 101713.116,406868.781,0.428 101729.771,406886.882,0.416 101738.192,406895.861,0.436 101758.214,406916.736,0.424 101777.561,406936.136,0.415 101795.418,406953.531,0.445 101811.252,406968.578,0.454 101833.562,406989.121,0.453 101844.168,406998.539,0.433 101858.37,407010.982,0.432 101878.625,407028.305,0.428 101890.902,407038.551,0.437 101903.27,407048.687,0.429 101924.459,407065.535,0.446 101945.683,407081.898,0.463 101962.837,407094.759,0.477 101986.905,407112.372,0.495 101993.205,407116.885,0.5 102014.521,407131.63,0.509 102034.604,407145.113,0.556 102054.066,407157.866,0.575 102080.025,407174.156,0.557 102094.53,407183.151,0.576 102117.346,407197.131,0.538 102316.663,407317.783,0.519 102526.381,407444.578,0.549 102736.099,407571.372,0.551 102997.323,407729.439,0.558 103123.24,407805.447,0.471 103300.266,407912.73,0.454 103453.824,408005.458,0.473 103552.3,408065.086,0.496 103590.945,408088.364,0.44 103867.349,408255.502,0.413 103949.199,408305.138,0.455 104043.342,408361.959,0.522 104124.645,408411.248,0.674 104137.407,408418.853,0.634 104331.787,408536.429,1.072 104463.537,408615.933,1.356 104515.51,408647.513,1.361 104558.699,408674.187,1.427 104586.5,408691.715,1.45 104598.27,408699.308,1.496 104613.098,408708.996,1.481 104637.619,408725.404,1.477 104658.617,408739.928,1.471 104670.669,408748.438,1.489 104698.166,408768.502,1.475 104716.723,408782.572,1.43 104730.964,408793.59,1.389 104752.023,408810.416,1.388 104759.133,408816.195,1.405 104774.144,408828.629,1.407 104786.3,408838.954,1.426 104800.585,408851.237,1.41 104817.119,408865.938,1.397 104830.135,408877.742,1.397 104837.514,408884.566,1.385 104854.709,408900.756,1.367 104872.223,408917.714,1.352 104890.02,408935.419,1.339 104909.269,408955.231,1.356 104919.001,408965.464,1.349 104927.598,408974.639,1.327 104944.437,408993.049,1.374 104952.789,409002.371,1.399 104973.639,409026.257,1.418 104979.877,409033.575,1.409 104992.983,409049.277,1.421 105005.673,409064.836,1.41 105015.974,409077.721,1.4 105029.723,409095.43,1.4 105042.824,409112.712,1.405 105055.275,409129.49,1.415 105065.793,409144.079,1.469 105077.633,409160.802,1.481 105090.434,409179.528,1.456 105102.199,409197.122,1.456 105113.951,409215.277,1.433 105126.123,409234.562,1.394 105136.82,409251.971,1.404 105146.313,409267.882,1.403 105158.161,409288.204,1.425 105163.929,409298.388,1.448 105175.626,409319.537,1.457 105181.138,409329.751,1.454 105192.285,409350.997,1.425 105197.26,409360.642,1.451 105205.763,409377.686,1.429 105213.895,409394.356,1.407 105218.299,409403.539,1.44 105226.006,409420.032,1.424 105230.024,409428.754,1.429 105238.096,409446.764,1.46 105241.654,409455.011,1.468 105249.45,409473.281,1.478 105253.464,409482.944,1.461 105261.275,409502.221,1.487 105264.943,409511.391,1.457 105274.777,409537.197,1.468 105281.651,409555.872,1.435 105290.869,409581.969,1.371 105298.471,409604.72,1.331 105302.495,409617.274,1.308 105309.25,409638.998,1.267 105312.039,409648.225,1.253 105317.825,409668.086,1.23 105323.653,409689.165,1.159 105328.75,409708.6,1.118 105331.217,409718.357,1.102 105335.255,409734.693,1.094 105340.448,409757.111,1.032 105344.417,409775.214,0.993 105348.426,409794.457,0.939 105350.441,409804.544,0.936 105355.244,409829.812,0.873 105357.897,409845.167,0.887 105360.763,409864.115,0.896 105363.849,409886.839,0.906 105369.863,409928.424,0.925 105371.535,409940.947,0.93 105373.989,409964.396,0.898 105376.193,409987.941,0.906 105378.332,410015.747,0.976 105379.853,410040.012,1.013 105381.461,410076.799,1.082 105382.237,410112.707,1.131 105382.203,410118.527,1.117 105382.329,410124.23,1.151 105382.135,410160.053,1.185 105381.291,410192.673,1.2 105380.561,410210.69,1.212 105379.625,410229.071,1.213 105378.277,410250.538,1.325 105377.537,410260.99,1.169 105375.149,410288.707,1.19 105374.162,410299.257,1.178 105371.905,410320.259,1.171 105370.443,410333.171,1.144 105369.576,410340.053,0.959 105358.118,410420.49,0.959 105346.359,410480.783,0.938 105342.269,410499.392,1.131 105333.408,410536.956,1.091 105332.054,410542.697,1.105 105321.415,410583.482,1.029 105314.319,410608.838,1.043 105306.363,410635.135,1.071 105298.775,410658.979,1.081 105292.034,410679.378,1.088 105286.606,410695.34,1.083 105273.783,410730.743,1.04 105267.305,410748.334,1.062 105260.244,410766.879,1.041 105248.737,410796.728,1.057 105217.414,410876.486,1.035 105193.219,410937.142,1.004"
    # )
    #
    # tester = await km_service.get_point("Zlw-Np", 8.8, 78, line_geometry)
    # response = await km_service.get_km(tester.x, tester.y)
    #

    #
    # tasks = [km_service.get_km(item[0], item[1]) for item in _]
    # result = await asyncio.gather(*tasks)
    # for item in result:
    #     print(item)


if __name__ == "__main__":
    asyncio.run(main())
