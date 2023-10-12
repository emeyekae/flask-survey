from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey 

app=Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

respond = "responses"
#session key

@app.route('/')
def root_page():
    """ home page for Satisfaction Survey"""
    return render_template("root.html", survey=satisfaction_survey,qnum = len(satisfaction_survey.questions))

@app.route("/start_survey", methods=["POST"])
def start_survey():
    """Clear responses list"""
    session[respond] = []
    return redirect("/questions/0")

@app.route("/questions/<int:questionid>")
def show_question(questionid):
    """Display Questions 1 at a time"""
    responses =session.get(respond)

    if (responses is None):
        # redirect to home page if no no response to question
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
        # All questions answered go to Thank you page.
        return redirect("/complete")

    if (len(responses) != questionid):
        # redirect back to proper question if URL is tappered with.
        flash(f"INVALID QUESTION ID: {questionid}.")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[questionid]
    return render_template("questions.html", question_num=questionid, question=question )


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save answer to responses list and continue to next question."""

    # get the answer chosen
    choice = request.form['answer']

    # save  answer in the responses list
    responses = session[respond]
    responses.append(choice)
    session[respond] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        # survey completed.  direct to thank you page
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route("/complete")
def complete():
    """ Thank them for completing the survey."""

    return render_template("complete.html",survey=satisfaction_survey,rep=session.get(respond) )