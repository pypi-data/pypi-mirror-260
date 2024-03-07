import os.path
import sqlite3


DB_PATH = db_path = os.path.join(os.path.dirname(__file__), "cakes.db")


def get_cake_amount() -> int:
    con = sqlite3.connect(str(DB_PATH))
    return int(con.execute("SELECT COUNT(*) FROM cakes").fetchone()[0])


def get_cake(index: int) -> str:
    con = sqlite3.connect(str(DB_PATH))

    return con.execute("SELECT name FROM cakes WHERE id = ?", (index,)).fetchone()[0]


__all__ = ["get_cake", "get_cake_amount"]
