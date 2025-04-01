# from flask import Flask, session, render_template, request, redirect, url_for
# import pyrebase
# import datetime
# import os
# from dotenv import load_dotenv

# load_dotenv()

# import cloudinary
# import cloudinary.uploader

# cloudinary.config(
#     cloud_name=os.environ.get("CLOUD_NAME"),
#     api_key=os.environ.get("API_KEY"),
#     api_secret=os.environ.get("API_SECRET"),
# )

# import firebase_admin
# from firebase_admin import credentials, db

# app = Flask(__name__)
# app.secret_key = os.environ.get("SECRET_KEY")

# config = {
#     "apiKey": os.environ.get("FIREBASE_API_KEY"),
#     "authDomain": os.environ.get("AUTHDOMAIN"),
#     "projectId": os.environ.get("PROJECTID"),
#     "storageBucket": os.environ.get("STORAGEBUCKET"),
#     "messagingSenderId": os.environ.get("MESSAGINGSENDERID"),
#     "appId": os.environ.get("APPID"),
#     "measurementId": os.environ.get("MEASUREMENTID"),
#     "databaseURL": os.environ.get("FIREBASE_DATABASE_URL"),
# }

# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()

# # Initialize firebase admin sdk.
# cred = credentials.Certificate(os.environ.get("FIREBASE_CREDENTIALS"))
# firebase_admin.initialize_app(cred, {"databaseURL": os.environ.get("FIREBASE_DATABASE_URL")})

# ref = db.reference("/")  # database reference.


# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         email = request.form["email"]
#         password = request.form["password"]
#         try:
#             user = auth.sign_in_with_email_and_password(email, password)
#             session["usr"] = user["idToken"]

#             user_info = auth.get_account_info(user["idToken"])
#             users_list = user_info.get("users", [])
#             if users_list:
#                 session["user_email"] = users_list[0].get("email", "Unknown")
#             else:
#                 session["user_email"] = "Unknown"

#             print("Session User Email:", session["user_email"])  # Debugging

#             return redirect(url_for("home"))

#         except Exception as e:
#             print(f"Error: {e}")  # Debugging
#             return render_template("index.html", error="Invalid credentials")

#     return render_template("index.html")


# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         email = request.form["email"]
#         password = request.form["password"]
#         try:
#             user = auth.create_user_with_email_and_password(email, password)
#             return redirect(url_for("index"))  # Redirect to login after successful signup
#         except Exception as e:
#             print(f"Signup Error: {e}")
#             return render_template("signup.html", error="Signup failed. Please try again.")
#     return render_template("signup.html")


# @app.route("/home")
# def home():
#     if "usr" in session:
#         posts_ref = ref.child("posts").get()
#         posts = []
#         if posts_ref:
#             for key, value in posts_ref.items():
#                 if "username" not in value or not value["username"]:
#                     value["username"] = "Unknown"
#                 if "time" in value and isinstance(value["time"], str):
#                     value["time"] = value["time"].replace("T", " ")
#                 posts.append(value)
#         posts.sort(key=lambda post: datetime.datetime.fromisoformat(post["time"]), reverse=True)

#         return render_template("home.html", posts=posts)
#     else:
#         return redirect(url_for("index"))


# @app.route("/post", methods=["GET", "POST"])
# def post():
#     if "usr" in session:
#         if request.method == "POST":
#             user_info = auth.get_account_info(session["usr"])["users"][0]
#             user_email = user_info["email"]

#             status = request.form["status"]
#             description = request.form["description"]
#             time = request.form["time"]
#             location = request.form["location"]
#             image = request.files["image"]

#             upload_result = cloudinary.uploader.upload(image)
#             image_url = upload_result["secure_url"]

#             print(upload_result["secure_url"])

#             post_data = {
#                 "username": session.get("user_email", "Unknown"),
#                 "status": status,
#                 "description": description,
#                 "time": time,
#                 "location": location,
#                 "image_url": image_url,
#             }

#             ref.child("posts").push(post_data)
#             return redirect(url_for("home"))
#         return render_template("post.html")
#     else:
#         return redirect(url_for("index"))


# @app.route("/logout")
# def logout():
#     session.pop("usr", None)
#     return redirect(url_for("index"))


# @app.route("/profile", methods=["GET", "POST"])
# def profile():
#     if "usr" in session:
#         user_info = auth.get_account_info(session["usr"])["users"][0]
#         user_email = user_info["email"]

#         posts_ref = ref.child("posts").get()
#         user_posts = []
#         if posts_ref:
#             for key, value in posts_ref.items():
#                 if value.get("username") == user_email:
#                     post_data = value
#                     post_data["id"] = key
#                     user_posts.append(post_data)

#         if request.method == "POST":
#             post_id = request.form["post_id"]
#             ref.child("posts").child(post_id).delete()
#             return redirect(url_for("profile"))

#         return render_template("profile.html", email=user_email, posts=user_posts)
#     else:
#         return redirect(url_for("index"))


from flask import Flask, session, render_template, request, redirect, url_for
import pyrebase
import datetime
import os
from dotenv import load_dotenv
import json  # Import the json library

load_dotenv()

import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=os.environ.get("CLOUD_NAME"),
    api_key=os.environ.get("API_KEY"),
    api_secret=os.environ.get("API_SECRET"),
)

import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

config = {
    "apiKey": os.environ.get("FIREBASE_API_KEY"),
    "authDomain": os.environ.get("AUTHDOMAIN"),
    "projectId": os.environ.get("PROJECTID"),
    "storageBucket": os.environ.get("STORAGEBUCKET"),
    "messagingSenderId": os.environ.get("MESSAGINGSENDERID"),
    "appId": os.environ.get("APPID"),
    "measurementId": os.environ.get("MEASUREMENTID"),
    "databaseURL": os.environ.get("FIREBASE_DATABASE_URL"),
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

# Initialize firebase admin sdk.
firebase_credentials_json = os.environ.get("FIREBASE_CREDENTIALS")
cred = credentials.Certificate(json.loads(firebase_credentials_json))

firebase_admin.initialize_app(cred, {"databaseURL": os.environ.get("FIREBASE_DATABASE_URL")})

ref = db.reference("/")  # database reference.


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session["usr"] = user["idToken"]

            user_info = auth.get_account_info(user["idToken"])
            users_list = user_info.get("users", [])
            if users_list:
                session["user_email"] = users_list[0].get("email", "Unknown")
            else:
                session["user_email"] = "Unknown"

            print("Session User Email:", session["user_email"])  # Debugging

            return redirect(url_for("home"))

        except Exception as e:
            print(f"Error: {e}")  # Debugging
            return render_template("index.html", error="Invalid credentials")

    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for("index"))  # Redirect to login after successful signup
        except Exception as e:
            print(f"Signup Error: {e}")
            return render_template("signup.html", error="Signup failed. Please try again.")
    return render_template("signup.html")


@app.route("/home")
def home():
    if "usr" in session:
        posts_ref = ref.child("posts").get()
        posts = []
        if posts_ref:
            for key, value in posts_ref.items():
                if "username" not in value or not value["username"]:
                    value["username"] = "Unknown"
                if "time" in value and isinstance(value["time"], str):
                    value["time"] = value["time"].replace("T", " ")
                posts.append(value)
        posts.sort(key=lambda post: datetime.datetime.fromisoformat(post["time"]), reverse=True)

        return render_template("home.html", posts=posts)
    else:
        return redirect(url_for("index"))


@app.route("/post", methods=["GET", "POST"])
def post():
    if "usr" in session:
        if request.method == "POST":
            user_info = auth.get_account_info(session["usr"])["users"][0]
            user_email = user_info["email"]

            status = request.form["status"]
            description = request.form["description"]
            time = request.form["time"]
            location = request.form["location"]
            image = request.files["image"]

            upload_result = cloudinary.uploader.upload(image)
            image_url = upload_result["secure_url"]

            print(upload_result["secure_url"])

            post_data = {
                "username": session.get("user_email", "Unknown"),
                "status": status,
                "description": description,
                "time": time,
                "location": location,
                "image_url": image_url,
            }

            ref.child("posts").push(post_data)
            return redirect(url_for("home"))
        return render_template("post.html")
    else:
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("usr", None)
    return redirect(url_for("index"))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "usr" in session:
        user_info = auth.get_account_info(session["usr"])["users"][0]
        user_email = user_info["email"]

        posts_ref = ref.child("posts").get()
        user_posts = []
        if posts_ref:
            for key, value in posts_ref.items():
                if value.get("username") == user_email:
                    post_data = value
                    post_data["id"] = key
                    user_posts.append(post_data)

        if request.method == "POST":
            post_id = request.form["post_id"]
            ref.child("posts").child(post_id).delete()
            return redirect(url_for("profile"))

        return render_template("profile.html", email=user_email, posts=user_posts)
    else:
        return redirect(url_for("index"))