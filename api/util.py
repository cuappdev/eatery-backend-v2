from api.datatype.Eatery import EateryID

CORNELL_DINING_URL = "https://now.dining.cornell.edu/api/1.0/dining/eateries.json"

def dining_id_to_internal_id(id: int):
    if id == 31:
        return EateryID.ONE_ZERO_FOUR_WEST
    elif id == 7:
        return EateryID.LIBE_CAFE
    elif id == 8:
        return EateryID.ATRIUM_CAFE
    elif id == 1:
        return EateryID.BEAR_NECESSITIES
    elif id == 25:
        return EateryID.BECKER_HOUSE
    elif id == 10:
        return EateryID.BIG_RED_BARN
    elif id == 11:
        return EateryID.BUS_STOP_BAGELS
    elif id == 12:
        return EateryID.CAFE_JENNIE
    elif id == 2:
        return EateryID.CAROLS_CAFE
    elif id == 26:
        return EateryID.COOK_HOUSE
    elif id == 14:
        return EateryID.DAIRY_BAR
    elif id == 41:
        return EateryID.CROSSINGS_CAFE
    elif id == 32:
        return EateryID.FRANNYS
    elif id == 16:
        return EateryID.GOLDIES_CAFE
    elif id == 15:
        return EateryID.GREEN_DRAGON
    elif id == 24:
        return EateryID.HOT_DOG_CART
    elif id == 34:
        return EateryID.ICE_CREAM_BIKE
    elif id == 27:
        return EateryID.BETHE_HOUSE
    elif id == 28:
        return EateryID.JANSENS_MARKET
    elif id == 29:
        return EateryID.KEETON_HOUSE
    elif id == 42:
        return EateryID.MANN_CAFE
    elif id == 18:
        return EateryID.MARTHAS_CAFE
    elif id == 19:
        return EateryID.MATTINS_CAFE
    elif id == 33:
        return EateryID.MCCORMICKS
    elif id == 3:
        return EateryID.NORTH_STAR_DINING
    elif id == 20:
        return EateryID.OKENSHIELDS
    elif id == 4:
        return EateryID.RISLEY
    elif id == 5:
        return EateryID.RPCC
    elif id == 30:
        return EateryID.ROSE_HOUSE
    elif id == 21:
        return EateryID.RUSTYS
    elif id == 13:
        return EateryID.STRAIGHT_FROM_THE_MARKET
    elif id == 23:
        return EateryID.TRILLIUM
    else:
        return None