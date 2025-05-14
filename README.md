# MuleSoft Documentation Generator - Cloud Foundry Deployment

This repository contains the MuleSoft Documentation Generator application, designed for deployment to Cloud Foundry environments. The application analyzes MuleSoft integration flows and helps find SAP Integration Suite equivalents.

## Directory Structure

- `app/` - Main Python application directory
  - Core application files (app.py, run_app.py)
  - Documentation generators
  - Templates and static files
  - Core modules for documentation generation
  - Upload and results directories
  
- `project/` - Frontend React application
  - Source code for the web interface
  - Build configuration
  - Deployment scripts

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
