import requests
import logging
from config import OVERPASS_API_URL, OVERPASS_TIMEOUT, PLACE_TYPES

logger = logging.getLogger(__name__)

class OverpassAPI:
    def __init__(self):
        self.api_url = OVERPASS_API_URL
        self.timeout = OVERPASS_TIMEOUT

    def get_places(self, latitude, longitude, radius):
        """Obtiene lugares cercanos usando Overpass API"""
        try:
            query = self._build_query(latitude, longitude, radius)
            response = requests.get(
                self.api_url,
                params={'data': query},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return self._process_results(response.json())
            
            logger.error(f"Error Overpass API: {response.status_code}")
            return []
            
        except Exception as e:
            logger.error(f"Error al obtener lugares: {str(e)}", exc_info=True)
            return []

    def _build_query(self, lat, lon, radius):
        """Construye la consulta Overpass"""
        query_parts = []
        
        for category, types in PLACE_TYPES.items():
            types_str = '|'.join(types)
            query_parts.append(
                f'node["{category}"~"{types_str}"](around:{radius},{lat},{lon});'
            )
        
        return f"""
        [out:json][timeout:{self.timeout}];
        ({' '.join(query_parts)});
        out body;
        """

    def _process_results(self, results):
        """Procesa los resultados de Overpass API"""
        places = []
        
        for element in results.get('elements', []):
            if 'tags' in element:
                place = {
                    "name": element['tags'].get('name', 'Desconocido'),
                    "latitude": element.get('lat'),
                    "longitude": element.get('lon'),
                    "type": self._get_place_type(element['tags']),
                    "description": element['tags'].get('description', ''),
                    "website": element['tags'].get('website', ''),
                    "rating": element['tags'].get('rating', 'No disponible'),
                    "opening_hours": element['tags'].get('opening_hours', ''),
                    "phone": element['tags'].get('phone', '')
                }
                if place['name'] != 'Desconocido':
                    places.append(place)
        
        return places

    def _get_place_type(self, tags):
        """Determina el tipo principal del lugar"""
        for category, types in PLACE_TYPES.items():
            if category in tags and tags[category] in types:
                return tags[category]
        return 'other' 