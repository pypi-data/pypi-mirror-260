from glom import glom

from calculations.types.services.calculations.lane import LaneInformation


def is_not_defined(data) -> bool:
    """
    Returns True if the data passed is not defined

    Parameters
    ----------
    data -> any data type

    Returns
    -------
    <bool> - status of whether data is defined
    """
    if data == None or data == "":
        return True

    return False


def get_lane_information(
    annotations, relay_leg: int, pool_length: int = 50
) -> LaneInformation:
    """
    Returns the information for the lane of the race

    Returns
    -------
    <dict> - information of the lane
    """
    metrics = glom(annotations, "metrics", default=None)

    if metrics is None:
        raise Exception("There is no metrics data available.")

    leg_data = glom(metrics, "legData", default=[])

    if leg_data == None or len(leg_data) == 0:
        raise Exception("There is no summary data available.")

    meta_data = glom(leg_data[0], "metadata", default={})

    return {
        "lap_distance": int(meta_data.get("distance", 0)),
        "pool_type": "LCM" if pool_length == 50 else "SCM",
        "relay_leg": relay_leg,
        "relay_type": meta_data.get("relayType", ""),
        "stroke_type": meta_data.get("strokeType", ""),
    }
