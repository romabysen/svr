import sqlalchemy

metadata = sqlalchemy.MetaData()

factions = sqlalchemy.Table(
    "factions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.VARCHAR, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.VARCHAR, nullable=False),
)

vehicle_classes = sqlalchemy.Table(
    "vehicle_classes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.VARCHAR, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.VARCHAR, nullable=False),
    sqlalchemy.Column("abbreviation", sqlalchemy.VARCHAR, nullable=True),
)

vehicles = sqlalchemy.Table(
    "vehicles",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.VARCHAR, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.VARCHAR, nullable=False),
    sqlalchemy.Column(
        "class",
        sqlalchemy.VARCHAR,
        sqlalchemy.ForeignKey(
            "vehicle_classes.id", onupdate="CASCADE", ondelete="CASCADE"
        ),
        nullable=False
    ),
    sqlalchemy.Column("crew", sqlalchemy.INT, nullable=False),
    sqlalchemy.Column("passengers", sqlalchemy.INT, nullable=False),
    sqlalchemy.Column("ticket_cost", sqlalchemy.INT, nullable=False),
    sqlalchemy.Column("ammo_points", sqlalchemy.INT, nullable=False),
    sqlalchemy.Column("construction_points", sqlalchemy.INT, nullable=True),
)


faction_vehicles = sqlalchemy.Table(
    "faction_vehicles",
    metadata,
    sqlalchemy.Column(
        "faction",
        sqlalchemy.VARCHAR,
        sqlalchemy.ForeignKey(
            "factions.id", onupdate="CASCADE", ondelete="CASCADE"
        ),
        primary_key=True
    ),
    sqlalchemy.Column(
        "vehicle",
        sqlalchemy.VARCHAR,
        sqlalchemy.ForeignKey(
            "vehicles.id", onupdate="CASCADE", ondelete="CASCADE"
        ),
        primary_key=True
    ),
)

armaments = sqlalchemy.Table(
    "armaments",
    metadata,
    sqlalchemy.Column("name", sqlalchemy.VARCHAR, primary_key=True),
    sqlalchemy.Column(
        "vehicle",
        sqlalchemy.VARCHAR,
        sqlalchemy.ForeignKey(
            "vehicles.id", onupdate="CASCADE", ondelete="CASCADE"
        ),
        primary_key=True
    ),
    sqlalchemy.Column("model", sqlalchemy.VARCHAR, nullable=False),
    sqlalchemy.Column("caliber", sqlalchemy.VARCHAR, nullable=False),
    sqlalchemy.Column("ammo", sqlalchemy.JSON, nullable=False),
    sqlalchemy.Column("order", sqlalchemy.INT, nullable=True)
)
