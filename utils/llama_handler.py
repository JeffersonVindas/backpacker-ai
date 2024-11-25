import requests
from datetime import datetime
import os
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

class LlamaHandler:
    def __init__(self):
        self.current_places = []
        self.current_location = None
        self.geolocator = Nominatim(user_agent="my_travel_app")
        
        # Patrones de lenguaje natural
        self.location_patterns = {
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

    def query_places(self, query_text):
        """Procesa consultas en lenguaje natural"""
        try:
            query_text = query_text.lower().strip()
            print(f"Procesando consulta: '{query_text}'")
            
            # Si es solo un saludo sin pregunta adicional
            if self._is_only_greeting(query_text):
                print("Detectado saludo simple")
                return self._get_greeting_response()
            
            # Si es una pregunta sobre el bot sin consulta de lugar
            if self._is_only_bot_question(query_text):
                print("Detectada pregunta sobre el bot")
                return self._get_bot_info_response()
            
            # Extraer ubicación y tipo de consulta
            location, query_type = self._parse_natural_query(query_text)
            print(f"Ubicación extraída: '{location}'")
            print(f"Tipo de consulta: '{query_type}'")
            
            if not location:
                return ("No he podido identificar el lugar del que me hablas. "
                       "¿Podrías decirme específicamente qué ciudad o lugar te interesa?")
            
            # Obtener coordenadas
            try:
                geo_location = self.geolocator.geocode(location, timeout=10)
                if not geo_location:
                    return f"No pude encontrar la ubicación de '{location}'. ¿Podrías ser más específico?"
                
                print(f"Coordenadas encontradas: {geo_location.latitude}, {geo_location.longitude}")
                
                # Actualizar ubicación y buscar lugares
                self.set_current_location(geo_location.latitude, geo_location.longitude)
                
                if not self.current_places:
                    return f"No encontré lugares de interés en {location}. ¿Quizás podrías probar con una zona más céntrica o turística?"
                
                # Generar respuesta según el tipo de consulta
                response = None
                if query_type == 'restaurantes':
                    response = self._get_restaurants_info(self.current_places)
                elif query_type == 'cultura':
                    response = self._get_cultural_places(self.current_places)
                elif query_type == 'naturaleza':
                    response = self._get_parks_info(self.current_places)
                else:
                    response = self._get_general_places_info(self.current_places)
                
                if not response or response.strip() == "":
                    return f"Encontré {len(self.current_places)} lugares en {location}, pero no del tipo específico que buscas. ¿Te gustaría ver otros tipos de lugares?"
                
                return response
                
            except Exception as e:
                print(f"Error al procesar ubicación: {str(e)}")
                return "Lo siento, tuve un problema buscando ese lugar. ¿Podrías intentarlo de nuevo?"
                
        except Exception as e:
            print(f"Error general en query_places: {str(e)}")
            return "Hubo un error procesando tu consulta. ¿Podrías reformularla?"

    def _is_only_greeting(self, text):
        """Detecta si el mensaje es únicamente un saludo sin consulta adicional"""
        greetings = ['hola', 'buenos días', 'buenas tardes', 'buenas noches', 
                    'hey', 'saludos', 'que tal', 'como estás']
        
        # Si el texto es solo un saludo (considerando algunas palabras adicionales comunes)
        words = text.split()
        if len(words) <= 3:  # Solo saludo o saludo con cortesía
            return any(greeting in text for greeting in greetings)
        return False

    def _is_only_bot_question(self, text):
        """Detecta si es únicamente una pregunta sobre el bot sin consulta adicional"""
        bot_questions = ['quien eres', 'que eres', 'como funcionas', 'que haces',
                        'como puedes ayudar', 'que me puedes decir']
        
        # Verificar si es solo una pregunta sobre el bot
        return any(question in text and len(text.split()) <= len(question.split()) + 2 
                  for question in bot_questions)

    def _parse_natural_query(self, query):
        """Analiza la consulta en lenguaje natural de manera más robusta"""
        print(f"Analizando consulta: '{query}'")
        
        # Primero buscar patrones conocidos
        for category, patterns in self.location_patterns.items():
            for pattern in patterns:
                if pattern in query:
                    # Extraer la ubicación que viene después del patrón
                    location = query.split(pattern)[-1].strip()
                    print(f"Patrón encontrado: '{pattern}' -> Ubicación: '{location}'")
                    return location, category
        
        # Si no encuentra patrones, buscar preposiciones comunes
        prepositions = ['en', 'de', 'sobre', 'cerca de', 'alrededor de']
        words = query.split()
        for i, word in enumerate(words):
            if word in prepositions and i + 1 < len(words):
                location = ' '.join(words[i+1:])
                print(f"Ubicación encontrada después de '{word}': '{location}'")
                return location, 'general'
        
        # Si aún no encuentra, buscar nombres propios o palabras capitalizadas en la consulta original
        original_words = query.split()
        for i, word in enumerate(original_words):
            if word[0].isupper():
                location = ' '.join(original_words[i:])
                print(f"Ubicación encontrada por mayúscula: '{location}'")
                return location, 'general'
        
        print("No se encontró ubicación")
        return None, 'general'

    def _format_place_info(self, place):
        """Formatea la información de un lugar de manera amigable"""
        info = [f"📍 {place['name']}"]
        
        if place.get('type'):
            info.append(f"   Tipo: {place['type']}")
        
        if place.get('description'):
            info.append(f"   📝 {place['description']}")
        
        if place.get('rating'):
            info.append(f"   ⭐ Calificación: {place['rating']}")
        
        if place.get('opening_hours'):
            info.append(f"   ⏰ Horario: {place['opening_hours']}")
        
        if place.get('website'):
            info.append(f"   🌐 Web: {place['website']}")
            
        if place.get('phone'):
            info.append(f"   📞 Tel: {place['phone']}")
            
        if place.get('address'):
            info.append(f"   📮 Dirección: {place['address']}")
            
        return "\n".join(info)

    def _get_nearby_places(self, lat, lon, radius=2000):
        """Obtiene lugares cercanos usando Overpass API"""
        query = f"""
        [out:json][timeout:25];
        (
            node["tourism"](around:{radius},{lat},{lon});
            node["historic"](around:{radius},{lat},{lon});
            node["amenity"~"restaurant|cafe|bar|museum|theatre"](around:{radius},{lat},{lon});
            node["leisure"~"park|garden"](around:{radius},{lat},{lon});
        );
        out body;
        """
        
        try:
            response = requests.get(
                "https://overpass-api.de/api/interpreter",
                params={'data': query},
                timeout=30
            )
            
            if response.status_code == 200:
                results = response.json()
                places = []
                
                for element in results.get('elements', []):
                    if 'tags' in element:
                        place = {
                            "name": element['tags'].get('name', 'Sin nombre'),
                            "type": (
                                element['tags'].get('tourism') or 
                                element['tags'].get('historic') or 
                                element['tags'].get('amenity') or
                                element['tags'].get('leisure')
                            ),
                            "latitude": element.get('lat'),
                            "longitude": element.get('lon'),
                            "rating": element['tags'].get('stars', 'No disponible'),
                            "description": element['tags'].get('description', ''),
                            "address": element['tags'].get('addr:street', ''),
                            "opening_hours": element['tags'].get('opening_hours', ''),
                            "website": element['tags'].get('website', ''),
                            "phone": element['tags'].get('phone', '')
                        }
                        if place['name'] != 'Sin nombre':
                            places.append(place)
                
                return places
            return []
        except Exception as e:
            print(f"Error al obtener lugares cercanos: {str(e)}")
            return []

    def _extract_place_name(self, query):
        """Extrae el nombre del lugar de la consulta"""
        location_indicators = ['en', 'de', 'sobre', 'acerca de', 'para', 'cerca de']
        
        query = query.lower()
        for indicator in location_indicators:
            if indicator in query:
                parts = query.split(indicator)
                if len(parts) > 1:
                    return parts[1].strip()
        
        return query.strip()

    def _generate_response(self, query, places):
        """Genera una respuesta basada en el tipo de consulta"""
        query = query.lower()
        
        if any(word in query for word in ['restaurante', 'comer', 'comida', 'café', 'bar']):
            return self._get_restaurants_info(places)
        elif any(word in query for word in ['museo', 'cultural', 'histórico', 'historia']):
            return self._get_cultural_places(places)
        elif any(word in query for word in ['parque', 'jardín', 'aire libre', 'naturaleza']):
            return self._get_parks_info(places)
        else:
            return self._get_general_places_info(places)

    def _get_restaurants_info(self, places):
        restaurants = [p for p in places if p['type'] in ['restaurant', 'cafe', 'bar']]
        if not restaurants:
            return "No encontré restaurantes en esta ubicación."
        
        response = [f"🍽️ Restaurantes y cafés en {self.current_location}:"]
        
        for rest in restaurants[:5]:
            info = [f"\n\n• {rest['name']}"]
            if rest['type']:
                info.append(f"Tipo: {rest['type']}")
            if rest.get('rating'):
                info.append(f"⭐ {rest['rating']}")
            if rest.get('opening_hours'):
                info.append(f"Horario: {rest['opening_hours']}")
            if rest.get('website'):
                info.append(f"Web: {rest['website']}")
            response.append(" | ".join(info))
        
        return "".join(response)

    def _get_cultural_places(self, places):
        cultural = [p for p in places if p['type'] in ['museum', 'historic', 'theatre']]
        if not cultural:
            return "No encontré lugares culturales en esta ubicación."
        
        response = [f"🏛️ Lugares culturales en {self.current_location}:\n"]
        
        for place in cultural[:5]:
            info = [f"• {place['name']}"]
            if place['type']:
                info.append(f"Tipo: {place['type']}")
            if place.get('rating'):
                info.append(f"⭐ {place['rating']}")
            if place.get('description'):
                info.append(f"{place['description']}")
            response.append(" | ".join(info))
        
        return "\n\n".join(response)

    def _get_parks_info(self, places):
        parks = [p for p in places if p['type'] in ['park', 'garden']]
        if not parks:
            return "No encontré parques en esta ubicación."
        
        response = [f"🌳 Parques y jardines en {self.current_location}:\n"]
        
        for park in parks[:5]:
            info = [f"• {park['name']}"]
            if park['type']:
                info.append(f"Tipo: {park['type']}")
            if park.get('rating'):
                info.append(f"⭐ {park['rating']}")
            if park.get('description'):
                info.append(f"{park['description']}")
            response.append(" | ".join(info))
        
        return "\n\n".join(response)

    def _get_general_places_info(self, places):
        if not places:
            return "No encontré lugares de interés en esta ubicación."
        
        response = [f"📍 Lugares de interés en {self.current_location}:\n"]
        
        for place in places[:8]:
            info = [f"• {place['name']}"]
            if place['type']:
                info.append(f"Tipo: {place['type']}")
            if place.get('rating'):
                info.append(f"⭐ {place['rating']}")
            if place.get('description'):
                info.append(f"{place['description']}")
            if place.get('website'):
                info.append(f"Web: {place['website']}")
            response.append(" | ".join(info))
        
        return "\n\n".join(response)

    def get_places_summary(self):
        """Retorna un resumen de los lugares actuales"""
        if not self.current_places:
            return "No hay lugares almacenados para la ubicación actual."
        
        try:
            # Contar lugares por tipo
            place_types = {}
            for place in self.current_places:
                place_type = place.get('type', 'Sin clasificar')
                place_types[place_type] = place_types.get(place_type, 0) + 1
            
            # Crear resumen
            summary = [
                f"📊 Resumen de lugares en {self.current_location or 'ubicación actual'}:",
                f"\n📍 Total de lugares: {len(self.current_places)}",
                "\n🏷️ Lugares por tipo:"
            ]
            
            for place_type, count in sorted(place_types.items()):
                summary.append(f"  • {place_type}: {count} lugares")
            
            # Agregar algunos lugares destacados si existen
            if self.current_places:
                summary.append("\n✨ Algunos lugares destacados:")
                for place in self.current_places[:3]:
                    summary.append(f"  • {place['name']}")
                    if place.get('type'):
                        summary.append(f"    Tipo: {place['type']}")
                    if place.get('opening_hours'):
                        summary.append(f"    Horario: {place['opening_hours']}")
            
            return "\n".join(summary)
        except Exception as e:
            print(f"Error al generar resumen: {str(e)}")
            return "Error al generar el resumen de lugares."

    def set_current_location(self, latitude, longitude, radius=2000):
        """Actualiza los lugares actuales basados en la ubicación"""
        try:
            print(f"Actualizando ubicación a: {latitude}, {longitude}")
            self.current_location = (latitude, longitude)
            
            # Buscar lugares cercanos usando Overpass API
            places = self._get_nearby_places(latitude, longitude, radius)
            
            if places:
                self.current_places = places
                print(f"Se encontraron {len(places)} lugares en la nueva ubicación")
            else:
                self.current_places = []
                print("No se encontraron lugares en la nueva ubicación")
            
            return len(self.current_places)
        
        except Exception as e:
            print(f"Error al actualizar ubicación: {str(e)}")
            self.current_places = []
            return 0