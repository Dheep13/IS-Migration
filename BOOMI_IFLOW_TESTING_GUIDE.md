# Boomi iFlow Generation Testing Guide

## 🎯 **Complete Pipeline Overview**

The Boomi iFlow generation pipeline consists of three main steps:

1. **📋 Documentation Generation** (Main App - Port 5000)
   - Upload Boomi XML files
   - Generate enhanced documentation with AI
   - Extract integration components and flows

2. **🔧 iFlow Metadata Generation** (BoomiToIS-API - Port 5003)
   - Convert documentation to structured JSON metadata
   - Create intermediate files for iFlow generation
   - Generate component mappings and flow definitions

3. **⚙️ iFlow Code Generation** (BoomiToIS-API - Port 5003)
   - Convert JSON metadata to SAP Integration Suite iFlow XML
   - Create deployable iFlow packages
   - Generate ZIP files for import

## 🧪 **Testing Steps**

### **Step 1: Start Both Services**

1. **Start Main Documentation Service:**
   ```bash
   cd app
   python app.py
   ```
   - Runs on: http://localhost:5000

2. **Start BoomiToIS-API Service:**
   ```bash
   # Option 1: Use the batch file
   start_boomi_iflow_service.bat
   
   # Option 2: Manual start
   cd BoomiToIS-API
   python app.py
   ```
   - Runs on: http://localhost:5003

### **Step 2: Generate Documentation with iFlow Metadata**

1. **Upload Boomi Files** via UI (http://localhost:5000)
2. **Enable AI Enhancement** (checkbox checked)
3. **Wait for completion** (1-2 minutes for AI enhancement)
4. **Check for iFlow metadata generation** in logs

### **Step 3: Verify Intermediate JSON Files**

Check these locations for generated files:

**Documentation Files:**
```
app/results/{JOB_ID}/
├── boomi_documentation.md
└── boomi_documentation.html
```

**iFlow Metadata Files:**
```
BoomiToIS-API/genai_debug/
├── iflow_input_components_{JOB_ID}.json  ⭐ Main input file
├── generation_approach_{JOB_ID}.json    - Generation strategy
├── final_components.json                - Component mapping
└── final_iflow_{JOB_ID}.xml            - Generated iFlow XML
```

### **Step 4: Generate Complete iFlow Package**

1. **Use the BoomiToIS-API directly** to generate complete iFlow:
   ```bash
   curl -X POST http://localhost:5003/api/generate-iflow \
     -H "Content-Type: application/json" \
     -d '{
       "markdown": "YOUR_DOCUMENTATION_CONTENT",
       "iflow_name": "BoomiTestFlow"
     }'
   ```

2. **Monitor progress** via job status endpoint:
   ```bash
   curl http://localhost:5003/api/jobs/{JOB_ID}
   ```

3. **Download generated iFlow** when complete:
   ```bash
   curl http://localhost:5003/api/jobs/{JOB_ID}/download
   ```

## 📁 **File Locations to Check**

### **Main App Results:**
- `app/results/{JOB_ID}/boomi_documentation.md`
- `app/results/{JOB_ID}/boomi_documentation.html`

### **BoomiToIS-API Debug Files:**
- `BoomiToIS-API/genai_debug/iflow_input_components_{JOB_ID}.json`
- `BoomiToIS-API/genai_debug/generation_approach_{JOB_ID}.json`
- `BoomiToIS-API/genai_debug/final_iflow_{JOB_ID}.xml`

### **BoomiToIS-API Results:**
- `BoomiToIS-API/results/{IFLOW_JOB_ID}/`
- Generated ZIP files for SAP Integration Suite import

## 🔍 **Troubleshooting**

### **If iFlow Metadata Generation Fails:**
1. Check if BoomiToIS-API is running on port 5003
2. Check main app logs for API call errors
3. Verify network connectivity between services

### **If iFlow Generation Fails:**
1. Check BoomiToIS-API logs for detailed errors
2. Verify Claude API key is configured in BoomiToIS-API/.env
3. Check intermediate JSON files are properly formatted

### **Common Issues:**
- **Port conflicts**: Ensure ports 5000 and 5003 are available
- **API key missing**: Configure ANTHROPIC_API_KEY in both .env files
- **Network issues**: Both services must be accessible to each other

## ✅ **Success Indicators**

You'll know the complete pipeline is working when you see:

1. **Documentation generated** with AI enhancement
2. **iFlow metadata files** created in BoomiToIS-API/genai_debug/
3. **Complete iFlow XML** generated and downloadable
4. **No errors** in either service logs

## 🚀 **Next Steps**

Once the pipeline is working:
1. **Import generated iFlow** into SAP Integration Suite
2. **Test the integration** in SAP BTP
3. **Deploy to production** environment
