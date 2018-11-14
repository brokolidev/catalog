from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, CategoryItem, Base


engine = create_engine('sqlite:///category.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
creater = "bocalist@gmail.com"  # enter your email(username)

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


electronics = Category(name="electronics", creater=creater)

session.add(electronics)
session.commit()

item = CategoryItem(name="Virtual Reality Headsets, Parts & Accessories",
                    description="""Virtual Reality Headsets,
                                    Parts & Accessories""",
                    category=electronics, creater=creater)

session.add(item)
session.commit()

item = CategoryItem(name="Cell Phones, Smart Watches & Accessories",
                    description="Cell Phones, Smart Watches & Accessories",
                    category=electronics, creater=creater)

session.add(item)
session.commit()

item = CategoryItem(name="TV, Video & Home Audio Electronics",
                    description="TV, Video & Home Audio Electronics",
                    category=electronics, creater=creater)

session.add(item)
session.commit()

item = CategoryItem(name="Video Games & Consoles",
                    description="Video Games & Consoles",
                    category=electronics, creater=creater)

session.add(item)
session.commit()

item = CategoryItem(name="Cameras & Photo",
                    description="Cameras & Photo",
                    category=electronics, creater=creater)

session.add(item)
session.commit()

item = CategoryItem(name="Vehicle Electronics & GPS",
                    description="Vehicle Electronics & GPS",
                    category=electronics, creater=creater)

session.add(item)
session.commit()

item = CategoryItem(name="Computers, Tablets & Network Hardware",
                    description="Computers, Tablets & Network Hardware",
                    category=electronics, creater=creater)

session.add(item)
session.commit()

item = CategoryItem(name="Smart Home",
                    description="Smart Home",
                    category=electronics, creater=creater)

session.add(item)
session.commit()


print "added electronics items!"
