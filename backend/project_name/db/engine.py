from sqlalchemy.engine import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from project_name.configs import POSTGRES_DB
from project_name.configs import POSTGRES_HOST
from project_name.configs import POSTGRES_PASSWORD
from project_name.configs import POSTGRES_PORT
from project_name.configs import POSTGRES_USER

_ENGINE: Engine | None = None


def build_connection_string(
    user: str = POSTGRES_USER,
    password: str = POSTGRES_PASSWORD,
    host: str = POSTGRES_HOST,
    port: str = POSTGRES_PORT,
    db: str = POSTGRES_DB,
) -> str:
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


def get_sqlalchemy_engine() -> Engine:
    global _ENGINE
    if _ENGINE is None:
        connection_string = build_connection_string()
        _ENGINE = create_engine(connection_string, pool_size=50, max_overflow=25)
    return _ENGINE


SessionFactory = sessionmaker(bind=get_sqlalchemy_engine())
