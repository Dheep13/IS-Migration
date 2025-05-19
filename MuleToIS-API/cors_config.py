"""
CORS configuration for the MuleToIS API.
This module provides a function to get the appropriate CORS origin based on the environment.
"""

import os

def get_cors_origin():
    """
    Get the appropriate CORS origin based on the environment.

    In development, use localhost.
    In production (Cloud Foundry), use the CF domain.

    Returns:
        str: The CORS origin to use
    """
    # First check if CORS_ORIGIN is explicitly set in environment variables
    if os.environ.get('CORS_ORIGIN'):
        return os.environ.get('CORS_ORIGIN')

    # Check if we're running in Cloud Foundry
    if os.environ.get('VCAP_APPLICATION'):
        # We're in Cloud Foundry, allow specific domains
        # You can add more domains if needed, separated by commas
        cf_domains = [
            'https://it-resonance-ui.cfapps.us10-001.hana.ondemand.com',
            'https://mulesoft-docs-ui.cfapps.us10-001.hana.ondemand.com',
            'https://ifa-frontend.cfapps.us10-001.hana.ondemand.com'
        ]

        # Return the list of allowed domains
        return ','.join(cf_domains)

    # Check if we're in development or production environment
    env = os.environ.get('FLASK_ENV', 'development')

    if env == 'production':
        # In production but not in CF, use a specific domain
        return os.environ.get('PROD_FRONTEND_URL', 'https://ifa-frontend.cfapps.us10-001.hana.ondemand.com')
    else:
        # We're in development, use localhost with the Vite dev server port
        return os.environ.get('DEV_FRONTEND_URL', 'http://localhost:5173')
