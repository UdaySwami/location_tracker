from math import sin, cos, sqrt, atan2, radians


def get_distance_covered(locations):
    # approximate radius of earth in km
    distance = 0

    for i in range(len(locations)):
        if i != len(locations) - 1:
            distance = distance + distance_between_two_points(locations[i], locations[i + 1])
    return distance


def distance_between_two_points(l1, l2):
    R = 6373.0

    lat1 = radians(l1.lat)
    lon1 = radians(l1.lng)
    lat2 = radians(l2.lat)
    lon2 = radians(l2.lng)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance
