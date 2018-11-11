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


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
