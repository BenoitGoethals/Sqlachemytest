from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base
from model import User

engine = create_engine('sqlite:///database.db', echo=True)


Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

users = [User(username=f'user{i}', password=f'password{i}', email=f'user{i}@example.com',
              first_name=f'FirstName{i}', last_name=f'LastName{i}', bio=f'Bio of user{i}',
              avatar_url=f'http://avatar{i}.example.com')
         for i in range(1, 101)]

session.add_all(users)

session.commit()

result = session.query(User).all()
for row in result:
    print(row.username)

session.close()
engine.dispose()