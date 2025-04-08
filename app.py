from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/tipo-cambio')
def obtener_tipo_cambio():
    try:
        url = "https://www.ficohsa.com/hn/honduras/tipo-cambio"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for row in soup.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) >= 2 and "Venta" in cols[0].text:
                valor = cols[1].text.strip().replace("Lps. ", "").replace(",", "")
                return jsonify({"tipoCambio": round(float(valor), 4)})

        return jsonify({"tipoCambio": 25.7784})
    except Exception as e:
        print("Error al obtener tipo de cambio:", e)
        return jsonify({"tipoCambio": 25.7784})
