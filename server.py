from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)
CORS(app)

# Variables para no saturar la web del BCV
ultima_tasa = None
ultima_actualizacion = 0

def obtener_tasa_real():
    global ultima_tasa, ultima_actualizacion
    ahora = time.time()
    
    # Si han pasado menos de 10 minutos, usamos la que ya tenemos guardada
    if ultima_tasa and (ahora - ultima_actualizacion < 600):
        return ultima_tasa

    try:
        url = "https://www.bcv.org.ve/"
        # El BCV a veces bloquea scripts, así que "simulamos" ser un navegador real
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscamos el contenedor específico del BCV para el dólar
        tasa_str = soup.find("div", id="dolar").find("strong").text.strip()
        tasa_limpia = tasa_str.replace(',', '.')
        
        ultima_tasa = tasa_limpia
        ultima_actualizacion = ahora
        print(f"Tasa actualizada desde el BCV: {ultima_tasa}")
        return ultima_tasa
    except Exception as e:
        print(f"Error en conexión: {e}")
        return ultima_tasa if ultima_tasa else "45.00"

@app.route('/api/tasa')
def get_tasa():
    return jsonify({"valor": obtener_tasa_real()})

if __name__ == '__main__':
    # Esto corre en tu PC con 8GB de RAM sin despeinarse
    app.run(host='0.0.0.0', port=5000)