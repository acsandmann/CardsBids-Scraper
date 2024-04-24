from flask import Flask
from models import Car, Base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

engine = create_engine("sqlite:///./cars.db")
db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = db.query_property()


def create_app():
    app = Flask(__name__)
    engine = create_engine("sqlite:///./cars.db", echo=True)
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    from routes import main

    app.register_blueprint(main)

    return app


from routes import main

if __name__ == "__main__":
    app = create_app()
    app.run(port=6969, debug=True)
