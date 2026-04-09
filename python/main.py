import time
from coleta_api import autenticar, listar_hosts, buscar_metricas

# ──────────────────────────────────────────
# CONFIGURAÇÕES GERAIS
# ──────────────────────────────────────────
INTERVALO_SEGUNDOS = 60   # coleta métricas a cada 60 segundos


# ──────────────────────────────────────────
# LOOP PRINCIPAL
# ──────────────────────────────────────────
def main():
    print("🚀 Sistema de monitoramento iniciado!\n")

    # 1. Autenticar no Zabbix
    token = autenticar()

    # 2. Listar hosts disponíveis
    hosts = listar_hosts(token)

    if not hosts:
        print("❌ Nenhum host encontrado. Verifique o Zabbix.")
        return

    # 3. Loop de coleta contínua
    print(f"\n🔄 Coletando métricas a cada {INTERVALO_SEGUNDOS}s... (Ctrl+C para parar)\n")
    while True:
        for host in hosts:
            buscar_metricas(token, host["hostid"], host["name"])

            # 🔜 Em breve: salvar no banco SQL
            # salvar_banco(metricas)

            # 🔜 Em breve: verificar alertas
            # verificar_alertas(metricas)

        time.sleep(INTERVALO_SEGUNDOS)


if __name__ == "__main__":
    main()