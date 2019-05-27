#!/usr/bin/env python3
import os
from flask import Flask, render_template
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item


engine = create_engine('sqlite:///database_tables.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/categories/')
def categoryMenu():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('main.html',categories=categories, items=items)

@app.route('/categories/<int:item_id>/item')
def categoryItem(item_id):
    return 'This page displays a list of specific items that are in that category %d' %item_id

@app.route('/categories/<int:item_id>/item/description')
def categoryItemDescribe(item_id):
    return 'This page will display the item plus a description that can be located by accessing the item.description field %d' %item_id

@app.route('/categories/<int:item_id>/item/new')
def categoryItemNew(item_id):
    return 'This page will allow an authorized user to add a new item within a category. %d' %item_id

@app.route('/categories/<int:item_id>/item/edit')
def categoryItemEdit(item_id):
    return 'This page will allow an authorized user to add a new item within a category. %d' %item_id

@app.route('/categories/<int:item_id>/item/delete')
def categoryItemDel(item_id):
    return 'This page will allow an authorized user to delete an item within a category. %d' %item_id


if __name__== '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)