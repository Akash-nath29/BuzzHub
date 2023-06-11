from flask import Flask, render_template, request, redirect, session, url_for
import json

app = Flask(__name__)
app.secret_key = "The_Pie"

def save_data(post_data):
    with open("data.json", "w") as file:
        json.dump(post_data, file, indent=4)

def save_credentials(credentials):
    # Load existing credentials (if any) or initialize an empty list
    try:
        with open('credentials.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    # Append new credentials to the list
    data.append(credentials)

    # Write the updated list to the JSON file
    with open('credentials.json', 'w') as file:
        json.dump(data, file)

def load_data():
    try:
        with open('data.json', 'r') as file:
            post_data = json.load(file)
    except FileNotFoundError:
        post_data = []
    
    return post_data

def load_users_data():
    try:
        with open("credentials.json", "r") as file:
            usersData = json.load(file)
    except FileNotFoundError:
        usersData = []
    
    return usersData[-1]

@app.route("/")
def index():
    post_data = load_data()
    return render_template("index.html", posts=post_data)

@app.route("/creat")
def creat():
    return render_template("creatPost.html")

@app.route("/post", methods=["POST"])
def post():
    users = load_users_data()
    post_data = load_data()
    post = request.form["post"]
    data = {
        "post": post,
        "user": {
            "userName": users['userName'],
            "userPassword": users['password']
        },
        'likes': 0,
        'comments': [],
    }
    post_data.append(data)
    save_data(post_data)
    return redirect('/')

@app.route('/accounts', methods=["GET", "POST"])
def account():
    return render_template("accounts.html")

@app.route('/customize', methods=["GET","POST"])
def customize():
    userName = request.form.get('userName', None)
    password = request.form.get('userPassword', None)
    userData = {
        "userName": userName,
        "password": password,
    }
    save_credentials(userData)
    session['userName'] = userName
    session['userPassword'] = password
    return redirect('/')

@app.route('/post/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    post_data = load_data()

    if post_id >= 0 and post_id < len(post_data):
        post = post_data[post_id]
        post['likes'] += 1
        save_data(post_data)

    return redirect('/')

@app.route('/post/comment/<int:post_id>', methods=['POST'])
def comment_post(post_id):
    post_data = load_data()

    if post_id >= 0 and post_id < len(post_data):
        post = post_data[post_id]
        comment = request.form['comment']
        post['comments'].append(comment)
        save_data(post_data)

    return redirect('/')   

@app.route('/post/comments/<int:post_id>', methods=['GET'])
def view_comments(post_id):
    post_data = load_data()

    if post_id >= 0 and post_id < len(post_data):
        post = post_data[post_id]
        return render_template('watchComments.html', post=post, post_id=post_id)

    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)