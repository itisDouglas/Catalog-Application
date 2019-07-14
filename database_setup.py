import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# this Base is my declarative defintion
Base = declarative_base()

class Category(Base):
    __tablename__="category"
    # defining Category table columns
    # this is my id column
    id = Column(Integer, primary_key=True)
    category_name = Column(String(50))
    # this is my category name column
    # holds up to 100 characters and MUST have a value
    # can't be null
    categories = relationship("Item", back_populates="category")

    @property
    def serialize(self):
        return
        {
            'category_name': self.category_name,
            'id': self.id,
        }

class Item(Base):
    __tablename__="item"
    id = Column(Integer, primary_key=True)
    item_name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="categories")

    @property
    def serialize(self):
        return{
            'item_name': self.item_name,
            'description': self.description,
            'id': self.id,
        }

#creating local permission for user here
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    sub = Column(String(500), nullable=False)


""" Instantiate create_engine object. Pass as argument the file name"""

engine = create_engine('sqlite:///database_tables.db')

# finally, create all tables in this engine
Base.metadata.create_all(engine)

"""Observation: the declarative base instantiated into Base gets passed as an argument into every class. In the final code Base.metadata.create_all(engine) this Base.metadata seems to hold these classes in order to create the tables. it's a declarative"""