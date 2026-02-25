from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# Permite que o celular se conecte à API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FILE_PATH = "sequencia.json"

def read_json():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, 'r') as f:
        return json.load(f)

@app.get("/get-config")
async def get_config():
    return read_json()

# A MÁGICA ACONTECE AQUI: Adicionamos o " = Body(...)"
@app.post("/save-config")
async def save_config(data: list = Body(...)):
    try:
        with open(FILE_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        return {"status": "sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Roda no IP do seu computador na porta 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)