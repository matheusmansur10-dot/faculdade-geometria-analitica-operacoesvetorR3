from flask import Flask, jsonify, request
import numpy as np 
import matplotlib.pyplot as pit
import os

app = Flask(__name__)

def gerar_grafico(A, B, C = None, resultado = None):
    fig = pit.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.quiver(0, 0, 0, A[0], A[1], A[2], color = 'blue', label = 'Vetor A')
    ax.quiver(0, 0, 0, B[0], B[1], B[2], color = 'red', label = 'Vetor B')
    if C:
        ax.quiver(0, 0, 0, C[0], C[1], C[2], color = 'orange', label = 'Vetor C')

    if resultado:
        if isinstance(resultado, (int, float)):
            res_vet = [resultado, 0, 0]
        else:
            res_vet = resultado
        ax.quiver(0, 0, 0, res_vet[0], res_vet[1], res_vet[2], color = 'green', label = 'Resultante')

    todos_valores = A + B
    if C:
        todos_valores += C
    if resultado:
        todos_valores += res_vet if isinstance(res_vet, list) else [res_vet]
    max_val = max(np.abs(todos_valores)) + 1
    ax.set_xlim([0, max_val])
    ax.set_ylim([0, max_val])
    ax.set_zlim([0, max_val])

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    if not os.path.exists("static"):
        os.makedirs("static")
    caminho = "static/grafico.png"
    pit.savefig(caminho)
    pit.close()
    return caminho

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

    cx = dados.get("cx")
    cy = dados.get("cy")
    cz = dados.get("cz")
    C = [cx, cy, cz] if cx is not None and cy is not None and cz is not None else None

    A = [ax, ay, az]
    B = [bx, by, bz]

    operacao = dados.get("operacao", "").lower()
    resultado = None

    if operacao == "adicao":
        resultado = [ax + bx, ay + by, az + bz]

    elif operacao == "multiplicacao_escalar":
        escalar = dados.get("escalar", 1)
        vetor = dados.get("vetor", "A").upper()  
        if vetor == "A":
            resultado = [ax * escalar, ay * escalar, az * escalar]
        elif vetor == "B":
            resultado = [bx * escalar, by * escalar, bz * escalar]
        else:
            resultado = [ax * escalar, ay * escalar, az * escalar]

    elif operacao == "produto_escalar":
        resultado = ax * bx + ay * by + az * bz

    elif operacao == "produto_vetorial":
        resultado = [
            ay * bz - az * by,
            az * bx - ax * bz,
            ax * by - ay * bx
        ]

    elif operacao == "produto_misto":
        if not C:
            return jsonify({"erro": "Produto misto requer vetor C"}), 400
        resultado = ax * (by * cz - bz * cy) - ay * (bx * cz - bz * cx) + az * (bx * cy - by * cx)

    else:
        return jsonify({"erro": "Operação inválida"}), 400

    caminho_grafico = gerar_grafico(A, B, C, resultado)

    return jsonify({
        "A": {"x": ax, "y": ay, "z": az},
        "B": {"x": bx, "y": by, "z": bz},
        "C": {"x": cx, "y": cy, "z": cz} if C else None,
        "resultado": resultado,
        "grafico": caminho_grafico
    })

if __name__ == '__main__':
    app.run(debug=True)
