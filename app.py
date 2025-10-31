from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"mensagem": "API de vetores em R³ funcionando!"})

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.get_json()

    ax = dados.get("ax", 0)
    ay = dados.get("ay", 0)
    az = dados.get("az", 0)
    bx = dados.get("bx", 0)
    by = dados.get("by", 0)
    bz = dados.get("bz", 0)
    operacao = dados.get("operacao", "").lower()

    if operacao == "adicao":
        resultado = [ax + bx, ay + by, az + bz]

    elif operacao == "produto_escalar":
        resultado = ax * bx + ay * by + az * bz

    elif operacao == "produto_vetorial":
        resultado = [
            ay * bz - az * by,
            az * bx - ax * bz,
            ax * by - ay * bx
        ]

    elif operacao == "produto_misto":
        resultado = ax * (by * bz - bz * by) - ay * (bx * bz - bz * bx) + az * (bx * by - by * bx)

    else:
        return jsonify({"erro": "Operação inválida"}), 400

    return jsonify({"resultado": resultado})

if __name__ == '__main__':
    app.run(debug=True)