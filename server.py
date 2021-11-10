from flask_app.controllers import users #the file from controllers called the plural of the class
from flask_app import app


if __name__=="__main__":
    app.run(debug=True)