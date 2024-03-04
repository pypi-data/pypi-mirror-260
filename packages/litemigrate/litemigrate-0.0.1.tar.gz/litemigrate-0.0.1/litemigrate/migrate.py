import sqlite3
import os
import glob
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("migrate")


def migrate():
    conn = sqlite3.connect("test.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    files = sorted(os.path.basename(p) for p in glob.glob("migrations/*.sql"))
    c.execute(
        """
        --sql
        create table if not exists migrations (
            id integer primary key autoincrement,
            filename text not null,
            run_at datetime not null default current_timestamp
        );
        """
    )
    migrations = c.execute("select * from migrations order by run_at asc").fetchall()
    migrations = {m["filename"] for m in migrations}
    print("Applying migrations:")
    for file in files:
        if file in migrations:
            continue

        print(f"- {file}")

        with open(f"migrations/{file}") as f:
            c.executescript(f.read())

        c.execute(
            "insert into migrations (filename) values (:filename)",
            {"filename": file},
        )
        conn.commit()

    conn.close()


if __name__ == "__main__":
    migrate()
