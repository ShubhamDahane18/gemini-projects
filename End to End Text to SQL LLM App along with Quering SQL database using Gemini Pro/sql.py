
import sqlite3 



connection = sqlite3.connect("student.db")

## Create a cursor object
cursor = connection.cursor()

table_info = """ 
CREATE TABLE IF NOT EXISTS STUDENT (NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT) ;

"""

cursor.execute(table_info)

# Insert multiple records using executemany()
# records = [
#     ('Shubh', 'Data Science', 'A', 90),
#     ('Krish', 'Data Science', 'A', 95),
#     ('Anil', 'Data Science', 'B', 85),
#     ('Shubham', 'DEVOPS', 'A', 35),
#     ('Shiv', 'DEVOPS', 'A', 50)
# ]

# cursor.executemany("INSERT INTO STUDENT VALUES(?, ?, ?, ?)", records)


### Insert records 
cursor.execute('''INSERT INTO STUDENT VALUES('Shubh', 'Data Science', 'A', 90) ''')
cursor.execute('''INSERT INTO STUDENT VALUES('Krish', 'Data Science', 'A', 95) ''')
cursor.execute('''INSERT INTO STUDENT VALUES('Anil', 'Data Science', 'B', 85) ''')
cursor.execute('''INSERT INTO STUDENT VALUES('Shubham', 'DEVOPS', 'A', 35) ''')
cursor.execute('''INSERT INTO STUDENT VALUES('Shiv', 'DEVOPS', 'A', 50) ''')

## Display all the records
print("All records in the table:")
data = cursor.execute('''SELECT * FROM STUDENT''')

for row in data :
    print(row)
    
connection.commit()
connection.close()