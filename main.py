import asyncio
import logging
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from alembic.config import Config
from alembic import command
from asyncrepository import AsyncRepository
from model import User, Domain
from base import Base


DATABASE_URL = "sqlite+aiosqlite:///./database.db"

# Initialize database
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



async def crud_demo():
    """
    Demonstrates CRUD operations using the AsyncRepository class for User and Domain models.
    """

    async with SessionLocal() as session:
        user_repo = AsyncRepository(session, User)
        domain_repo = AsyncRepository(session, Domain)

        try:
            # Domain Creation
            logger.info("Creating Domains...")
            domain1 = await domain_repo.create(name='domain1', description='Description of domain 1')
            domain2 = await domain_repo.create(name='domain2', description='Description of domain 2')
            logger.info(f"Created Domains: {domain1}, {domain2}")

            # User Creation (Adding Users to Domains)
            logger.info("Creating Users and associating them with Domains...")
            user1 = await user_repo.create(
                username='user1',
                password='secure_password1',
                email='user1@example.comg',
                domain_id=domain1.id
            )
            user2 = await user_repo.create(
                username='user2',
                password='secure_password2',
                email='user2@example.com',
                domain_id=domain1.id  # Associate with the same domain as user1
            )
            user3 = await user_repo.create(
                username='user3',
                password='secure_password3',
                email='user3@example.com',
                domain_id=domain2.id  # Associate with a different domain
            )
            logger.info(f"Created Users: {user1}, {user2}, {user3}")

            # Reading All Domains and their Users
            logger.info("Reading All Domains and their Users...")
            domains = await domain_repo.read_all()
            for domain in domains:
                logger.info(f"Domain: {domain.name}, Description: {domain.description}")
                logger.info(f"Users in Domain '{domain.name}': {domain.users}")

            # Update User
            logger.info("Updating User 1...")
            updated_user = await user_repo.update(user1.id, first_name="Updated User One")
            logger.info(f"Updated User: {updated_user}")

            # Update Domain
            logger.info("Updating Domain 1...")
            updated_domain = await domain_repo.update(domain1.id, name="Updated Domain One")
            logger.info(f"Updated Domain: {updated_domain}")

            # Deleting a User
            logger.info("Deleting User 3...")
            await user_repo.delete(user3.id)

            # Deleting a Domain (Cascade delete for associated users)
            logger.info("Deleting Domain 2...")
            await domain_repo.delete(domain2.id)
            logger.info("Deleting Domain 2 deletes all associated users due to cascade rules.")

        except Exception as e:
            logger.error(f"Error: {e}")
            await session.rollback()


asyncio.run(crud_demo())
