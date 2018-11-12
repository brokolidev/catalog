from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, CategoryItem, Base
app = Flask(__name__)

engine = create_engine('sqlite:///category.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Restaurant CRUD
@app.route('/')
def showAll():
    title = "Welcome to Item Catalog Website"
    categories = session.query(Category).all()
    recentItems = session.query(CategoryItem).order_by(CategoryItem.datetime.desc()).limit(10)
    return render_template('index.html', title=title, categories=categories, recentItems=recentItems)

@app.route('/category/<int:category_id>')
def showCategoryItems(category_id):
    categories = session.query(Category).all()
    cur_category = session.query(Category).filter_by(id=category_id).one()
    title = "Items of {}".format(cur_category.name.capitalize())
    items = session.query(CategoryItem).filter_by(category_id=category_id).order_by(CategoryItem.datetime.desc()).all()
    return render_template('category.html', title=title, categories=categories, cur_category=cur_category, items=items)

@app.route('/category/<int:category_id>/item/<int:item_id>')
def showItemDetails(category_id, item_id):
    categories = session.query(Category).all()
    cur_category = session.query(Category).filter_by(id=category_id).one()
    cur_item = session.query(CategoryItem).filter_by(id=item_id).one()
    title = "Details of {}".format(cur_item.name.capitalize())
    return render_template('item.html', title=title, cur_category=cur_category, cur_item=cur_item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
