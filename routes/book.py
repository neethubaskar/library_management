from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import BookCreate, BookResponse, BookUpdate, CategoryResponse, CategoryCreate
from models import Book, Category
from auth import get_current_user

router = APIRouter()


@router.post("/books", status_code=status.HTTP_201_CREATED)
def add_book(book: BookCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "librarian":
        raise HTTPException(status_code=403, detail="Only librarians can add books")

    existing_book = db.query(Book).filter(Book.isbn_number == book.isbn_number).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    
    category = db.query(Category).filter(Category.id == book.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"message": "Book added successfully", "book": new_book}


@router.put("/books/{isbn_number}")
def update_book(isbn_number: str, book_data: BookUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "librarian":
        raise HTTPException(status_code=403, detail="Only librarians can update books")

    book = db.query(Book).filter(Book.isbn_number == isbn_number).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_data.dict(exclude_unset=True).items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return {"message": "Book updated successfully", "book": book}


@router.delete("/books/{isbn_number}")
def delete_book(isbn_number: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "librarian":
        raise HTTPException(status_code=403, detail="Only librarians can delete books")

    book = db.query(Book).filter(Book.isbn_number == isbn_number).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}


@router.get("/", response_model=list[BookResponse])
def list_books(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    books = db.query(Book).all()
    return books


@router.get("/books/{isbn}", response_model=BookResponse)
def get_book_by_id(isbn: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    book = db.query(Book).filter(Book.isbn_number == isbn).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/books/search")
def search_books(title: str = None, author: str = None, category_id: int = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    query = db.query(Book)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if category_id:
        query = query.filter(Book.category_id == category_id)
    
    books = query.all()
    return {"books": books}


@router.post("/categories", response_model=CategoryResponse)
def add_category(category_data: CategoryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Only librarians can add book categories."""

    if current_user.role != "librarian":
        raise HTTPException(status_code=403, detail="Only librarians can add categories")

    existing_category = db.query(Category).filter(Category.name == category_data.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = Category(**category_data.dict())
    db.add(new_category)
    db.commit()
    return new_category


@router.get("/categories", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Fetch all available book categories."""
    
    return db.query(Category).all()


@router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Fetch category details by ID."""
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category
