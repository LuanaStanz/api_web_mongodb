from fastapi import APIRouter, HTTPException
from modelos import Atendente

router = APIRouter(prefix="/atendentes", tags=["Atendentes"])

# | GET | `/atendentes/` | Listar atendentes |
@router.get("/")
async def listar_atendentes():
    return await Atendente.find_all().to_list()

# | POST | `/atendentes/` | Criar atendente |
@router.post("/")
async def criar_atendente(atendente: Atendente):
    await atendente.insert()
    return atendente

# | GET | `/atendentes/buscar/nome` | Buscar atendente por nome |
@router.get("/buscar/nome")
async def buscar_atendente_por_nome(nome: str):
    return await Atendente.find(
        {"nome": {"$regex": nome, "$options": "i"}}
    ).to_list()

# | PUT | `/atendentes/{atendente_id}` | Atualizar atendente |
@router.put("/{atendente_id}")
async def atualizar_atendente(atendente_id: str, dados: dict):
    atendente = await Atendente.get(atendente_id)

    if not atendente:
        raise HTTPException(
            status_code=404,
            detail="Atendente não encontrado"
        )

    await atendente.set(dados)
    return atendente

# | DELETE | `/atendentes/{atendente_id}` | Deletar atendente |
@router.delete("/{atendente_id}")
async def deletar_atendente(atendente_id: str):
    atendente = await Atendente.get(atendente_id)

    if not atendente:
        raise HTTPException(
            status_code=404,
            detail="Atendente não encontrado"
        )

    await atendente.delete()
    return {"msg": "Atendente removido com sucesso"}

# | GET | `/atendentes/{atendente_id}` | Buscar atendente por ID |
@router.get("/{atendente_id}")
async def buscar_atendente_por_id(atendente_id: str):
    atendente = await Atendente.get(atendente_id)

    if not atendente:
        raise HTTPException(
            status_code=404,
            detail="Atendente não encontrado"
        )

    return atendente
