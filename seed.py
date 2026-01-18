import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from datetime import datetime

from modelos import Animal, Adotante, Atendente, Adocao


async def seed():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["adocao_animais"]

    await init_beanie(
        database=db,
        document_models=[Animal, Adotante, Atendente, Adocao]
    )

    # Limpa coleções
    await Animal.delete_all()
    await Adotante.delete_all()
    await Atendente.delete_all()
    await Adocao.delete_all()

    atendentes = []
    for i in range(10):
        atendente = Atendente(
            nome=f"Atendente {i+1}",
            email=f"atendente{i+1}@ong.org",
            telefone="(88) 99999-0000"
        )
        await atendente.insert()
        atendentes.append(atendente)

    adotantes = []
    for i in range(10):
        adotante = Adotante(
            nome=f"Adotante {i+1}",
            email=f"adotante{i+1}@email.com",
            telefone="(88) 98888-0000",
            cidade="Quixadá"
        )
        await adotante.insert()
        adotantes.append(adotante)

    animais = []
    for i in range(12):
        animal = Animal(
            nome=f"Animal {i+1}",
            especie="Cachorro" if i % 2 == 0 else "Gato",
            raca="Vira-lata",
            idade=1 + i % 8,
            disponivel=True
        )
        await animal.insert()
        animais.append(animal)

    for i in range(10):
        adocao = Adocao(
            animal=animais[i],
            adotante=adotantes[i],
            atendente=atendentes[i],
            data=datetime(2024, 5, 10),
            status="Concluída"
        )
        await adocao.insert()

    print("✅ Banco populado com sucesso!")

if __name__ == "__main__":
    asyncio.run(seed())
