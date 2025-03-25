import os
import logging
from flask import Flask
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "neural-chem-ai-default-key")

# Enable CORS to allow requests from frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure app settings
app.config.from_object('config')

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import and register routes
from routes.api import api_bp
from routes.web import web_bp

app.register_blueprint(api_bp)
app.register_blueprint(web_bp)

logger.info("Neural Chem AI application initialized")
