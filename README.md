# Backpacker.AI 🌎

Una aplicación web inteligente que te ayuda a planificar tus viajes y descubrir lugares interesantes.

## Características principales 🌟

- **Chat Inteligente**: Interactúa con un asistente virtual que te ayuda a encontrar lugares turísticos, restaurantes, museos y más.
- **Búsqueda de Lugares**: Descubre sitios interesantes cerca de tu ubicación o en cualquier ciudad del mundo.
- **Visualización en Mapa**: Explora los lugares recomendados en un mapa interactivo.
- **Interfaz Intuitiva**: Diseño moderno y fácil de usar con un estilo visual atractivo.

## Tecnologías utilizadas 🛠️

- Python
- Flask
- HTML5/CSS3
- JavaScript
- Bootstrap 5
- Leaflet.js para mapas interactivos
- OpenStreetMap & Overpass API

## Instalación 🚀

1. Clona el repositorio:
```bash
git clone https://github.com/JeffersonVindas/backpacker-ai.git
cd backpacker-ai
```

2. **Crea y activa el entorno virtual**
```bash
python -m venv venv
```

En Windows:
```bash
venv\Scripts\activate
```

En macOS/Linux:
```bash
source venv/bin/activate
```
3. **Instala las dependencias**
pip install -r requirements.txt


4. **Ejecuta la aplicación**
```bash
python .\index.py
```

5. Abre tu navegador y visita `http://localhost:5000`

## Guía de Uso 📖

### Página Principal
- Vista general de la aplicación
- Acceso a todas las funcionalidades
- Visualización de tu ubicación actual

### Chat Inteligente
- Interactúa con el asistente de viaje
- Pregunta sobre lugares específicos
- Obtén recomendaciones personalizadas

### Explorador de Lugares
- Busca lugares por nombre o ciudad
- Visualiza ubicaciones en el mapa
- Obtén información detallada de cada lugar

## Estructura del Proyecto 📁
backpacker-ai/
├── static/
│ ├── images/
│ │ ├── frog.jpg
│ │ ├── mountains.jpg
│ │ └── sunset.jpg
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── chat.html
│ └── visit.html
├── utils/
│ ├── llama_handler.py
│ ├── overpass_api.py
│ └── geo_utils.py
├── config.py
├── index.py
└── requirements.txt


## Requisitos 📋

- Python 3.8 o superior
- Conexión a internet (para acceder a OpenStreetMap)
- Navegador web moderno

## Autores ✒️

* **Jefferson Vindas Castillo** - *Desarrollo inicial* - [JeffersonVindas](https://github.com/JeffersonVindas)