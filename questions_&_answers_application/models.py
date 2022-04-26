import datetime
from database import db

#Model for the Questions in DB
class Question(db.Model):
    #Integer column holding the specific id's for Questions in DB
    id = db.Column("id", db.Integer, primary_key=True)
    #String column holding the specific title's for Questions in DB
    title = db.Column("title", db.String(200))
    #String column holding the specific Question's text for Questions in DB
    text = db.Column("text", db.String(100))
    #String column holding the date's for Questions in DB
    date = db.Column("date", db.String(50))
    #String column holding the 'Answered' status for Questions in DB
    status = db.Column("status", db.String(50))
    #String column holding the specific path for images uploaded for Questions in DB
    image_file = db.Column("image_file", db.String(200))
    #Integer column holding the specific user id's for Questions in DB
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    #A relationship between the Question and Comment Tables
    comments = db.relationship("Comment", backref="question", cascade="all, delete-orphan", lazy=True)
    #Makes the title's of Question's in DB searchable
    __searchable__ = ['title']

    #Initializes all variable passed in
    def __init__(self, title, text, date, status, image_file, user_id):
        self.title = title
        self.text = text
        self.date = date
        self.status = status
        self.user_id = user_id
        self.image_file = image_file

#Model for the Users in DB
class User(db.Model):
    #Integer column holding the specific id's for User's in DB
    id = db.Column("id", db.Integer, primary_key=True)
    #String column for User's first name in DB
    first_name = db.Column("first_name", db.String(100))
    #String column for User's last name in DB
    last_name = db.Column("last_name", db.String(100))
    #String column for User's email in DB
    email = db.Column("email", db.String(100))
    #String column for User's password in DB
    password = db.Column(db.String(255), nullable=False)
    #DateTime column for User's date registered in DB
    registered_on = db.Column(db.DateTime, nullable=False)
    #A relationship between the User and Question Tables
    question = db.relationship("Question", backref="user", lazy=True)
    #A relationship between the User and Comment Tables
    comments = db.relationship("Comment", backref="user", lazy=True)

    #Initializes all variable passed in
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()


#Model for the Comments in DB
class Comment(db.Model):
    #Integer column holding the specific id's for Comment's in DB
    id = db.Column(db.Integer, primary_key=True)
    #DateTime column for User's date registered in DB
    date_posted = db.Column(db.DateTime, nullable=False)
    #Column for comments context
    content = db.Column(db.VARCHAR, nullable=False)
    #Integer Column that stores which question was commented on by the questions id
    q_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    #Integer Column that stores which user commented on the question by the users id
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    #Initializes all variable passed in
    def __init__(self, content, q_id, user_id):
        self.date_posted = datetime.date.today()
        self.content = content
        self.q_id = q_id
        self.user_id = user_id


#Model for the Score of votes in DB
class Score(db.Model):
    #Integer column holding the specific id's for Comment's in DB
    id = db.Column(db.Integer, primary_key=True)
    #Integer column holding the number of votes for a question in DB
    vote = db.Column(db.Integer)
    #Integer Column that stores which question was voted on by the questions id
    q_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    #Integer Column that stores which user voted on the question by the users id
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    #Initializes all variable passed in
    def __init__(self, vote, q_id, user_id):
        self.vote = vote
        self.q_id = q_id
        self.user_id = user_id
