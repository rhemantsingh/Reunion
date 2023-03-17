import psycopg2

conn = psycopg2.connect(database="Reunion_DB", user="postgres", password="rootroot", host="database-1.c068glaizvq1.us-east-1.rds.amazonaws.com", port="5432")
cur = conn.cursor()
# cur.execute("create table test(id int, name varchar(10));")
# cur.execute("insert into test values(1,'hemant');")
# cur.execute("Select * from test;")
# data = cur.fetchall()
# print(len(data))
# print(data)


def run_querry(query):
    cur.execute(query)

# run_querry("create table Users(id int not null primary key, name varchar(20), email varchar(20), password varchar(20));")
# run_querry("Insert into Users values(1,'Hemant','hemant123','hemant123');")
# run_querry("Insert into Users values(2,'Akshay','akshay123','akshay123');")
# run_querry("Insert into Users values(3,'Salman','salman123','salman123');")
#
#
# run_querry("create table Follow(user_id int references Users(id) on delete cascade, follow_id int);")
# run_querry("Insert into Follow values(1,2);")
# run_querry("Insert into Follow values(1,3);")
# run_querry("Insert into Follow values(2,1);")
# run_querry("Insert into Follow values(2,3);")
#
#
# run_querry("create table Posts(post_id serial primary key, title varchar(20), description varchar(50), create_time date default current_date, user_id int references Users(id) on delete cascade);")
# run_querry("insert into posts(title,description,user_id) values('Holi', 'Playing Holi',1); ")
# run_querry("insert into posts(title,description,user_id,create_time) values('Lovely Holi', 'Playing holi woth lovely colors',2, '2023-03-16');")
# run_querry("insert into posts(title,description,user_id,create_time) values('Holi', 'Washing Clothes',1, '2023-03-18');")
# run_querry("insert into posts(title,description,user_id,create_time) values('Deewali', 'Crackers and Sweets',2, '2023-03-22');")
# run_querry("insert into posts(title,description,user_id,create_time) values('Movie shoot', 'Khatron ke Khiladi',2, '2023-03-25');")
#
# run_querry("create table userlikes(user_id int references Users(id) on delete cascade, post_id int references Posts(post_id) on delete cascade);")
# run_querry("insert into userlikes values(1,2);")
# run_querry("insert into userlikes values(2,1);")
# run_querry("insert into userlikes values(3,2);")
# run_querry("insert into userlikes values(1,4);")
# run_querry("insert into userlikes values(2,3);")
#
# run_querry("create table Comments(post_id int references Posts(post_id) on delete cascade, comment varchar(50) not null, commented_by int references Users(id));")
# run_querry("insert into comments values(1, 'Happy Holi brother', 2); ")
# run_querry("insert into comments values(3, 'Hahahahahaha', 2); ")
# run_querry("insert into comments values(1, 'Happy Holi you too bro..... let meet up later', 1); ")
# run_querry("insert into comments values(2, 'Aee bahut bdyaaa', 1); ")
# run_querry("insert into comments values(2, 'Aee bahut bdyaaa from salman bhai', 3); ")


conn.commit()
conn.close()
