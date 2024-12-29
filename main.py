import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.exc import IntegrityError

from asyncrepository import AsyncRepository
from model import User  # Import the User model
from base import Base  # Import Base to initialize the database schema


# Define the database URL
DATABASE_URL = "sqlite+aiosqlite:///./database.db"  # Example using SQLite for simplicity

# Create async database engine
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create async session factory
SessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


# Create database tables
async def init_db():
    """
    Initializes the database by creating the required tables.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def crud_demo():
    """
    Demonstrates CRUD operations using the AsyncRepository class.
    """
    # Initialize the database
    await init_db()

    # Start using an async session
    async with SessionLocal() as session:
        # Create an instance of the repository for `User`
        user_repo = AsyncRepository(session, User)

        # **CREATE**: Add new users
        print("Creating users...")
        try:
            user1 = await user_repo.create(
                username="user1",
                password="secure_password1",
                email="user1@example.com",
                first_name="User",
                last_name="One",
                bio="This is User One.",
                avatar_url="http://example.com/avatar1.png"
            )
            user2 = await user_repo.create(
                username="user2",
                password="secure_password2",
                email="user2@example.com",
                first_name="User",
                last_name="Two",
                bio="This is User Two.",
                avatar_url="http://example.com/avatar2.png"
            )
            print(f"Created User 1: {user1}")
            print(f"Created User 2: {user2}")
        except IntegrityError:
            print("Failed to create some users, possibly due to duplicate entries.")

        # **READ ALL**: Fetch all users
        print("\nFetching all users...")
        users = await user_repo.read_all()
        print("All users:")
        for user in users:
            print(user)

        # **READ BY ID**: Fetch a single user by ID
        print("\nFetching user with ID 1...")
        single_user = await user_repo.read_by_id(1)
        if single_user:
            print(f"User with ID 1: {single_user}")
        else:
            print("User with ID 1 not found.")

        # **UPDATE**: Update a user's information
        print("\nUpdating user with ID 1...")
        try:
            updated_user = await user_repo.update(
                1,  # ID of the user to update
                first_name="Updated",
                last_name="User",
                bio="Updated bio for User One."
            )
            print(f"Updated User: {updated_user}")
        except ValueError as e:
            print(f"Update failed: {e}")

        # **DELETE**: Delete a user by ID
        print("\nDeleting user with ID 2...")
        try:
            if await user_repo.delete(2):
                print("User with ID 2 deleted successfully.")
        except ValueError as e:
            print(f"Deletion failed: {e}")


# Run the CRUD demo
asyncio.run(crud_demo())
