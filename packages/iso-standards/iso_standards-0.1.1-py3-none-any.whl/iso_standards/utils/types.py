from iso_standards.iso3166.types import Iso3166_1, Iso3166_2


class Country(Iso3166_1):
    """Country lightweight immutable entity."""

    # Country subdivisions.
    subdivisions: Iso3166_2
