import time
from datetime import datetime
from coleta_api import autenticar, listar_hosts, buscar_metricas
from banco import conectar
from bot_alertas import verificar_alertas

# ──────────────────────────────────────────
# CONFIGURAÇÕES
# ──────────────────────────────────────────
INTERVALO_SEGUNDOS = 300   # 5 minutos


# ──────────────────────────────────────────
# LOOP PRINCIPAL
# ──────────────────────────────────────────
def main():
    print("🚀 Sistema de monitoramento iniciado!")
    print(f"🔄 Ciclo a cada {INTERVALO_SEGUNDOS // 60} minutos\n")

    while True:
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"\n{'=' * 50}")
        print(f"  🕐 Ciclo iniciado em {agora}")
        print(f"{'=' * 50}")

        try:
            # 1. Autenticar no Zabbix
            token = autenticar()

            # 2. Listar hosts
            hosts = listar_hosts(token)

            if hosts:
                # 3. Conectar ao banco
                conn = conectar()

                # 4. Coletar e salvar métricas de cada host
                for host in hosts:
                    buscar_metricas(token, host["hostid"], host["name"], conn)

                conn.close()

                # 5. Verificar alertas e notificar no Telegram
                print("\n")
                verificar_alertas()

            else:
                print("❌ Nenhum host encontrado.")

        except Exception as e:
            print(f"\n❌ Erro no ciclo: {e}")

        # 6. Aguardar próximo ciclo
        print(f"\n⏳ Próximo ciclo em {INTERVALO_SEGUNDOS // 60} minutos...")
        time.sleep(INTERVALO_SEGUNDOS)


if __name__ == "__main__":
    main()