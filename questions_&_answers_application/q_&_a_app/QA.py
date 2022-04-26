# imports test commit
import os  # os is used to get environment variables IP & PORT
import bcrypt
from flask import Flask  # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask import session
from sqlalchemy import update

from database import db
from models import Question as Question
from models import User as User
from models import Comment as Comment
from models import Score as Score
# from models import Upvote as Upvote
from forms import RegisterForm, LoginForm, CommentForm
# Search import
from flask_msearch import Search
#Secure filename import for picture storage
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/img'

app = Flask(__name__)  # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

app.config['SECRET_KEY'] = 'SE3155'

# Search posts
search = Search(app)
search.init_app(app)


# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/index')
def index():
    if session.get('user'):
        return render_template('index.html', user=session['user'])
    return render_template("index.html")

# route for the "All Questions" page
@app.route('/questions')
def get_questions():
    #Checks if a user is logged in
    if session.get('user'):
        #Queries all of the questions made by a specific user
        my_questions = db.session.query(Question).filter_by(user_id=session['user_id']).all()
        #Returns the questions as specififed in the "questions.html"
        return render_template('questions.html', questions=my_questions, user=session['user'])
    else:
        #returns to login if a user is not logged in
        return redirect(url_for('login'))

#Route for a specific question from the "All Questions" page
@app.route('/questions/<q_id>')
def get_question(q_id):
    #Checks if a user is logged in
    if session.get('user'):
        #Query to display the specific question by a specific user
        my_question = db.session.query(Question).filter_by(id=q_id, user_id=session['user_id']).one()
        #Creates a CommentForm form from 'forms.py' named 'form'
        form = CommentForm()
        #Creates a Score table and sets vote score to 0.
        score_zero = 0
        vote_score_zero = Score(score_zero, int(q_id), session['user_id'])
        db.session.add(vote_score_zero)
        db.session.commit()
        #Query to display the vote integer field in Score table
        question_score = db.session.query(Score).filter_by(id=q_id).one()
        #returns the question based on 'q_id' displayed how 'question.html' has specified
        return render_template('question.html', question=my_question, image_file=my_question.image_file,
                               user=session['user'], form=form, question_score=question_score)
    else:
        #returns to login if a user is not logged in
        return redirect(url_for('login'))

#Route for a new question to be added by user
@app.route('/questions/new', methods=['GET', 'POST'])
def new_question():
    #Checks if a user is logged in a session
    if session.get('user'):
        #Checks if the method requested is a POST method
        if request.method == 'POST':
            #Sets the 'title', question's 'text', and 'date' of the Question by the user
            title = request.form['title']
            text = request.form['noteText']
            from datetime import date
            today = date.today()
            today = today.strftime("%m-%d-%Y")
            #Requests the questions status ('Answered" or 'Unanswered') and sets it 'status'
            status = request.form['qstatus']
            #Request any files named 'file' from the question
            file = request.files['file']
            #Sets a filename to "sample.png" in case no file is uploaded
            filename = "sample.png"
            #If file exists
            if file:
                #Saves filename as a secured filename so it doesn't overwrite duplicate named files
                filename = secure_filename(file.filename)
                #Saves the filename string value to the path in UPLOAD_FOLDER
                file.save(os.path.join(UPLOAD_FOLDER, filename))
            #Creates a 'new_record' with all of the information saved in it and adds it to the "Question" model db
            new_record = Question(title, text, today, status, filename, session['user_id'])
            db.session.add(new_record)
            db.session.commit()
            #Returns user to the "All Quesitons" page
            return redirect(url_for('get_questions'))
        else:
            #Otherwise returns user to a new question form page
            return render_template('new.html', user=session['user'])
    else:
        #returns to login if a user is not logged in
        return redirect(url_for('login'))


#Route to edit a specific question from the "All Questions" page
@app.route('/questions/edit/<q_id>', methods=['GET', 'POST'])
def update_question(q_id):
    #Checks if a user is logged in a session
    if session.get('user'):
        # check method used for request
        if request.method == 'POST':
            # get title data
            title = request.form['title']
            # get question data
            text = request.form['noteText']
            # get question status
            status = request.form['qstatus']
            question = db.session.query(Question).filter_by(id=q_id).one()
            # update question data
            question.title = title
            # update question text
            question.text = text
            # update question status
            question.status = status
            # update question in DB
            db.session.add(question)
            db.session.commit()
            #Returns user to their "All Questions" page
            return redirect(url_for('get_questions'))
        else:
            # GET request - show new question form to edit question
            # retrieve note from database
            my_question = db.session.query(Question).filter_by(id=q_id).one()
            return render_template('new.html', question=my_question, user=session['user'])
    else:
        #returns to login if a user is not logged in
        return redirect(url_for('login'))


#Route to delete a specific question from the "All Questions" page
@app.route('/questions/delete/<q_id>', methods=['POST'])
def delete_question(q_id):
    #Checks if a user is logged in a session
    if session.get('user'):
        # retrieve question from database
        my_question = db.session.query(Question).filter_by(id=q_id).one()
        #deletes question from database and commits the change
        db.session.delete(my_question)
        db.session.commit()
        #returns user to their "All Questions" page
        return redirect(url_for('get_questions'))
    else:
        #returns to login if a user is not logged in
        return redirect(url_for('login'))

#Route to register a new user
@app.route('/register', methods=['POST', 'GET'])
def register():
    #Creates a new RegisterForm form from the 'forms.py' page
    form = RegisterForm()
    #checks if the request method is POST and that the input from the forms is valid
    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('get_questions'))

    # something went wrong - display register view
    return render_template('register.html', form=form)


#Route to login a specific user
@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view for the users "All Questions" page
            return redirect(url_for('get_questions'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)


#Route to logout of application
@app.route('/logout')
def logout():
    #Checks if a user is logged in a session
    if session.get('user'):
        session.clear()
    return redirect(url_for('index'))

#Route to make a new comment on a specific question
@app.route('/questions/<q_id>/comment', methods=['POST'])
def new_comment(q_id):
    #Checks if a user is logged in a session
    if session.get('user'):
        comment_form = CommentForm()
        # validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # get comment data
            comment_text = request.form['comment']
            #Creates a 'new_record' of the CommentForm passing in the comment text, question id, and user id for DB
            new_record = Comment(comment_text, int(q_id), session['user_id'])
            db.session.add(new_record)
            db.session.commit()
        #Returns user to the question that they just edited
        return redirect(url_for('get_question', q_id=q_id))

    else:
        #Returns to login if a user is not logged in
        return redirect(url_for('login'))


#Route to allows users to "upvote" or "downvote" a specificquestion
@app.route('/questions/<q_id>/score', methods=['POST', 'GET'])
def vote_score(q_id):
    #Checks if a user is logged in a session
    if session.get('user'):
        #Sets the score for 'vote' equal to zero and commits to DB
        score_zero = 0
        vote_score_zero = Score(score_zero, int(q_id), session['user_id'])
        db.session.add(vote_score_zero)
        db.session.commit()
        #Checks if the user is selecting the "upvote" option
        if request.form.get('upvote', False):
            #Gets the current score of 'vote', adds 1 to it, and commits to DB
            question_score = db.session.query(Score).filter_by(id=q_id).one()
            question_score.vote = question_score.vote + 1
            db.session.add(question_score)
            db.session.commit()
         #Checks if the user is selecting the "downvote" option
        if request.form.get('downvote', False):
            #Gets the current score of 'vote', subtracts 1 from it, and commits to DB
            question_score = db.session.query(Score).filter_by(id=q_id).one()
            question_score.vote = question_score.vote - 1
            db.session.add(question_score)
            db.session.commit()
        #Returns user to the question they just voted on
        return redirect(url_for('get_question', q_id=q_id))

    else:
        #Returns to login if a user is not logged in
        return redirect(url_for('login'))

#Route to search for a specific keyword in the title of a question passed in by the user
@app.route('/search', methods=['GET', 'POST'])
def search_question():
    #Checks if a user is logged in a session
    if session.get('user'):
        #Takes in user's keyword to search
        keyword = request.args.get('search')
        #Queries all Questions for the keyword searched
        question = Question.query.msearch(keyword, fields=['title']).filter_by(user_id=session['user_id']).all()
        #Returns user to Search page which shows all questions matched by keyword
        return render_template("search.html", questions=question)
    else:
        #returns to login if a user is not logged in
        return redirect(url_for('login'))


#Route to report a question
@app.route('/report')
def report_question():
    #Checks if a user is logged in a session
    if session.get('user'):
        #Returns user to report page
        return render_template("report.html")
    else:
        #returns user to login if a user is not logged in
        return redirect(url_for('login'))


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)
# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
