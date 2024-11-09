from quart import Quart, render_template
from quart_db import QuartDB

from . import database, jinjafilters

app = Quart(__name__)
app.config.from_object("svr.defaults")
app.config.from_prefixed_env(prefix="APP")
app.add_template_filter(jinjafilters.plural, "plural")

db = QuartDB(app)


@app.route('/')
async def show_index():
    factions = await database.get_factions()
    vehicle_classes = await database.get_vehicles_classes()

    return await render_template(
        'index.html.j2',
        factions=factions,
        vehicle_classes=vehicle_classes
    )


@app.route('/factions/<faction>')
async def show_faction(faction):
    current_faction = await database.get_faction(faction)
    if not current_faction:
        return "Faction not found", 404

    factions = await database.get_factions()
    vehicle_classes = await database.get_vehicles_classes()
    vehicles = await database.get_faction_vehicles(faction)

    return await render_template(
        'vehicles.html.j2',
        factions=factions,
        vehicle_classes=vehicle_classes,
        vehicles=vehicles,
        current_faction=current_faction
    )


@app.route('/vehicleclasses/<klass>')
async def show_vehicle_class(klass):
    current_class = await database.get_class(klass)
    if not current_class:
        return "Vehicle class not found", 404

    factions = await database.get_factions()
    vehicle_classes = await database.get_vehicles_classes()
    vehicles = await database.get_class_vehicles(klass)

    return await render_template(
        'vehicles.html.j2',
        factions=factions,
        vehicle_classes=vehicle_classes,
        vehicles=vehicles,
        current_class=current_class
    )


@app.route('/status')
async def status():
    database.status_query()
    return {"status": "ok"}
