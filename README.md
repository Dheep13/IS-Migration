# MuleSoft Documentation Generator - Cloud Foundry Deployment

This directory contains an organized structure for deploying the MuleSoft Documentation Generator to Cloud Foundry.

## Directory Structure

- pp/ - Main application directory
  - Core application files (app.py, run_app.py)
  - Documentation generators
  - Templates and static files
  - inal/ - Core modules from final directory
  - uploads/ - Directory for file uploads
  - esults/ - Directory for generated documentation

## Deployment Steps

1. Login to Cloud Foundry:
   `
   cf login -a <CF_API_ENDPOINT>
   `

2. Deploy the application from this directory:
   `
   cf push
   `

3. Set required environment variables:
   `
   cf set-env mulesoft-documentation-generator ANTHROPIC_API_KEY your-api-key
   cf set-env mulesoft-documentation-generator OPENAI_API_KEY your-api-key
   cf restage mulesoft-documentation-generator
   `

For more details, see the README_DEPLOYMENT.md file in the app directory.
