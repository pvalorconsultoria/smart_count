from src.db.db import DB
from src.db.migrations import batches

if __name__ == '__main__':
    db = DB('sqlite:///smart_count.db')

    batches.run_migrations(db)