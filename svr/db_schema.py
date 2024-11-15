from sqlalchemy import MetaData, Table, Column, ForeignKey, text
from sqlalchemy import BOOLEAN, INTEGER, JSON, VARCHAR

metadata = MetaData()

factions = Table(
    "factions",
    metadata,
    Column("id", VARCHAR, primary_key=True),
    Column("name", VARCHAR, nullable=False),
)

vehicle_classes = Table(
    "vehicle_classes",
    metadata,
    Column("id", VARCHAR, primary_key=True),
    Column("name", VARCHAR, nullable=False)
)

vehicles = Table(
    "vehicles",
    metadata,
    Column("id", VARCHAR, primary_key=True),
    Column("name", VARCHAR, nullable=False),
    Column(
        "class",
        VARCHAR,
        ForeignKey(
            "vehicle_classes.id", onupdate="CASCADE", ondelete="RESTRICT"
        ),
        nullable=False
    ),
    Column("crew", INTEGER, nullable=False),
    Column("passengers", INTEGER, nullable=False),
    Column("ticket_cost", INTEGER, nullable=False),
    Column("ammo_points", INTEGER, nullable=False),
    Column(
        "construction_points", INTEGER, nullable=True
    ),
    Column(
        "amphibious",
        BOOLEAN,
        nullable=False,
        server_default=text("FALSE")
    )
)


faction_vehicles = Table(
    "faction_vehicles",
    metadata,
    Column(
        "faction",
        VARCHAR,
        ForeignKey(
            "factions.id", onupdate="CASCADE", ondelete="RESTRICT"
        ),
        primary_key=True
    ),
    Column(
        "vehicle",
        VARCHAR,
        ForeignKey(
            "vehicles.id", onupdate="CASCADE", ondelete="RESTRICT"
        ),
        primary_key=True
    ),
)

armaments = Table(
    "armaments",
    metadata,
    Column("name", VARCHAR, primary_key=True),
    Column(
        "vehicle",
        VARCHAR,
        ForeignKey(
            "vehicles.id", onupdate="CASCADE", ondelete="RESTRICT"
        ),
        primary_key=True
    ),
    Column("model", VARCHAR, nullable=False),
    Column("caliber", VARCHAR, nullable=False),
    Column("ammo", JSON, nullable=False),
    Column("order", INTEGER, nullable=True)
)
