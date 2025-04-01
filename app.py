from flask import Flask,session, render_template, request, redirect, url_for
import pyrebase
import datetime
import os
import config
from dotenv import load_dotenv
load_dotenv()
####new code

import cloudinary 
import cloudinary.uploader

cloudinary.config(
  cloud_name = os.environ.get("CLOUD_NAME"),    
    api_key = os.environ.get("API_KEY"),
    api_secret = os.environ.get("API_SECRET")
)
###3
config_dict={
    "apiKey": config.FIREBASE_API_KEY,
    "databaseURL": config.FIREBASE_DATABASE_URL,

}
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)
from dotenv import load_dotenv
import os

database_url = os.environ.get("FIREBASE_DATABASE_URL")
print(f"databaseURL: {database_url}") #check the database url.
config={
    "apiKey": os.environ.get('FIREBASE_API_KEY'),
  "authDomain": os.environ.get('AUTHDOMAIN'),
  "projectId": os.environ.get('PROJECTID'),
  "storageBucket": os.environ.get('STORAGEBUCKET'),
  "messagingSenderId":os.environ.get('MESSAGINGSENDERID'),
  "appId": os.environ.get('APPID'),
  "measurementId": os.environ.get('MEASUREMENTID'),
 "databaseURL": os.environ.get('FIREBASE_DATABASE_URL')
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
app.secret_key=os.environ.get('SECRET_KEY')
print(f"databaseURL: {config['databaseURL']}") #added print statement.

#######
# Initialize firebase admin sdk.
cred = credentials.Certificate(os.environ.get("FIREBASE_CREDENTIALS"))
firebase_admin.initialize_app(cred, {
    'databaseURL': config['databaseURL']
})

ref = db.reference('/') #database reference.


@app.route('/',methods=['GET','POST'])
def index():
    # if('usr' in session):
    #     return render_template('home.html')
    # if request.method=='POST':
    #     email=request.form['email']
    #     password=request.form['password']
    #     try:
    #         user=auth.sign_in_with_email_and_password(email,password)
    #         session['usr']=user['idToken']


    #         user_info = auth.get_account_info(user['idToken'])['users'][0]
    #         session['user_email'] = user_info.get('email', "Unknown")  # Store email
    #         print("Logged in as:", session["user_email"])  # Debugging





    #         #redirect user to home page after successful login.
    #         return redirect(url_for('home'))
    #     except Exception as e:
    #         print(f"Error: {e}")
    #         if hasattr(e, "args") and len(e.args) > 1:
    #             print(f"server response: {e.args[1]}")
    #             return render_template('index.html', error = e.args[1])
    #         else:
    #             return render_template('index.html', error = "an unknown error occured")
    # return render_template('index.html')



    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['usr'] = user['idToken']

            # ✅ Fetch user email correctly
            user_info = auth.get_account_info(user['idToken'])
            users_list = user_info.get('users', [])
            if users_list:
                session['user_email'] = users_list[0].get('email', 'Unknown')
            else:
                session['user_email'] = 'Unknown'

            print("Session User Email:", session['user_email'])  # Debugging

            return redirect(url_for('home'))

        except Exception as e:
            print(f"Error: {e}")  # Debugging
            return render_template('index.html', error="Invalid credentials")

    return render_template('index.html')  # ✅ Ensure GET request returns a response


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('index'))  # Redirect to login after successful signup
        except Exception as e:
            print(f"Signup Error: {e}")
            return render_template('signup.html', error="Signup failed. Please try again.")
    return render_template('signup.html')


@app.route('/home')
def home():
    if 'usr' in session:
         # Here you would fetch posts from a database and pass them to the template
         posts_ref = ref.child('posts').get()
         posts=[]
         if posts_ref:
            for key,value in posts_ref.items():
               # value["username"] = session.get("user_email", "Unknown")  
                if "username" not in value or not value["username"]:
                    value["username"] = "Unknown"
                if 'time' in value and isinstance(value['time'], str): # add check if time is a String
                    value['time'] = value['time'].replace('T', ' ') #replace the T
                posts.append(value)
         posts.sort(key=lambda post: datetime.datetime.fromisoformat(post['time']), reverse=True) #sort by time.

         
         return render_template('home.html',posts=posts)
    else:
        return redirect(url_for('index'))

posts=[]

####adding cloudinary to the post route
@app.route('/post',methods=['GET','POST'])

def post():
    if 'usr' in session:
        if request.method=='POST':
             # Fetch email from Firebase Auth
            user_info = auth.get_account_info(session['usr'])['users'][0]
            user_email = user_info['email']  # Get the actual email
            
            #handle post submission
            status=request.form['status']
            description=request.form['description']
            time=request.form['time']
            location=request.form['location']
            image=request.files['image']
            #save image to storage

            ###############
            upload_result=cloudinary.uploader.upload(image)
            image_url=upload_result['secure_url']

 # Debugging

            print(upload_result["secure_url"])
    

            post_data = {
                 
                'username': session.get('user_email', 'Unknown'),  # Use email instead
                'status': status,
                'description': description,
                'time': time,
                'location': location,
                'image_url': image_url
                }





            ####store in firebase
            ref.child('posts').push(post_data)
            ####
         
            #posts.append(post_data)
            return redirect(url_for('home'))
        return render_template('post.html')
    else :
        return redirect(url_for('index'))    



@app.route('/logout')
def logout():
    session.pop('usr',None)
    return redirect(url_for('index'))

####
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'usr' in session:
        # Fetch user personal details (e.g., email)
        user_info = auth.get_account_info(session['usr'])['users'][0]
        user_email = user_info['email']

        # Fetch all posts from Firebase
        posts_ref = ref.child('posts').get()
        user_posts = []
        if posts_ref:
            # Filter posts where the username matches the user's email
            for key, value in posts_ref.items():
                if value.get('username') == user_email:  # Compare username directly
                    post_data = value
                    post_data['id'] = key  # Add the unique Firebase key for deletion
                    user_posts.append(post_data)

        # Handle post deletion
        if request.method == 'POST':
            post_id = request.form['post_id']  # Get the post ID from the form
            ref.child('posts').child(post_id).delete()  # Delete the post from Firebase
            return redirect(url_for('profile'))  # Reload the profile page after deletion

        return render_template('profile.html', email=user_email, posts=user_posts)
    else:
        return redirect(url_for('index'))

#########
