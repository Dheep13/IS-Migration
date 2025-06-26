import os
import sys
import uuid
import json
import zipfile
import shutil

from flask import Flask, request, jsonify, send_file, render_template
from utils.cors_helper import enable_cors
from werkzeug.utils import secure_filename
import threading
import time
from datetime import datetime
import logging

# Set up NLTK data
try:
    import nltk_setup
    print("NLTK setup completed")
except Exception as e:
    print(f"Warning: NLTK setup failed: {str(e)}")

# Run startup checks
try:
    import cf_startup_check
    if cf_startup_check.check_imports():
        print("Startup checks completed successfully!")
    else:
        print("WARNING: Startup checks failed!")
except Exception as e:
    print(f"Error running startup checks: {str(e)}")

# Add GetIflowEquivalent directory to path for imports
getiflow_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "GetIflowEquivalent")
sys.path.append(getiflow_path)
print(f"Added GetIflowEquivalent path: {getiflow_path}")

# Create the Flask application
app = Flask(__name__)
# Apply CORS after creating the app
app = enable_cors(app)

# Initialize database
try:
    from database import init_database, create_tables, test_connection, DatabaseManager, migrate_existing_jobs

    # Initialize database configuration
    if init_database(app):
        logging.info("Database initialized successfully")

        # Test connection
        if test_connection(app):
            logging.info("Database connection verified")

            # Create tables if they don't exist
            create_tables(app)

            # Set up database manager
            db_manager = DatabaseManager()
            use_database = True
            logging.info("Database integration enabled")
        else:
            logging.warning("Database connection failed, falling back to file-based storage")
            use_database = False
    else:
        logging.warning("Database initialization failed, falling back to file-based storage")
        use_database = False

except Exception as e:
    logging.error(f"Database setup failed: {str(e)}")
    use_database = False
    logging.warning("Falling back to file-based storage")

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    # First, try to load environment-specific .env file
    env = os.getenv('FLASK_ENV', 'development')
    env_file = f".env.{env}"
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), env_file)

    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f"Loaded environment variables from: {env_path} ({env} environment)")
    else:
        # Fall back to default .env file
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        if os.path.exists(env_path):
            load_dotenv(env_path)
            print(f"Loaded environment variables from: {env_path} (default)")
        else:
            print("No .env file found at expected locations")

    # Log environment configuration
    print(f"Environment: {env}")
    print(f"API Port: {os.getenv('PORT', '5000')}")
    print(f"iFlow API URL: {os.getenv('IFLOW_API_URL', 'http://localhost:5001')}")

except ImportError:
    print("dotenv package not installed. Environment variables may not be loaded correctly.")

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "final"))

# Import the enhanced documentation generator
try:
    from enhanced_doc_generator import generate_enhanced_documentation
except ImportError:
    print("Enhanced documentation generator not found. Using standard generator.")
    use_enhanced_generator = False
else:
    use_enhanced_generator = True
    print("Using enhanced documentation generator with support for additional file types.")

# Custom patch for LLMDocumentationEnhancer to use Anthropic
class CustomLLMDocumentationEnhancer:
    def __init__(self):
        # Use Anthropic instead of OpenAI
        self.service = os.getenv('LLM_SERVICE', 'anthropic')
        logging.info(f"Using {self.service} for LLM enhancement")
        logging.info(f"ANTHROPIC_API_KEY available: {bool(os.getenv('ANTHROPIC_API_KEY'))}")
        logging.info(f"OPENAI_API_KEY available: {bool(os.getenv('OPENAI_API_KEY'))}")

        try:
            from documentation_enhancer import DocumentationEnhancer
            self.enhancer = DocumentationEnhancer(selected_service=self.service)
            logging.info(f"DocumentationEnhancer initialized with '{self.service}' service.")
        except Exception as e:
            logging.error(f"Error initializing DocumentationEnhancer: {str(e)}")
            logging.error(f"Error type: {type(e).__name__}")
            try:
                # Try to initialize with default settings
                from documentation_enhancer import DocumentationEnhancer
                self.enhancer = DocumentationEnhancer()
                logging.info("DocumentationEnhancer initialized with default settings.")
            except Exception as fallback_error:
                logging.error(f"Failed to initialize DocumentationEnhancer with default settings: {str(fallback_error)}")
                # Create a dummy enhancer that returns the original documentation
                self.enhancer = None
                logging.error("Using dummy enhancer that returns original documentation.")

    def enhance_documentation(self, base_documentation: str) -> str:
        """Enhance documentation using LLM.

        Args:
            base_documentation: Base documentation to enhance

        Returns:
            Enhanced documentation
        """
        logging.info(f"Processing documentation as a single unit (size: {len(base_documentation)} chars)")

        # If enhancer is None, return the original documentation
        if self.enhancer is None:
            logging.error("No enhancer available. Returning original documentation.")
            return base_documentation

        try:
            logging.info(f"Starting LLM enhancement with {self.service} service")

            # Add a timeout to prevent hanging
            import threading
            import time

            # Variable to store the result
            result = {"enhanced_documentation": None, "error": None}

            # Function to run in a separate thread
            def run_enhancement():
                try:
                    result["enhanced_documentation"] = self.enhancer.enhance_documentation(base_documentation)
                except Exception as e:
                    result["error"] = e

            # Create and start the thread
            enhancement_thread = threading.Thread(target=run_enhancement)
            enhancement_thread.daemon = True
            enhancement_thread.start()

            # Wait for the thread to complete with a timeout
            enhancement_thread.join(timeout=600)  # 10 minutes timeout

            # Check if the thread is still running (timeout occurred)
            if enhancement_thread.is_alive():
                logging.error("LLM enhancement timed out after 10 minutes")
                return base_documentation

            # Check if there was an error
            if result["error"]:
                logging.error(f"Error during LLM enhancement: {str(result['error'])}")
                return base_documentation

            # Get the enhanced documentation
            enhanced_documentation = result["enhanced_documentation"]

            # If the result is identical to the input, enhancement likely failed
            if enhanced_documentation and enhanced_documentation != base_documentation:
                logging.info(f"Documentation successfully enhanced with {self.service}.")
                return enhanced_documentation
            else:
                logging.warning(f"LLM enhancement did not produce different results - using original documentation.")
                return base_documentation

        except Exception as e:
            logging.error(f"Error during LLM enhancement: {str(e)}")
            logging.error(f"Error type: {type(e).__name__}")
            return base_documentation

# Import the documentation generators
try:
    from mule_flow_documentation import MuleFlowParser, HTMLGenerator, FlowDocumentationGenerator
    from md_to_html_with_mermaid import convert_markdown_to_html
    # Use our custom enhancer instead of the original
    LLMDocumentationEnhancer = CustomLLMDocumentationEnhancer

    # Import Boomi documentation generator
    from boomi_flow_documentation import BoomiFlowDocumentationGenerator
    boomi_generator_available = True
    print("Boomi documentation generator loaded successfully")
except ImportError as e:
    print(f"Error importing documentation modules: {e}")
    boomi_generator_available = False
    sys.exit(1)

# Configure Flask app
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['RESULTS_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
app.config['JOBS_FILE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jobs.json')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max upload size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'xml', 'zip'}

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

# Function to load jobs from JSON file (fallback)
def load_jobs():
    if os.path.exists(app.config['JOBS_FILE']):
        try:
            with open(app.config['JOBS_FILE'], 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error loading jobs file. Starting with empty jobs dictionary.")
    return {}

# Function to save jobs to JSON file (fallback)
def save_jobs(jobs_dict):
    try:
        with open(app.config['JOBS_FILE'], 'w') as f:
            json.dump(jobs_dict, f, indent=2)
    except Exception as e:
        print(f"Error saving jobs file: {str(e)}")

# Initialize job storage
if use_database:
    # Migrate existing jobs from file to database
    try:
        migrate_existing_jobs(app, app.config['JOBS_FILE'])
    except Exception as e:
        logging.error(f"Failed to migrate existing jobs: {str(e)}")

    # Use database for job storage
    jobs = {}  # Keep empty dict for compatibility
else:
    # Fall back to file-based storage
    jobs = load_jobs()

# Save the job state
def update_job(job_id, updates):
    """Update a job's data and save to persistent storage"""
    if use_database:
        try:
            db_manager.update_job(job_id, **updates)
        except Exception as e:
            logging.error(f"Failed to update job {job_id} in database: {str(e)}")
            # Fall back to file storage
            if job_id in jobs:
                jobs[job_id].update(updates)
                jobs[job_id]['last_updated'] = datetime.now().isoformat()
                save_jobs(jobs)
    else:
        if job_id in jobs:
            jobs[job_id].update(updates)
            jobs[job_id]['last_updated'] = datetime.now().isoformat()
            save_jobs(jobs)

def get_job(job_id):
    """Get a job from storage"""
    if use_database:
        try:
            job = db_manager.get_job(job_id)
            return job.to_dict() if job else None
        except Exception as e:
            logging.error(f"Failed to get job {job_id} from database: {str(e)}")
            # Fall back to file storage
            return jobs.get(job_id)
    else:
        return jobs.get(job_id)

def create_job(job_id, filename, enhance_with_llm=False, platform='mulesoft'):
    """Create a new job in storage"""
    if use_database:
        try:
            job = db_manager.create_job(job_id, filename, enhance_with_llm, platform)
            return job.to_dict()
        except Exception as e:
            logging.error(f"Failed to create job {job_id} in database: {str(e)}")
            # Fall back to file storage
            job_data = {
                'id': job_id,
                'filename': filename,
                'status': 'pending',
                'timestamp': datetime.now().isoformat(),
                'enhance': enhance_with_llm,
                'platform': platform
            }
            jobs[job_id] = job_data
            save_jobs(jobs)
            return job_data
    else:
        job_data = {
            'id': job_id,
            'filename': filename,
            'status': 'pending',
            'timestamp': datetime.now().isoformat(),
            'enhance': enhance_with_llm,
            'platform': platform
        }
        jobs[job_id] = job_data
        save_jobs(jobs)
        return job_data

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_zip(zip_path, extract_to):
    """Extract a ZIP file to the specified directory"""
    try:
        logging.info(f"Extracting ZIP file from {zip_path} to {extract_to}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Create the extraction directory
            os.makedirs(extract_to, exist_ok=True)
            logging.info(f"Created extraction directory: {extract_to}")

            # Get file count for logging
            file_count = len(zip_ref.namelist())
            logging.info(f"ZIP contains {file_count} files")

            # Extract all files
            zip_ref.extractall(extract_to)
            logging.info(f"Successfully extracted all {file_count} files")

            return True
    except Exception as e:
        logging.error(f"Error extracting ZIP file: {str(e)}")
        return False

def find_mule_directory(base_dir):
    """Find the MuleSoft 'src/main/mule' directory in the extracted files"""
    # Check for standard MuleSoft project structure
    mule_dir = None
    resources_dir = None

    logging.info(f"Searching for MuleSoft project structure in: {base_dir}")

    # First pass: Look for the standard MuleSoft project structure
    for root, dirs, files in os.walk(base_dir):
        root_basename = os.path.basename(root)
        parent_dir = os.path.dirname(root)
        grandparent_dir = os.path.dirname(parent_dir)

        # Look for 'mule' directory under 'src/main'
        if root_basename == 'mule' and 'main' in os.path.basename(parent_dir) and 'src' in os.path.basename(grandparent_dir):
            mule_dir = root
            logging.info(f"Found 'mule' directory at: {mule_dir}")

        # Look for 'resources' directory under 'src/main'
        if root_basename == 'resources' and 'main' in os.path.basename(parent_dir) and 'src' in os.path.basename(grandparent_dir):
            resources_dir = root
            logging.info(f"Found 'resources' directory at: {resources_dir}")

        # If we found both, we can stop searching
        if mule_dir and resources_dir:
            break

    # If we found either the mule or resources directory in the standard structure,
    # we'll create a temporary directory to combine their contents
    if mule_dir or resources_dir:
        # Create a temporary directory to combine contents
        combined_dir = os.path.join(base_dir, "combined_mule_resources")
        os.makedirs(combined_dir, exist_ok=True)
        logging.info(f"Created combined directory at: {combined_dir}")

        # Copy contents from mule directory if it exists
        if mule_dir:
            logging.info(f"Found MuleSoft 'mule' directory: {mule_dir}")
            for item in os.listdir(mule_dir):
                source = os.path.join(mule_dir, item)
                dest = os.path.join(combined_dir, item)
                if os.path.isdir(source):
                    shutil.copytree(source, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(source, dest)

        # Copy contents from resources directory if it exists
        if resources_dir:
            logging.info(f"Found MuleSoft 'resources' directory: {resources_dir}")
            for item in os.listdir(resources_dir):
                source = os.path.join(resources_dir, item)
                dest = os.path.join(combined_dir, item)
                if os.path.isdir(source):
                    shutil.copytree(source, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(source, dest)

        logging.info(f"Returning combined directory: {combined_dir}")
        return combined_dir

    # If not found, look for any directory with XML files that could be MuleSoft flows
    logging.info("Standard MuleSoft structure not found. Looking for directories with XML files...")
    xml_dirs = set()
    for root, _, files in os.walk(base_dir):
        if any(f.lower().endswith('.xml') for f in files):
            xml_dirs.add(root)

    logging.info(f"Found {len(xml_dirs)} directories containing XML files")

    # If multiple directories have XML files, prioritize those with MuleSoft-related names
    for xml_dir in xml_dirs:
        dir_name = os.path.basename(xml_dir).lower()
        if any(keyword in dir_name for keyword in ['mule', 'flow', 'api']):
            logging.info(f"Selected directory with MuleSoft-related name: {xml_dir}")
            return xml_dir

    # If we still don't have a match, return the first directory with XML files
    if xml_dirs:
        selected_dir = next(iter(xml_dirs))
        logging.info(f"Selecting first directory with XML files: {selected_dir}")
        return selected_dir
    else:
        logging.warning(f"No directories with XML files found. Using base directory: {base_dir}")
        return base_dir

def process_documentation(job_id, input_dir, enhance=False, platform='mulesoft'):
    """Process documentation generation in a background thread"""
    try:
        # Log the processing start
        logging.info(f"Job {job_id}: process_documentation called with enhance={enhance}, platform={platform}")
        logging.info(f"Job {job_id}: Using platform: {platform}")

        # Update job status
        update_job(job_id, {'status': 'processing', 'platform': platform})

        # Route to appropriate processor based on platform
        if platform == 'boomi':
            logging.info(f"Job {job_id}: Routing to Boomi processor with enhance={enhance}")
            return process_boomi_documentation(job_id, input_dir, enhance)
        else:
            logging.info(f"Job {job_id}: Routing to MuleSoft processor with enhance={enhance}")
            return process_mulesoft_documentation(job_id, input_dir, enhance)

    except Exception as e:
        logging.error(f"Job {job_id}: CRITICAL ERROR in process_documentation: {str(e)}")
        logging.error(f"Job {job_id}: Exception type: {type(e).__name__}")
        import traceback
        logging.error(f"Job {job_id}: Traceback: {traceback.format_exc()}")
        update_job(job_id, {
            'status': 'failed',
            'error': str(e),
            'processing_step': 'error',
            'processing_message': f'Processing failed: {str(e)}'
        })

def generate_boomi_iflow_metadata(job_id, documentation, processing_results):
    """Generate iFlow metadata JSON files from Boomi documentation"""
    try:
        import requests
        import json

        # BoomiToIS-API endpoint (use environment variable or fallback to localhost)
        boomi_api_url = os.getenv('BOOMI_API_URL', 'http://localhost:5003')

        # Prepare the request data
        request_data = {
            "markdown": documentation,
            "iflow_name": f"BoomiFlow_{job_id[:8]}",
            "job_id": job_id
        }

        # Call the BoomiToIS-API to generate iFlow metadata
        response = requests.post(
            f"{boomi_api_url}/api/generate-iflow/{job_id}",
            json=request_data,
            timeout=30
        )

        if response.status_code == 202:
            # Successfully queued for processing
            result = response.json()
            logging.info(f"Job {job_id}: Boomi iFlow metadata generation queued with job ID: {result.get('job_id')}")
            return True
        else:
            logging.error(f"Job {job_id}: Failed to queue Boomi iFlow metadata generation: {response.text}")
            return False

    except Exception as e:
        logging.error(f"Job {job_id}: Error calling BoomiToIS-API: {str(e)}")
        return False

def process_boomi_documentation(job_id, input_dir, enhance=False):
    """Process Dell Boomi documentation generation"""
    try:
        # Create job results directory
        job_result_dir = os.path.join(app.config['RESULTS_FOLDER'], job_id)
        os.makedirs(job_result_dir, exist_ok=True)

        # Log file information before processing
        logging.info(f"Job {job_id}: Analyzing Boomi files in: {input_dir}")

        # Update job status
        update_job(job_id, {
            'processing_step': 'file_analysis',
            'processing_message': 'Analyzing Dell Boomi files...'
        })

        # Initialize Boomi documentation generator
        if not boomi_generator_available:
            raise Exception("Boomi documentation generator not available")

        boomi_generator = BoomiFlowDocumentationGenerator()

        # Process Boomi directory
        processing_results = boomi_generator.process_directory(input_dir)

        # Update job with file info
        update_job(job_id, {
            'file_info': {
                'total_files': processing_results['total_files'],
                'processed_files': processing_results['processed_files'],
                'processes': len(processing_results['processes']),
                'maps': len(processing_results['maps']),
                'connectors': len(processing_results['connectors']),
                'errors': len(processing_results['errors'])
            },
            'processing_step': 'documentation_generation',
            'processing_message': 'Generating Dell Boomi documentation...'
        })

        # Generate base documentation
        documentation = boomi_generator.generate_documentation(processing_results)

        # Enhance documentation with LLM if requested
        if enhance:
            update_job(job_id, {
                'processing_step': 'llm_enhancing',
                'processing_message': 'Base Boomi documentation generated, starting AI enhancement (this may take 1-2 minutes)...'
            })

            try:
                # Initialize LLM enhancer
                llm_enhancer = LLMDocumentationEnhancer()

                # Use a timeout to prevent indefinite hanging
                import threading

                # Function to be run in thread with timeout
                def enhance_with_timeout():
                    nonlocal documentation
                    try:
                        enhanced_content = llm_enhancer.enhance_documentation(documentation)
                        if enhanced_content:
                            documentation = enhanced_content
                            return True
                        else:
                            logging.warning(f"Job {job_id}: LLM enhancement returned empty content")
                            return False
                    except Exception as e:
                        logging.error(f"Job {job_id}: Error in Boomi enhancement thread: {str(e)}")
                        return False

                # Create and start the enhancement thread
                enhancement_thread = threading.Thread(target=enhance_with_timeout)
                enhancement_thread.daemon = True
                enhancement_thread.start()

                # Wait for the thread with timeout (10 minutes)
                enhancement_thread.join(timeout=600)  # 10 minutes timeout

                # Check if thread is still alive (timeout occurred)
                if enhancement_thread.is_alive():
                    logging.error("Boomi LLM enhancement timed out after 10 minutes")
                    update_job(job_id, {
                        'processing_step': 'llm_timeout',
                        'processing_message': 'AI enhancement timed out. Using base Boomi documentation instead.'
                    })
                    # Thread will continue running but we proceed with base documentation
                else:
                    update_job(job_id, {
                        'processing_step': 'llm_complete',
                        'processing_message': 'AI enhancement complete, saving final Boomi documentation...'
                    })

            except Exception as llm_error:
                logging.error(f"Boomi LLM enhancement failed: {str(llm_error)}")
                update_job(job_id, {
                    'processing_step': 'llm_failed',
                    'processing_message': f'AI enhancement failed: {str(llm_error)}. Using base Boomi documentation instead.'
                })
                # Continue with base documentation

        # Save documentation
        doc_file = os.path.join(job_result_dir, 'boomi_documentation.md')
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(documentation)

        # Convert to HTML (pass file path, not content)
        html_file = os.path.join(job_result_dir, 'boomi_documentation.html')
        convert_markdown_to_html(doc_file, html_file)

        # Generate iFlow intermediate JSON files if enhancement was used
        if enhance:
            try:
                logging.info(f"Job {job_id}: Starting Boomi iFlow metadata generation...")
                update_job(job_id, {
                    'processing_step': 'iflow_metadata_generation',
                    'processing_message': 'Generating iFlow metadata from Boomi documentation...'
                })

                # Call the Boomi iFlow generator to create intermediate JSON files
                generate_boomi_iflow_metadata(job_id, documentation, processing_results)

                logging.info(f"Job {job_id}: Boomi iFlow metadata generation completed")
            except Exception as e:
                logging.error(f"Job {job_id}: Error generating iFlow metadata: {str(e)}")
                # Don't fail the entire job if iFlow metadata generation fails
                pass

        # Update job completion
        enhancement_status = "with AI enhancement" if enhance else "without AI enhancement"
        update_job(job_id, {
            'status': 'completed',
            'processing_step': 'completed',
            'processing_message': f'Dell Boomi documentation generation completed successfully {enhancement_status}',
            'files': {
                'markdown': os.path.join('results', job_id, 'boomi_documentation.md'),
                'html': os.path.join('results', job_id, 'boomi_documentation.html')
            },
            'parsed_details': processing_results
        })

        logging.info(f"Job {job_id}: Dell Boomi documentation generation completed successfully")

    except Exception as e:
        logging.error(f"Error in process_boomi_documentation for job {job_id}: {str(e)}")
        update_job(job_id, {
            'status': 'failed',
            'error': str(e),
            'processing_step': 'error',
            'processing_message': f'Dell Boomi processing failed: {str(e)}'
        })

def process_mulesoft_documentation(job_id, input_dir, enhance=False):
    """Process MuleSoft documentation generation (original functionality)"""
    try:
        # Create job results directory
        job_result_dir = os.path.join(app.config['RESULTS_FOLDER'], job_id)
        os.makedirs(job_result_dir, exist_ok=True)

        # Log file information before processing
        logging.info(f"Job {job_id}: Analyzing MuleSoft files in: {input_dir}")
        file_count = {"xml": 0, "properties": 0, "json": 0, "yaml": 0, "raml": 0, "dwl": 0, "other": 0}
        all_files = []

        for root, _, files in os.walk(input_dir):
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)

                if file.endswith('.xml'):
                    file_count["xml"] += 1
                elif file.endswith('.properties'):
                    file_count["properties"] += 1
                elif file.endswith('.json'):
                    file_count["json"] += 1
                elif file.endswith(('.yaml', '.yml')):
                    file_count["yaml"] += 1
                elif file.endswith('.raml'):
                    file_count["raml"] += 1
                elif file.endswith('.dwl'):
                    file_count["dwl"] += 1
                else:
                    file_count["other"] += 1

        logging.info(f"Job {job_id}: Found {len(all_files)} files: "
                     f"{file_count['xml']} XML, {file_count['properties']} properties, "
                     f"{file_count['json']} JSON, {file_count['yaml']} YAML, "
                     f"{file_count['raml']} RAML, {file_count['dwl']} DWL, "
                     f"{file_count['other']} other files")

        # Add file info to job status for UI display
        update_job(job_id, {
            'file_info': {
                'total_files': len(all_files),
                'xml_files': file_count['xml'],
                'properties_files': file_count['properties'],
                'json_files': file_count['json'],
                'yaml_files': file_count['yaml'],
                'raml_files': file_count['raml'],
                'dwl_files': file_count['dwl'],
                'other_files': file_count['other']
            },
            'processing_step': 'file_analysis',
            'processing_message': 'File analysis completed, starting MuleSoft parsing...'
        })

        # Initialize components for standard approach
        flow_parser = MuleFlowParser()
        html_gen = HTMLGenerator()
        doc_gen = FlowDocumentationGenerator()
        llm_enhancer = LLMDocumentationEnhancer()

        # Check if we should use the enhanced generator
        use_enhanced = use_enhanced_generator and (
            file_count['dwl'] > 0 or file_count['yaml'] > 0 or
            file_count['raml'] > 0 or file_count['properties'] > 0 or
            file_count['json'] > 0
        )

        # Generate documentation
        try:
            # Parse MuleSoft files (required for both approaches)
            logging.info(f"Job {job_id}: Starting MuleSoft file parsing...")
            parsed_data = flow_parser.parse_mule_files(input_dir)

            # Log parsing results
            logging.info(f"Job {job_id}: Parsing complete: Found {len(parsed_data['flows'])} flows, {len(parsed_data['subflows'])} subflows, {len(parsed_data['configs'])} configs, {len(parsed_data['error_handlers'])} error handlers")

            # Add detailed parsing information for terminal output
            if parsed_data['flows']:
                logging.info(f"Job {job_id}: FLOWS FOUND:")
                for flow_name in parsed_data['flows'].keys():
                    logging.info(f"Job {job_id}:   - {flow_name}")

            if parsed_data['subflows']:
                logging.info(f"Job {job_id}: SUBFLOWS FOUND:")
                for subflow_name in parsed_data['subflows'].keys():
                    logging.info(f"Job {job_id}:   - {subflow_name}")

            if parsed_data['configs']:
                logging.info(f"Job {job_id}: CONFIGS FOUND:")
                for config_name in parsed_data['configs'].keys():
                    logging.info(f"Job {job_id}:   - {config_name}")

            if parsed_data['error_handlers']:
                logging.info(f"Job {job_id}: ERROR HANDLERS FOUND:")
                for handler_name in parsed_data['error_handlers'].keys():
                    logging.info(f"Job {job_id}:   - {handler_name}")

            # Add parsing details to job status
            update_job(job_id, {
                'parsed_details': {
                    'flows': len(parsed_data['flows']),
                    'subflows': len(parsed_data['subflows']),
                    'configs': len(parsed_data['configs']),
                    'error_handlers': len(parsed_data['error_handlers'])
                },
                'processing_step': 'mule_parsing',
                'processing_message': 'MuleSoft parsing complete, generating documentation...'
            })

            if not parsed_data['flows'] and not parsed_data['configs'] and not parsed_data['error_handlers']:
                update_job(job_id, {
                    'status': 'failed',
                    'error': "No valid MuleSoft components found in the uploaded files"
                })
                return

            # Generate HTML visualization (same for both approaches)
            html_content = html_gen.generate_html(parsed_data)
            html_file = os.path.join(job_result_dir, "flow_visualization.html")
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_content)

            update_job(job_id, {
                'processing_step': 'visualization',
                'processing_message': 'Flow visualization complete, generating base documentation...'
            })

            # Generate base documentation (either standard or enhanced)
            if use_enhanced:
                logging.info(f"Job {job_id}: Using enhanced documentation generator to include additional file types")
                update_job(job_id, {
                    'processing_message': 'Using enhanced documentation generator to include additional file types'
                })
                doc_content = generate_enhanced_documentation(input_dir, include_additional_files=True)
            else:
                doc_content = doc_gen.generate_documentation(parsed_data)

            # Enhance documentation with LLM if requested
            if enhance:
                update_job(job_id, {
                    'processing_step': 'llm_enhancing',
                    'processing_message': 'Base documentation generated, starting AI enhancement (this may take 1-2 minutes)...'
                })

                try:
                    # Use a timeout to prevent indefinite hanging
                    import threading
                    import time

                    # Function to be run in thread with timeout
                    def enhance_with_timeout():
                        nonlocal doc_content
                        try:
                            enhanced_content = llm_enhancer.enhance_documentation(doc_content)
                            if enhanced_content:
                                doc_content = enhanced_content
                                return True
                            return False
                        except Exception as e:
                            logging.error(f"Error in enhancement thread: {str(e)}")
                            return False

                    # Create and start the enhancement thread
                    enhancement_thread = threading.Thread(target=enhance_with_timeout)
                    enhancement_thread.daemon = True
                    enhancement_thread.start()

                    # Wait for the thread with timeout (10 minutes)
                    enhancement_thread.join(timeout=600)  # 10 minutes timeout

                    # Check if thread is still alive (timeout occurred)
                    if enhancement_thread.is_alive():
                        logging.error("LLM enhancement timed out after 10 minutes")
                        update_job(job_id, {
                            'processing_step': 'llm_timeout',
                            'processing_message': 'AI enhancement timed out. Using base documentation instead.'
                        })
                        # Thread will continue running but we proceed with base documentation
                    else:
                        update_job(job_id, {
                            'processing_step': 'llm_complete',
                            'processing_message': 'AI enhancement complete, saving final documentation...'
                        })

                except Exception as llm_error:
                    logging.error(f"LLM enhancement failed: {str(llm_error)}")
                    update_job(job_id, {
                        'processing_step': 'llm_failed',
                        'processing_message': f'AI enhancement failed: {str(llm_error)}. Using base documentation instead.'
                    })
                    # Continue with base documentation

            # Save markdown documentation
            md_file = os.path.join(job_result_dir, "flow_documentation.md")
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(doc_content)

            # Convert markdown to HTML with Mermaid diagrams
            html_output = os.path.join(job_result_dir, "flow_documentation_with_mermaid.html")
            convert_markdown_to_html(md_file, html_output)

            # Update job with file paths
            update_job(job_id, {
                'files': {
                    'markdown': os.path.join('results', job_id, "flow_documentation.md"),
                    'html': os.path.join('results', job_id, "flow_documentation_with_mermaid.html"),
                    'visualization': os.path.join('results', job_id, "flow_visualization.html")
                },
                'status': 'completed',
                'processing_step': 'completed',
                'processing_message': 'Documentation generation completed successfully!'
            })

        except Exception as e:
            logging.error(f"Error generating documentation: {str(e)}")
            update_job(job_id, {
                'status': 'failed',
                'error': str(e),
                'processing_step': 'failed',
                'processing_message': f'Error generating documentation: {str(e)}'
            })

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        update_job(job_id, {
            'status': 'failed',
            'error': str(e),
            'processing_step': 'failed',
            'processing_message': f'Unexpected error: {str(e)}'
        })

@app.route('/api/generate-docs', methods=['POST'])
def generate_docs():
    # Check if files were uploaded
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400

    files = request.files.getlist('files[]')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400

    # Get platform selection (default to mulesoft for backward compatibility)
    platform = request.form.get('platform', 'mulesoft').lower()
    if platform not in ['mulesoft', 'boomi']:
        return jsonify({'error': 'Invalid platform. Must be "mulesoft" or "boomi"'}), 400

    # Force enhancement to be always on, regardless of the form parameter
    enhance = True
    logging.info(f"LLM Enhancement is ENABLED for platform: {platform}")

    try:
        # Generate a unique job ID
        job_id = str(uuid.uuid4())

        # Create job folder
        job_folder = os.path.join(app.config['UPLOAD_FOLDER'], job_id)
        os.makedirs(job_folder, exist_ok=True)

        # Create a directory for extracted files if needed
        extracted_dir = os.path.join(job_folder, "extracted")

        # Flag to track if we have processed a ZIP file
        zip_processed = False
        xml_files_found = False
        mule_dir = None

        # Save uploaded files
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(job_folder, filename)
                file.save(file_path)
                logging.info(f"Job {job_id}: Saved uploaded file: {filename}")

                # If it's a ZIP file, extract it
                if filename.lower().endswith('.zip'):
                    logging.info(f"Job {job_id}: Extracting ZIP file: {filename}")
                    zip_processed = True
                    extraction_successful = extract_zip(file_path, extracted_dir)

                    if not extraction_successful:
                        return jsonify({'error': 'Failed to extract ZIP file'}), 400

                    if platform == 'mulesoft':
                        # Find the MuleSoft directory in the extracted files
                        mule_dir = find_mule_directory(extracted_dir)
                        logging.info(f"Job {job_id}: MuleSoft directory found: {mule_dir}")

                        # Check if the MuleSoft directory contains any XML files
                        for root, _, files in os.walk(mule_dir):
                            if any(f.lower().endswith('.xml') for f in files):
                                xml_files_found = True
                                break
                    else:
                        # For Boomi, use extracted directory directly and check for XML files
                        mule_dir = extracted_dir
                        logging.info(f"Job {job_id}: Using extracted directory for Boomi: {mule_dir}")

                        # Check if the directory contains any XML files
                        for root, _, files in os.walk(mule_dir):
                            if any(f.lower().endswith('.xml') for f in files):
                                xml_files_found = True
                                break
                elif filename.lower().endswith('.xml'):
                    xml_files_found = True
                    logging.info(f"Job {job_id}: XML file found: {filename}")

        # Check if we found any XML files
        if zip_processed and not xml_files_found:
            # Clean up the job folder
            shutil.rmtree(job_folder, ignore_errors=True)
            platform_name = platform.title()
            return jsonify({'error': f'No {platform_name} XML files found in the ZIP archive'}), 400
        elif not zip_processed and not xml_files_found:
            # Clean up the job folder
            shutil.rmtree(job_folder, ignore_errors=True)
            platform_name = platform.title()
            return jsonify({'error': f'No valid {platform_name} XML files uploaded'}), 400

        # Determine the directory to process
        process_dir = mule_dir if zip_processed and mule_dir else (extracted_dir if zip_processed else job_folder)

        # Create job record
        job_data = {
            'id': job_id,
            'status': 'queued',
            'created': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'enhance': enhance,
            'platform': platform,
            'input_directory': process_dir,
            'zip_file': zip_processed
        }

        jobs[job_id] = job_data
        save_jobs(jobs)  # Save job data to file
        logging.info(f"Job {job_id}: Created new {platform} job, starting documentation processing")

        # Start processing in background with platform information
        logging.info(f"Job {job_id}: Starting background processing with enhance={enhance}, platform={platform}")

        # Use threading for both platforms to ensure proper UI flow
        thread = threading.Thread(target=process_documentation, args=(job_id, process_dir, enhance, platform))
        thread.daemon = True
        thread.start()
        logging.info(f"Job {job_id}: Background thread started successfully")

        return jsonify({
            'job_id': job_id,
            'status': 'queued',
            'platform': platform,
            'message': f'{platform.title()} documentation generation started'
        }), 202
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404

    job = jobs[job_id]
    return jsonify(job), 200

@app.route('/api/jobs', methods=['GET'])
def list_jobs():
    # Return a list of all jobs (limited info)
    job_list = []
    for job_id, job_data in jobs.items():
        job_list.append({
            'id': job_id,
            'status': job_data['status'],
            'created': job_data['created'],
            'last_updated': job_data['last_updated']
        })

    return jsonify(job_list), 200

@app.route('/api/docs/<job_id>/<file_type>', methods=['GET'])
def get_documentation(job_id, file_type):
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404

    job = jobs[job_id]

    if job['status'] != 'completed':
        return jsonify({'error': 'Documentation not ready', 'status': job['status']}), 404

    if 'files' not in job or file_type not in job['files']:
        return jsonify({'error': 'Requested file not available'}), 404

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), job['files'][file_type])

    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found on server'}), 404

    return send_file(file_path)

@app.route('/api/iflow-match/<job_id>', methods=['GET'])
def get_iflow_match_status(job_id):
    """Get the status of the iFlow match processing"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404

    job = jobs[job_id]

    # Check if iFlow match has been processed
    if 'iflow_match_status' not in job:
        return jsonify({
            'status': 'not_started',
            'message': 'SAP Integration Suite equivalent search has not been started'
        })

    # Return the iFlow match status
    return jsonify({
        'status': job.get('iflow_match_status', 'unknown'),
        'message': job.get('iflow_match_message', ''),
        'result': job.get('iflow_match_result', {}),
        'files': job.get('iflow_match_files', {})
    })

@app.route('/api/iflow-match/<job_id>/<file_type>', methods=['GET'])
def get_iflow_match_file(job_id, file_type):
    """Get a file from the iFlow match results"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404

    job = jobs[job_id]

    # Check if iFlow match has been processed
    if 'iflow_match_status' not in job or job['iflow_match_status'] != 'completed':
        return jsonify({
            'error': 'SAP Integration Suite equivalent search not completed',
            'status': job.get('iflow_match_status', 'not_started')
        }), 404

    # Check if the requested file exists
    if 'iflow_match_files' not in job or file_type not in job['iflow_match_files']:
        return jsonify({'error': 'Requested file not available'}), 404

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), job['iflow_match_files'][file_type])

    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found on server'}), 404

    return send_file(file_path)

@app.route('/api/iflow-match/<job_id>/charts/<chart_name>', methods=['GET'])
def get_iflow_match_chart(job_id, chart_name):
    """Get a chart from the iFlow match results"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404

    job = jobs[job_id]

    # Check if iFlow match has been processed
    if 'iflow_match_status' not in job or job['iflow_match_status'] != 'completed':
        return jsonify({
            'error': 'SAP Integration Suite equivalent search not completed',
            'status': job.get('iflow_match_status', 'not_started')
        }), 404

    # Check if the iFlow match files exist
    if 'iflow_match_files' not in job or 'report' not in job['iflow_match_files']:
        return jsonify({'error': 'iFlow match files not available'}), 404

    # Construct the path to the charts directory
    report_path = job['iflow_match_files']['report']
    report_dir = os.path.dirname(os.path.join(os.path.dirname(os.path.abspath(__file__)), report_path))
    charts_dir = os.path.join(report_dir, 'charts')
    chart_path = os.path.join(charts_dir, chart_name)

    if not os.path.exists(chart_path):
        return jsonify({'error': f'Chart {chart_name} not found'}), 404

    return send_file(chart_path)

# New endpoint for generating similarity report
@app.route('/api/generate-similarity-report/<job_id>', methods=['POST'])
def generate_similarity_report(job_id):
    """
    Generate an SAP Integration Suite iFlow similarity report based on the already generated documentation
    """
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404

    job = jobs[job_id]

    if job['status'] != 'completed':
        return jsonify({'error': 'Documentation not ready, cannot generate similarity report', 'status': job['status']}), 404

    if 'files' not in job or 'markdown' not in job['files']:
        return jsonify({'error': 'Markdown documentation not available'}), 404

    md_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), job['files']['markdown'])

    if not os.path.exists(md_file_path):
        return jsonify({'error': 'Markdown file not found on server'}), 404

    try:
        # Path to the GetIflowEquivalent script
        iflow_equiv_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'GetIflowEquivalent')

        # Create a directory for the similarity report if it doesn't exist
        report_dir = os.path.join(app.config['RESULTS_FOLDER'], job_id, 'similarity_report')
        os.makedirs(report_dir, exist_ok=True)

        # Output file path for the similarity report
        report_file = os.path.join(report_dir, 'iflow_similarity_report.html')

        # Call the GetIflowEquivalent functionality (implement the specific call based on the module's interface)
        # This is a placeholder - replace with actual implementation
        from subprocess import run, PIPE

        # Run the similarity report generator script
        result = run([
            'python',
            os.path.join(iflow_equiv_dir, 'generate_report.py'),
            '--input', md_file_path,
            '--output', report_file
        ], stdout=PIPE, stderr=PIPE, text=True)

        if result.returncode != 0:
            logging.error(f"Error generating similarity report: {result.stderr}")
            return jsonify({'error': f'Failed to generate similarity report: {result.stderr}'}), 500

        # Update job with similarity report file path
        relative_report_path = os.path.join('results', job_id, 'similarity_report', 'iflow_similarity_report.html')
        update_job(job_id, {
            'files': {
                **job['files'],
                'similarity_report': relative_report_path
            }
        })

        return jsonify({
            'status': 'success',
            'message': 'Similarity report generated successfully',
            'report_path': f'/api/docs/{job_id}/similarity_report'
        }), 200

    except Exception as e:
        logging.error(f"Error generating similarity report: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return render_template('upload.html')

@app.route('/api_docs', methods=['GET'])
def api_docs():
    return render_template('api_docs.html')

# Add a health endpoint for API connectivity testing
@app.route('/api/health', methods=['GET', 'HEAD'])
def health_check():
    """Health check endpoint for frontend to test API connectivity"""
    return jsonify({'status': 'ok', 'message': 'API is available'})

@app.route('/api/generate-iflow-match/<job_id>', methods=['POST'])
def generate_iflow_match(job_id):
    """
    Process the markdown file with GetIflowEquivalent to find SAP Integration Suite equivalents

    Args:
        job_id: Job ID to identify which documentation to process
    """
    try:
        # Check if job exists
        if job_id not in jobs:
            return jsonify({'error': 'Job not found'}), 404

        # Check if job is completed
        job = jobs[job_id]
        if job['status'] != 'completed':
            return jsonify({'error': 'Documentation not ready', 'status': job['status']}), 400

        # Check if markdown file exists
        if 'files' not in job or 'markdown' not in job['files']:
            return jsonify({'error': 'Markdown file not available'}), 404

        # Get the markdown file path
        markdown_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), job['files']['markdown'])

        if not os.path.exists(markdown_file_path):
            return jsonify({'error': 'Markdown file not found on server'}), 404

        # Update job status
        update_job(job_id, {
            'iflow_match_status': 'processing',
            'iflow_match_message': 'Processing markdown file to find SAP Integration Suite equivalents...'
        })

        # Start processing in background
        thread = threading.Thread(
            target=process_iflow_match,
            args=(job_id, markdown_file_path)
        )
        thread.daemon = True
        thread.start()

        return jsonify({
            'status': 'processing',
            'message': 'SAP Integration Suite equivalent search started'
        }), 202

    except Exception as e:
        logging.error(f"Error starting iFlow match processing: {str(e)}")
        return jsonify({'error': str(e)}), 500

def process_iflow_match(job_id, markdown_file_path):
    """
    Process the markdown file with GetIflowEquivalent in a background thread

    Args:
        job_id: Job ID to identify which documentation to process
        markdown_file_path: Path to the markdown file
    """
    try:
        # Import the local iflow_matcher module
        try:
            from iflow_matcher import process_markdown_for_iflow
            print("Successfully imported process_markdown_for_iflow from local iflow_matcher module")
        except ImportError as e:
            print(f"Error importing from iflow_matcher: {str(e)}")
            raise ImportError(f"Could not import process_markdown_for_iflow: {str(e)}")

        # Create output directory in the job results folder
        job_result_dir = os.path.join(app.config['RESULTS_FOLDER'], job_id)
        iflow_output_dir = os.path.join(job_result_dir, "iflow_match")
        os.makedirs(iflow_output_dir, exist_ok=True)

        # Update job status
        update_job(job_id, {
            'iflow_match_status': 'processing',
            'iflow_match_message': 'Extracting terms from markdown and searching for matches...'
        })

        # Get GitHub token from environment
        github_token = os.environ.get("GITHUB_TOKEN")
        if not github_token:
            logging.warning("No GitHub token found in environment. SAP Integration Suite equivalent search may fail.")

        # Process the markdown file
        result = process_markdown_for_iflow(
            markdown_file_path=markdown_file_path,
            output_dir=iflow_output_dir,
            github_token=github_token
        )

        if result["status"] == "success":
            # Prepare file paths
            files_dict = {
                'report': os.path.relpath(result["files"]["report"], os.path.dirname(os.path.abspath(__file__))),
                'summary': os.path.relpath(result["files"]["summary"], os.path.dirname(os.path.abspath(__file__)))
            }

            # Add chart files if they exist
            if "charts" in result["files"]:
                chart_files = result["files"]["charts"]
                if isinstance(chart_files, dict):
                    for chart_name, chart_path in chart_files.items():
                        files_dict[f'chart_{chart_name}'] = os.path.relpath(chart_path, os.path.dirname(os.path.abspath(__file__)))
                elif isinstance(chart_files, list):
                    for i, chart_path in enumerate(chart_files):
                        files_dict[f'chart_{i}'] = os.path.relpath(chart_path, os.path.dirname(os.path.abspath(__file__)))

            # Update job with file paths
            update_job(job_id, {
                'iflow_match_status': 'completed',
                'iflow_match_message': 'SAP Integration Suite equivalent search completed successfully!',
                'iflow_match_files': files_dict,
                'iflow_match_result': {
                    'message': result["message"]
                }
            })
        else:
            # Update job with error
            update_job(job_id, {
                'iflow_match_status': 'failed',
                'iflow_match_message': f'SAP Integration Suite equivalent search failed: {result["message"]}'
            })

    except Exception as e:
        logging.error(f"Error processing iFlow match: {str(e)}")
        update_job(job_id, {
            'iflow_match_status': 'failed',
            'iflow_match_message': f'Error processing iFlow match: {str(e)}'
        })

if __name__ == '__main__':
    # Set up stdout logger for better visibility
    class CustomFormatter(logging.Formatter):
        """Custom formatter to add color to console output"""
        green = "\033[92m"
        blue = "\033[94m"
        yellow = "\033[93m"
        red = "\033[91m"
        bold = "\033[1m"
        reset = "\033[0m"

        format_str = "%(asctime)s - %(levelname)s - %(message)s"

        FORMATS = {
            logging.DEBUG: blue + format_str + reset,
            logging.INFO: green + format_str + reset,
            logging.WARNING: yellow + format_str + reset,
            logging.ERROR: red + format_str + reset,
            logging.CRITICAL: bold + red + format_str + reset
        }

        def format(self, record):
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return formatter.format(record)

    # Add console handler with custom formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CustomFormatter())
    logging.getLogger().addHandler(console_handler)
    logging.getLogger().setLevel(logging.INFO)

    print("\n" + "="*80)
    print("Starting MuleSoft Documentation Generator API")
    print("Environment variables loaded from: " + os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "final", ".env"))
    print("Using Anthropic for LLM enhancement")
    print("Enhancement is FORCED ON for all documentation")
    print("="*80 + "\n")

    # Run Flask app without reloader to prevent issues with file uploads
    PORT = int(os.getenv('PORT', 5000))
    print(f"Starting Flask application on port {PORT}")
    app.run(debug=True, host='0.0.0.0', port=PORT, use_reloader=False)



