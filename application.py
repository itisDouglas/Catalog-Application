#!/usr/bin/env python3
import os
from flask import Flask, render_template, url_for, jsonify, redirect, request
from flask import session as login_session
import random, string
import hashlib
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

#oauth imports
# from google.auth import credentials
# from google_auth_oauthlib.flow import Flow
# from google.auth.transport.requests import AuthorizedSession
import google.auth.credentials
import google_auth_oauthlib.flow
import google.auth.transport.requests
import json
from flask import make_response
import requests
import httplib2

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = 'https://www.googleapis.com/auth/userinfo.email'

engine = create_engine('sqlite:///database_tables.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#add JSON endpoints

#creating a state token
@app.route('/login')
def showLogin():
    #my CSRF token
    state=hashlib.sha256(os.urandom(1024)).hexdigest()
    #login_session holds my string value called "state"
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    #RECEIVE auth_code BY HTTPS POST
    #auth_code must be double checked with google API so we can receive the access tokens and id tokens
    
    #making sure the HTTP request received is validj
    #request access incoming request data
    if request.args.get('state') != login_session['state']:
        #always include this json response
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #auth_code must be sent back to google api
    #that way we can get an access token, and all other tokens
    auth_code = request.data

    try:
    #request.data contains incoming request data as string
    #need to find out how to exchange with googleauth
    #use credentials object to exchange auth code for access token

        flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        flow.redirect_uri = "postmessage"
        access_token = flow.fetch_token(auth_code)
        credentials = credentials(access_token)

    except Exception.with_traceback():
        response = make_response(json.dumps('Failed to upgrade auth code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        #storing the user access and refresh token
        login_session['credentials'] = {
            'token' : credentials.token,
            'refresh_token' : credentials.refresh_token,
            'token_uri' : credentials.token_uri,
            'client_id' : credentials.client_id,
            'client_secret' : credentials.client_secret,
            'scopes' : credentials.scopes
        }
        #check access token in credentials is valid
        authed_session = AuthorizedSession(credentials)
        #request adds credentials headers to the HTTP request and refershes credentials
        result = authed_session.request('GET', 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
        
        if result.get('error') is not None:
            response = make_response(json.dump(result.get('error')), 500)
            response.headers['Content-Type'] = 'application/json'
            return response

@app.route('/')
@app.route('/categories/')
def categoryMenu():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('main.html',categories=categories, items=items)

@app.route('/categories/<int:item_id>/item')
def categoryItem(item_id):
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_id=item_id)
    return render_template('categoryitem.html', categories=categories, items=items, item_id=item_id)
    

@app.route('/categories/<int:item_id>/item/description')
def categoryItemDescribe(item_id):
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(id=item_id)
    item_names = session.query(Item).filter_by(item_name=item_id)
    return render_template('categoryItemDescription.html', categories=categories, items=items, item_id=item_id, item_names=item_names)

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