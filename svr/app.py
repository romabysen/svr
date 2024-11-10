from quart import Quart, render_template, url_for
from databases import Database

from . import cli, jinjafilters, queries

app = Quart(__name__)
app = cli.init_app(app)
app.config.from_object("svr.defaults")
app.config.from_prefixed_env(prefix="APP")
app.add_template_filter(jinjafilters.plural, "plural")


@app.route('/')
async def show_index():
    async with Database(app.config["DB_URL"]) as db:
        factions = await queries.get_factions(db)
        vehicle_classes = await queries.get_vehicles_classes(db)

    return await render_template(
        'index.html.j2',
        factions=factions,
        vehicle_classes=vehicle_classes
    )


@app.route('/factions/<faction>')
async def show_faction(faction):
    async with Database(app.config["DB_URL"]) as db:
        current_faction = await queries.get_faction(db, faction)
        if not current_faction:
            return "Faction not found", 404

        factions = await queries.get_factions(db)
        vehicle_classes = await queries.get_vehicles_classes(db)
        vehicles = await queries.get_faction_vehicles(db, faction)

    return await render_template(
        'vehicles.html.j2',
        factions=factions,
        vehicle_classes=vehicle_classes,
        vehicles=vehicles,
        current_faction=current_faction
    )


@app.route('/vehicleclasses/<klass>')
async def show_vehicle_class(klass):
    async with Database(app.config["DB_URL"]) as db:
        current_class = await queries.get_class(db, klass)
        if not current_class:
            return "Vehicle class not found", 404

        factions = await queries.get_factions(db)
        vehicle_classes = await queries.get_vehicles_classes(db)
        vehicles = await queries.get_class_vehicles(db, klass)

    return await render_template(
        'vehicles.html.j2',
        factions=factions,
        vehicle_classes=vehicle_classes,
        vehicles=vehicles,
        current_class=current_class
    )


@app.route('/api/vehicles/<klass>')
async def api_get_vehicle_details(klass):
    async with Database(app.config["DB_URL"]) as db:
        vehicle = await queries.get_vehicle_details(db, klass)
        if not vehicle:
            return "Vehicle not found", 404
        vehicle['image'] = url_for(
            "static", filename=f"img/vehicles/{vehicle['id']}.png"
        )
    return dict(vehicle)


@app.route('/status')
async def status():
    return {"status": "ok"}
