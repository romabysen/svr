from quart import current_app
from sqlalchemy import select
from sqlalchemy.sql.functions import coalesce

from .db_schema import armaments, factions, faction_vehicles, vehicle_classes
from .db_schema import vehicles


async def get_faction(db, faction: str):
    return await db.fetch_one(
            query=select(factions).where(factions.c.id == faction)
        )


async def get_class(db, klass: str):
    return await db.fetch_one(
            query=select(vehicle_classes).where(vehicle_classes.c.id == klass)
        )


async def get_factions(db):
    return await db.fetch_all(
        query=select(factions).order_by(factions.c.name)
    )


async def get_faction_vehicles(db, faction: str):
    return await db.fetch_all(
        query=select(
            vehicles,
            vehicle_classes.c.name.label("class_name"),
            (vehicles.c.ammo_points + coalesce(vehicles.c.construction_points, 0)).label("total_points")  # noqa: E501
        ).select_from(
            vehicles
        ).join(
            vehicle_classes, vehicles.c["class"] == vehicle_classes.c.id
        ).join(
            faction_vehicles, vehicles.c.id == faction_vehicles.c.vehicle
        ).where(faction_vehicles.c.faction == faction).order_by(
            vehicle_classes.c.name, vehicles.c.name
        )
    )


async def get_class_vehicles(db, klass: str):
    return await db.fetch_all(
        query=select(
            vehicles,
            vehicle_classes.c.name.label("class_name"),
            (vehicles.c.ammo_points + coalesce(vehicles.c.construction_points, 0)).label("total_points")  # noqa: E501
        ).select_from(
            vehicles
        ).join(
            vehicle_classes, vehicles.c["class"] == vehicle_classes.c.id
        ).where(vehicle_classes.c.id == klass).order_by(
            vehicle_classes.c.name, vehicles.c.name
        )
    )


async def get_vehicles_classes(db):
    return await db.fetch_all(
        query=select(vehicle_classes).order_by(vehicle_classes.c.name)
    )


async def get_vehicle_details(db, vehicle_id: str):
    vehicle = await db.fetch_one(
        query=select(
            vehicles,
            vehicle_classes.c.name.label("class_name"),
            (vehicles.c.ammo_points + coalesce(vehicles.c.construction_points, 0)).label("total_points")  # noqa :E501
        ).join(
            vehicle_classes, vehicles.c["class"] == vehicle_classes.c.id
        ).where(vehicles.c.id == vehicle_id)
    )
    arms = await db.fetch_all(
        query=select(
            armaments
        ).where(
            armaments.c.vehicle == vehicle_id
        ).order_by(armaments.c.order)
    )
    data = dict(vehicle)
    for item in arms:
        for option in item.ammo.get("options", []):
            option["description"] = current_app.config[
                "AMMO_OPTION_NAMES"
            ].get(option["type"])
    data["armaments"] = [dict(row) for row in arms]
    return data
