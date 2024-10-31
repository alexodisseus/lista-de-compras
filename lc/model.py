import sys
import inspect

from typing import Optional, List
from sqlmodel import SQLModel ,or_, Field, create_engine, Session, select, Relationship
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLModel()

def configure(app):
    app.db = db



class Person(SQLModel, table=True):
    """Modelo para a tabela de pessoas ."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    password: str  # Considere usar hashing para segurança
    types: str  # Tipo do usuário: master ou comum
    todos: List['Todo'] = Relationship(back_populates='person')


class User(SQLModel, table=True):
    """Modelo para a tabela de usuários"""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str  
    password: str  
    email: str  
    user_type: str  
    active: bool = Field(default=False)  

class Todo(SQLModel, table=True):
    """Modelo para a tabela de tarefas do sistema."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    observation: str
    nature: str
    value: str
    date: str  # Considere usar um tipo de dado de data
    status: str
    person_id: int = Field(foreign_key='person.id')
    person: Optional[Person] = Relationship(back_populates='todos')



engine = create_engine('sqlite:///db.db')

SQLModel.metadata.create_all(engine)



"""
current_module = sys.modules[__name__]

def list_models():
    models = []
    for name, obj in inspect.getmembers(current_module, inspect.isclass):
        if issubclass(obj, SQLModel) and obj is not SQLModel:
            models.append(name)
    return models
"""


#funcao person
def create_person(name: str, password: str, types: str):
    with Session(engine) as session:
        person = Person(name=name, password=password, types=types)
        session.add(person)
        session.commit()


def list_person(filters: str = None, offset: int = 0, per_page: int = 10):
    with Session(engine) as session:
        query = select(Person)
        if filters:
            query = query.where(Person.name.contains(filters))
        query = query.offset(offset).limit(per_page)
        return session.exec(query).all()




def update_person(id: int, name: str, password: str, types: str):
    with Session(engine) as session:
        person = session.get(Person, id)
        if person:
            person.name = name
            person.password = password
            person.types = types
            session.commit()

def delete_person(id: int):
    with Session(engine) as session:
        person = session.get(Person, id)
        if person:
            session.delete(person)
            session.commit()

def get_person(id:int):
	with Session(engine) as session:
		person = session.get(Person, id)
		return person








#funçao user


def get_user(id:int):
	with Session(engine) as session:
		user = session.get(User, id)
		return user

# Supondo que você tenha uma função para criar um usuário
def create_user(username: str, password: str, email: str) -> bool:
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password, email=email,user_type="admin", active=False)
    
    with Session(engine) as session:
        session.add(user)
        session.commit()
    return True


def read_user(email: str) -> Optional[User]:
    with Session(engine) as session:
        user = session.query(User).filter(User.email == email).first()
    return user
