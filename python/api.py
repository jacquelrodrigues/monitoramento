import json
import fastapi
from banco import conectar
from bot_alertas import enviar_telegram

app = fastapi.FastAPI()

@app.post("/alerta")
async def receber_alerta(request: fastapi.Request):
    body = await request.body()
    data = json.loads(body)
    
    print("📥 Alerta recebido:", data)
    
    host     = data.get("host")
    problema = data.get("trigger")
    valor    = data.get("valor")
    status   = data.get("status")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO incidentes (host, problema, valor, status, data_abertura)
        VALUES (%s, %s, %s, %s, NOW())
    """, (host, problema, valor, status))
    conn.commit()
    cursor.close()
    conn.close()

    mensagem = f"""
🚨 ALERTA
Host: {host}
Problema: {problema}
Valor: {valor}
Status: {status}
"""
    enviar_telegram(mensagem)
    return {"status": "ok"}