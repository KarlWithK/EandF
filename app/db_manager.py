import sqlite3


# for testing only
# import os
# os.remove("../blogdata.db")

DB_FILE = "blogdata.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()


# creates the tables
def createTables():

    # command to create the table of all users.
    # Columns:
    # username (str)
    # password (str)
    # unique id (int primary key)
    command = "CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);"

    # command to create the table of all blogs.
    # Columns:
    # user id (int)
    # username (str)
    # blog title (str)
    # blog id (int primary key)
    # date created (str)
    # blog bio (str)
    command += "CREATE TABLE IF NOT EXISTS blogs(user_id INT, username TEXT, blog_title TEXT, blog_id INTEGER PRIMARY KEY AUTOINCREMENT, date_created TEXT, blog_bio TEXT);"

    # command to create table of all blog entries.
    # Columns:
    # blog id (int)
    # username (str)
    # entry id (int primary key)
    # entry title (str)
    # entry content (str)
    # date created (str)
    command += "CREATE TABLE IF NOT EXISTS entries(blog_id INT, username TEXT, entry_id INTEGER PRIMARY KEY AUTOINCREMENT, entry_title TEXT, entry_content TEXT, date_created TEXT);"

    # executes the command and commits the change
    c.executescript(command)
    db.commit()


# returns the username and password for a given user_id in a tuple (username,
# password)
# consider case when 2 users have the same username and password. Technically
# would work because they have different ids. Should we make username unique as well?
def getUserId(username: str) -> int:
    command = 'SELECT id FROM users WHERE username = "{}";'.format(
        username)
    info = 0
    for row in c.execute(command):
        info = row[0]

    return info


# returns a username for any given user_id
def getUsername(user_id: int) -> str:
    command = 'SELECT username FROM users WHERE id = "{}";'.format(user_id)
    user = ""
    for row in c.execute(command):
        user = row[0]
    return user


# returns a list of all the user_ids in the db
def getAllUsers():
    command = 'SELECT id FROM users'
    ids = []
    for row in c.execute(command):
        ids.append(row[0])
    return ids


# returns (username, password, user_id) for a given username. Returns None
# if argument username is not present in the database
def getUserInfo(username: str):
    command = 'SELECT username, password, id FROM users WHERE username = "{}";'.format(
        username)
    info = ()
    for row in c.execute(command):
        info += (row[0], row[1], row[2])
    if info == ():
        return None
    return info


# returns a list of blog_ids given a user_id
def getUserBlogs(user_id: int) -> list:
    command = 'SELECT blog_id FROM blogs WHERE user_id = "{}";'.format(user_id)
    blog_ids = []
    for row in c.execute(command):
        blog_ids.append(row[0])
    return blog_ids


# returns a tuple (title, bio, date_created, blog_id,) for any given blog_id
def getBlogBasic(blog_id: int) -> tuple:
    command = 'SELECT blog_title, blog_bio, date_created, blog_id, username FROM blogs WHERE blog_id = "{}";'.format(
        blog_id)
    blog_info = ()
    for row in c.execute(command):
        blog_info += (row[0], row[1], row[2], row[3], row[4])
    return blog_info


# returns a username for any given blog_id
def getBlogUser(blog_id: int) -> str:
    command = 'SELECT username FROM blogs WHERE blog_id = "{}";'.format(
        blog_id)
    username = ""
    for row in c.execute(command):
        username = row[0]
    return username


# returns a tuple of all entries for a given blog
def getBlogEntries(blog_id: int) -> list:
    command = 'SELECT entry_id FROM entries WHERE blog_id = "{}";'.format(
        blog_id)
    entry_ids = []
    for row in c.execute(command):
        entry_ids.append(row[0])
    return entry_ids


def getEntryInfo(entry_id: int) -> tuple:
    command = 'SELECT blog_id, entry_id, entry_title, entry_content, date_created FROM entries WHERE entry_id = "{}";'.format(
        entry_id)
    entry_info = ()
    for row in c.execute(command):
        entry_info += (row[0], row[1], row[2], row[3], row[4])
    return entry_info


# returns a tuple in the following format: (login_successful, issue, user_id)
# login_successful will be either True (correct info) or False
# issue will be None if login_successful is True. Otherwise will be "user not found" or
# "incorrect username or password"
# user_id will be returned if login_successful. None if not login_successful
def checkLogin(username: str, password: str) -> tuple:
    info = getUserInfo(username)
    if info == None:
        return (False, "User not found", None)
    elif (info[0] == username) and (info[1] == password):
        return (True, None, info[2])
    return (False, "Incorrect username or password", None)


# registers a new user by adding their info to the db
# returns the unique user_id so that it can be added to the session in app.py
def registerUser(username: str, password: str):
    command = 'INSERT INTO users VALUES ("{}", "{}", NULL);'.format(
        username, password)

    c.execute(command)
    db.commit()


# creates a blog by inserting the necessary data into the db
def createBlog(user_id: int, username: str, blog_title: str, date_created: str, blog_bio: str):
    command = 'INSERT INTO blogs VALUES ({}, "{}", "{}", NULL, "{}", "{}");'.format(
        user_id, username, blog_title, date_created, blog_bio)

    c.execute(command)
    db.commit()


# creates an entry by inserting the necessary data into the db
def createEntry(blog_id: int, username: str, entry_title: str, entry_content: str, date_created: str):
    command = 'INSERT INTO entries VALUES({}, "{}", NULL, "{}", "{}", "{}");'.format(
        blog_id, username, entry_title, entry_content, date_created)

    c.execute(command)
    db.commit()


def editEntry(entry_id: int, entry_title: str, entry_content: str):
    command = 'UPDATE entries SET entry_title = "{}", entry_content = "{}" WHERE entry_id = "{}";'.format(
        entry_title, entry_content, entry_id)
    c.execute(command)
    db.commit()


# closes the database (only use if user logging out i think)
def close():
    db.close()


# Helper functions (DO NOT USE IN app.py):


# For testing only
# if __name__ == "__main__":
#     createTables()

#     print(getUserId("ben"))
#     # createBlog(getUserId("ben"), "ben", "Doodoo",
#     #            "10/12/2020", "This is my blog.")

#     command = 'SELECT * FROM blogs'
#     for row in c.execute(command):
#         print(row)

#     print(checkLogin("benn", "dover"))

#     blogs = getUserBlogs(getUserId("ben"))

#     for blog in blogs:
#         title, bio, date = getBlogBasic(blog)
#         print(title)
#         print(bio)
#         print(date)
