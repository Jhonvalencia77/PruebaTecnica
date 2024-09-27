from flask import Flask, render_template, request, jsonify
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import threading
import time


app = Flask(__name__) #Flask va a ser el servidor de mi API


# Variable global para almacenar los datos
dataBitCoin = {'data': []}  #Creamos un dicionario con la clave data

def fetch_data():
    global dataBitCoin
    api_key = 'd1c51888-744b-4368-82c9-e8ff4f3ab22b'
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {
        'start': '1',
        'limit': '10',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        dataBitCoin = json.loads(response.text) #convierte cadena JSON en un objeto de python
        #print(dataBitCoin)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

@app.route('/', methods=['GET'])
def index():
    fetch_data()  # Obtener los datos antes de renderizar la página
    return render_template('index.html', data=dataBitCoin['data']) #accedemos a la clave "data" del diccionar

# Ruta para actualizar datos mediante PUT
@app.route('/update')
def update_data():
    global dataBitCoin
    fetch_data()  # Actualiza los datos
    return jsonify({"message": "Data updated successfully", "data": dataBitCoin['data']})

@app.route("/cryptos/")
def get_cryptos():
    return jsonify(dataBitCoin)

@app.route("/cryptos/<id>")
def get_crypto(id): 
    crypto_id = None 
    id = int(id)  
    for crypto in dataBitCoin['data']:        
        if crypto['id'] == id:            
            crypto_id = crypto            
            break        
    #return jsonify(crypto_id)
    if crypto_id is not None:
        return jsonify(crypto_id)  # Devuelve la criptomoneda encontrada
    else:
        return jsonify({"error": "not found"}) 

if __name__ == '__main__':
    # Iniciar el hilo para obtener datos automáticamente cada 5 minutos
    def auto_update_data():
        while True:
            fetch_data()
            time.sleep(60)

    data_thread = threading.Thread(target=auto_update_data)
    data_thread.daemon = True  # Hilo en segundo plano
    data_thread.start()

    #app.run(host="0.0.0.0",port=4000, debug=True)
    app.run(port=4000, debug=True)
