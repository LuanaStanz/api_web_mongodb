
from beanie import Document, Link
from beanie.odm.fields import PydanticObjectId
from pydantic import Field, BaseModel
from datetime import date
#AniAdocaoAtendAdot para request/response body?

class Atendente(Document):
    nome: str 
    adocoes: list[Link["Adocao"]] = Field(default_factory=list)

    class Settings:
        name = "atendentes"

class Animal(Document):
    nome: str
    especie: str
    idade: int
    data_resgate: date
    status_adocao: bool = False
    
    adocoes: list[Link["Adocao"]] = Field(default_factory=list)

    class Settings:
        name = "animais"

class Adotante(Document):
    nome: str
    contato: str
    endereco: str
    preferencias: str
    
    adocoes: list[Link["Adocao"]] = Field(default_factory=list)
    
    class Settings:
        name = "adotantes"

class Adocao(Document):
    data_adocao: date
    descricao: str
    cancelamento: bool = False

    animal: Link["Animal"]
    adotante: Link["Adotante"]
    atendentes: list[Link["Atendente"]] = Field(default_factory=list)

    class Settings:
        name = "adocoes"

#relacionamento muitos-para-muitos é representado diretamente por: 
# atendentes: list[Link[Atendente]]
#dentro do documento Adoção.