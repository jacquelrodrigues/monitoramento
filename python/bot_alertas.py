import requests
import mysql.connector
import os
from dotenv import load_dotenv

# ──────────────────────────────────────────
# CONFIGURAÇÕES — carregadas do arquivo .env
# ──────────────────────────────────────────
load_dotenv()

TELEGRAM_TOKEN   = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

MYSQL_HOST    = os.getenv("MYSQL_HOST")
MYSQL_USUARIO = os.getenv("MYSQL_USUARIO")
MYSQL_SENHA   = os.getenv("MYSQL_SENHA")
MYSQL_BANCO   = os.getenv("MYSQL_BANCO")

# ──────────────────────────────────────────
# LIMITES DE ALERTA
# ──────────────────────────────────────────
LIMITES = {
    "CPU utilization":    25.0,   # alerta se CPU > 10%
    "Memory utilization": 50.0,   # alerta se memória > %
    "vm.memory.util":     50.0,   # chave alternativa do Windows
    "Used disk space":    85.0,   # alerta se disco > 85%
}


# ──────────────────────────────────────────
# ENVIAR MENSAGEM NO TELEGRAM
# ──────────────────────────────────────────
def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text":    mensagem,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            print(f"✅ Alerta enviado: {mensagem[:50]}...")
        else:
            print(f"❌ Erro ao enviar alerta: {r.text}")
    except Exception as e:
        print(f"❌ Erro de conexão com Telegram: {e}")


# ──────────────────────────────────────────
# CONECTAR AO BANCO
# ──────────────────────────────────────────
def conectar():
    try:
        conn = mysql.connector.connect(
            host     = MYSQL_HOST,
            user     = MYSQL_USUARIO,
            password = MYSQL_SENHA,
            database = MYSQL_BANCO
        )
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        exit()


# ──────────────────────────────────────────
# VERIFICAR ALERTAS
# ──────────────────────────────────────────
def verificar_alertas():
    print("🔍 Verificando métricas...\n")
    conn = conectar()
    cursor = conn.cursor()

    # Busca a métrica mais recente de cada host
    cursor.execute("""
        SELECT host_nome, metrica, chave, valor, unidade, coletado_em
        FROM metricas m1
        WHERE coletado_em = (
            SELECT MAX(coletado_em)
            FROM metricas m2
            WHERE m1.host_nome = m2.host_nome
            AND m1.metrica = m2.metrica
        )
        ORDER BY host_nome, metrica
    """)

    registros = cursor.fetchall()
    cursor.close()
    conn.close()

    alertas_encontrados = False

    for r in registros:
        host_nome, metrica, chave, valor, unidade, coletado_em = r

        # Verifica se a métrica tem um limite definido
        limite = None
        for chave_limite, valor_limite in LIMITES.items():
            if chave_limite.lower() in metrica.lower() or chave_limite.lower() in chave.lower():
                limite = valor_limite
                break

        if limite is None:
            continue

        try:
            valor_float = float(valor)
        except ValueError:
            continue

        status = "✅ Normal"
        if valor_float >= limite:
            status = "🔴 CRÍTICO"
            alertas_encontrados = True

            mensagem = (
                f"⚠️ <b>ALERTA DE MONITORAMENTO</b>\n\n"
                f"🖥️ Host: <b>{host_nome}</b>\n"
                f"📊 Métrica: {metrica}\n"
                f"📈 Valor atual: <b>{valor_float:.1f}{unidade}</b>\n"
                f"🚨 Limite: {limite}%\n"
                f"🕐 Horário: {coletado_em}"
            )
            enviar_telegram(mensagem)

        print(f"  {status} | {host_nome} | {metrica}: {valor_float:.1f}{unidade} (limite: {limite}%)")

    if not alertas_encontrados:
        print("\n✅ Tudo dentro dos limites, nenhum alerta disparado.")


# ──────────────────────────────────────────
# EXECUÇÃO PRINCIPAL
# ──────────────────────────────────────────
if __name__ == "__main__":
    print("🤖 Bot de alertas iniciado!\n")
    verificar_alertas()