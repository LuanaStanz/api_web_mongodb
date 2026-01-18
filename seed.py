import asyncio
import os
from datetime import date

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv

from modelos import Animal, Adotante, Atendente, Adocao

load_dotenv()


async def seed():
    mongodb_uri = os.getenv("DATABASE_URL")

    if not mongodb_uri:
        raise RuntimeError("DATABASE_URL não encontrada no .env")

    client = AsyncIOMotorClient(mongodb_uri)
    db = client.get_default_database()

    await init_beanie(
        database=db,
        document_models=[Animal, Adotante, Atendente, Adocao]
    )

    # Limpa coleções
    await Animal.delete_all()
    await Adotante.delete_all()
    await Atendente.delete_all()
    await Adocao.delete_all()

    # -------------------------
    # Atendentes
    # -------------------------
    atendentes = []
    for i in range(5):
        atendente = Atendente(
            nome=f"Atendente {i + 1}"
        )
        await atendente.insert()
        atendentes.append(atendente)

    # -------------------------
    # Adotantes
    # -------------------------
    adotantes = []
    for i in range(5):
        adotante = Adotante(
            nome=f"Adotante {i + 1}",
            contato="(88) 98888-0000",
            endereco="Quixadá - CE",
            preferencias="Cães de pequeno porte"
        )
        await adotante.insert()
        adotantes.append(adotante)

    # -------------------------
    # Animais
    # -------------------------
    animais = []
    for i in range(6):
        animal = Animal(
            nome=f"Animal {i + 1}",
            especie="Cachorro" if i % 2 == 0 else "Gato",
            idade=2 + i,
            data_resgate=date(2024, 1, 10),
            status_adocao=False
        )
        await animal.insert()
        animais.append(animal)

    # -------------------------
    # Adoções
    # -------------------------
    for i in range(5):
        adocao = Adocao(
            data_adocao=date(2024, 5, 10),
            descricao="Adoção realizada com acompanhamento da ONG",
            animal=animais[i],
            adotante=adotantes[i],
            atendentes=[atendentes[i]]
        )

        await adocao.insert()

        # Atualiza vínculos inversos
        animais[i].adocoes.append(adocao)
        adotantes[i].adocoes.append(adocao)
        atendentes[i].adocoes.append(adocao)

        animais[i].status_adocao = True

        await animais[i].save()
        await adotantes[i].save()
        await atendentes[i].save()

    print("✅ Banco MongoDB Atlas populado com sucesso!")


if __name__ == "__main__":
    asyncio.run(seed())
