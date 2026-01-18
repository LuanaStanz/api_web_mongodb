from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from beanie.odm.fields import Link
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from datetime import date
from modelos import Adocao

router = APIRouter(prefix="/adocao", tags=["Adocao"])

#POST /adocoes/ - Criar adoção
@router.post("/")
async def criar_adocao(adocao: Adocao):
    await adocao.insert()
    return adocao

#GET /adocoes/canceladas - Adoções canceladas
@router.get("/canceladas")
async def adocoes_canceladas():
    return await Adocao.find(Adocao.cancelamento == True).to_list()


#GET /adocoes/recentes - Adoções mais recentes
@router.get("/recentes", response_model=Page[Adocao])
async def adocoes_recentes() -> Page[Adocao]:
    return await apaginate(Adocao.find_all().sort("-data_adocao").to_list())

#DELETE /adocoes/{adocao_id}/cancelar- Cancelar adoção (soft delete)
@router.delete("/{adocao_id}/cancelar")
async def cancelar_adocao(adocao_id: str):
    adocao = await Adocao.get(adocao_id)
    adocao.cancelamento = True
    await adocao.save()
    return {"msg": "Adoção cancelada"}

#DELETE /adocoes/{adocao_id}/hard - Deletar adoção (hard delete)
@router.delete("/{adocao_id}/hard")
async def hard_delete(adocao_id: str):
    adocao = await Adocao.get(adocao_id)
    await adocao.delete()

# | GET | `/adocoes/` | Listar adoções |
@router.get("/")
async def listar_adocoes():
    adocoes = await Adocao.find_all().to_list()
    return adocoes

# | GET | `/adocoes/relatorio/completo/ordenados` | Relatório completo de adoções |
@router.get("/relatorio/completo/ordenados")
async def relatorio_completo_adocoes():
    adocoes = await Adocao.find_all(fetch_links=True).sort("-data_adocao").to_list()

    return adocoes

# | PUT | `/adocoes/{adocao_id}` | Atualizar adoção |
@router.put("/{adocao_id}")
async def atualizar_adocao(adocao_id: str, dados: dict):
    adocao = await Adocao.get(adocao_id)

    if not adocao:
        raise HTTPException(
            status_code=404,
            detail="Adoção não encontrada"
        )

    await adocao.set(dados)
    return adocao

# | GET | `/adocoes/ano/{ano}` | Adoções por ano |
@router.get("/ano/{ano}")
async def adocoes_por_ano(ano: int):
    inicio = date(ano, 1, 1)
    fim = date(ano, 12, 31)

    adocoes = await Adocao.find(
        Adocao.data_adocao >= inicio,
        Adocao.data_adocao <= fim
    ).to_list()

    return adocoes

# | GET | `/adocoes/id/{adocao_id}` | Buscar adoção por ID |
@router.get("/id/{adocao_id}")
async def buscar_adocao_por_id(adocao_id: str):
    adocao = await Adocao.get(adocao_id, fetch_links=True)

    if not adocao:
        raise HTTPException(
            status_code=404,
            detail="Adoção não encontrada"
        )

    return adocao
