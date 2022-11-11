from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from multiprocessing import Process
from app.udaconnect.server_utils import run_grpc_server

def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="UdaConnect API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)

    grpc_server_process = Process(target=run_grpc_server)

    @app.route("/grpcstart")
    def grpc_server():

        grpc_server_process.start()
        grpc_server_process.join()
        return jsonify(f"start consumer on {grpc_server_process.pid}")


    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
