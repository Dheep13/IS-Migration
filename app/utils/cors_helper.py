# cors_helper.py - Helper for enabling CORS in Flask app

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
        # Set a specific origin for local development
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept, Origin'
        response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
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
