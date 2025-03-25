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

# Initialize sample data
from routes.api import molecules, binding_sites
from services.sample_data import create_sample_molecules, create_sample_binding_sites

# Only add sample data if we don't have any
if not molecules:
    sample_molecules = create_sample_molecules()
    molecules.update(sample_molecules)
    logger.info(f"Added {len(sample_molecules)} sample molecules")

if not binding_sites:
    sample_binding_sites = create_sample_binding_sites()
    binding_sites.update(sample_binding_sites)
    logger.info(f"Added {len(sample_binding_sites)} sample binding sites")

logger.info("Neural Chem AI application initialized")
