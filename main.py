from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import json
import os

# Importando o controle do seu projeto
from Conexoes.controlePS4 import controle

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FILE_PATH = "sequencia.json" # Lembre de ajustar para "Parametros/parametros.json" se for o caso!

def read_json():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, 'r') as f:
        return json.load(f)

# 🚦 NOVO ENDPOINT: O App vai ficar perguntando aqui se pode editar
@app.get("/status")
async def get_status():
    # Retorna True se estiver travado (seguro), e False se estiver andando (perigo)
    return {"trava": controle.travaDeLocomocao}

@app.get("/get-config")
async def get_config():
    return read_json()

@app.post("/save-config")
async def save_config(data: list = Body(...)):
    # BLINDAGEM: Se a trava estiver False (robô andando), ele rejeita o salvamento
    if controle.travaDeLocomocao == False:
        raise HTTPException(status_code=403, detail="Robô em movimento! Edição bloqueada.")

    try:
        with open(FILE_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        return {"status": "sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
