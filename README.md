# 🖥️ Sistema de Monitoramento com Zabbix + Python + SQL + ELK Stack
 
> Projeto pessoal de aprendizado para monitorar servidores e serviços usando ferramentas open source.
 
---
 
## 📌 Objetivo
 
Criar um sistema completo de monitoramento que:
- Coleta métricas de servidores e serviços (CPU, memória, disco, rede)
- Armazena histórico em banco de dados SQL
- Processa e enriquece dados com scripts Python
- Indexa logs com a ELK Stack (Elasticsearch, Logstash, Kibana)
- Visualiza tudo em dashboards e dispara alertas automáticos
 
---
 
## 🏗️ Arquitetura
 
```
┌─────────────────────────────────────────────────────────┐
│                   CAMADA 1 — ORIGENS                    │
│   Servidor / VM    Serviço / App    Logs do sistema     │
└────────┬──────────────────┬──────────────┬──────────────┘
         │                  │              │
         ▼                  ▼              ▼
┌─────────────────────────────────────────────────────────┐
│                   CAMADA 2 — COLETA                     │
│   Zabbix Server + Agente      Logstash / Filebeat       │
└────────────────┬────────────────────────┬───────────────┘
                 │                        │
                 ▼                        ▼
┌─────────────────────────────────────────────────────────┐
│            CAMADA 3 — PROCESSAMENTO                     │
│      Bot Python (scripts)        Elasticsearch          │
│      Banco SQL                                          │
└────────────────┬────────────────────────┬───────────────┘
                 │                        │
                 ▼                        ▼
┌─────────────────────────────────────────────────────────┐
│               CAMADA 4 — VISUALIZAÇÃO                   │
│       Dashboard Zabbix           Kibana                 │
└─────────────────────────────────────────────────────────┘
```
 
---
 
## 🧰 Tecnologias utilizadas
 
| Tecnologia | Papel no projeto |
|---|---|
| **Zabbix** | Coleta métricas de servidores e serviços via agente |
| **Python** | Scripts de automação, alertas e integração via API |
| **SQL** (MySQL ou PostgreSQL) | Armazena histórico de métricas e incidentes |
| **Elasticsearch** | Indexa e armazena logs para busca rápida |
| **Logstash / Filebeat** | Coleta e envia logs ao Elasticsearch |
| **Kibana** | Dashboards visuais de logs e eventos |
 
---
 
## 🤖 Como o agente Zabbix funciona
 
O agente Zabbix é um programa leve instalado em cada máquina monitorada. Ele opera em dois modos:
 
- **Modo passivo:** o servidor Zabbix consulta o agente periodicamente (ex: a cada 1 minuto)
- **Modo ativo:** o agente envia os dados por conta própria, ideal para máquinas atrás de firewall
 
O agente coleta: CPU, memória, disco, rede, processos, logs e checks personalizados via scripts.
 
### Instalação rápida do agente (Ubuntu/Debian)
 
```bash
apt install zabbix-agent
 
# Editar configuração
nano /etc/zabbix/zabbix_agentd.conf
# Alterar: Server=<IP_DO_SERVIDOR_ZABBIX>
 
# Iniciar o serviço
systemctl enable --now zabbix-agent
```
 
---
 
## 📁 Estrutura do repositório
 
```
📦 monitoramento/
├── 📂 zabbix/
│   ├── templates/          # Templates de monitoramento exportados
│   └── scripts/            # Scripts customizados para checks
├── 📂 python/
│   ├── bot_alertas.py      # Bot de alertas (Telegram/e-mail)
│   ├── coleta_api.py       # Consulta à API do Zabbix
│   └── requirements.txt    # Dependências Python
├── 📂 sql/
│   ├── schema.sql          # Estrutura do banco de dados
│   └── queries/            # Consultas úteis
├── 📂 elk/
│   ├── logstash.conf       # Pipeline do Logstash
│   ├── filebeat.yml        # Configuração do Filebeat
│   └── kibana/             # Dashboards exportados
├── 📂 docs/
│   └── arquitetura.md      # Detalhamento da arquitetura
└── README.md
```
 
---
 
## 🚀 Roadmap de implementação
 
- [ ] Instalar e configurar o Zabbix Server
- [ ] Instalar o agente Zabbix em uma máquina de teste
- [ ] Criar o primeiro dashboard no Zabbix
- [ ] Criar script Python que consome a API do Zabbix
- [ ] Modelar e criar o banco de dados SQL
- [ ] Configurar Filebeat + Logstash + Elasticsearch
- [ ] Criar dashboard no Kibana
- [ ] Implementar bot de alertas (Telegram ou e-mail)
- [ ] Documentar cada etapa com prints e exemplos
 
---
 
## 📚 Referências e links úteis
 
- [Documentação oficial do Zabbix](https://www.zabbix.com/documentation)
- [API do Zabbix](https://www.zabbix.com/documentation/current/en/manual/api)
- [Elastic Stack (ELK)](https://www.elastic.co/guide/index.html)
- [Documentação do Python](https://docs.python.org/3/)
 
---
 
## 👩‍💻 Sobre o projeto
 
Projeto em desenvolvimento como parte do aprendizado em monitoramento de infraestrutura.  
Contribuições, sugestões e dúvidas são bem-vindas via Issues!
 