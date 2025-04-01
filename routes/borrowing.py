from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import MemberBook, Book, User
from schemas import BorrowBookRequest, BorrowingHistoryResponse
from auth import get_current_user
import datetime

router = APIRouter()


@router.post("/borrow")
def borrow_book(request: BorrowBookRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    book = db.query(Book).filter(Book.isbn_number == request.book_id, Book.availability_status == True).first()
    if not book:
        raise HTTPException(status_code=400, detail="Book is not available for borrowing")

    existing_borrow = db.query(MemberBook).filter(
        MemberBook.user_id == current_user.id, 
        MemberBook.book_id == request.book_id, 
        MemberBook.status == "borrowed"
    ).first()

    if existing_borrow:
        raise HTTPException(status_code=400, detail="You already borrowed this book")
    
    borrow_record  = MemberBook(book_id=request.book_id, user_id=current_user.id, borrow_date=datetime.datetime.utcnow(), status="borrowed")
    book.availability_status = False
    db.add(borrow_record)
    db.commit()
    return {"message": "Book borrowed successfully"}


@router.post("/return/{book_id}")
def return_book(book_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    borrow_record = db.query(MemberBook).filter(
        MemberBook.book_id == book_id, 
        MemberBook.status == "borrowed",
        MemberBook.user_id == current_user.id
        ).first()
    if not borrow_record:
        raise HTTPException(status_code=400, detail="No active borrow record found")
    
    borrow_record.return_date = datetime.datetime.utcnow()
    borrow_record.status = "returned"
    
    book = db.query(Book).filter(Book.isbn_number == book_id).first()
    book.availability_status = True
    db.commit()
    return {"message": "Book returned successfully"}


@router.get("/borrow-history")
def get_borrowing_history(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    history = db.query(MemberBook).filter(MemberBook.user_id == current_user.id).all()
    return {"borrowing_history": history}


@router.get("/borrow-history/{user_id}", response_model=list[BorrowingHistoryResponse])
def get_borrowing_history(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Ensure users can only view their own history unless they are a librarian
    if current_user.role != "librarian" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this user's borrowing history."
        )

    borrow_records = db.query(MemberBook).filter(MemberBook.user_id == user_id).all()

    if not borrow_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No borrowing history found for this user."
        )

    return borrow_records