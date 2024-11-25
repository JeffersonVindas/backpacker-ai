import logging
from flask import Flask, request, jsonify, render_template
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from utils.llama_handler import LlamaHandler
from utils.overpass_api import OverpassAPI
from utils.geo_utils import calculate_distance, get_nearby_places
from config import *
import os
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
load_dotenv()

# Inicializar servicios
llama_handler = LlamaHandler()
geolocator = Nominatim(user_agent=NOMINATIM_USER_AGENT)
overpass_api = OverpassAPI()

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/visit')
def visit():
    return render_template('chat.html')

@app.route('/discover')
def discover():
    return render_template('visit.html')

@app.route('/get-places', methods=['POST'])
def get_places():
    try:
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        radius = data.get('radius', SEARCH_RADIUS)
        
        if not all([latitude, longitude]):
            return jsonify({"error": "Se requieren latitud y longitud"}), 400
        
        logger.info(f"Buscando lugares en ({latitude}, {longitude}) con radio {radius}m")
        
        # Obtener lugares usando Overpass API
        places = overpass_api.get_places(latitude, longitude, radius)
        
        if places:
            # Actualizar ubicación actual y lugares en el handler
            llama_handler.set_current_location(latitude, longitude)
            llama_handler.current_places = places
            
            # Filtrar lugares cercanos
            nearby_places = get_nearby_places(
                latitude, longitude, 
                radius, places
            )
            return jsonify(nearby_places)
        
        return jsonify({"message": "No se encontraron lugares cercanos."}), 200
            
    except Exception as e:
        logger.error(f"Error en get_places: {str(e)}", exc_info=True)
        return jsonify({"error": "Error al buscar lugares"}), 500

@app.route('/geocode', methods=['POST'])
def geocode_location():
    try:
        data = request.json
        place_name = data.get('place_name')
        
        if not place_name:
            return jsonify({'error': 'Nombre del lugar no proporcionado'}), 400
            
        logger.info(f"Geocodificando: {place_name}")
        
        try:
            location = geolocator.geocode(place_name, timeout=NOMINATIM_TIMEOUT)
        except GeocoderTimedOut:
            return jsonify({'error': 'Tiempo de espera agotado'}), 408
            
        if location:
            logger.info(f"Ubicación encontrada: {location.address}")
            
            # Actualizar ubicación y buscar lugares
            llama_handler.set_current_location(location.latitude, location.longitude)
            places = overpass_api.get_places(
                location.latitude, 
                location.longitude, 
                SEARCH_RADIUS
            )
            
            return jsonify({
                'latitude': location.latitude,
                'longitude': location.longitude,
                'address': location.address,
                'places': places
            })
            
        return jsonify({'error': 'No se encontró el lugar'}), 404
            
    except Exception as e:
        logger.error(f"Error en geocode: {str(e)}", exc_info=True)
        return jsonify({'error': 'Error al geocodificar ubicación'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({"error": "Mensaje vacío"}), 400
        
        logger.info(f"Mensaje recibido: {user_message}")
        logger.debug(f"Estado actual - Ubicación: {llama_handler.current_location}, "
                    f"Lugares: {len(llama_handler.current_places)}")
        
        response = llama_handler.query_places(user_message)
        logger.info(f"Respuesta generada: {response[:100]}...")
        
        return jsonify({"response": response})
        
    except Exception as e:
        logger.error(f"Error en chat: {str(e)}", exc_info=True)
        return jsonify({"error": "Error al procesar mensaje"}), 500

@app.route('/places-summary')
def places_summary():
    try:
        summary = llama_handler.get_places_summary()
        return jsonify({"summary": summary})
    except Exception as e:
        logger.error(f"Error en places_summary: {str(e)}", exc_info=True)
        return jsonify({"error": "Error al generar resumen"}), 500

if __name__ == '__main__':
    app.run(debug=True)