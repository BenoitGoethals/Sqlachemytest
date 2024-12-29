from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError


class AsyncRepository:
    def __init__(self, session: AsyncSession, model):
        """
        Initializes the repository with an async database session and a specific model.

        :param session: Async SQLAlchemy session object.
        :param model: SQLAlchemy model class.
        """
        self.session = session
        self.model = model

    async def create(self, **kwargs):
        """
        Asynchronously creates a new record in the database.

        :param kwargs: Dictionary of attributes and their values for the model.
        :return: The created model instance.
        """
        new_instance = self.model(**kwargs)
        self.session.add(new_instance)
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        return new_instance

    async def read_all(self):
        """
        Asynchronously retrieves all records of the model from the database.

        :return: List of model instances.
        """
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def read_by_id(self, id):
        """
        Asynchronously retrieves a single record by its primary key ID.

        :param id: Primary key of the record to retrieve.
        :return: Model instance if found, otherwise None.
        """
        return await self.session.get(self.model, id)

    async def update(self, id, **kwargs):
        """
        Asynchronously updates a record with the given attributes.

        :param id: Primary key of the record to update.
        :param kwargs: Dictionary of attributes to update.
        :return: The updated model instance if successful, otherwise raises an error.
        """
        instance = await self.read_by_id(id)
        if not instance:
            raise ValueError(f"Record with id {id} not found")

        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise e

        return instance

    async def delete(self, id):
        """
        Asynchronously deletes a record by its primary key ID.

        :param id: Primary key of the record to delete.
        :return: True if deletion was successful, otherwise raises an error.
        """
        instance = await self.read_by_id(id)
        if not instance:
            raise ValueError(f"Record with id {id} not found")

        await self.session.delete(instance)
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise e

        return True
