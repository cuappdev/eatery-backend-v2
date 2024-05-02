def eatery_is_cafe(json_eatery):
    return not "Dining Room" in [eatery_type["descr"] for eatery_type in json_eatery["eateryTypes"]]