from src.db.base import Base
from src.db.database import Session

session = Session()

for table in reversed(Base.metadata.sorted_tables):
    session.execute(table.delete())
session.commit()

session.close()

