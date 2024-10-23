def eatery_is_cafe(json_eatery):
    return "Dining Room" not in [
        eatery_type["descr"] for eatery_type in json_eatery["eateryTypes"]
    ]
