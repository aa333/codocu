from peewee import Model, SqliteDatabase

db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


def init_db(path: str) -> None:
    db.init(path, pragmas={"journal_mode": "wal", "foreign_keys": 1})
    db.connect()
