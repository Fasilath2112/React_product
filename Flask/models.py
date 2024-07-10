from flask_sqlalchemy import SQLAlchemy
from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship
from sqlalchemy import String, create_engine, Integer, ForeignKey, UniqueConstraint
import logging

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Category(db.Model):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    products: Mapped[List['Product']] = relationship('Product', back_populates='category')

class Product(db.Model):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    category: Mapped['Category'] = relationship('Category', back_populates='products')
    images: Mapped[List['Image']] = relationship('Image', back_populates='product')

class Image(db.Model):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    product: Mapped['Product'] = relationship('Product', back_populates='images')

class User(Base):
    __tablename__ = "user"
    __table_args__ = (UniqueConstraint('firstname', 'lastname', 'email'),)
    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(150))
    ph_no: Mapped[str] = mapped_column(String(50))

def init_db(db_uri='postgresql+psycopg2://postgres:password@localhost:5432/flaskdb'):
    logger = logging.getLogger("FlaskApp")
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
    logger.info("Created database")

def get_session(db_uri):    
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
