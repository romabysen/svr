from quart import g


async def get_faction(faction: str):
    return await g.connection.fetch_one(
            "SELECT * FROM factions WHERE id = :id", {"id": faction}
        )


async def get_class(klass: str):
    return await g.connection.fetch_one(
            "SELECT * FROM vehicle_classes WHERE id = :id", {"id": klass}
        )


async def get_factions():
    return await g.connection.fetch_all(
        "SELECT * FROM factions ORDER BY name"
    )


async def get_faction_vehicles(faction: str):
    return await g.connection.fetch_all(
        """SELECT
vehicles.*, vc.name AS class_name,
vehicles.ammo_points + COALESCE(vehicles.construction_points, 0) AS total_points
FROM vehicles
JOIN faction_vehicles ON vehicles.id = faction_vehicles.vehicle
JOIN vehicle_classes AS vc ON vehicles.class = vc.id
WHERE faction_vehicles.faction = :faction ORDER BY class""",  # noqa: E501
        {"faction": faction}
    )


async def get_class_vehicles(klass: str):
    return await g.connection.fetch_all(
        """SELECT
vehicles.*, vc.name AS class_name,
vehicles.ammo_points + COALESCE(vehicles.construction_points, 0) AS total_points
FROM vehicles
JOIN vehicle_classes AS vc ON vehicles.class = vc.id
WHERE vehicles.class = :klass ORDER BY vehicles.name""",  # noqa: E501
        {"klass": klass}
    )


async def get_vehicles_classes():
    return await g.connection.fetch_all(
        """SELECT * FROM vehicle_classes ORDER BY name"""
    )


async def status_query():
    return await g.connection.fetch_one(
        """SELECT COUNT(*) FROM factions"""
    )
