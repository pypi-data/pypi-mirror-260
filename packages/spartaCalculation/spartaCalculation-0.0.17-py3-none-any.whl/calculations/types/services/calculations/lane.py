from typing_extensions import TypedDict


class LaneInformation(TypedDict):
    lap_distance: int
    pool_type: str
    relay_leg: int
    relay_type: str
    stroke_type: str
