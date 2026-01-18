from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import date
from modelos import Animal, Adocao

router = APIRouter(prefix="/animais", tags=["Animais"])

#POST /animais/ – Criar animal
@router.post("/")
async def criar_animal(animal: Animal):
    await animal.insert()
    return animal

#GET /animais/ – Listar animais
@router.get("/")
async def listar_animais():
    return await Animal.find_all().to_list()

#GET /animais/{animal_id} – Buscar por ID
@router.get("/{animal_id}")
async def buscar_animal(animal_id: str):
    animal = await Animal.get(animal_id)
    if not animal:
        raise HTTPException(404, "Animal não encontrado")
    return animal

#GET /animais/buscar/nome - Busca parcial + case-insensitive
@router.get("/buscar/nome")
async def buscar_por_nome(nome: str):
    return await Animal.find(
        {"nome": {"$regex": nome, "$options": "i"}}
    ).to_list()

#GET /animais/resgatados/ano
@router.get("/resgatados/ano")
async def resgatados_por_ano(ano: int):
    inicio = date(ano, 1, 1)
    fim = date(ano, 12, 31)

    return await Animal.find(
        {"data_resgate": {"$gte": inicio, "$lte": fim}}
    ).to_list()

#GET /animais/disponiveis
@router.get("/disponiveis")
async def animais_disponiveis():
    return await Animal.find(Animal.status_adocao == False).to_list()

#GET /animais/ordenar/idade
@router.get("/ordenar/idade")
async def ordenar_por_idade():
    return await Animal.find_all().sort("idade").to_list()

#GET /animais/stats/total
@router.get("/stats/total")
async def total_animais():
    return {"total": await Animal.count()}

#/animais/stats/status/{status}
@router.get("/stats/status/{status}")
async def total_por_status(status: int):
    return {
        "total": await Animal.find(
            Animal.status_adocao == bool(status)
        ).count()
    }

#/animais/adotados/adotante - Consulta envolvendo múltiplas coleções
@router.get("/adotados/adotante")
async def animais_por_adotante(adotante_id: str):
    adocoes = await Adocao.find(
        Adocao.adotante.id == adotante_id
    ).to_list(fetch_links=True)

    return [a.animal for a in adocoes]

# | GET | `/animais/stats/status/0` | Total de animais disponíveis |
@router.get("/stats/status/0")
async def total_animais_disponiveis():
    total = await Animal.find(Animal.status_adocao == False).count()
    return {"total_disponiveis": total}

# | GET | `/animais/stats/status/1` | Total de animais adotados |
@router.get("/stats/status/1")
async def total_animais_adotados():
    total = await Animal.find(Animal.status_adocao == True).count()
    return {"total_adotados": total}

# | GET | `/animais/detalhes` | Animais adotados (com detalhes) |
@router.get("/detalhes")
async def animais_adotados_com_detalhes():
    animais = await Animal.find(
        Animal.status_adocao == True
    ).to_list()

    return animais

# | PUT | `/{animal_id}` | Atualizar animal |
@router.put("/animais/{animal_id}")
async def atualizar_animal(animal_id: str, dados: dict):
    animal = await Animal.get(animal_id)

    if not animal:
        raise HTTPException(
            status_code=404,
            detail="Animal não encontrado"
        )

    await animal.set(dados)
    return animal

# | DELETE | `/{animal_id}` | Deletar animal |
@router.delete("/animais/{animal_id}")
async def deletar_animal(animal_id: str):
    animal = await Animal.get(animal_id)

    if not animal:
        raise HTTPException(
            status_code=404,
            detail="Animal não encontrado"
        )

    await animal.delete()
    return {"msg": "Animal removido com sucesso"}
