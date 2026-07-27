from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models so Alembic can discover them.
#from src.models.reference import *  # noqa: F401,F403,E402
#from src.models.compliance import *  # noqa: F401,F403,E402