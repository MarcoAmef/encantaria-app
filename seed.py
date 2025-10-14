# seed.py
from db import usuarios, anuncios, mensagens
from utils.auth import gerar_senha_hash
from bson import ObjectId
from datetime import datetime
import pprint

def seed():
    print("🧹 Limpando coleções...")
    usuarios.delete_many({})
    anuncios.delete_many({})
    mensagens.delete_many({})

    print("✨ Inserindo usuários de exemplo...")
    usuarios_docs = [
        {
            "nome": "Luna Andrade",
            "email": "luna@arte.com",
            "senha": gerar_senha_hash("senha123"),
            "descricao": "Cantora e compositora de MPB. Trabalho com apresentações em bares e eventos.",
            "tipo_usuario": "artista",
            "localizacao": {"cidade": "Belém", "estado": "PA"},
            "categorias": ["música", "voz", "MPB"],
            "portfolio": [{"link": "https://instagram.com/luna.mpb"}],
            "foto_url": None,
            "avaliacoes": [],
            "avaliacoes_resumo": {"media": None, "count": 0},
            "data_criacao": datetime.utcnow().isoformat()
        },
        {
            "nome": "Rafael Gomes",
            "email": "rafa@eventos.com",
            "senha": gerar_senha_hash("senha123"),
            "descricao": "Produtor cultural e organizador de eventos artísticos.",
            "tipo_usuario": "contratante",
            "localizacao": {"cidade": "Belém", "estado": "PA"},
            "categorias": ["produção", "eventos"],
            "portfolio": [],
            "foto_url": None,
            "avaliacoes": [],
            "avaliacoes_resumo": {"media": None, "count": 0},
            "data_criacao": datetime.utcnow().isoformat()
        },
        {
            "nome": "Clara Santos",
            "email": "clara@circo.com",
            "senha": gerar_senha_hash("senha123"),
            "descricao": "Malabarista e artista de circo. Atuo em festas infantis, praças e shows de rua.",
            "tipo_usuario": "artista",
            "localizacao": {"cidade": "Ananindeua", "estado": "PA"},
            "categorias": ["circo", "malabarismo"],
            "portfolio": [{"link": "https://instagram.com/claracirco"}],
            "foto_url": None,
            "avaliacoes": [],
            "avaliacoes_resumo": {"media": None, "count": 0},
            "data_criacao": datetime.utcnow().isoformat()
        },
        {
            "nome": "Marco Estrada",
            "email": "marco@encantaria.com",
            "senha": gerar_senha_hash("marco123"),
            "descricao": "Animador de festas, DJ e organizador de pequenos eventos.",
            "tipo_usuario": "artista",
            "localizacao": {"cidade": "Belém", "estado": "PA"},
            "categorias": ["animação", "DJ", "eventos"],
            "portfolio": [{"link": "https://instagram.com/marcoencanta"}],
            "foto_url": None,
            "avaliacoes": [],
            "avaliacoes_resumo": {"media": None, "count": 0},
            "data_criacao": datetime.utcnow().isoformat()
        }
    ]

    result = usuarios.insert_many(usuarios_docs)
    inserted_ids = result.inserted_ids
    print(f"Usuários inseridos: {len(inserted_ids)}")

    # Buscar usuários por email (para garantir ObjectId corretos)
    luna = usuarios.find_one({"email": "luna@arte.com"})
    rafa = usuarios.find_one({"email": "rafa@eventos.com"})
    clara = usuarios.find_one({"email": "clara@circo.com"})
    marco = usuarios.find_one({"email": "marco@encantaria.com"})

    print("✨ Inserindo anúncios de exemplo...")
    anuncios_docs = [
        {
            "usuario_id": luna["_id"],
            "titulo": "Procuro banda para barzinho - cantora disponível",
            "descricao": "Sou cantora de MPB e procuro músicos para apresentações semanais em barzinhos locais.",
            "categoria": "música",
            "tipo": "procura",
            "localizacao": {"cidade": "Belém", "estado": "PA"},
            "data_publicacao": datetime.utcnow().isoformat(),
            "status": "ativo"
        },
        {
            "usuario_id": rafa["_id"],
            "titulo": "Contratando artistas para feira cultural",
            "descricao": "Evento cultural no centro de Belém. Procuramos músicos, palhaços e performers para o dia 20/11.",
            "categoria": "eventos",
            "tipo": "procura",
            "localizacao": {"cidade": "Belém", "estado": "PA"},
            "data_publicacao": datetime.utcnow().isoformat(),
            "status": "ativo"
        },
        {
            "usuario_id": clara["_id"],
            "titulo": "Shows de malabarismo e circo para festas",
            "descricao": "Apresentações de malabarismo, equilibrismo e números cômicos para festas infantis e eventos empresariais.",
            "categoria": "circo",
            "tipo": "oferece",
            "localizacao": {"cidade": "Ananindeua", "estado": "PA"},
            "data_publicacao": datetime.utcnow().isoformat(),
            "status": "ativo"
        },
        {
            "usuario_id": marco["_id"],
            "titulo": "Animador e DJ para festas infantis",
            "descricao": "Animação completa com brincadeiras, músicas e sonorização. Atuo em Belém e região metropolitana.",
            "categoria": "animação",
            "tipo": "oferece",
            "localizacao": {"cidade": "Belém", "estado": "PA"},
            "data_publicacao": datetime.utcnow().isoformat(),
            "status": "ativo"
        }
    ]

    anuncios_result = anuncios.insert_many(anuncios_docs)
    print(f"Anúncios inseridos: {len(anuncios_result.inserted_ids)}")

    print("✨ Inserindo mensagens de exemplo...")
    mensagens_docs = [
        {
            "remetente_id": rafa["_id"],
            "destinatario_id": clara["_id"],
            "conteudo": "Oi Clara, adorei seu trabalho! Você tem disponibilidade para o evento da semana que vem?",
            "data_envio": datetime.utcnow().isoformat(),
            "lida": False
        },
        {
            "remetente_id": clara["_id"],
            "destinatario_id": rafa["_id"],
            "conteudo": "Olá Rafael! Tenho sim. Me envie os detalhes do horário e cachê.",
            "data_envio": datetime.utcnow().isoformat(),
            "lida": False
        },
        {
            "remetente_id": marco["_id"],
            "destinatario_id": luna["_id"],
            "conteudo": "Oi Luna, vi seu anúncio — topa uma apresentação num bar no sábado?",
            "data_envio": datetime.utcnow().isoformat(),
            "lida": False
        }
    ]

    mensagens.insert_many(mensagens_docs)
    print(f"Mensagens inseridas: {len(mensagens_docs)}")

    print("✅ Seed concluído com sucesso!")
    print("\nUsuários inseridos (exemplo):")
    for u in usuarios.find({}, {"senha": 0}).limit(10):
        pprint.pprint({k: v for k, v in u.items()})

if __name__ == "__main__":
    seed()
