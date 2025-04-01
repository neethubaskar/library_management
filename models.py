from sqlalchemy import Integer, String, ForeignKey, Boolean, DateTime, BigInteger
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column
import datetime


class Base(DeclarativeBase):
    """Base class that inherit from DeclarativeBase of SQLAlchemy"""
    pass


class MemberBook(Base):
    __tablename__ = 'member_book'
    id = mapped_column(Integer, primary_key=True, index=True)
    user_id = mapped_column('user_id', Integer, ForeignKey('users.id'))
    book_id = mapped_column('book_id', String, ForeignKey('books.isbn_number'))
    borrow_date = mapped_column(DateTime, default=datetime.datetime.utcnow)
    return_date = mapped_column(DateTime, nullable=True)
    status = mapped_column(String, default="borrowed")  # "borrowed" or "returned"
    user = relationship("User", back_populates="borrowed_books")
    book = relationship("Book", back_populates="borrow_records")


class Book(Base):
    __tablename__ = "books"
    
    isbn_number = mapped_column(String, primary_key=True, index=True)  # ISBN as primary key
    title = mapped_column(String(255), nullable=False)
    author = mapped_column(String(255), nullable=False)
    category_id = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    availability_status = mapped_column(Boolean, default=True)
    borrow_records = relationship("MemberBook", back_populates="book")
    category = relationship("Category", back_populates="books")


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer(), primary_key=True, index=True)
    name = mapped_column(String, nullable=False)
    email = mapped_column(String(50), nullable=False, unique=True)
    password = mapped_column(String, nullable=False, deferred=True)
    phone_number = mapped_column(BigInteger)
    role = mapped_column(String, nullable=False)  # "user" or "librarian")
    borrowed_books = relationship("MemberBook", back_populates="user")

class Category(Base):
    __tablename__ = "categories"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, unique=True, nullable=False)
    books = relationship("Book", back_populates="category")

