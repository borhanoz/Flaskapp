
import sqlite3

con=sqlite3.connect('capcake.db')
print("connected successfully!" )
# create table cart
# con.execute("drop table cart ;")
# con.execute("""CREATE TABLE cart (
#     cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     product_id INTEGER,
#     quantity INTEGER,
#     total_price REAL,
#     FOREIGN KEY (product_id) REFERENCES CAKE(Id)
# )""")

# print("table cart created successfully!" )

# con.execute("drop table CAKE ;")
# con.execute("""CREATE TABLE CAKE (
#     Id INTEGER PRIMARY KEY AUTOINCREMENT,
#     NAME TEXT NOT NULL,
#     PRICE INTEGER NOT NULL,
#     rate REAL,  -- Add the "rate" column with REAL data type
#     image BLOB
# )""")

# print("table CAKE created successfully!" )
con.execute("drop table user ;")
con.execute("CREATE TABLE user(Id INTEGER, NAME TEXT, email TEXT, password TEXT, mobile_number INTEGER);")
print("table User created successfully!" )
con.commit()
con.close()