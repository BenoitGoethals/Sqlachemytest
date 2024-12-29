import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from alembic.config import Config
from alembic import command
from asyncrepository import AsyncRepository

from model import User  # Import the User model
from base import Base  # Base for models

DATABASE_URL = "sqlite+aiosqlite:///./database.db"

# Initialize async database engine
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create async session factory
SessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)


# Run Alembic migrations programmatically
async def run_migrations():
    """
    Runs Alembic migrations using the alembic.ini configuration file.
    """
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


async def crud_demo():
    """
    Demonstrates CRUD operations using the AsyncRepository class.
    """
    # Run migrations
    await run_migrations()

    # Use an async database session
    async with SessionLocal() as session:
        user_repo = AsyncRepository(session, User)

        # CRUD operations
        try:
            print("Creating Users...")
            user1 = await user_repo.create(username='user1', password='secure_password1', email='user1@example.com')
            user2 = await user_repo.create(username='user2', password='secure_password2', email='user2@example.com')
            print(f"Created Users: {user1}, {user2}")

            print("Reading All Users...")
            users = await user_repo.read_all()
            print(users)

            print("Updating User 1...")
            updated_user = await user_repo.update(1, first_name="Updated User One")
            print(updated_user)

            print("Deleting User 2...")
            await user_repo.delete(2)

        except Exception as e:
            print(f"Error: {e}")


asyncio.run(crud_demo())
