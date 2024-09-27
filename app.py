from flask import Flask, render_template, request, jsonify # renderizar archivos HTML, solicitudes HTTP
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects  #Gestionar los errores
import json  #datos en formato JSON
import threading #múltiples operaciones en paralelo
import time  #Contar segundos


app = Flask(__name__) #Creamos una instancia de la app flask #Flask va a ser el servidor de mi API


# Variable global para almacenar los datos
dataCryptos = {'data': []}  #Creamos un dicionario con la clave data

def Acceso_API():
    global dataCryptos
    api_key = 'd1c51888-744b-4368-82c9-e8ff4f3ab22b'  # Api key
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest" #URL a la que se enviará la solicitud HTTP
    parameters = {     #Diccionario con los parametros, limite de 10 criptomonedas
        'start': '1',
        'limit': '10',
        'convert': 'USD'
    }
    headers = {                          
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    session = Session()
    session.headers.update(headers)   #Pasamos la Api

    try:
        response = session.get(url, params=parameters)
        dataCryptos = json.loads(response.text) #convierte cadena JSON en un objeto de python
        #print(dataBitCoin)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

#Función se ejecuta cada vez que accedemos a la raiz del proyecto 
@app.route('/', methods=['GET'])
def index():
    Acceso_API()  # Obtener los datos antes de renderizar la página
    return render_template('index.html', data=dataCryptos['data']) #"data" contiene la información de criptomonedas

#Definimos el endpoint cryptos para exponer datos de API REST
@app.route("/cryptos/")
def get_cryptos():
    return jsonify(dataCryptos) #Retornamos datos en formato JSON

#Definimos el endpoint /cryptos/{id} para exponer datos de API REST
@app.route("/cryptos/<id>")
def get_crypto(id): 
    crypto_id = None   #Variable que alamacena información específica
    id = int(id)  
    for crypto in dataCryptos['data']:   #Ciclo itera a través de la lista de criptomonedas
        if crypto['id'] == id: #Comparamos el id de la criptomoneda actual con el id proporcionado en URL           
            crypto_id = crypto        #Guardamos la coincidencia en nueva variable    
            break        
    
    # Verificamos que se haya encontrado la id y retornamos info o mensaje
    if crypto_id is not None:
        return jsonify(crypto_id)  # Devuelve la criptomoneda encontrada en JSON
    else:
        return jsonify({"error": "not found"}) 

#Siempre entra a esta condición cuando se ejecuta directamente el script
if __name__ == '__main__':
    
    # Iniciar el hilo para obtener datos automáticamente cada 5 minutos
    def update_data():
        while True:
            Acceso_API()
            time.sleep(60)

#Creamos hilo para que la app ejecute en paralelo la función update_data()
#De esta manera la app ejecuta al mismo tiempo update_data y todas las demás funciones de la app
    data_thread = threading.Thread(target=update_data)
    data_thread.daemon = True  # Hilo en segundo plano
    data_thread.start()

    #Inciamos servidor web de flask
    app.run(port=4000, debug=True)
