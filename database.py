from dotenv import load_dotenv #env
from pymongo import AsyncMongoClient
from beanie import init_beanie
import os
import logging
from modelos import Atendente, Animal, Adocao, Adotante

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
DBNAME = os.getenv("DBNAME")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

_client: AsyncMongoClient | None = None #unica conexao para toda aplicação


async def init_db(): #inicializar fastapi
    global _client
    _client = AsyncMongoClient(DATABASE_URL)
    logger.info(f"Using DATABASE_URL: {DATABASE_URL}")
    db = _client[DBNAME]

    #inicializar beanie com os modelos -> registra coleções, habilita uso do ODM
    await init_beanie(database=db,document_models=[Atendente, Animal, Adocao, Adotante],)

async def close_db(): #fechar conexão
    global _client
    if _client is not None:
        _client.close()
        logger.info(f"Closed DATABASE_URL: {DATABASE_URL}")
        _client = None