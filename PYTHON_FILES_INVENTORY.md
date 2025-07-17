# Python Files Inventory - IMigrate Platform

## 📋 **Complete List of Python Files in Project**

### **🎯 CORE SERVICES (Keep - Essential)**

#### **Main API (app/)**
- `app/app.py` ⭐ **MAIN** - Primary Flask API server
- `app/document_processor.py` ⭐ **CORE** - Document processing logic
- `app/documentation_enhancer.py` ⭐ **CORE** - LLM integration for document enhancement
- `app/utils/cors_helper.py` ⭐ **CORE** - CORS configuration

#### **BoomiToIS-API/**
- `BoomiToIS-API/app.py` ⭐ **MAIN** - Boomi to Integration Suite API
- `BoomiToIS-API/boomi_xml_processor.py` ⭐ **CORE** - Boomi XML parsing
- `BoomiToIS-API/bpmn_templates.py` ⭐ **CORE** - BPMN template system
- `BoomiToIS-API/enhanced_iflow_templates.py` ⭐ **CORE** - Enhanced template system
- `BoomiToIS-API/json_to_iflow_converter.py` ⭐ **CORE** - JSON to iFlow conversion
- `BoomiToIS-API/client.py` ⭐ **CORE** - API client utilities

#### **MuleToIS-API-Gemma3/**
- `MuleToIS-API-Gemma3/app.py` ⭐ **MAIN** - Gemma-3 API service (handles both platforms)

#### **MuleToIS-API/**
- `MuleToIS-API/app.py` ⭐ **MAIN** - MuleSoft to Integration Suite API
- `MuleToIS-API/client.py` ⭐ **CORE** - API client utilities

### **🔧 UTILITY & SUPPORT FILES (Keep - Important)**

#### **Main API Utils**
- `app/additional_file_parser.py` - Additional file format parsing
- `app/boomi_flow_documentation.py` - Boomi flow documentation generator
- `app/mule_flow_documentation.py` - MuleSoft flow documentation generator
- `app/enhanced_doc_generator.py` - Enhanced documentation generation
- `app/iflow_matcher.py` - iFlow matching logic
- `app/database.py` - Database utilities
- `app/models.py` - Data models

#### **Deployment & Setup**
- `app/cf_startup_check.py` - Cloud Foundry startup checks
- `app/prepare_deployment.py` - Deployment preparation
- `app/nltk_setup.py` - NLTK data setup
- `app/download_nltk_data.py` - NLTK data downloader

#### **BoomiToIS-API Utils**
- `BoomiToIS-API/cors_config.py` - CORS configuration
- `BoomiToIS-API/enhanced_genai_iflow_generator.py` - Enhanced GenAI generator
- `BoomiToIS-API/enhanced_prompt_generator.py` - Enhanced prompt generation
- `BoomiToIS-API/iflow_deployment.py` - iFlow deployment utilities
- `BoomiToIS-API/sap_btp_integration.py` - SAP BTP integration
- `BoomiToIS-API/setup_dependencies.py` - Dependency setup
- `BoomiToIS-API/nltk_setup.py` - NLTK setup

#### **MuleToIS-API Utils**
- `MuleToIS-API/cors_config.py` - CORS configuration
- `MuleToIS-API/enhanced_genai_iflow_generator.py` - Enhanced GenAI generator
- `MuleToIS-API/enhanced_prompt_generator.py` - Enhanced prompt generation
- `MuleToIS-API/enhanced_iflow_templates.py` - Enhanced templates
- `MuleToIS-API/bpmn_templates.py` - BPMN templates
- `MuleToIS-API/json_to_iflow_converter.py` - JSON to iFlow converter
- `MuleToIS-API/iflow_deployment.py` - iFlow deployment
- `MuleToIS-API/direct_iflow_deployment.py` - Direct deployment
- `MuleToIS-API/sap_btp_integration.py` - SAP BTP integration
- `MuleToIS-API/setup_dependencies.py` - Dependency setup
- `MuleToIS-API/nltk_setup.py` - NLTK setup

### **🧪 TEST FILES (Review - Can Archive)**

#### **Main API Tests**
- `app/test_document_conversion.py` - Document conversion tests
- `app/test_iflow_import.py` - iFlow import tests
- `app/test_iflow_matcher.py` - iFlow matcher tests
- `app/test_import.py` - Import functionality tests

#### **BoomiToIS-API Tests**
- `BoomiToIS-API/test_api.py` - API endpoint tests
- `BoomiToIS-API/test_bpmn_templates.py` - BPMN template tests
- `BoomiToIS-API/test_enhanced_templates_d0a449df.py` - Enhanced template tests
- `BoomiToIS-API/test_iflow_generation.py` - iFlow generation tests
- `BoomiToIS-API/test_new_templates.py` - New template tests
- `BoomiToIS-API/test_odata_adapter_fix.py` - OData adapter tests
- `BoomiToIS-API/test_receiver_adapter_fix.py` - Receiver adapter tests
- `BoomiToIS-API/test_receiver_templates.py` - Receiver template tests
- `BoomiToIS-API/simple_test.py` - Simple API tests
- `BoomiToIS-API/verify_templates.py` - Template verification

#### **MuleToIS-API Tests**
- `MuleToIS-API/test_api.py` - API endpoint tests

#### **Gemma-3 API Tests**
- `MuleToIS-API-Gemma3/test_response_parsing.py` - Response parsing tests
- `MuleToIS-API-Gemma3/test_runpod_api.py` - RunPod API tests

### **🗑️ LEGACY/DUPLICATE FILES (Can Delete)**

#### **Minimal/Alternative Versions**
- `BoomiToIS-API/app_minimal.py` ❌ **DELETE** - Minimal version (use main app.py)
- `MuleToIS-API/app_minimal.py` ❌ **DELETE** - Minimal version (use main app.py)

#### **Legacy/Unused Files**
- `app/main.py` ❌ **DELETE** - Legacy main file (use app.py)
- `app/run_app.py` ❌ **DELETE** - Legacy runner (use app.py)
- `app/use_anthropic.py` ❌ **DELETE** - Legacy Anthropic integration
- `BoomiToIS-API/run.py` ❌ **DELETE** - Legacy runner
- `MuleToIS-API/run.py` ❌ **DELETE** - Legacy runner

#### **Analysis/Debug Files**
- `BoomiToIS-API/analyze_all_artifacts.py` ❌ **DELETE** - One-time analysis
- `BoomiToIS-API/compare_8d24267d_outputs.py` ❌ **DELETE** - Specific comparison
- `BoomiToIS-API/test_0d2fdc81_fix.py` ❌ **DELETE** - Specific test case
- `BoomiToIS-API/test_8d24267d_generation.py` ❌ **DELETE** - Specific test case

#### **Fixer/Repair Files**
- `BoomiToIS-API/fix_iflow.py` ❌ **DELETE** - One-time fix utility
- `BoomiToIS-API/iflow_fixer.py` ❌ **DELETE** - Legacy fixer
- `MuleToIS-API/fix_iflow.py` ❌ **DELETE** - One-time fix utility
- `MuleToIS-API/iflow_fixer.py` ❌ **DELETE** - Legacy fixer

### **📁 ROOT LEVEL FILES**

#### **Utilities**
- `enhanced_txt_to_xml_converter.py` - Text to XML converter
- `markdown_to_html_converter.py` - Markdown to HTML converter
- `iflow_deployer.py` - iFlow deployment utility

#### **Boomi API**
- `boomi-api/convert_txt_to_xml.py` - Text to XML conversion

#### **CI/CD**
- `ci-cd-deployment/deploy.py` - Deployment automation

#### **Archive (Legacy)**
- Various files in `archive/` folder - Keep archived

### **📊 SUMMARY**

**Total Python Files**: ~150+
**Core Essential**: ~25 files
**Utility/Support**: ~40 files  
**Test Files**: ~30 files
**Can Delete**: ~25 files
**Archive/Legacy**: ~30 files

### **🎯 CLEANUP RECOMMENDATIONS**

1. **Keep Core Services**: All main app.py files and core utilities
2. **Archive Test Files**: Move test files to `archive/tests/`
3. **Delete Legacy**: Remove minimal, legacy, and one-time fix files
4. **Consolidate**: Consider merging similar utilities across services
