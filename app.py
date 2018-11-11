from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
app = Flask(__name__)

# Restaurant CRUD
@app.route('/')
def showCatalog():
    title = "Welcome to Item Catalog Website"
    return render_template('index.html', title=title)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
