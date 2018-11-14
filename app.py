from flask import Flask, render_template, request, url_for
from flask import redirect, flash, jsonify, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from database_setup import Category, CategoryItem, Base
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests


app = Flask(__name__)

engine = create_engine('sqlite:///category.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(open(
                'client_secret.json', 'r').read())['web']['client_id']


# Index page
@app.route('/')
def showAll():
    state = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    title = "Welcome to Item Catalog Website"
    categories = session.query(Category).all()
    recentItems = session.query(CategoryItem).order_by(
                    CategoryItem.datetime.desc()).limit(10)
    return render_template(
                'index.html',
                title=title, categories=categories,
                recentItems=recentItems, STATE=state,
                login_session=login_session)


# show category and it's items
@app.route('/category/<int:category_id>')
def showCategoryItems(category_id):
    state = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    categories = session.query(Category).all()
    cur_category = session.query(Category).filter_by(id=category_id).one()
    title = "Items of {}".format(cur_category.name.capitalize())
    items = session.query(CategoryItem).filter_by(
                category_id=category_id
            ).order_by(CategoryItem.datetime.desc()).all()
    return render_template(
            'category.html',
            title=title, categories=categories,
            cur_category=cur_category, items=items,
            STATE=state, login_session=login_session)


# show item's detail
@app.route('/item/<int:item_id>')
def showItemDetails(item_id):
    state = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    categories = session.query(Category).all()
    cur_item = session.query(CategoryItem).filter_by(id=item_id).one()
    title = "Details of {}".format(cur_item.name.capitalize())
    return render_template(
            'item.html',
            title=title, cur_item=cur_item,
            STATE=state, login_session=login_session)


# add a new category
@app.route('/category/new', methods=['GET', 'POST'])
def addCategory():
    if "username" not in login_session:
        return redirect("/")
    if request.method == 'POST':  # save a new category
        newCategory = Category(
                        name=request.form['categoryName'],
                        creater=login_session["email"])
        session.add(newCategory)
        session.commit()
        flash('New category created!!')
        return redirect('/')
    else:
        state = ''.join(random.choice(
                    string.ascii_uppercase + string.digits
                    ) for x in xrange(32))
        login_session['state'] = state
        title = "Add a new category"
    return render_template(
            'addcategory.html',
            title=title, login_session=login_session)


# edit a category
@app.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
def editCategory(category_id):
    if "username" not in login_session:
        return redirect("/")
    if request.method == 'POST':  # save a new category
        targetCategory = session.query(Category).filter_by(
                                                    id=category_id).one()
        if targetCategory.creater != login_session['email']:
            flash('You can only edit the categories you created.')
            return redirect("/")
        targetCategory.name = request.form['categoryName']
        session.add(targetCategory)
        session.commit()
        flash('Category edited successfully!!')
        return redirect('/')
    else:
        targetCategory = session.query(Category).filter_by(
                                                id=category_id).one()
        state = ''.join(random.choice(
                    string.ascii_uppercase + string.digits
                    ) for x in xrange(32))
        login_session['state'] = state
        title = "Edit {} category".format(targetCategory.name)
    return render_template(
            'editcategory.html',
            title=title,
            login_session=login_session,
            targetCategory=targetCategory)


# delete a category
@app.route('/category/delete/<int:category_id>', methods=['GET'])
def deleteCategory(category_id):
    if "username" not in login_session:
        return redirect("/")
    targetCategory = session.query(Category).filter_by(id=category_id).one()
    if targetCategory.creater != login_session['email']:
        flash('You can only delete the categories you created.')
        return redirect("/")
    session.delete(targetCategory)
    session.commit()
    # todo : need to delete all belonging items as well
    flash('Category deleted successfully!!')
    return redirect('/')


# add a new item
@app.route('/item/new', methods=['GET', 'POST'])
def addItem():
    if "username" not in login_session:
        return redirect("/")
    if request.method == 'POST':  # save a new category
        newItem = CategoryItem(
                    name=request.form['itemname'],
                    category_id=request.form['category_id'],
                    description=request.form['description'],
                    creater=login_session["email"])
        session.add(newItem)
        session.commit()
        flash('New item created!!')
        return redirect('/')
    else:
        state = ''.join(random.choice(
                    string.ascii_uppercase + string.digits
                    ) for x in xrange(32))
        login_session['state'] = state
        title = "Add a new item"
        categories = session.query(Category).all()
    return render_template(
            'additem.html',
            title=title, login_session=login_session,
            categories=categories)


# edit an item
@app.route('/item/edit/<int:item_id>', methods=['GET', 'POST'])
def editItem(item_id):
    if "username" not in login_session:
        return redirect("/")
    if request.method == 'POST':  # save a edited item
        targetItem = session.query(CategoryItem).filter_by(id=item_id).one()
        if targetItem.creater != login_session['email']:
            flash('You can only edit the items you created.')
            return redirect("/")
        targetItem.name = request.form['itemname']
        targetItem.description = request.form['description']
        targetItem.category_id = request.form['category_id']
        session.add(targetItem)
        session.commit()
        flash('Item edited successfully!!')
        return redirect('/')
    else:
        state = ''.join(random.choice(
                    string.ascii_uppercase + string.digits
                    ) for x in xrange(32))
        login_session['state'] = state
        title = "Add a new item"
        categories = session.query(Category).all()
        targetItem = session.query(CategoryItem).filter_by(id=item_id).one()
    return render_template(
            'edititem.html',
            title=title, login_session=login_session,
            categories=categories, targetItem=targetItem)


# delete an item
@app.route('/item/delete/<int:item_id>', methods=['GET'])
def deleteItem(item_id):
    if "username" not in login_session:
        return redirect("/")
    targetItem = session.query(CategoryItem).filter_by(id=item_id).one()
    if targetItem.creater != login_session['email']:
        flash('You can only delete the items you created.')
        return redirect("/")
    session.delete(targetItem)
    session.commit()
    flash('Item deleted successfully!!')
    return redirect('/')


# JSON API - whole catalog
@app.route('/catalog.json')
def categoryJSON():
    categories = session.query(Category).options(
                    joinedload(Category.items)).all()
    return jsonify(
            category=[
                dict(c.serialize, items=[i.serialize for i in c.items])
                for c in categories])


# JSON API - all categories
@app.route('/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(category=[c.serialize for c in categories])


# JSON API - all items
@app.route('/items/JSON')
def itemsJSON():
    items = session.query(CategoryItem).all()
    return jsonify(items=[i.serialize for i in items])


# JSON API - details of an item
@app.route('/item/<int:item_id>/JSON')
def itemDeatilJSON(item_id):
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    return jsonify(item=[item.serialize])


# Google login connect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                    json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['gplus_id'] = data['id']
    login_session['email'] = data['email']

    return 'success!'


# Google login disconnect
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
                    json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/\
            o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['picture']
        # response = make_response(
        #               son.dumps('Successfully disconnected.'), 200)
        # response.headers['Content-Type'] = 'application/json'
        # return response
        return redirect('/')
    else:
        response = make_response(
                    json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
