import mysql.connector
import os
from dotenv import load_dotenv

# ──────────────────────────────────────────
# CONFIGURAÇÕES — carregadas do arquivo .env
# ──────────────────────────────────────────
load_dotenv()

MYSQL_HOST    = os.getenv("MYSQL_HOST")
MYSQL_USUARIO = os.getenv("MYSQL_USUARIO")
MYSQL_SENHA   = os.getenv("MYSQL_SENHA")
MYSQL_BANCO   = os.getenv("MYSQL_BANCO")


# ──────────────────────────────────────────
# CONEXÃO — abre e retorna a conexão com o banco
# ──────────────────────────────────────────
def conectar():
    try:
        conn = mysql.connector.connect(
            host     = MYSQL_HOST,
            user     = MYSQL_USUARIO,
            password = MYSQL_SENHA,
            database = MYSQL_BANCO
        )
        print("✅ Conectado ao banco de dados!")
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        exit()


# ──────────────────────────────────────────
# SALVAR — insere uma métrica na tabela
# ──────────────────────────────────────────
def salvar_metrica(conn, host_id, host_nome, metrica, chave, valor, unidade):
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO metricas (host_id, host_nome, metrica, chave, valor, unidade)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (host_id, host_nome, metrica, chave, valor, unidade))
        conn.commit()
        cursor.close()
    except mysql.connector.Error as e:
        print(f"❌ Erro ao salvar métrica: {e}")


# ──────────────────────────────────────────
# LISTAR — mostra as últimas métricas salvas
# ──────────────────────────────────────────
def listar_metricas(conn, limite=10):
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT host_nome, metrica, valor, unidade, coletado_em
            FROM metricas
            ORDER BY coletado_em DESC
            LIMIT {limite}
        """)
        registros = cursor.fetchall()
        cursor.close()

        print(f"\n📋 Últimas {limite} métricas salvas:")
        print("-" * 60)
        for r in registros:
            print(f"  Host: {r[0]}  |  {r[1]}: {r[2]} {r[3]}  |  {r[4]}")
        print("-" * 60)
    except mysql.connector.Error as e:
        print(f"❌ Erro ao listar métricas: {e}")


# ──────────────────────────────────────────
# TESTE — executa ao rodar o arquivo direto
# ──────────────────────────────────────────
if __name__ == "__main__":
    conn = conectar()

    # Insere um registro de teste
    salvar_metrica(
        conn,
        host_id   = "99999",
        host_nome = "teste",
        metrica   = "CPU utilization",
        chave     = "system.cpu.util",
        valor     = "5.5",
        unidade   = "%"
    )
    print("✅ Métrica de teste inserida!")

    # Lista os registros salvos
    listar_metricas(conn)

    conn.close()