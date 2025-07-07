import app.database as database

import sqlalchemy as sa


class Note(database.Base):
    __tablename__ = "notes"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String)
    body = sa.Column(sa.String)
    private = sa.Column(sa.Boolean, default=False)
