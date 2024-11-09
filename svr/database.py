async def get_faction(db, faction: str):
    return await db.fetch_one(
            query="SELECT * FROM factions WHERE id = :id",
            values={"id": faction}
        )


async def get_class(db, klass: str):
    return await db.fetch_one(
            query="SELECT * FROM vehicle_classes WHERE id = :id",
            values={"id": klass}
        )


async def get_factions(db):
    return await db.fetch_all(
        "SELECT * FROM factions ORDER BY name"
    )


async def get_faction_vehicles(db, faction: str):
    return await db.fetch_all(
        query="""SELECT
vehicles.*, vc.name AS class_name,
vehicles.ammo_points + COALESCE(vehicles.construction_points, 0) AS total_points
FROM vehicles
JOIN faction_vehicles ON vehicles.id = faction_vehicles.vehicle
JOIN vehicle_classes AS vc ON vehicles.class = vc.id
WHERE faction_vehicles.faction = :faction ORDER BY class""",  # noqa: E501
        values={"faction": faction}
    )


async def get_class_vehicles(db, klass: str):
    return await db.fetch_all(
        query="""SELECT
vehicles.*, vc.name AS class_name,
vehicles.ammo_points + COALESCE(vehicles.construction_points, 0) AS total_points
FROM vehicles
JOIN vehicle_classes AS vc ON vehicles.class = vc.id
WHERE vehicles.class = :klass ORDER BY vehicles.name""",  # noqa: E501
        values={"klass": klass}
    )


async def get_vehicles_classes(db):
    return await db.fetch_all(
        """SELECT * FROM vehicle_classes ORDER BY name"""
    )


async def status_query(db):
    return await db.fetch_one(
        """SELECT COUNT(*) FROM factions"""
    )
