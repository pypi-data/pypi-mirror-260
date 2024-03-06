from flask import Flask

def start_flask_app(host='0.0.0.0', port=5000):
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return 'Hello, World!'

    app.run(host=host, port=port)

