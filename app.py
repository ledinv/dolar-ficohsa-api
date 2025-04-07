from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/tipo-cambio')
def obtener_tipo_cambio():
    try:
        url = "https://www.ficohsa.com/hn/honduras/tipo-cambio"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Busca donde aparece "Venta" y toma el valor siguiente
        for td in soup.find_all("td"):
            if "Venta" in td.text:
                valor = td.find_next_sibling("td").text.strip().replace("Lps. ", "").replace(",", "")
                return jsonify({"tipoCambio": float(valor)})

        return jsonify({"tipoCambio": 25.78})
    except:
        return jsonify({"tipoCambio": 25.78})
