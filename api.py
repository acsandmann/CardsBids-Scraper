from flask import Flask
from flask_cors import CORS
from models import Base
from db import db_session, init_db
from joblib import load

Base.query = db_session.query_property()


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    CORS(app, origins=["http://127.0.0.1:3000", "http://localhost:3000", "https://cb-frontend-kappa.vercel.app"],
        supports_credentials=True)
    init_db(Base)
    model = load("best_model_pipeline.joblib")

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    from routes import main

    app.register_blueprint(main)

    return app

if __name__ == "__main__":
    app = create_app()
    #app.run(host='0.0.0.0', port=6969, debug=False, ssl_context=('/etc/ssl/certificate.crt', '/etc/ssl/private.key'))
    #app.run(host='0.0.0.0', port=6969, debug=True)
    from gevent import pywsgi
    server = pywsgi.WSGIServer(('0.0.0.0', 6969), app, keyfile='/etc/ssl/private.key', certfile='/etc/ssl/certificate.crt')
    server.serve_forever()
