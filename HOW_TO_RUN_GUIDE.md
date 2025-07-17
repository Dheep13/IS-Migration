# HOW TO RUN GUIDE - IMigrate Platform

## 🚀 Quick Start Options

### Option 1: Interactive Quick Start (Recommended)
```bash
./quick-start.bat
```
This provides an interactive menu with all common operations.

### Option 2: Direct Commands

#### Local Development Setup
```bash
# Setup local environment
deployment/scripts/manage-env.bat setup-local

# Start all local servers
deployment/scripts/manage-env.bat start-local
```

#### Production Deployment
```bash
# Deploy all applications
deployment/scripts/manage-env.bat deploy-all

# Deploy single application
deployment/scripts/manage-env.bat deploy-single [app_name]
# Available apps: main_api, mule_api, boomi_api, frontend
```

## 🌐 Service URLs

### Local Development
- **Frontend**: http://localhost:3000
- **Main API**: http://localhost:5000  
- **MuleToIS API**: http://localhost:5001
- **BoomiToIS API**: http://localhost:5003

### Production (Cloud Foundry)
- **Frontend**: https://ifa-project.cfapps.eu10.hana.ondemand.com
- **Main API**: https://mule2is-api.cfapps.eu10.hana.ondemand.com
- **BoomiToIS API**: https://boomitois-api.cfapps.eu10.hana.ondemand.com

## 📋 Prerequisites

### Local Development
1. **Node.js** (v18+) for frontend
2. **Python** (3.9+) for APIs
3. **Git** for version control

### Production Deployment  
1. **Cloud Foundry CLI** installed and configured
2. **SAP BTP account** with appropriate permissions
3. **Environment variables** configured (see PROJECT_DOCS.md)

## 🔧 Manual Setup Instructions

### 1. Frontend Setup
```bash
cd IFA-Project/frontend
npm install
npm run dev
```

### 2. Main API Setup
```bash
cd app
pip install -r requirements.txt
python app.py
```

### 3. BoomiToIS API Setup
```bash
cd BoomiToIS-API
pip install -r requirements.txt
python app.py
```

### 4. MuleToIS API Setup
```bash
cd MuleToIS-API
pip install -r requirements.txt
python app.py
```

## 🔍 Testing & Verification

### Health Checks
```bash
# Test API routing
./test_api_routing.bat

# Check deployment status
deployment/scripts/manage-env.bat status
```

### Manual Testing
1. **Upload Document**: Use frontend to upload a Word document or XML file
2. **Generate Documentation**: Verify markdown generation works
3. **Generate iFlow**: Test iFlow generation from documentation
4. **Deploy to SAP**: Test SAP BTP integration (production only)

## 🛠️ Troubleshooting

### Common Issues
1. **Port conflicts**: Ensure ports 3000, 5000, 5001, 5003 are available
2. **Python dependencies**: Run `pip install -r requirements.txt` in each API folder
3. **Node.js dependencies**: Run `npm install` in frontend folder
4. **Environment variables**: Check .env files in each service

### Logs & Debugging
- **Frontend logs**: Browser developer console
- **API logs**: Terminal output where services are running
- **Production logs**: `cf logs [app-name]` for Cloud Foundry

## 📁 Project Structure Reference

```
├── app/                    # Main API (Port 5000)
│   ├── app.py             # Main application
│   ├── requirements.txt   # Python dependencies
│   └── .env              # Environment variables
├── BoomiToIS-API/         # Boomi API (Port 5003)
├── MuleToIS-API/          # MuleSoft API (Port 5001)  
├── IFA-Project/frontend/  # React Frontend (Port 3000)
├── deployment/            # Deployment scripts & configs
└── archive/              # Archived files (ignore)
```

For technical details and architecture information, see [PROJECT_DOCS.md](./PROJECT_DOCS.md).
