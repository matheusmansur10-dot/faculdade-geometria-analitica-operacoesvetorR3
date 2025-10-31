from flask import Flask, jsonify, request 

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"mensagem": "API de vetores em R³ funcionando!"})

if __name__ == '__main__':
    app.run(debug = True)