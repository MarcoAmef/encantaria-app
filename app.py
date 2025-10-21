from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from db import get_conn
from utils.auth import gerar_token, gerar_senha_hash, verificar_senha, decodificar_token
from utils.cloudinary_upload import upload_image
from datetime import datetime
import os
import json

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

def serialize_row(row):
    return dict(row)

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

# Registro
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=?", (data["email"],))
    if cursor.fetchone():
        return jsonify({"error":"Email já cadastrado"}),400
    senha_hash = gerar_senha_hash(data["senha"])
    now = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO usuarios (nome,email,senha,descricao,tipo_usuario,cidade,estado,categorias,portfolio,foto_url,data_criacao)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data.get("nome"),
        data.get("email"),
        senha_hash,
        data.get("descricao",""),
        data.get("tipo_usuario","artista"),
        data.get("cidade",""),
        data.get("estado",""),
        ",".join(data.get("categorias",[])),
        json.dumps(data.get("portfolio",[])),
        data.get("foto_url",None),
        now
    ))
    conn.commit()
    conn.close()
    return jsonify({"message":"Usuário registrado com sucesso!"}),201

# Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=?",(data["email"],))
    row = cursor.fetchone()
    conn.close()
    if not row or not verificar_senha(data["senha"], row["senha"]):
        return jsonify({"error":"Credenciais inválidas"}),401
    token = gerar_token(row["id"])
    return jsonify({"token": token})

# Listar usuários
@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([serialize_row(r) for r in rows])

# Criar anúncio
@app.route("/anuncios", methods=["POST"])
def criar_anuncio():
    token = request.headers.get("Authorization")
    payload = decodificar_token(token) if token else None
    if not payload:
        return jsonify({"error":"Token inválido"}),401
    data = request.json
    now = datetime.utcnow().isoformat()
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO anuncios (usuario_id,titulo,descricao,categoria,tipo,cidade,estado,data_publicacao)
        VALUES (?,?,?,?,?,?,?,?)
    """, (
        payload["id"],
        data.get("titulo"),
        data.get("descricao"),
        data.get("categoria"),
        data.get("tipo"),
        data.get("cidade",""),
        data.get("estado",""),
        now
    ))
    conn.commit()
    conn.close()
    return jsonify({"message":"Anúncio criado com sucesso!"}),201

# Listar anúncios
@app.route("/anuncios", methods=["GET"])
def listar_anuncios():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM anuncios")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([serialize_row(r) for r in rows])

# Upload de imagem
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error":"Nenhum arquivo enviado"}),400
    file = request.files["file"]
    url = upload_image(file)
    return jsonify({"url": url})

if __name__ == "__main__":
    app.run(debug=True)
