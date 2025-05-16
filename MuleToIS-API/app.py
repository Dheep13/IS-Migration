"""
Flask API for the MuleToIS iFlow Generator.
This module provides a REST API for generating iFlows from markdown content.
"""

import os
import sys
import logging
import tempfile
import json
import uuid
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Import the iFlow generator API
from iflow_generator_api import generate_iflow_from_markdown

# Import the SAP BTP integration module
from sap_btp_integration import SapBtpIntegration

# SAP BTP Integration configuration
SAP_BTP_TENANT_URL = os.getenv('SAP_BTP_TENANT_URL')
SAP_BTP_CLIENT_ID = os.getenv('SAP_BTP_CLIENT_ID')
SAP_BTP_CLIENT_SECRET = os.getenv('SAP_BTP_CLIENT_SECRET')
SAP_BTP_OAUTH_URL = os.getenv('SAP_BTP_OAUTH_URL')
SAP_BTP_DEFAULT_PACKAGE = os.getenv('SAP_BTP_DEFAULT_PACKAGE')

# Create the Flask application
app = Flask(__name__)
# Enable CORS for all routes with additional options
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": False}})

# Add a global CORS handler
@app.after_request
def after_request(response):
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.set('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    # Don't set Access-Control-Allow-Credentials since we're not using credentials
    return response

# Get the Claude API key from the .env file
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
if not CLAUDE_API_KEY:
    logger.warning("No Claude API key found in .env file. API will not work without it.")

# In-memory job storage (in a production environment, use a database)
jobs = {}

# Configure Flask app
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['RESULTS_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    response = jsonify({
        'status': 'ok',
        'message': 'MuleToIS API is running',
        'api_key_configured': bool(CLAUDE_API_KEY)
    })
    # Add CORS headers
    response.headers.set('Access-Control-Allow-Origin', 'http://localhost:5173')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.set('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.set('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/api/generate-iflow/<job_id>', methods=['POST', 'OPTIONS'])
@app.route('/api/generate-iflow', methods=['POST', 'OPTIONS'])
def generate_iflow(job_id=None):
    """
    Generate an iFlow from markdown content

    Request body:
    {
        "markdown": "# API Documentation...",
        "iflow_name": "MyIFlow" (optional)
    }

    Or if job_id is provided, it will fetch the markdown from the job.
    """
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.set('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.set('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.set('Access-Control-Allow-Credentials', 'true')
        return response, 200

    try:
        # Check if API key is configured
        if not CLAUDE_API_KEY:
            return jsonify({
                'status': 'error',
                'message': 'Claude API key not configured. Please set CLAUDE_API_KEY in .env file.'
            }), 500

        # If job_id is provided, fetch the markdown from the main API
        if job_id:
            try:
                import requests

                # Get the main API URL from environment variable or use default
                MAIN_API_URL = os.getenv('MAIN_API_URL', 'http://localhost:5000')

                # Fetch the markdown content from the main API
                logger.info(f"Fetching markdown content for job {job_id} from {MAIN_API_URL}")
                response = requests.get(f"{MAIN_API_URL}/api/docs/{job_id}/markdown")

                if response.status_code != 200:
                    logger.error(f"Error fetching markdown for job {job_id}: {response.status_code} {response.text}")
                    return jsonify({
                        'status': 'error',
                        'message': f'Error fetching markdown for job {job_id}: {response.status_code} {response.text}'
                    }), 500

                # Get the markdown content from the response
                markdown_content = response.text
                logger.info(f"Received markdown content length: {len(markdown_content)} characters")

                # Generate a job ID
                iflow_job_id = str(uuid.uuid4())

                # Create job record
                jobs[iflow_job_id] = {
                    'id': iflow_job_id,
                    'original_job_id': job_id,
                    'status': 'queued',
                    'created': str(uuid.uuid1()),
                    'message': 'Job queued. Starting iFlow generation...'
                }

                # Start processing in background
                thread = threading.Thread(
                    target=process_iflow_generation,
                    args=(iflow_job_id, markdown_content, f"IFlow_{job_id[:8]}")
                )
                thread.daemon = True
                thread.start()

                return jsonify({
                    'status': 'queued',
                    'message': 'iFlow generation started',
                    'job_id': iflow_job_id
                }), 202
            except Exception as e:
                logger.error(f"Error fetching markdown for job {job_id}: {str(e)}")
                return jsonify({
                    'status': 'error',
                    'message': f'Error fetching markdown for job {job_id}: {str(e)}'
                }), 500

        # If no job_id, get markdown from request body
        data = request.json
        logger.info(f"Received request data: {data}")

        if not data or 'markdown' not in data:
            logger.error("Missing required parameter: markdown")
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameter: markdown'
            }), 400

        markdown_content = data['markdown']
        logger.info(f"Received markdown content length: {len(markdown_content)} characters")

        iflow_name = data.get('iflow_name')
        logger.info(f"Using iFlow name: {iflow_name}")

        # Generate a job ID
        job_id = str(uuid.uuid4())

        # Create job record
        jobs[job_id] = {
            'id': job_id,
            'status': 'queued',
            'created': str(uuid.uuid1()),
            'message': 'Job queued. Starting iFlow generation...'
        }

        # Start processing in background
        thread = threading.Thread(
            target=process_iflow_generation,
            args=(job_id, markdown_content, iflow_name)
        )
        thread.daemon = True
        thread.start()

        response = jsonify({
            'status': 'queued',
            'message': 'iFlow generation started',
            'job_id': job_id
        })
        # Add CORS headers
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response, 202

    except Exception as e:
        logger.error(f"Error starting iFlow generation: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error starting iFlow generation: {str(e)}'
        }), 500

def process_iflow_generation(job_id, markdown_content, iflow_name=None):
    """
    Process the markdown content to generate an iFlow in a background thread

    Args:
        job_id: Job ID to identify the job
        markdown_content: Markdown content to process
        iflow_name: Name of the iFlow (optional)
    """
    try:
        # Create output directory in the job results folder
        job_result_dir = os.path.join(app.config['RESULTS_FOLDER'], job_id)
        os.makedirs(job_result_dir, exist_ok=True)

        # Update job status
        jobs[job_id].update({
            'status': 'processing',
            'message': 'Initializing iFlow generator...'
        })

        # Update job status
        jobs[job_id].update({
            'status': 'processing',
            'message': 'Analyzing markdown and generating iFlow...'
        })

        # Generate the iFlow
        if iflow_name is None:
            iflow_name = f"GeneratedIFlow_{job_id[:8]}"

        result = generate_iflow_from_markdown(
            markdown_content=markdown_content,
            api_key=CLAUDE_API_KEY,
            output_dir=job_result_dir,
            iflow_name=iflow_name
        )

        if result["status"] == "success":
            # Update job with file paths
            zip_path = result["files"]["zip"]
            relative_zip_path = os.path.relpath(zip_path, os.path.dirname(os.path.abspath(__file__)))

            # Add debug files if they exist
            debug_files = {}
            for debug_file, debug_path in result["files"]["debug"].items():
                relative_debug_path = os.path.relpath(debug_path, os.path.dirname(os.path.abspath(__file__)))
                debug_files[debug_file] = relative_debug_path

            jobs[job_id].update({
                'status': 'completed',
                'message': 'iFlow generation completed successfully!',
                'files': {
                    'zip': relative_zip_path,
                    'debug': debug_files
                },
                'iflow_name': iflow_name
            })
        else:
            jobs[job_id].update({
                'status': 'failed',
                'message': result["message"]
            })

    except Exception as e:
        logger.error(f"Error generating iFlow: {str(e)}")
        jobs[job_id].update({
            'status': 'failed',
            'message': f'Error generating iFlow: {str(e)}'
        })

@app.route('/api/jobs/<job_id>', methods=['GET', 'OPTIONS'])
@app.route('/api/iflow-generation/<job_id>', methods=['GET', 'OPTIONS'])
def get_job_status(job_id):
    """Get the status of a job"""
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.set('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.set('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.set('Access-Control-Allow-Credentials', 'true')
        return response, 200

    if job_id not in jobs:
        # Check if the job has completed and the result file exists
        job_result_dir = os.path.join(app.config['RESULTS_FOLDER'], job_id)
        if os.path.exists(job_result_dir):
            # Look for zip files in the result directory
            zip_files = []
            for root, dirs, files in os.walk(job_result_dir):
                for file in files:
                    if file.endswith('.zip'):
                        rel_path = os.path.relpath(os.path.join(root, file), os.path.dirname(os.path.abspath(__file__)))
                        zip_files.append(rel_path)

            if zip_files:
                # Job has completed and result file exists
                # Create a job record with completed status
                iflow_name = f"GeneratedIFlow_{job_id[:8]}"
                job_info = {
                    'id': job_id,
                    'status': 'completed',
                    'created': str(uuid.uuid1()),
                    'last_updated': str(uuid.uuid1()),
                    'message': 'iFlow generation completed successfully',
                    'files': {
                        'zip': zip_files[0],  # Use the first zip file
                        'debug': {}  # No debug files available
                    },
                    'iflow_name': iflow_name
                }
                # Store the job info for future requests
                jobs[job_id] = job_info

                # Return the job info
                response = jsonify(job_info)
                response.headers.set('Access-Control-Allow-Origin', 'http://localhost:5173')
                response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
                response.headers.set('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
                response.headers.set('Access-Control-Allow-Credentials', 'true')
                return response, 200

        # If we get here, the job doesn't exist
        response = jsonify({'error': 'Job not found'})
        response.headers.set('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.set('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.set('Access-Control-Allow-Credentials', 'true')
        return response, 404

    response = jsonify(jobs[job_id])
    response.headers.set('Access-Control-Allow-Origin', 'http://localhost:5173')
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.set('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.set('Access-Control-Allow-Credentials', 'true')
    return response, 200

@app.route('/api/jobs/<job_id>/download', methods=['GET'])
@app.route('/api/iflow-generation/<job_id>/download', methods=['GET'])
def download_iflow(job_id):
    """Download the generated iFlow ZIP file"""
    # First check if the job is in our jobs dictionary
    if job_id in jobs:
        job = jobs[job_id]

        # Check if job is completed
        if job['status'] != 'completed':
            return jsonify({
                'error': 'iFlow generation not completed',
                'status': job['status']
            }), 400

        # Check if ZIP file exists
        if 'files' not in job or 'zip' not in job['files']:
            return jsonify({'error': 'iFlow ZIP file not available'}), 404

        zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), job['files']['zip'])

        if not os.path.exists(zip_path):
            return jsonify({'error': 'iFlow ZIP file not found on server'}), 404

        return send_file(
            zip_path,
            as_attachment=True,
            download_name=f"{job.get('iflow_name', f'GeneratedIFlow_{job_id[:8]}')}.zip",
            mimetype='application/zip'
        )

    # If the job is not in our jobs dictionary, check if the result file exists directly
    job_result_dir = os.path.join(app.config['RESULTS_FOLDER'], job_id)
    if os.path.exists(job_result_dir):
        # Look for zip files in the result directory
        for root, _, files in os.walk(job_result_dir):
            for file in files:
                if file.endswith('.zip'):
                    zip_path = os.path.join(root, file)
                    if os.path.exists(zip_path):
                        # Found a zip file, return it
                        return send_file(
                            zip_path,
                            as_attachment=True,
                            download_name=f"GeneratedIFlow_{job_id[:8]}.zip",
                            mimetype='application/zip'
                        )

    # If we get here, the job or zip file doesn't exist
    return jsonify({'error': 'iFlow ZIP file not found'}), 404

@app.route('/api/jobs/<job_id>/debug/<file_name>', methods=['GET'])
@app.route('/api/iflow-generation/<job_id>/debug/<file_name>', methods=['GET'])
def download_debug_file(job_id, file_name):
    """Download a debug file"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404

    job = jobs[job_id]

    # Check if job is completed
    if job['status'] != 'completed':
        return jsonify({
            'error': 'iFlow generation not completed',
            'status': job['status']
        }), 400

    # Check if debug file exists
    if ('files' not in job or
        'debug' not in job['files'] or
        file_name not in job['files']['debug']):
        return jsonify({'error': 'Debug file not available'}), 404

    debug_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), job['files']['debug'][file_name])

    if not os.path.exists(debug_path):
        return jsonify({'error': 'Debug file not found on server'}), 404

    return send_file(
        debug_path,
        as_attachment=True,
        download_name=file_name,
        mimetype='text/plain'
    )

@app.route('/api/jobs/<job_id>/deploy', methods=['POST', 'OPTIONS'])
@app.route('/api/iflow-generation/<job_id>/deploy', methods=['POST', 'OPTIONS'])
def deploy_to_sap(job_id):
    """
    Deploy the generated iFlow to SAP Integration Suite

    Request body:
    {
        "package_id": "MyPackage", // Optional, will use default if not provided
        "description": "My iFlow description" // Optional
    }
    """
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.set('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.set('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.set('Access-Control-Allow-Credentials', 'true')
        return response, 200

    try:
        # Check if SAP BTP integration is configured
        if not all([SAP_BTP_TENANT_URL, SAP_BTP_CLIENT_ID, SAP_BTP_CLIENT_SECRET]):
            return jsonify({
                'status': 'error',
                'message': 'SAP BTP integration not configured. Please set SAP_BTP_* environment variables.'
            }), 500

        # Check if job exists
        if job_id not in jobs:
            return jsonify({'error': 'Job not found'}), 404

        job = jobs[job_id]

        # Check if job is completed
        if job['status'] != 'completed':
            return jsonify({
                'error': 'iFlow generation not completed',
                'status': job['status']
            }), 400

        # Check if ZIP file exists
        if 'files' not in job or 'zip' not in job['files']:
            return jsonify({'error': 'iFlow ZIP file not available'}), 404

        zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), job['files']['zip'])

        if not os.path.exists(zip_path):
            return jsonify({'error': 'iFlow ZIP file not found on server'}), 404

        # Get request data
        data = request.json or {}

        # Get package ID from request or use default
        package_id = data.get('package_id') or SAP_BTP_DEFAULT_PACKAGE
        if not package_id:
            return jsonify({
                'status': 'error',
                'message': 'No package ID provided and no default package configured'
            }), 400

        # Get description from request or use default
        description = data.get('description')

        # Get iFlow name from job
        iflow_name = job.get('iflow_name', f"GeneratedIFlow_{job_id[:8]}")

        # Update job status
        jobs[job_id].update({
            'deployment_status': 'deploying',
            'deployment_message': 'Deploying to SAP Integration Suite...'
        })

        # Initialize SAP BTP integration client
        sap_client = SapBtpIntegration(
            tenant_url=SAP_BTP_TENANT_URL,
            client_id=SAP_BTP_CLIENT_ID,
            client_secret=SAP_BTP_CLIENT_SECRET,
            oauth_url=SAP_BTP_OAUTH_URL
        )

        # Deploy the iFlow
        result = sap_client.deploy_integration_flow(
            package_id=package_id,
            iflow_name=iflow_name,
            iflow_zip_path=zip_path,
            description=description
        )

        # Update job status
        jobs[job_id].update({
            'deployment_status': 'completed',
            'deployment_message': 'Deployment completed successfully',
            'deployment_details': result
        })

        return jsonify({
            'status': 'success',
            'message': 'iFlow deployed successfully',
            'details': result
        }), 200

    except Exception as e:
        logger.error(f"Error deploying iFlow: {str(e)}")

        # Update job status
        if job_id in jobs:
            jobs[job_id].update({
                'deployment_status': 'failed',
                'deployment_message': f'Error deploying iFlow: {str(e)}'
            })

        return jsonify({
            'status': 'error',
            'message': f'Error deploying iFlow: {str(e)}'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
