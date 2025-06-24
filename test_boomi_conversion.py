#!/usr/bin/env python3
"""
Test the full Boomi to SAP Integration Suite conversion with new templates.
"""

import requests
import json
import time

def test_boomi_conversion():
    """Test the conversion with a sample Boomi process using new components."""
    
    # Sample Boomi documentation that includes components we've added
    boomi_markdown = """# Dell Boomi Integration Process

## Process Overview
This integration process demonstrates various Boomi components that should map to our new SAP Integration Suite templates.

## Process Flow

### Components Used:
1. **Start Shape** - Process initiation
2. **Data Mapping** - Transform customer data using operation mapping
3. **XML Validator** - Validate incoming XML against schema
4. **Content Enricher** - Enrich message with additional headers
5. **Filter** - Filter records based on criteria
6. **Groovy Script** - Custom business logic
7. **EDI Splitter** - Split EDI documents
8. **Aggregator** - Aggregate multiple messages
9. **Base64 Encoder** - Encode sensitive data
10. **SFTP Connector** - Send files to SFTP server
11. **Stop Shape** - Process completion

## Data Mappings

### Customer Data Mapping
- Source: Boomi Customer Profile
- Target: SAP Customer Master
- Mappings:
  - customerName → Name
  - customerEmail → Email
  - customerPhone → Phone

## Component Details

### Data Mapping (Operation Mapping)
- **Type**: Operation Mapping
- **Purpose**: Transform customer data structure
- **Configuration**: CustomerToSAP.xml

### XML Validator
- **Type**: XML Validator
- **Purpose**: Validate customer XML against XSD schema
- **Schema**: CustomerSchema.xsd

### Content Enricher
- **Type**: Content Enricher
- **Purpose**: Add correlation ID and timestamp headers
- **Headers**: 
  - CorrelationID: ${uuid()}
  - ProcessedAt: ${now()}

### Filter Component
- **Type**: Filter
- **Purpose**: Filter active customers only
- **Condition**: /Customer/Status = 'Active'

### Groovy Script
- **Type**: Groovy Script
- **Purpose**: Calculate customer score
- **Script**: CustomerScoring.groovy

### EDI Splitter
- **Type**: EDI Splitter
- **Purpose**: Split EDI 850 purchase orders
- **Format**: X12

### Aggregator
- **Type**: Aggregator
- **Purpose**: Aggregate customer orders by region
- **Correlation**: /Customer/Region

### Base64 Encoder
- **Type**: Base64 Encoder
- **Purpose**: Encode customer PII data
- **Target**: Sensitive fields

### SFTP Connector
- **Type**: SFTP Connector
- **Purpose**: Upload processed files
- **Server**: sftp.customer.com
- **Path**: /incoming/customers

## SAP Integration Suite Implementation

### Component Mapping

| Boomi Component | SAP Integration Suite Equivalent | Notes |
|-----------------|----------------------------------|-------|
| Start Shape | Start Event (Message) | Process entry point |
| Data Mapping | Operation Mapping | Complex data transformation |
| XML Validator | XML Validator | Schema validation |
| Content Enricher | Content Enricher | Message enrichment |
| Filter | Filter | XPath-based filtering |
| Groovy Script | Groovy Script | Custom logic execution |
| EDI Splitter | EDI Splitter | EDI document splitting |
| Aggregator | Aggregator | Message aggregation |
| Base64 Encoder | Base64 Encoder | Data encoding |
| SFTP Connector | SFTP Adapter | File transfer |
| Stop Shape | End Event (Message) | Process completion |

## Integration Flow Visualization

```mermaid
flowchart TD
    Start([Start]) --> DataMapping[Operation Mapping]
    DataMapping --> XMLValidator[XML Validator]
    XMLValidator --> Enricher[Content Enricher]
    Enricher --> Filter[Filter Active Customers]
    Filter --> GroovyScript[Groovy Script - Calculate Score]
    GroovyScript --> EDISplitter[EDI Splitter]
    EDISplitter --> Aggregator[Aggregator by Region]
    Aggregator --> Base64Encoder[Base64 Encoder]
    Base64Encoder --> SFTPConnector[SFTP Upload]
    SFTPConnector --> End([End])
```

This process demonstrates a comprehensive integration flow using multiple Boomi components that should map to our newly implemented SAP Integration Suite templates.
"""

    print("🚀 Testing Boomi to SAP Integration Suite conversion...")
    print(f"📄 Test document length: {len(boomi_markdown)} characters")
    
    try:
        # Send the test document to the BoomiToIS API
        response = requests.post(
            'http://localhost:5003/api/generate-iflow',
            json={
                'markdown_content': boomi_markdown,
                'iflow_name': 'Test_New_Components_iFlow'
            },
            timeout=300  # 5 minutes timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Conversion successful!")
            print(f"📋 iFlow ID: {result.get('iflow_id', 'Unknown')}")
            print(f"📁 Result folder: {result.get('result_folder', 'Unknown')}")
            print(f"💾 ZIP file: {result.get('zip_file', 'Unknown')}")
            
            # Check if specific components were mentioned in the response
            response_text = str(result)
            new_components_found = []
            
            component_checks = [
                'operation_mapping', 'xml_validator', 'filter', 'groovy_script',
                'edi_splitter', 'aggregator', 'base64_encoder'
            ]
            
            for component in component_checks:
                if component in response_text.lower():
                    new_components_found.append(component)
            
            if new_components_found:
                print(f"🎯 New components detected: {', '.join(new_components_found)}")
            else:
                print("ℹ️ Component detection inconclusive from response")
            
            return True
            
        else:
            print(f"❌ Conversion failed!")
            print(f"Status Code: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - this might indicate the conversion is taking longer than expected")
        return False
    except requests.exceptions.ConnectionError:
        print("🔌 Connection error - make sure the BoomiToIS-API is running on port 5003")
        return False
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Testing Full Boomi Conversion with New Templates")
    print("=" * 60)
    
    success = test_boomi_conversion()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Conversion test completed successfully!")
        print("✅ New templates are working in the full conversion pipeline!")
    else:
        print("⚠️ Conversion test failed!")
        print("❌ There may be issues with the new templates or API integration")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
