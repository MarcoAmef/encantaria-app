from db import get_conn
from utils.auth import gerar_senha_hash
from datetime import datetime

def seed():
    conn = get_conn()
    cursor = conn.cursor()

    # Limpa tabelas
    cursor.execute("DELETE FROM usuarios")
    cursor.execute("DELETE FROM anuncios")
    cursor.execute("DELETE FROM mensagens")

    now = datetime.utcnow().isoformat()

    # Usuários de exemplo
    usuarios = [
        ("Luna Andrade","luna@arte.com",gerar_senha_hash("senha123"),"Cantora e compositora de MPB","artista","Belém","PA","música,voz,MPB","https://instagram.com/luna.mpb",None,now),
        ("Rafael Gomes","rafa@eventos.com",gerar_senha_hash("senha123"),"Produtor cultural","contratante","Belém","PA","produção,eventos","",None,now),
        ("Clara Santos","clara@circo.com",gerar_senha_hash("senha123"),"Malabarista e artista de circo","artista","Ananindeua","PA","circo,malabarismo","https://instagram.com/claracirco",None,now),
        ("Marco Estrada","marco@encantaria.com",gerar_senha_hash("marco123"),"Animador de festas, DJ e organizador de pequenos eventos","artista","Belém","PA","animação,DJ,eventos","https://instagram.com/marcoencanta",None,now)
    ]
    cursor.executemany("""
        INSERT INTO usuarios
        (nome,email,senha,descricao,tipo_usuario,cidade,estado,categorias,portfolio,foto_url,data_criacao)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, usuarios)

    # Busca IDs para anúncios
    cursor.execute("SELECT id,email FROM usuarios")
    user_map = {row["email"]: row["id"] for row in cursor.fetchall()}

    anuncios = [
        (user_map["luna@arte.com"],"Procuro banda para barzinho - cantora disponível",
         "Sou cantora de MPB e procuro músicos para apresentações semanais em barzinhos locais.",
         "música","procura","Belém","PA",now),
        (user_map["rafa@eventos.com"],"Contratando artistas para feira cultural",
         "Evento cultural no centro de Belém. Procuramos músicos, palhaços e performers.",
         "eventos","procura","Belém","PA",now),
        (user_map["clara@circo.com"],"Shows de malabarismo e circo para festas",
         "Apresentações de malabarismo, equilibrismo e números cômicos para festas infantis.",
         "circo","oferece","Ananindeua","PA",now),
        (user_map["marco@encantaria.com"],"Animador e DJ para festas infantis",
         "Animação completa com brincadeiras, músicas e sonorização. Atuo em Belém e região.",
         "animação","oferece","Belém","PA",now)
    ]
    cursor.executemany("""
        INSERT INTO anuncios
        (usuario_id,titulo,descricao,categoria,tipo,cidade,estado,data_publicacao)
        VALUES (?,?,?,?,?,?,?,?)
    """, anuncios)

    conn.commit()
    conn.close()
    print("✅ Seed concluído com sucesso!")

if __name__ == "__main__":
    seed()
