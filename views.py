from flask import Blueprint, render_template, request

views = Blueprint("views", __name__)

# @views.route("/", methods= ['GET','POST'])
# def home():
#     data = request.form
#     print(data)
#     return render_template("index.html")
