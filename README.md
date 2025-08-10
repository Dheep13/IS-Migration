# IMigrate - Integration Migration Platform

##  Quick Start

IMigrate is a comprehensive platform for migrating integration flows from Boomi and MuleSoft to SAP Integration Suite. The platform provides automated documentation generation, AI-powered iFlow creation, and seamless deployment capabilities.

### **System Architecture**
- **Main API** (Port 5000): Core documentation processing and job management
- **BoomiToIS-API** (Port 5003): Boomi XML processing and iFlow generation
- **MuleToIS-API** (Port 5001): MuleSoft XML processing and iFlow generation
- **Gemma-3 API** (Port 5002): RunPod Gemma-3 integration for alternative LLM processing
- **Frontend** (React/Vite): User interface for uploads and workflow management

### ** Python Launcher Features**
The new **`platform_launcher.py`** provides:
- **Cross-platform compatibility** (Windows, Linux, Mac)
- **Interactive menu system** with organized options
- **Process management** with proper cleanup and monitoring
- **Real-time server status** checking and health monitoring
- **Unified logging** with timestamped log files
- **Deployment management** for Cloud Foundry
- **Environment cleanup** and dependency management

### **Quick Commands**
```bash
# Primary launcher (Python - Cross-platform)
python platform_launcher.py

# Simple wrapper scripts
./start.bat        # Windows
./start.sh         # Linux/Mac

# Legacy launcher (redirects to Python launcher)
./quick-start-fixed.bat

# Direct Python execution
python platform_launcher.py
```

## 📖 Documentation

- **[HOW_TO_RUN_GUIDE.md](./HOW_TO_RUN_GUIDE.md)** - Complete setup and usage instructions
- **[PROJECT_DOCS.md](./PROJECT_DOCS.md)** - Technical details, architecture, and status

## 🔧 Key Features

1. **Document Upload & Processing**: Upload Word documents or XML files for analysis
2. **AI-Enhanced Documentation**: Automatic markdown generation with technical details
3. **iFlow Generation**: Convert Boomi/MuleSoft flows to SAP Integration Suite iFlows
4. **Progress Tracking**: Real-time status updates with visual progress indicators
5. **SAP BTP Integration**: Direct deployment to SAP Integration Suite

## 🌐 Live Deployment

- **Frontend**: https://ifa-project.cfapps.eu10.hana.ondemand.com
- **Main API**: https://mule2is-api.cfapps.eu10.hana.ondemand.com  
- **BoomiToIS-API**: https://boomitois-api.cfapps.eu10.hana.ondemand.com

## 📁 Project Structure

```
├── app/                    # Main API (documentation processing)
├── BoomiToIS-API/         # Boomi processing service
├── MuleToIS-API/          # MuleSoft processing service  
├── IFA-Project/frontend/  # React frontend application
├── archive/               # Archived/deprecated files
└── deployment/            # Deployment configurations
```

For detailed setup instructions, see [HOW_TO_RUN_GUIDE.md](./HOW_TO_RUN_GUIDE.md).
