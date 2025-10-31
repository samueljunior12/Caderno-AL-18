# app.py - Backend Flask para salvar/carregar logs em um arquivo JSON e servir o frontend

from flask import Flask, request, jsonify, render_template # render_template adicionado
from flask_cors import CORS
import json
import os

# NOTA: Assumindo que o arquivo 'index.html' está na pasta 'templates/'
app = Flask(__name__)

# Configuração do CORS: Permite requisições de qualquer origem para a API
CORS(app)

# Caminho para o arquivo onde os logs serão salvos
LOGS_FILE = 'logs.json'


# --- Funções de Leitura/Escrita de Arquivo ---

def load_logs():
    """Carrega os logs do arquivo JSON. Cria um arquivo vazio se não existir."""
    if not os.path.exists(LOGS_FILE):
        with open(LOGS_FILE, 'w', encoding='utf-8') as f:
            f.write('[]')
        return []

    try:
        with open(LOGS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []  # Garante que é uma lista
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"Erro ao ler ou parsear {LOGS_FILE}. Iniciando com array vazio.")
        return []


def save_logs(logs):
    """Salva o array de logs no arquivo JSON com formatação."""
    try:
        with open(LOGS_FILE, 'w', encoding='utf-8') as f:
            # indent=2 formata o JSON para fácil leitura
            json.dump(logs, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar logs.json: {e}")


# --- Endpoints da API REST ---

# Rota 4. GET /: Rota principal para servir a interface HTML
@app.route('/', methods=['GET'])
def serve_frontend():
    """Serve o arquivo index.html da pasta 'templates'."""
    # O Flask procura automaticamente por 'index.html' na pasta 'templates'
    return render_template('index.html')

# Rota 1. GET /api/logs: Retorna todos os logs
@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Rota para carregar os logs no Frontend."""
    logs = load_logs()
    return jsonify(logs), 200


# Rota 2. POST /api/logs: Recebe o array completo do Frontend e salva
@app.route('/api/logs', methods=['POST'])
def save_data():
    """Rota para salvar o array completo de logs enviado pelo Frontend."""
    # Garante que o conteúdo é JSON
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    new_logs = request.get_json()

    # Garante que o payload é um array
    if not isinstance(new_logs, list):
        return jsonify({"error": "A requisição deve conter um array de logs."}), 400

    save_logs(new_logs)

    print(f"Logs atualizados no servidor. Total de registros: {len(new_logs)}")
    return jsonify({"message": "Logs salvos com sucesso no backend.", "total": len(new_logs)}), 200


# Rota 3. DELETE /api/logs/all: Rota para limpar todos os dados (opcional)
@app.route('/api/logs/all', methods=['DELETE'])
def clear_logs():
    """Rota para apagar todos os logs."""
    save_logs([])
    print("Todos os logs foram apagados.")
    return jsonify({"message": "Todos os logs foram apagados."}), 200


# --- Inicialização do Servidor ---
if __name__ == '__main__':
    # Inicializa o arquivo logs.json se ele não existir
    load_logs()

    print(f"\n=================================================")
    print(f"✅ Servidor Flask Iniciado!")
    print(f"Rodando em: http://127.0.0.1:5000/ (Para o Frontend)")
    print(f"URL da API: http://127.0.0.1:5000/api/logs")
    print(f"=================================================\n")

    # Roda a aplicação Flask na porta padrão 5000
    app.run(debug=True, port=5000)
