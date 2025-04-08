from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/api/tipo-cambio')
def obtener_tipo_cambio():
    try:
        url = "https://www.ficohsa.com/hn/honduras/tipo-cambio"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }

        # Se ignora la verificación SSL
        response = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        for p in soup.find_all("p"):
            if "Venta: Lps" in p.get_text():
                texto = p.get_text().strip()
                valor = texto.split("Venta: Lps")[-1].strip()
                return jsonify({"tipoCambio": round(float(valor), 4)})

        return jsonify({"tipoCambio": 25.78, "error": "Valor no encontrado"})
    except Exception as e:
        return jsonify({"tipoCambio": 25.78, "error": str(e)})

# Para que Render detecte el puerto
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
