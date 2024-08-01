from sanic import Blueprint, response
import aiohttp
import logging
from application.database.db import database_connection, fetch_all, fetch_one, execute_query
from sports import get_sport
from application.schemas.schemas import EventBase, EventCreate, EventUpdate

bp = Blueprint('events', url_prefix='/events')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('events.log'),
        logging.StreamHandler()
    ]
)

async def fetch_team_logo(team_name):
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={team_name}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data['teams']:
                        return data['teams'][0]['strLogo']
                logging.error(f"No logo found for team {team_name}")
                return ""
        except Exception as e:
            logging.error(f"Error fetching logo for team {team_name}: {str(e)}")
            return ""

async def get_sport_id_by_name(db, sport_name):
    query = "SELECT id FROM sport WHERE name = ?"
    params = (sport_name,)
    result = await fetch_one(db, query, params)
    if result:
        return result['id']
    return None

@bp.route('/', methods=['GET'])
async def get_all_events(request):
    events = []

    return response.json(events)

@bp.route('/<event_id>', methods=['GET'])
async def get_event_by_id(request, event_id):
    event = None

    if event:
        return response.json(event)
    else:
        return response.json({'error': 'Event not found'}, status=404)

@bp.route('/', methods=['POST'])
async def create_event(request):
    try:
        event_data = EventCreate(**request.json)
    except ValidationError as e:
        return response.json({"error": str(e)}, status=400)
    
    sport_name = event_data.name
    async with database_connection('events.db') as db:
        sport_id = await get_sport_id_by_name(db, sport_name)
        if not sport_id:
            return response.json({'error': 'Sport not found'}, status=404)

        event_name = event_data.name
        if " v " in event_name:
            team1, team2 = event_name.split(" v ")
            logo1 = await fetch_team_logo(team1.strip())
            logo2 = await fetch_team_logo(team2.strip())
            logos = f"{logo1}|{logo2}" if logo1 or logo2 else None
        else:
            logos = None

        query = """
            INSERT INTO event (name, active, slug, type, status, start_time, actual_start_time, sport_id, logos)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            event_data.name,
            event_data.active,
            event_data.slug,
            event_data.type,
            event_data.status,
            event_data.start_time,
            event_data.actual_start_time,
            sport_id,
            logos
        )

        await execute_query(db, query, params)

    
    return response.json(event_data, status=201)


@bp.route('/<event_id>', methods=['PATCH'])
async def update_event(request, event_id):
    event_data = request.json
    # Your code to validate and update the event in the database
    fields = ', '.join([f"{key} = ?" for key in event_data.keys()])
    query = f"UPDATE event SET {fields} WHERE id = ?"
    params = list(event_data.values()) + [event_id]

    async with database_connection('events.db') as db:
        await execute_query(db, query, params)

    async with database_connection('events.db') as db:
        updated_event = await fetch_one(db, "SELECT * FROM event WHERE id = ?", (event_id,))

    return response.json(event_data)

@bp.route('/<event_id>', methods=['DELETE'])
async def delete_event(request, event_id):
    # Your code to delete the event with the given ID from the database
    query = "DELETE FROM event WHERE id = ?"
    params = (event_id,)

    async with database_connection('events.db') as db:
        await execute_query(db, query, params)

    return response.empty(status=204)