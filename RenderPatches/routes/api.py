"""
API routes for the Neural Chem AI application
"""

import logging
import json
import random
from flask import Blueprint, request, jsonify
from models import Molecule, BindingSite, DockingResult
import services.molecule_service as molecule_service
import uuid

# Create a blueprint for the API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)

# In-memory storage for demonstration
molecules = {}
binding_sites = {}
docking_results = {}

@api_bp.route('/molecules', methods=['GET'])
def get_molecules():
    """Get all molecules"""
    try:
        return jsonify({
            'status': 'success',
            'data': [molecule.to_dict() for molecule in molecules.values()]
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving molecules: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Failed to retrieve molecules: {str(e)}"
        }), 500

@api_bp.route('/molecules/<molecule_id>', methods=['GET'])
def get_molecule(molecule_id):
    """Get a specific molecule by ID"""
    try:
        molecule = molecules.get(molecule_id)
        if not molecule:
            return jsonify({
                'status': 'error',
                'message': f"Molecule with ID {molecule_id} not found"
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': molecule.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving molecule {molecule_id}: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Failed to retrieve molecule: {str(e)}"
        }), 500

@api_bp.route('/molecules', methods=['POST'])
def create_molecule():
    """Create a new molecule"""
    try:
        data = request.json
        
        # Generate a unique ID
        mol_id = str(uuid.uuid4())
        
        # Create the molecule object
        molecule = Molecule(
            mol_id=mol_id,
            smiles=data.get('smiles'),
            name=data.get('name'),
            mol_file=data.get('mol_file')
        )
        
        # Process the molecule (generate SVG, etc.)
        molecule = molecule_service.process_molecule(molecule)
        
        # Store the molecule
        molecules[mol_id] = molecule
        
        return jsonify({
            'status': 'success',
            'data': molecule.to_dict(),
            'message': 'Molecule created successfully'
        }), 201
    except Exception as e:
        logger.error(f"Error creating molecule: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Failed to create molecule: {str(e)}"
        }), 500

@api_bp.route('/binding-sites', methods=['GET'])
def get_binding_sites():
    """Get all binding sites"""
    try:
        return jsonify({
            'status': 'success',
            'data': [site.to_dict() for site in binding_sites.values()]
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving binding sites: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Failed to retrieve binding sites: {str(e)}"
        }), 500

@api_bp.route('/binding-sites/<binding_site_id>', methods=['GET'])
def get_binding_site(binding_site_id):
    """Get a specific binding site by ID"""
    try:
        binding_site = binding_sites.get(binding_site_id)
        if not binding_site:
            return jsonify({
                'status': 'error',
                'message': f"Binding site with ID {binding_site_id} not found"
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': binding_site.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving binding site {binding_site_id}: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Failed to retrieve binding site: {str(e)}"
        }), 500

@api_bp.route('/binding-sites', methods=['POST'])
def create_binding_site():
    """Create a new binding site"""
    try:
        data = request.json
        
        # Generate a unique ID
        site_id = str(uuid.uuid4())
        
        # Create the binding site object
        binding_site = BindingSite(
            site_id=site_id,
            protein_id=data.get('protein_id'),
            name=data.get('name'),
            coordinates=data.get('coordinates')
        )
        
        # Process the binding site
        import services.binding_site_service as binding_site_service
        binding_site = binding_site_service.process_binding_site(binding_site)
        
        # Store the binding site
        binding_sites[site_id] = binding_site
        
        return jsonify({
            'status': 'success',
            'data': binding_site.to_dict(),
            'message': 'Binding site created successfully'
        }), 201
    except Exception as e:
        logger.error(f"Error creating binding site: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Failed to create binding site: {str(e)}"
        }), 500

@api_bp.route('/molecules/<molecule_id>/enrich', methods=['POST'])
def enrich_molecule(molecule_id):
    """Enrich a molecule with ML-based predictions"""
    try:
        molecule = molecules.get(molecule_id)
        if not molecule:
            return jsonify({
                'status': 'error',
                'message': f"Molecule with ID {molecule_id} not found"
            }), 404
        
        # Enrich molecule with ML predictions
        import services.ml_service as ml_service
        molecule = ml_service.enrich_molecule_with_predictions(molecule)
        
        return jsonify({
            'status': 'success',
            'data': molecule.to_dict(),
            'message': 'Molecule enriched with predictions'
        }), 200
    except Exception as e:
        logger.error(f"Error enriching molecule: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Failed to enrich molecule: {str(e)}"
        }), 500

@api_bp.route('/molecules/similarity', methods=['POST'])
def similarity_search():
    """Search for similar molecules"""
    try:
        data = request.json
        molecule_id = data.get('molecule_id')
        
        # Validate inputs
        if not molecule_id:
            return jsonify({
                'status': 'error',
                'message': 'Molecule ID is required'
            }), 400
        
        # Retrieve query molecule
        query_molecule = molecules.get(molecule_id)
        
        if not query_molecule:
            return jsonify({
                'status': 'error',
                'message': 'Query molecule not found'
            }), 404
        
        # Perform similarity search
        import services.ml_service as ml_service
        similar_molecules = ml_service.structure_similarity_search(
            query_molecule, 
            list(molecules.values())
        )
        
        # Limit to top 10 results
        top_results = similar_molecules[:10]
        
        # Format results for return
        results = [{
            'molecule': mol.to_dict(),
            'similarity': round(score, 2)
        } for mol, score in top_results]
        
        return jsonify({
            'status': 'success',
            'data': results,
            'message': 'Similarity search completed'
        }), 200
    except Exception as e:
        logger.error(f"Error in similarity search: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Failed to perform similarity search: {str(e)}"
        }), 500

@api_bp.route('/molecules/<molecule_id>/toxicity', methods=['GET'])
def get_toxicity(molecule_id):
    """Get toxicity prediction for a molecule"""
    try:
        molecule = molecules.get(molecule_id)
        if not molecule:
            return jsonify({
                'status': 'error',
                'message': f"Molecule with ID {molecule_id} not found"
            }), 404
        
        # Get toxicity prediction
        import services.binding_site_service as binding_site_service
        toxicity = binding_site_service.calculate_toxicity(molecule)
        
        return jsonify({
            'status': 'success',
            'data': toxicity,
            'message': 'Toxicity prediction completed'
        }), 200
    except Exception as e:
        logger.error(f"Error predicting toxicity: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Failed to predict toxicity: {str(e)}"
        }), 500

@api_bp.route('/docking/predict', methods=['POST'])
def predict_docking():
    """Predict docking of a molecule to a binding site"""
    try:
        data = request.json
        molecule_id = data.get('molecule_id')
        binding_site_id = data.get('binding_site_id')
        
        # Validate inputs
        if not molecule_id or not binding_site_id:
            return jsonify({
                'status': 'error',
                'message': 'Both molecule_id and binding_site_id are required'
            }), 400
        
        # Retrieve molecule and binding site
        molecule = molecules.get(molecule_id)
        binding_site = binding_sites.get(binding_site_id)
        
        if not molecule or not binding_site:
            return jsonify({
                'status': 'error',
                'message': 'Molecule or binding site not found'
            }), 404
        
        # Predict docking
        import services.binding_site_service as binding_site_service
        import services.ml_service as ml_service
        
        # Get docking result
        docking_result = binding_site_service.predict_docking(molecule, binding_site)
        
        # Add binding affinity prediction
        docking_result.binding_affinity = ml_service.binding_affinity_prediction(molecule, binding_site)
        
        # Generate a unique ID for the result
        result_id = str(uuid.uuid4())
        docking_result.id = result_id
        docking_results[result_id] = docking_result
        
        return jsonify({
            'status': 'success',
            'data': docking_result.to_dict(),
            'message': 'Docking prediction completed'
        }), 200
    except Exception as e:
        logger.error(f"Error predicting docking: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Failed to predict docking: {str(e)}"
        }), 500

@api_bp.route('/docking/results', methods=['GET'])
def get_docking_results():
    """Get all docking results"""
    try:
        return jsonify({
            'status': 'success',
            'data': [result.to_dict() for result in docking_results.values()]
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving docking results: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Failed to retrieve docking results: {str(e)}"
        }), 500

@api_bp.route('/docking/results/<result_id>', methods=['GET'])
def get_docking_result(result_id):
    """Get a specific docking result by ID"""
    try:
        docking_result = docking_results.get(result_id)
        if not docking_result:
            return jsonify({
                'status': 'error',
                'message': f"Docking result with ID {result_id} not found"
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': docking_result.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving docking result {result_id}: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Failed to retrieve docking result: {str(e)}"
        }), 500

@api_bp.route('/docking/improvement-suggestions', methods=['POST'])
def get_binding_improvement_suggestions():
    """Get suggestions for improving binding between molecule and binding site"""
    try:
        data = request.get_json()
        molecule_id = data.get('molecule_id')
        binding_site_id = data.get('binding_site_id')
        
        if not molecule_id or not binding_site_id:
            return jsonify({
                'status': 'error',
                'message': 'Both molecule_id and binding_site_id are required'
            }), 400
        
        # Retrieve molecule and binding site
        molecule = molecules.get(molecule_id)
        binding_site = binding_sites.get(binding_site_id)
        
        if not molecule:
            return jsonify({
                'status': 'error',
                'message': 'Molecule not found'
            }), 404
            
        if not binding_site:
            return jsonify({
                'status': 'error',
                'message': 'Binding site not found'
            }), 404
        
        logger.info(f"Generating improvement suggestions for molecule {molecule_id} and binding site {binding_site_id}")
        
        # Create simulated data as requested by the user
        
        # Additional properties (focused on H-bonds, etc.)
        additional_properties = {
            'h_bond_donors': random.randint(1, 5),
            'h_bond_acceptors': random.randint(2, 8),
            'h_atoms': random.randint(8, 25),
            'logp': round(random.uniform(1.5, 4.5), 2)
        }
        
        # Example binding improvement suggestions
        suggestions = [
            {
                'category': 'Functional Group Modification',
                'description': 'Add hydrogen bond donors on the R1 position to increase binding affinity through interaction with polar residues in the binding pocket.',
                'confidence': round(random.uniform(0.65, 0.95), 2),
                'alternatives': [
                    'Consider adding a hydroxyl group at the para position',
                    'Amide substitution may also improve H-bonding capabilities'
                ]
            },
            {
                'category': 'Hydrophobic Interaction Enhancement',
                'description': 'Introduce alkyl substituents or aromatic rings to strengthen hydrophobic interactions with the non-polar pocket region.',
                'confidence': round(random.uniform(0.55, 0.85), 2),
                'alternatives': [
                    'Consider adding a phenyl group',
                    'Extending the alkyl chain may improve binding'
                ]
            },
            {
                'category': 'Conformational Restriction',
                'description': 'Reduce rotatable bonds by introducing ring structures to limit conformational freedom and improve binding entropy.',
                'confidence': round(random.uniform(0.6, 0.9), 2),
                'alternatives': [
                    'Consider adding a cyclohexyl group',
                    'Adding a piperidine ring might increase specificity'
                ]
            }
        ]
        
        # Example literature references
        literature_examples = [
            {
                'title': 'Structural modifications of benzodiazepines for selective binding',
                'authors': 'Johnson M, Smith A, Zhang Y',
                'journal': 'Journal of Medicinal Chemistry',
                'year': 2022,
                'doi': '10.1021/jmedchem.2022.12345',
                'finding': 'Addition of fluorine substituents at the para position increases binding affinity to GABA receptors by 3-fold.',
                'relevance': round(random.uniform(0.75, 0.95), 2)
            },
            {
                'title': 'H-bond network analysis in kinase inhibitor design',
                'authors': 'Wilson K, Patel R, Garcia J',
                'journal': 'ACS Medicinal Chemistry Letters',
                'year': 2021,
                'doi': '10.1021/acsmedchemlett.2021.56789',
                'finding': 'Incorporating a pyridine ring in place of phenyl creates additional H-bond acceptors, improving potency against ALK kinase.',
                'relevance': round(random.uniform(0.65, 0.85), 2)
            },
            {
                'title': 'Optimizing lipophilicity profiles in NSAID development',
                'authors': 'Brown T, Anderson H, Miller P',
                'journal': 'European Journal of Medicinal Chemistry',
                'year': 2023,
                'doi': '10.1016/j.ejmech.2023.12345',
                'finding': 'Compounds with LogP values between 2.5-4.0 showed optimal balance between COX-2 selectivity and membrane permeability.',
                'relevance': round(random.uniform(0.6, 0.8), 2)
            }
        ]
        
        return jsonify({
            'status': 'success',
            'data': {
                'molecule_id': molecule_id,
                'binding_site_id': binding_site_id,
                'additional_properties': additional_properties,
                'improvement_suggestions': suggestions,
                'literature_examples': literature_examples
            }
        }), 200
    except Exception as e:
        logger.error(f"Error getting binding improvement suggestions: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f"Failed to get improvement suggestions: {str(e)}"
        }), 500
