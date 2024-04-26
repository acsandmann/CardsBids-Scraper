from flask_MAIN import Flask
from models import Base
from db import db_session, init_db

Base.query = db_session.query_property()


def create_app():
    app = Flask(__name__)
    init_db(Base)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    from routes import main

    app.register_blueprint(main)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=6969, debug=True)
