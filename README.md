# python initial web development model

This is a simple code for understanding python web development using _Flask_ and _SQLAlchemy_.

## The database

The database has 2 tables. And database_setup.py contains the definition of it.

- Category
- CategoryItem

## Installation & Usage

Clone the GitHub repository
```
$ git clone https://github.com/brokolidev/catalog.git
$ cd crud
```

And then simply use your command line tool to generate DB and insert some sample data.
```
$ python database_setup.py
$ python samplecategory.py
```

It has developed on VM environment. So you need to setup VM or equivalant env to run this app.
Once your VM is ready, just type python app.py(python 2.x)
```
$ python app.py
```

By default, the port was set to 8000. use your browser and access http://localhost:8000 to check this webpage.
