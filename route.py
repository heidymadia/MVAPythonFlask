from flask import Flask, url_for, request, render_template;
from app import app;
import redis;

# Redis Connection
r = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses="True");
 
@app.route('/')
def hello():
    createlink = "<a href ='" + url_for('create') + "'>create a question</a>";
    body = """
    <html>
        <head>
            <title>Hello, world!</title>
        <head>
        <body>
            <h1>""" + createlink + """</h1>
        </body>
    </html>""";
    return render_template()
    return body;

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("CreateQuestion.html");
    elif request.method == "POST":
        # Reading from form. 
        # Make sure you have the same name from form
        title = request.form["title"];
        question = request.form["question"];
        answer = request.form["answer"];
         
        # Try Catch this maybe? 
        r.set(title +":question", question);
        r.set(title +":answer", answer);

        return render_template("CreatedQuestion.html", question = question);
    else:
        return "<h2>Invalid request</h2>";

@app.route("/question/<title>", methods=["GET", "POST"])
def question(title):
    if request.method == "GET":
        question = "Question here.";
        question = r.get(title +":question");

        return render_template("AnswerQuestion.html", question = question);
    elif request.method == "POST":
        submittedAnswer = request.form['answer'];

        answer = "Answer";
        answer = r.get(title +":answer");
        if submittedAnswer == answer:
            return render_template("Correct.html");
        else:
            return render_template("Incorrect.html", submittedAnswer = submittedAnswer, answer = answer);
    else:
        return "<h2>Invalid request</h2>";