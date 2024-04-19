import motor.motor_asyncio
from backend.config import settings


client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DB_KEY)
database = client.raifbot  # Replace with your database name
