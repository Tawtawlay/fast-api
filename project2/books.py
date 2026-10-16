from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()


# regular book class
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: float
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


# book class for validation
class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=3)
    description: str = Field(max_length=1000)
    rating: float = Field(ge = 0, le = 5.0)
    published_date: int = Field(ge=2000, le=2026)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Badriyah",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2026
            }
        }
    }


BOOKS = [
    Book(
        id = 1,
        title = 'Computer Science Pro',
        author = 'Tawtaw',
        description = 'A very nice book!',
        rating = 4.8,
        published_date = 2024
    ),
    Book(
        id = 2,
        title = 'Be Fast with API',
        author = 'Tawtaw',
        description = 'A great book!',
        rating = 4.3,
        published_date = 2026
    ),
    Book(
        id = 3,
        title = 'Master Endpoints',
        author = 'Tawtaw',
        description = 'An awesome book!',
        rating = 4.8,
        published_date = 2020
    ),
    Book(
        id = 4,
        title = 'HP1',
        author = 'Author 1',
        description = 'Book Description',
        rating = 1.8,
        published_date = 2015
    ),
    Book(
        id = 5,
        title = 'HP2',
        author = 'Author 2',
        description = 'Book Description',
        rating = 2.8,
        published_date = 2010
    ),
    Book(
        id = 6,
        title = 'HP3',
        author = 'Author 3',
        description = 'Book Description',
        rating = 3,
        published_date = 2026
    )
]


@app.get('/')
async def home():
    return {
        "message": "Welcome to my API"
    }

# GET request
@app.get('/books', status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


# find a book based on book_id
@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def get_book_id(book_id: int = Path(gt=0)):  # will give error when id is less than 1
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')


# find books based on rating
@app.get('/books/', status_code=status.HTTP_200_OK)
async def get_book_by_rating(rating: float = Query(ge=0, le=5)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return


# get by published date
@app.get('/books/published_date/', status_code=status.HTTP_200_OK)
async def read_book_by_date(date: int = Query(ge=2000, le=2026)):
    return [book for book in BOOKS if book.published_date == date]


# update book
@app.put('/books/update_book', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(new_book: BookRequest):
    book_changed = False
    for book in range(len(BOOKS)):
        if BOOKS[book].id == new_book.id:
            BOOKS[book] = new_book
            book_change = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')



# POST Request
@app.post('/create-book', status_code=status.HTTP_201_CREATED)
async def create_book(new_book: BookRequest):
    new_book = Book(**new_book.model_dump())
    BOOKS.append(find_book_id(new_book))


# delete request
@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_bok(book_id: int = Path(gt=0)):
    book_found = False
    for book in BOOKS:
        if book.id == book_id:
            BOOKS.remove(book)
            book_found = True
            break
    if not book_found:
        raise HTTPException(status_code=404, detail='Item not found')

    
# increment book by 1
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book





    
    