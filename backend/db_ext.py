from flask_sqlalchemy import SQLAlchemy


class NoLegacyQuerySQLAlchemy(SQLAlchemy):
    pass


db = NoLegacyQuerySQLAlchemy()

