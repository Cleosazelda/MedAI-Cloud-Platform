import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
import logging
# pyrefly: ignore [missing-import]
from flask import Flask, jsonify
from flask_cors import CORS
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Import and register blueprints here to avoid circular imports if any
    from routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Global error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Resource not found."}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "An internal error occurred."}), 500

    @app.route('/')
    def index():
        return jsonify({
            "name": "MedAI Cloud API",
            "version": "1.0.0",
            "status": "running"
        })

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5001))
    # In production, use Gunicorn instead of Flask's built-in server.
    app.run(host='0.0.0.0', port=port, debug=(os.getenv('FLASK_ENV') == 'development'))
