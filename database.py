from sqlite3 import *

conn = connect('Univs.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS universities(
                                                   univName TEXT NOT NULL ,
                                                   dept TEXT NOT NULL,
                                                   years INTEGER NOT NULL,
                                                   language text NOT NULL,
                                                   fees INTEGER NOT NULL,
                                                   langFees INTEGER NOT NULL,
                                                   PRIMARY KEY (univName, dept)
                                                   )""")


conn.commit()




