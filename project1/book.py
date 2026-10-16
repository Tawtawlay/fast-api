from fastapi import FastAPI, Body

BOOKS = [
    {'title': 'Title One', 
     'author': 'Author One', 
     'category': 'science'},

    {'title': 'Title Two', 
     'author': 'Author Two', 
     'category': 'science'},

    {'title': 'Title Three', 
     'author': 'Author Three', 
     'category': 'history'},

    {'title': 'Title Four', 
     'author': 'Author Four', 
     'category': 'math'},

    {'title': 'Title Five', 
     'author': 'Author Five', 
     'category': 'math'},

    {'title': 'Title Six', 
     'author': 'Author Two', 
     'category': 'math'}
]

app = FastAPI()

# GET Method
@app.get('/')
async def home():
    return {"message": "Welcome to my API!"}

@app.get("/book")
async def read_all_books():
    return BOOKS

# endpoint for specific book
@app.get('/book/id/{book_id}')
async def read_a_book(book_id: int):
    return BOOKS[book_id]

# dynamic parameter
# endpoint for specific book, passing string
@app.get('/book/title/{book_title}')
async def read_a_book_string(book_title:str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

# query parameter
@app.get('/book/')
async def get_book(title: str | None = None, 
                   author: str | None = None,
                   category: str | None = None):
    if title:
        results = [
            book for book in BOOKS 
            if book['title'].casefold() == title.casefold()
            ]
    if author:
        results = [
            book for book in BOOKS 
            if book['author'].casefold() == author.casefold()
            ]
    if category:
        results = [
            book for book in BOOKS 
            if book['category'].casefold() == category.casefold()
            ]
    return results

# uese both dynamic and query parameter
@app.get('/book/{book_author}/')
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = [
        book for book in BOOKS
        if book['author'].casefold() == book_author.casefold() and
        book['category'].casefold() == category.casefold()
]
    return books_to_return


# POST Method
# adding NEW

@app.post('/book/create_book')
async def create_book(new_book: dict = Body()):
    BOOKS.append(new_book)


# PUT Method
# updating 
@app.put('/book/update_book')
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


# DELETE Method
# used to delete data
@app.delete('/book/delete_book/{book_title}/{author}/{category}')
async def delete_book(book_title: str, author: str, category: str):
    for i in range(len(BOOKS)):
        if (BOOKS[i].get('title').casefold() == book_title.casefold() and
           BOOKS[i].get('author').casefold() == author.casefold() and
           BOOKS[i].get('category').casefold() == category.casefold()):
           BOOKS.pop(i)
           break
            
# API assignmenr
@app.get('/book/{author}')
async def get_book_by_author(author:str):
    books_to_return = [
        book for book in BOOKS if
        book.get('author').casefold() == author.casefold()
    ]
    return books_to_return


