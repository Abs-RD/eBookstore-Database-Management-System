# =====Importing Libraries===========
import sqlite3
from tabulate import tabulate

# creating database
database = sqlite3.connect("ebookstore_db")

# Get a cursor object
cursor = database.cursor()

# ================== functions ================
# creating table
cursor.execute('''CREATE TABLE IF NOT EXISTS books
        (id int primary key,
        Title varchar(50) not null,
        Author varchar(50) not null,
        Qty int not null)
    ''')


# validating existence of records in ebookstore_db
numb_of_rows = len(cursor.execute(''' select * from books where id >= 3001 ''').fetchall())
print(f"\nNumber of rows = {numb_of_rows}\n")

# populating table
ebookstore_records = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
                    (3002, 'Harry Potter and the Philosopher''s Stone', 'J.K. Rowling', 40),
                    (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
                    (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
                    (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]
if numb_of_rows == 0:
    cursor.executemany('''INSERT INTO books (id, Title, Author, Qty) VALUES(?,?,?,?)''', ebookstore_records)
    print()


# function to view table
def table_view(books_data):
    heading = ["id", "Title", "Author", "Qty"]
    print(tabulate(books_data, heading, tablefmt="fancy_grid"), '\n')


# view_data(books_data)
bookstore_data = cursor.execute('''SELECT * FROM books''')
table_view(bookstore_data)


# function to add new books to the database
def add_new_book():
    id = int(input("Enter book id: "))
    Title = input("Enter book title: ")
    Author = input("Enter book author: ")
    Qty = int(input("Enter book quantity: "))
    cursor.execute('''INSERT INTO books (id, Title, Author, Qty) VALUES (?,?,?,?) ''', (id, Title, Author, Qty))
    cursor.execute('''SELECT * FROM books WHERE id=?''', (id,))
    new_book = cursor.fetchone()
    print(new_book)
    print("Database updated")


# function to update book information
def update_book_info():
    id = int(input("Enter book id: "))
    Title = input("Enter new book title: ")
    Author = input("Enter new book author: ")
    Qty = int(input("Enter book quantity: "))
    cursor.execute('''UPDATE books SET Title=?, Author=?, Qty=? WHERE id=?''', (Title, Author, Qty, id))
    print("Book information updated")


# function to delete book from the database
def delete_book():
    id = int(input("Enter book id: "))
    cursor.execute('''DELETE FROM books WHERE id=?''', (id,))
    print("Book deleted from database")


# function to search the database to find a specific book
def search_for_book():
    Title = input("Enter title of book: ")
    Author = input("Enter new book author: ")
    cursor.execute('''SELECT * FROM books WHERE Title=? OR Author=?''', (Title, Author))
    book = cursor.fetchone()
    print(book)



# ================== main block of code ================
# presenting the menu to the user
while True:
    menu = int(input('''\n\nPlease select one of the following options below:
1. Enter book
2. Update book
3. Delete book
4. Search books
5. View table
0. Exit

: '''))

    # add new book to the database
    if menu == 1:
        add_new_book()

    # update book information
    elif menu == 2:
        update_book_info()

    # delete book from the database
    elif menu == 3:
        delete_book()

    # search database to find a specific book
    elif menu == 4:
        search_for_book()

    # view table
    elif menu == 5:
        bookstore_data = cursor.execute('''SELECT * FROM books''')
        table_view(bookstore_data)

    # exit
    elif menu == 0:
        print("Goodbye")
        break
    else:
        print("Invalid choice, try again")

database.commit()
database.close()
