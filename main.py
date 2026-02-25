from app.db import init_db
from app.ui.interface import run_app

if __name__ == "__main__":
    init_db()
    run_app()