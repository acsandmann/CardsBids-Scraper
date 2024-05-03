from flask import Flask
from flask_cors import CORS
from models import Base
from db import db_session, init_db

Base.query = db_session.query_property()


def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://127.0.0.1:3000", "http://localhost:3000", "https://cb-frontend-kappa.vercel.app/"])
    init_db(Base)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    from routes import main

    app.register_blueprint(main)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=6969, debug=True)
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=6969)
