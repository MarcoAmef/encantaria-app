from flask import Flask, jsonify, request
from flask_cors import CORS
from bson import ObjectId
from db import usuarios, anuncios, mensagens
from utils.auth import gerar_token, gerar_senha_hash, verificar_senha, decodificar_token
from utils.cloudinary_upload import upload_image
from datetime import datetime

app = Flask(__name__)
CORS(app)

def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# 🧍 Registro
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if usuarios.find_one({"email": data["email"]}):
        return jsonify({"error": "Email já cadastrado"}), 400

    data["senha"] = gerar_senha_hash(data["senha"])
    data["data_criacao"] = datetime.utcnow().isoformat()
    usuarios.insert_one(data)
    return jsonify({"message": "Usuário registrado com sucesso!"}), 201

# 🔐 Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    usuario = usuarios.find_one({"email": data["email"]})
    if not usuario or not verificar_senha(data["senha"], usuario["senha"]):
        return jsonify({"error": "Credenciais inválidas"}), 401

    token = gerar_token(usuario["_id"])
    return jsonify({"token": token})

# 👤 Perfil (GET)
@app.route("/usuarios/<id>", methods=["GET"])
def get_user(id):
    usuario = usuarios.find_one({"_id": ObjectId(id)})
    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return jsonify(serialize_doc(usuario))

# 🎭 Listar artistas
@app.route("/usuarios", methods=["GET"])
def get_all_users():
    lista = [serialize_doc(u) for u in usuarios.find()]
    return jsonify(lista)

# 📢 Criar anúncio
@app.route("/anuncios", methods=["POST"])
def criar_anuncio():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token ausente"}), 401
    payload = decodificar_token(token)
    if not payload:
        return jsonify({"error": "Token inválido"}), 401

    data = request.json
    data["usuario_id"] = ObjectId(payload["id"])
    data["data_publicacao"] = datetime.utcnow().isoformat()
    anuncios.insert_one(data)
    return jsonify({"message": "Anúncio criado com sucesso!"}), 201

# 🔎 Buscar anúncios
@app.route("/anuncios", methods=["GET"])
def listar_anuncios():
    todos = [serialize_doc(a) for a in anuncios.find()]
    return jsonify(todos)

# 📬 Enviar mensagem
@app.route("/mensagens", methods=["POST"])
def enviar_mensagem():
    data = request.json
    mensagens.insert_one({
        "remetente_id": ObjectId(data["remetente_id"]),
        "destinatario_id": ObjectId(data["destinatario_id"]),
        "conteudo": data["conteudo"],
        "data_envio": datetime.utcnow().isoformat(),
        "lida": False
    })
    return jsonify({"message": "Mensagem enviada!"}), 201

# 🌟 Avaliar usuário
@app.route("/avaliar/<id>", methods=["POST"])
def avaliar_usuario(id):
    data = request.json
    avaliacao = {
        "usuario_id": data.get("avaliador_id"),
        "nota": data.get("nota"),
        "comentario": data.get("comentario")
    }
    usuarios.update_one({"_id": ObjectId(id)}, {"$push": {"avaliacoes": avaliacao}})
    return jsonify({"message": "Avaliação registrada!"}), 200

# 📸 Upload de imagem
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    file = request.files["file"]
    url = upload_image(file)
    return jsonify({"url": url})

if __name__ == "__main__":
    app.run(debug=True)
