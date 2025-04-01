from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
import datetime


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50, description="User's full name")
    email: EmailStr = Field(description="Valid email address")
    password: str = Field(min_length=6, description="Password with at least 6 characters")
    phone_number: Optional[int] = Field(None, description="User's phone number (optional)")
    role: Literal["user", "librarian"]


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50, description="Category name")


class CategoryResponse(BaseModel):
    id: int
    name: str


class BookCreate(BaseModel):
    isbn_number: str = Field(min_length=10, max_length=13, description="ISBN-10 or ISBN-13 format")
    title: str = Field(min_length=3, max_length=255, description="Book title")
    author: str = Field(min_length=3, max_length=255, description="Author's full name")
    category_id: int = Field(gt=0, description="Valid category ID")


class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    category_id: Optional[int]


class BookResponse(BaseModel):
    isbn_number: str
    title: str
    author: str
    category_id: int
    availability_status: bool

class BorrowBookRequest(BaseModel):
    book_id: str = Field(min_length=10, max_length=13, description="ISBN of the book to borrow")

class BorrowingHistoryResponse(BaseModel):
    book_id: str
    borrow_date: datetime.datetime
    return_date: Optional[datetime.datetime]
    status: Literal["borrowed", "returned"]
