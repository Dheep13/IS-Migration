# Cloud Foundry Commands Reference

This document provides a consolidated list of Cloud Foundry (CF) commands used for deploying and managing our applications.

## Authentication and Setup

```bash
# Login to Cloud Foundry
cf login -a https://api.cf.us10-001.hana.ondemand.com -u your_email@example.com -p your_password

# Target a specific org and space
cf target -o "IT Resonance Inc_itr-internal-2hco92jx" -s "dev"

# View current target information
cf target
```

## Application Deployment

```bash
# Push an application using a manifest file
cf push -f manifest.yml

# Push an application with specific parameters
cf push app-name -p path/to/app -b buildpack-name -m 1024M -i 1

# Push an application with environment variables
cf push app-name --var ANTHROPIC_API_KEY=your_api_key --var GITHUB_TOKEN=your_token

# Push with no start (upload but don't start the application)
cf push app-name --no-start

# Push with random-route to avoid route conflicts
cf push app-name --random-route
```

## Environment Variables

```bash
# Set environment variables for an application
cf set-env app-name ANTHROPIC_API_KEY your_api_key
cf set-env app-name GITHUB_TOKEN your_github_token

# View environment variables for an application
cf env app-name

# Unset an environment variable
cf unset-env app-name VARIABLE_NAME
```

## Application Management

```bash
# Start an application
cf start app-name

# Stop an application
cf stop app-name

# Restart an application
cf restart app-name

# Delete an application
cf delete app-name -f  # -f forces deletion without confirmation

# Rename an application
cf rename app-name new-app-name
```

## Application Information

```bash
# List all applications in the current space
cf apps

# Display detailed information about an application
cf app app-name

# View application logs
cf logs app-name --recent  # Show recent logs
cf logs app-name  # Stream logs (Ctrl+C to stop)

# View application events
cf events app-name

# View application health and status
cf app app-name
```

## Routes and Domains

```bash
# List available domains
cf domains

# List routes in the current space
cf routes

# Create a route
cf create-route space-name domain-name --hostname hostname

# Map a route to an application
cf map-route app-name domain-name --hostname hostname

# Unmap a route from an application
cf unmap-route app-name domain-name --hostname hostname

# Delete a route
cf delete-route domain-name --hostname hostname -f
```

## Services

```bash
# List available service offerings
cf marketplace

# List service instances in the current space
cf services

# Create a service instance
cf create-service service-name plan-name instance-name

# Bind a service to an application
cf bind-service app-name service-instance-name

# Unbind a service from an application
cf unbind-service app-name service-instance-name

# Delete a service instance
cf delete-service service-instance-name -f
```

## Organizations and Spaces

```bash
# List organizations
cf orgs

# List spaces in the current organization
cf spaces

# Create a new space
cf create-space space-name

# Delete a space
cf delete-space space-name -f
```

## Buildpacks

```bash
# List available buildpacks
cf buildpacks

# Specify a buildpack during deployment
cf push app-name -b buildpack-name
```

## Quotas and Limits

```bash
# View organization quotas
cf org-quotas

# View space quotas
cf space-quotas

# View quota for a specific organization
cf org org-name --quota
```

## Deployment Commands for Our Applications

```bash
# Deploy the main API application
cf push it-resonance-api-wacky-panther-za -f manifest.yml

# Deploy the iFlow API application
cf push mulesoft-iflow-api -f MuleToIS-API/manifest.yml

# Deploy the frontend application
cf push ifa-project-frontend -f IFA-Project/frontend/manifest.yml
```

## Troubleshooting

```bash
# SSH into an application container
cf ssh app-name

# Run a specific command in the application container
cf ssh app-name -c "command"

# View crash logs
cf logs app-name --recent | grep -i crash

# View staging logs
cf logs app-name --recent | grep -i staging
```

## Manifest Examples

### Main API Manifest (manifest.yml)
```yaml
applications:
- name: it-resonance-api-wacky-panther-za
  memory: 1024M
  instances: 1
  buildpack: python_buildpack
  command: python app.py
  env:
    ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
    GITHUB_TOKEN: ${GITHUB_TOKEN}
```

### iFlow API Manifest (MuleToIS-API/manifest.yml)
```yaml
applications:
- name: mulesoft-iflow-api
  memory: 1024M
  instances: 1
  buildpack: python_buildpack
  command: python app.py
  env:
    ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
    MAIN_API_URL: https://it-resonance-api-wacky-panther-za.cfapps.us10-001.hana.ondemand.com
```

### Frontend Manifest (IFA-Project/frontend/manifest.yml)
```yaml
applications:
- name: ifa-project-frontend
  memory: 256M
  instances: 1
  buildpack: staticfile_buildpack
  path: dist
  env:
    VITE_API_BASE_URL: https://it-resonance-api-wacky-panther-za.cfapps.us10-001.hana.ondemand.com/api
    VITE_IFLOW_API_BASE_URL: https://mulesoft-iflow-api.cfapps.us10-001.hana.ondemand.com/api
```
