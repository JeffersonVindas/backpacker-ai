# Configuración general
SEARCH_RADIUS = 2000  # metros
DEFAULT_TIMEOUT = 10  # segundos
MAX_PLACES_GENERAL = 8
MAX_PLACES_CATEGORY = 5

# Configuración de Nominatim
NOMINATIM_USER_AGENT = "my_travel_app"
NOMINATIM_TIMEOUT = 10

# Configuración de Overpass API
OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"
OVERPASS_TIMEOUT = 25

# Tipos de lugares
PLACE_TYPES = {
    'tourism': ['museum', 'attraction', 'viewpoint', 'artwork', 'gallery'],
    'historic': ['monument', 'castle', 'ruins', 'archaeological_site'],
    'amenity': ['restaurant', 'cafe', 'bar', 'museum', 'theatre'],
    'leisure': ['park', 'garden']
}

# Patrones de lenguaje natural
LANGUAGE_PATTERNS = {
    'preguntas_generales': [
        'que hay en', 'que puedo ver en', 'que visitar en', 'lugares para ver en',
        'que hacer en', 'que me recomiendas en', 'lugares de interés en',
        'sitios para visitar en', 'atracciones en', 'puntos de interés en'
    ],
    'restaurantes': [
        'donde comer en', 'restaurantes en', 'lugares para comer en',
        'sitios para cenar en', 'cafeterías en', 'bares en',
        'donde cenar en', 'comida en', 'gastronomía de'
    ],
    'cultura': [
        'museos en', 'lugares históricos en', 'sitios culturales en',
        'monumentos en', 'arte en', 'historia de', 'teatros en',
        'arquitectura de', 'patrimonio de'
    ],
    'naturaleza': [
        'parques en', 'jardines en', 'espacios verdes en',
        'naturaleza en', 'aire libre en', 'zonas verdes de'
    ]
} 