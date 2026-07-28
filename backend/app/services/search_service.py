def build_query(brands, rating, countries, popularity, excluded_descriptors):
    query = {}
    if brands:
        query["brand"] = {"$in": brands}
    if rating:
        query["rating"] = {"$gte": rating}
    if countries:
        query["country"] = {"$in": countries}
    if popularity:
        query["popularity"] = {"$in": popularity}
    if excluded_descriptors:
        query["top_notes"] = {"$nin": excluded_descriptors}
        query["mid_notes"] = {"$nin": excluded_descriptors}
        query["base_notes"] = {"$nin": excluded_descriptors}
        query["accords"] = {"$nin": excluded_descriptors}
    return query
