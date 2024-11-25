from math import radians, sin, cos, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calcula la distancia entre dos puntos usando la fórmula haversine"""
    R = 6371000  # Radio de la Tierra en metros
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c

def get_nearby_places(lat, lon, radius_meters, places):
    """Filtra lugares dentro del radio especificado"""
    nearby_places = []
    
    for place in places:
        distance = calculate_distance(
            lat, lon,
            place['latitude'],
            place['longitude']
        )
        if distance <= radius_meters:
            place['distance'] = round(distance)
            nearby_places.append(place)
    
    # Ordenar por distancia
    nearby_places.sort(key=lambda x: x.get('distance', float('inf')))
    return nearby_places 