# IS-Migration Server Management Scripts

This directory contains scripts to easily start and stop all IS-Migration platform servers with a single command.

## 🚀 **Quick Start**

### Windows
```bash
# Start all servers
start-all-servers.bat

# Stop all servers
stop-all-servers.bat
```

### Linux/Mac
```bash
# Start all servers
./start-all-servers.sh

# Stop all servers
./stop-all-servers.sh
```

## 📋 **What Gets Started**

The scripts will start all these servers automatically:

| Service | Port | Purpose |
|---------|------|---------|
| **Frontend** | 5173 | React frontend interface |
| **Main API** | 5000 | Documentation generator |
| **BoomiToIS API** | 5003 | Boomi to SAP Integration Suite converter |
| **MuleToIS API** | 5001 | MuleSoft to SAP Integration Suite converter |
| **Gemma-3 API** | 5002 | AI-powered enhancement service |

## ✅ **Features**

- **One Command Start**: All servers start with a single command
- **Automatic Browser Opening**: Frontend opens automatically in your browser
- **Color-Coded Output**: Easy to see what's happening
- **Error Checking**: Validates Python and Node.js are installed
- **Clean Shutdown**: Stop script cleanly terminates all processes
- **Log Management**: Logs are created and cleaned up automatically
- **Cross-Platform**: Works on Windows, Linux, and Mac

## 🔧 **Prerequisites**

Make sure you have these installed:
- **Python 3.7+** (with pip)
- **Node.js 16+** (with npm)
- All project dependencies installed

## 📝 **Usage Examples**

### Start Everything
```bash
# Windows
start-all-servers.bat

# Linux/Mac  
./start-all-servers.sh
```

### Stop Everything
```bash
# Windows
stop-all-servers.bat

# Linux/Mac
./stop-all-servers.sh
```

### Check What's Running
After starting, you can access:
- **Frontend**: http://localhost:5173
- **Main API Health**: http://localhost:5000/api/health
- **BoomiToIS API Health**: http://localhost:5003/api/health

## 🐛 **Troubleshooting**

### Port Already in Use
If you get port conflicts:
1. Run the stop script first
2. Wait 10 seconds
3. Run the start script again

### Missing Dependencies
If servers fail to start:
1. Check that Python and Node.js are installed
2. Install project dependencies:
   ```bash
   # In each API directory
   pip install -r requirements.txt
   
   # In frontend directory
   npm install
   ```

### Permission Issues (Linux/Mac)
If you get permission errors:
```bash
chmod +x start-all-servers.sh stop-all-servers.sh
```

## 📊 **Server Status**

The start script will show you:
- ✅ Which servers started successfully
- ❌ Any servers that failed to start
- 🌐 URLs to access each service
- 📝 Log file locations

## 🔄 **Development Workflow**

1. **Start Development**: `start-all-servers.bat`
2. **Make Changes**: Edit your code
3. **Test Changes**: Refresh browser or restart specific servers
4. **Stop Development**: `stop-all-servers.bat`

## 📁 **Log Files**

Logs are stored in the `logs/` directory:
- `main-api-5000.log`
- `boomitois-api-5003.log`
- `muletois-api-5001.log`
- `gemma3-api-5002.log`
- `frontend-5173.log`

These help debug any startup issues.
