import requests
import json
from dotenv import load_dotenv
import os

# ──────────────────────────────────────────
# CONFIGURAÇÕES — ajuste para o seu ambiente
# ──────────────────────────────────────────
load_dotenv()

ZABBIX_URL = os.getenv("ZABBIX_URL")
USUARIO    = os.getenv("ZABBIX_USUARIO")
SENHA      = os.getenv("ZABBIX_SENHA")


# ──────────────────────────────────────────
# FUNÇÃO BASE — envia qualquer chamada à API
# ──────────────────────────────────────────
def zabbix_api(metodo, params, token=None):
    payload = {
        "jsonrpc": "2.0",
        "method":  metodo,
        "params":  params,
        "id":      1,
    }
    if token:
        payload["auth"] = token

    resposta = requests.post(
        ZABBIX_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    return resposta.json().get("result")


# ──────────────────────────────────────────
# PASSO 1 — Autenticar e obter o token
# ──────────────────────────────────────────
def autenticar():
    token = zabbix_api("user.login", {
        "username": USUARIO,
        "password": SENHA
    })
    if token:
        print(f"✅ Autenticado com sucesso! Token: {token[:10]}...")
    else:
        print("❌ Falha na autenticação. Verifique usuário e senha.")
        exit()
    return token


# ──────────────────────────────────────────
# PASSO 2 — Listar todos os hosts cadastrados
# ──────────────────────────────────────────
def listar_hosts(token):
    hosts = zabbix_api("host.get", {
        "output": ["hostid", "host", "name", "status"]
    }, token)

    print("\n📋 Hosts cadastrados no Zabbix:")
    print("-" * 40)
    for h in hosts:
        status = "✅ Ativo" if h["status"] == "0" else "⛔ Desabilitado"
        print(f"  ID: {h['hostid']}  |  Nome: {h['name']}  |  {status}")
    print("-" * 40)
    return hosts


# ──────────────────────────────────────────
# PASSO 3 — Buscar métricas recentes de um host
# ──────────────────────────────────────────
def buscar_metricas(token, host_id, host_nome):

    print(f"\n{'=' * 50}")
    print(f"  📊 {host_nome}")
    print(f"{'=' * 50}")

    items = zabbix_api("item.get", {
        "output":  ["itemid", "name", "key_", "lastvalue", "units"],
        "hostids": host_id,
        "search":  {"key_": "system.cpu"},
        "filter":  {"state": 0},
        "limit":   50
    }, token)

    items += zabbix_api("item.get", {
        "output":  ["itemid", "name", "key_", "lastvalue", "units"],
        "hostids": host_id,
        "search":  {"key_": "vm.memory"},
        "filter":  {"state": 0},
        "limit":   10
    }, token)

    items += zabbix_api("item.get", {
        "output":  ["itemid", "name", "key_", "lastvalue", "units"],
        "hostids": host_id,
        "search":  {"key_": "vfs.fs.size"},
        "filter":  {"state": 0},
        "limit":   10
    }, token)

    for item in items:
        valor   = item.get("lastvalue", "sem dado")
        unidade = item.get("units", "")
        print(f"  {item['name']}")
        print(f"    Valor: {valor} {unidade}")
        print(f"    Chave: {item['key_']}")
        print()

    print("=" * 50)


# ──────────────────────────────────────────
# EXECUÇÃO PRINCIPAL
# ──────────────────────────────────────────
if __name__ == "__main__":
    print("🔌 Conectando ao Zabbix...\n")

    token = autenticar()
    hosts = listar_hosts(token)

    if hosts:
        for host in hosts:
            buscar_metricas(token, host["hostid"], host["name"])
    else:
        print("Nenhum host encontrado.")