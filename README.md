# MuleSoft Documentation Generator - Cloud Foundry Deployment

This repository contains the MuleSoft Documentation Generator application, designed for deployment to Cloud Foundry environments. The application analyzes MuleSoft integration flows and helps find SAP Integration Suite equivalents.

## Directory Structure

- `app/` - Main API (Flask application)
  - Core application files (app.py, run_app.py)
  - Documentation generators
  - Templates and static files
  - Core modules for documentation generation
  - Upload and results directories

- `MuleToIS-API/` - iFlow API (Flask application)
  - iFlow generation functionality
  - SAP BTP Integration Suite deployment

- `IFA-Project/frontend/` - Frontend React application
  - Source code for the web interface
  - Build configuration
  - Deployment scripts

## Environment Configuration

The application uses environment-specific configuration files to manage URLs and API endpoints:

- **Development**: `.env.development` files in each component
- **Production**: `.env.production` files in each component

To switch between environments, use the provided scripts:

```bash
# Set development environment
set-env.bat development

# Set production environment
set-env.bat production
```

Or use the convenience scripts to start each component:

```bash
# Development
start-main-api-development.bat
start-iflow-api-development.bat
start-frontend-development.bat

# Production
start-main-api-production.bat
start-iflow-api-production.bat
start-frontend-production.bat
```

## Quick Deployment Guide

1. **Login to Cloud Foundry:**
   ```bash
   cf login -a <CF_API_ENDPOINT>
   ```

2. **Deploy the backend application:**
   ```bash
   cf push -f manifest.yml
   ```

3. **Set required environment variables:**
   ```bash
   cf set-env mulesoft-documentation-generator ANTHROPIC_API_KEY your-api-key
   cf set-env mulesoft-documentation-generator OPENAI_API_KEY your-api-key
   cf restage mulesoft-documentation-generator
   ```

4. **Deploy the frontend application:**
   ```bash
   cd project
   npm install
   npm run build
   cf push -f frontend-manifest.yml
   ```

## Documentation

- For detailed backend deployment instructions, see `app/README_DEPLOYMENT.md`
- For frontend deployment and development, see `project/README.md`

## Features

- Upload and analyze MuleSoft XML files
- Generate comprehensive documentation with flow diagrams
- Find SAP Integration Suite equivalents for MuleSoft components
- Generate SAP API/iFlow definitions
- Optional LLM-enhanced documentation using Anthropic Claude or OpenAI

## Accessing the Application

- **Development**: http://localhost:5173/projects/1/flow
- **Production**: https://ifa-frontend.cfapps.us10-001.hana.ondemand.com/projects/1/flow

## API Endpoints

### Main API

- **Development**: http://localhost:5000/api
- **Production**: https://it-resonance-api-wacky-panther-za.cfapps.us10-001.hana.ondemand.com/api

### iFlow API

- **Development**: http://localhost:5001/api
- **Production**: https://mulesoft-iflow-api.cfapps.us10-001.hana.ondemand.com/api
