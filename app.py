from flask import Flask
import database
from Config import Config

conf = Config()

app = Flask(__name__)
app.config['SECRET_KEY'] = conf.SECRET_KEY

database.create_db(app)


import routes


@app.route('/')
@app.route('/home')
@app.route('/news')
def index():
    return routes.index()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return routes.login()

@app.route('/logout')
def logout():
    return routes.logout()

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    return routes.create_post(conf.UPLOAD_FOLDER)

@app.route('/post/<int:id>')
def post(id):
    return routes.post(id)

@app.route('/profile')
def profile():
    return routes.profile()

@app.route('/update_post/<int:id>', methods=['GET', 'POST'])
def update_post(id):
    return routes.udate_post(id, conf.UPLOAD_FOLDER)

@app.route('/delete_post/<int:id>')
def delete_post(id):
    return routes.delete_post(id, conf.UPLOAD_FOLDER)

@app.route('/about')
def about():
    return routes.about()


# @app.route('/registration', methods=['GET', 'POST'])
# def registration():
#     return routes.registration()


if __name__ == '__main__':
    app.run(debug=True)
