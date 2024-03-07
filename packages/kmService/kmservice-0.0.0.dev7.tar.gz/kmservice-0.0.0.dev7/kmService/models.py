from dataclasses import dataclass, field

from shapely.geometry import LineString, Point, Polygon

from kmService.uitils.shapleyTools import extend_line


@dataclass
class KmVlak:
    object_id: int
    km_lint_naam: str
    km_lint_omschrijving: str
    geometry: Polygon

    def xy_within(self, x: float, y: float):
        return Point(x, y).within(self.geometry)


@dataclass
class Raai:
    geometry_corrected: LineString = None


@dataclass
class KmRaai:
    object_id: int
    geo_code: str
    sub_code: str
    _hectometer_str: str
    geometry: LineString
    geometry_extended: LineString | None = None
    geometry_corrected: LineString | None = None
    hectometer: float = 0

    def __post_init__(self):
        extend_offset = 500
        self.hectometer = float(self._hectometer_str.replace(",", "."))
        self.geometry_extended = extend_line(self.geometry, extend_offset)

    def __str__(self):
        return (
            f"geocode:{self.geo_code} sub_geocode={self.sub_code} hm={self.hectometer}"
        )


# todo: make config file, and parse to objects so we can add objects to value_objects_dict
#  use case: missing raaien, and new tracé, future feature is to use to build raaien...
@dataclass
class CustomKmRaai:
    lint_name: str
    lint_afkorting: str
    hectometer: float
    geocode: str
    sub_code: str
    geometry: LineString
    object_id: str = field(init=False)

    def from_dict(self):
        pass


@dataclass
class KmPunt:
    object_id: int
    geo_code: str
    sub_code: str
    hectometer: float
    km_lint: str
    km_lint_omschrijving: str
    geometry: LineString

    def __str__(self):
        return f"km_lint={self.km_lint} geocode={self.geo_code} sub_geocode={self.sub_code} hm={self.hectometer}"


@dataclass
class KmSubGeocode:
    object_id: int
    geo_code: str
    sub_code: str
    naam: str
    geometry: Polygon

    def xy_within(self, x: float, y: float):
        return Point(x, y).within(self.geometry)


@dataclass
class KmValueObject:
    geometry: Polygon
    km_vlak: KmVlak
    sub_geocode: KmSubGeocode
    km_punten: list[KmPunt] = field(default_factory=list)
    km_raaien: list[KmRaai] = field(default_factory=list)
    matched: list[KmPunt | KmRaai | None] = field(default_factory=list)

    def __str__(self):
        return f"{self.sub_geocode.geo_code}_{self.sub_geocode.sub_code}_{self.km_vlak.km_lint_naam} lint_naam={self.km_vlak.km_lint_naam} geo_code={self.sub_geocode.geo_code} sub_gecode={self.sub_geocode.sub_code} intersection={self.geometry.wkt}"

    def __repr__(self):
        self.__str__()
