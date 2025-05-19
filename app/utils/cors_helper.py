# cors_helper.py - Helper for enabling CORS in Flask app

import os
from flask import request

def enable_cors(app):
    """
    Enable CORS for the Flask application with settings appropriate for local development and Cloud Foundry
    """
    # Instead of using the Flask-CORS extension, we'll handle CORS manually
    # to avoid duplicate headers

    # Create a simple OPTIONS route handler for the root path
    @app.route('/', methods=['OPTIONS'])
    def options_root():
        return _build_cors_preflight_response()

    # Create a simple OPTIONS route handler for all other paths
    @app.route('/<path:path>', methods=['OPTIONS'])
    def options_path(path):
        return _build_cors_preflight_response()

    # Create a simple OPTIONS route handler for API paths
    @app.route('/api/<path:path>', methods=['OPTIONS'])
    def options_api(path):
        return _build_cors_preflight_response()

    # Helper function to build preflight response
    def _build_cors_preflight_response():
        response = app.make_default_options_response()
        _add_cors_headers(response)
        return response

    # Helper function to add CORS headers
    def _add_cors_headers(response):
        # Get the origin from the request
        origin = request.headers.get('Origin')

        # Get allowed origins from environment variables or use defaults
        dev_frontend_url = os.environ.get('DEV_FRONTEND_URL', 'http://localhost:5173')
        prod_frontend_url = os.environ.get('PROD_FRONTEND_URL', 'https://ifa-frontend.cfapps.us10-001.hana.ondemand.com')

        # Check if CORS_ORIGIN is explicitly set
        if os.environ.get('CORS_ORIGIN'):
            # Parse the CORS_ORIGIN value - it might contain multiple origins separated by commas
            cors_origins = [origin.strip() for origin in os.environ.get('CORS_ORIGIN').split(',')]

            # If the request origin is in the allowed list, use it
            if origin and origin in cors_origins:
                response.headers['Access-Control-Allow-Origin'] = origin
            # If the request has no origin or it's not in the allowed list, use the first one
            elif cors_origins:
                response.headers['Access-Control-Allow-Origin'] = cors_origins[0]
            # Fallback to * if no origins are specified
            else:
                response.headers['Access-Control-Allow-Origin'] = '*'

            # Make sure we still set the credentials header
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept, Origin'
            response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Credentials'] = os.environ.get('CORS_ALLOW_CREDENTIALS', 'true')
            response.headers['Access-Control-Max-Age'] = '3600'  # Cache preflight response for 1 hour
            response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition, Content-Length, Content-Type'
            return response

        # List of allowed origins
        allowed_origins = [
            dev_frontend_url,  # Local development
            prod_frontend_url  # Production frontend
        ]

        # Add any additional origins from environment variable
        additional_origins = os.environ.get('ADDITIONAL_CORS_ORIGINS', '')
        if additional_origins:
            for additional_origin in additional_origins.split(','):
                if additional_origin.strip():
                    allowed_origins.append(additional_origin.strip())

        # Set the appropriate CORS header based on the request origin
        if origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
        else:
            # Check environment to determine default
            env = os.environ.get('FLASK_ENV', 'development')
            if env == 'production':
                # Default to the production frontend if origin is not in the allowed list
                response.headers['Access-Control-Allow-Origin'] = prod_frontend_url
            else:
                # Default to the development frontend
                response.headers['Access-Control-Allow-Origin'] = dev_frontend_url

        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept, Origin'
        response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Credentials'] = os.environ.get('CORS_ALLOW_CREDENTIALS', 'true')
        response.headers['Access-Control-Max-Age'] = '3600'  # Cache preflight response for 1 hour

        # Add Content-Disposition to the exposed headers for file downloads
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition, Content-Length, Content-Type'

        return response

    # Add CORS headers to all responses
    @app.after_request
    def after_request(response):
        # Add CORS headers to every response
        _add_cors_headers(response)

        # For non-OPTIONS methods, ensure we have the right content type
        if request.method != 'OPTIONS':
            # If it's a JSON response, ensure proper content type
            if response.headers.get('Content-Type') is None:
                if response.get_json() is not None:
                    response.headers['Content-Type'] = 'application/json'

        return response

    return app
