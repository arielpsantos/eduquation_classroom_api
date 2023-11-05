from flask import Flask
from blueprints.documentation import blueprint

app = Flask(__name__)
app.config['RESTPLUS_MASK_SWAGGER'] = False
app.config['SECRET_KEY'] = 'c0f10696d83052b5186359d46b803851'
app.register_blueprint(blueprint)


if __name__ == "__main__":
    app.run()