import os
import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    # client = MongoClient("mongodb+srv://satzmongo:w-Zet7tVY-ZwiDZ@cluster0.zdg56mh.mongodb.net/test")

    client = MongoClient(os.environ.get("MONGODB_URI"))

    # mongodb+srv://satzmongo:<password>@cluster0.zdg56mh.mongodb.net/test
    app.db = client.microblogdb

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
        
        entries_with_date = [
            (   
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        for entry in app.db.entries.find({}):
            print(entry)
        return render_template("home.html", entries=entries_with_date)
    
    return app
