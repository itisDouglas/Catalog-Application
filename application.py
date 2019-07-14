#!/usr/bin/env python3
import os
from flask import (Flask, flash,render_template, url_for, jsonify, redirect, request, make_response, json)
from flask import session as login_session
import random, string
import hashlib
app = Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from database_setup import Base, Category, Item


from google.oauth2 import (credentials, id_token)
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import AuthorizedSession
from googleapiclient.discovery import build
import requests
import httplib2

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = 'https://www.googleapis.com/auth/userinfo.email'
CLIENT_ID = '357027840207-p8tmt9tpe4t9icdh37ftuo0daijl4u9u.apps.googleusercontent.com'
SECRET_KEY = app.secret_key = os.urandom(24)


engine = create_engine('sqlite:///database_tables.db')
Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
Session()

#add JSON endpoints
@app.route('/categories/<int:item_id>/JSON')
def categoriesItemsJSON(item_id):
    categories = Session.query(Category).all()
    items = Session.query(Item).filter_by(category_id=item_id).all()
    return jsonify(Categories=[c.serialize for c in categories],Items=[i.serialize for i in items])

@app.route('/categories/JSON')
def categoriesJSON():
    categories = Session.query(Category).all()
    return jsonify(Category=[c.serialize for c in categories])

#end API endpoints

@app.route('/login')
def showLogin():
    #my CSRF token
    state =''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    #login_session holds my string value called "state"
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['GET','POST'])
def gconnect():
    #verify integrity of the id token
    # state = hashlib.sha256(os.urandom(1024)).hexdigest()
    # #login_session holds my string value called "state"
    # login_session['state'] = state
    
    # if not request.headers.get('X-Requested-With'):
    #     abort(403)

    # if request.args.get('state') != login_session['state']:
    #     response = make_response(json.dumps('Invalid state parameter.'), 401)
    #     response.headers['Content-Type'] = 'application/json'
    # return response

    code = request.data
    #exchange the auth code here
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.redirect_uri('http://localhost:8000/login')
    authorization_url, state = flow.authorization_url(
        access_type = 'offline',
        include_granted_scopes='true',
        prompt='select_account'
    )

    login_session['state'] = state
    return redirect(authorization_url)
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES, STATE=state)
    flow.redirect_uri = url_for('http://localhost:8000', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    login_session['credentials'] = {
        'token' : credentials.token,
        'refresh_token' : credentials.refresh_token,
        'token_uri' : credentials.token_uri,
        'client_id' : credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes' : credentials.scopes
    }

    auth = build('oauth2', 'v2', credentials=credentials)
    return redirect(url_for(auth))
    
    #the response should be sent back to my application here
    # return redirect(authorization_url)
    # credentials = flow.fetch_token(code=code)
    # #call google api
    # #cred are sent over through here
    # #request session class with credentials
    # authed_session = AuthorizedSession(credentials)
    # response = authed_session.request('GET','https://www.googleapis.com/oauth2/v1/certs')
    # #request will return the http response, so handle the http response dammit; Response is an http response data type
    # #status: http status code
    # #headers: mampping[str,str] http response headers
    # #data: bytes, the response body
    # #I need to read the JSON file here and trap the access token
    # #handle google access token and id token
    
    # try:
    #     access_token = id_token.verify_oauth2_token(response, CLIENT_ID)

    #     if access_token['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
    #         raise ValueError('Wrong Issuer!')

    #     #userid = access_token['sub']
    # except ValueError:
    #     pass
    # #store userid into my database
    # try:
    #     if access_token['aud'] not in [CLIENT_ID]:
    #         raise ValueError('Wrong audience!')
    # except ValueError:
    #     pass

    # url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %access_token)
    # h = httplib2.Http()
    # result = json.loads(h.request(url, 'GET')[1])
    # if result.get('error') is not None:
    #     resp = make_response(json.dumps(result.get('error'), 500))
    #     resp.headers['Content-Type'] = 'application/json'


    # login_session['credentials'] = credentials

    # #get user info
    # userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    # params = {'access_token': access_token, 'alt':'json'}
    # answer = requests.get(userinfo_url, params=params)
    # data = json.loads(answer.text)

    # login_session['username'] = data['name']
    # login_session['picture'] = data['picture']
    # login_session['email'] = data['email']
    # flash('you are logged in as %s'%login_session['username'])

    # if request.args.get('state') != login_session['state']:
    #     response = make_response(json.dumps('Invalid state parameter.'), 401)
    #     response.headers['Content-Type'] = 'application/json'
    #     return response

    # flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    # flow.redirect_uri = url_for('http://localhost:8000')
    # authorization_response = request.url
    # flow.fetch_token(authorization_response=authorization_response)
    # credentials = flow.credentials
    # login_session['credentials'] = credentials

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], sub=login_session['sub'])
    Session.add(newUser)
    Session.commit()
    user = Session.query(User).filter_by(sub=login_session['sub']).one()
    return user.id

def getUserInfo(user_id):
    user = Session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(sub):
    try:
        user = Session.query(User).filter_by(sub=sub).one()
        return user.id
    except:
        return None

@app.route('/')
@app.route('/categories/')
def categoryMenu():
    categories = Session.query(Category).all()
    items = Session.query(Item).all()
    return render_template('main.html',categories=categories, items=items)
    Session.remove()

@app.route('/categories/<int:item_id>/item')
def categoryItem(item_id):
    categories = Session.query(Category).all()
    items = Session.query(Item).filter_by(category_id=item_id)
    return render_template('categoryitem.html', categories=categories, items=items, item_id=item_id)
    Session.remove()
    

@app.route('/categories/<int:item_id>/item/description')
def categoryItemDescribe(item_id):
    categories = Session.query(Category).all()
    items = Session.query(Item).filter_by(id=item_id)
    item_names = Session.query(Item).filter_by(item_name=item_id)
    return render_template('categoryItemDescription.html', categories=categories, items=items, item_id=item_id, item_names=item_names)
    Session.remove()

@app.route('/categories/item/new')
def categoryItemNew(methods=['GET','POST']):
    #CREATING ITEMS SHOULD HOLD CREATOR INFORMATION
    #HANDLE IT WITH AUTHORIZATION
    if 'sub' not in login_session:
        return redirect('/login')
        
    if request.method == 'POST':
        newItem = Item(item_name = request.form['item_name'], user_id=login_session['user_id'])
        Session.add(newItem)
        flash('New item %s Successfuljly added' %newItem.item_name)
        Session.commit()
        return redirect(url_for('/categories'))
    else:
        return render_template('categoryItemEdit')
    categories = Session.query(Category).all()
    return render_template('categoryItemNew.html', categories=categories)
    Session.remove()

@app.route('/categories/<int:item_id>/item/edit')
def categoryItemEdit(item_id):
    if 'sub' not in login_session:
        return redirect('/login')
    #check if user is authorized AND AUTHENTICATED
    #if not, give error message and send to login with quick splash javascript text output "please login to visit this page"
    item_edit = Session.query(Item).filter_by(item_id=item_id).one()
    if request.form['item_name']:
        item_edit.item_name = request.form['item_name']
        return redirect(url_for('/categories'))    
    else:
        return render_template('categoryItemEdit.html')

@app.route('/categories/<int:item_id>/item/delete')
def categoryItemDel(item_id, methods=['POST']):
    if 'sub' not in login_session:
        return redirect('/login')
    item_delete = Session.query(Item).fitler_by(item_id=item_id).ONe()
    if request.method == 'POST':
        Session.delete(item_delete)
        Session.commit()
        return redirect(url_for('/categories'))
    return render_template('categoryItemDel.html')
     #USE DELETE HTTP METHOD HEREF
    #check if user is authorized 
    #if not, give error message and send to login with quick splash javascript text output "please login to visit this page"


if __name__== '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)