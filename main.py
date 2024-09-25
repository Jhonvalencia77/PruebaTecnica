from flask import Flask, render_template, request
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import threading
import time

app = Flask(__name__)

# Variable global para almacenar los datos
dataBitCoin = {'data': []}

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

    while True:
        try:
            response = session.get(url, params=parameters)
            dataBitCoin = json.loads(response.text)
            print(dataBitCoin)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        
        time.sleep(60)  # Espera 5 minutos (300 segundos)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', data=dataBitCoin['data'])

if __name__ == '__main__':
    # Iniciar el hilo para obtener datos
    data_thread = threading.Thread(target=fetch_data)
    data_thread.daemon = True  # Hilo en segundo plano
    data_thread.start()
    
    app.run(host="0.0.0.0",port=5000, debug=True)
    #app.run(port=4000, debug=True)
