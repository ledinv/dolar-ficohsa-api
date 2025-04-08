from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/tipo-cambio')
def obtener_tipo_cambio():
    try:
        url = "https://www.ficohsa.com/hn/honduras/tipo-cambio"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        for p in soup.find_all("p"):
            if "Venta: Lps" in p.get_text():
                texto = p.get_text().strip()
                valor = texto.split("Venta: Lps")[-1].strip()
                return jsonify({"tipoCambio": float(valor)})

        return jsonify({"tipoCambio": 25.78})
    except Exception as e:
        return jsonify({"tipoCambio": 25.78, "error": str(e)})
