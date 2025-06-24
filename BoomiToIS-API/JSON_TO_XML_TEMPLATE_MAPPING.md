# JSON to XML Template Mapping Reference

## 🎯 **Complete Developer Guide: JSON Components → XML Templates**

This document provides a comprehensive mapping of JSON component structures to their corresponding XML templates in the SAP Integration Suite iFlow generation system.

**📅 Last Updated:** Based on corrected `.iflw` file analysis and enhanced template implementation
**🔧 Status:** All templates updated to match SAP Integration Suite import requirements
**✅ Verified:** Templates generate components that are visible after import

---

## 📋 **Table of Contents**
1. [Request-Reply Components](#request-reply-components)
2. [Enricher & Content Modifier Components](#enricher--content-modifier-components)
3. [Groovy Script Components](#groovy-script-components)
4. [Router & Gateway Components](#router--gateway-components)
5. [Converter Components](#converter-components)
6. [Error Handling Components](#error-handling-components)
7. [Event Components](#event-components)
8. [Logging Components](#logging-components)
9. [Message Mapping Components](#message-mapping-components)
10. [SFTP Components](#sftp-components)
11. [SuccessFactors Components](#successfactors-components)
12. [SOAP Components](#soap-components)
13. [ProcessDirect Components](#processdirect-components)
14. [Call Activity Components](#call-activity-components)
15. [Template Method Reference](#template-method-reference)

---

## 🔄 **Request-Reply Components**

### **1. Request-Reply with OData Adapter (Salesforce)**

#### **JSON Input:**
```json
{
  "type": "request_reply",
  "name": "Create_Salesforce_Opportunity",
  "id": "create_opportunity",
  "receiver_adapter": {
    "type": "odata_adapter",
    "operation": "POST",
    "endpoint": "/services/data/v52.0/sobjects/Opportunity",
    "connection": "salesforce_odata_connection"
  },
  "config": {
    "endpoint_path": "/services/data/v52.0/sobjects/Opportunity",
    "method": "POST",
    "address": "https://mycompany.salesforce.com"
  }
}
```

#### **🔧 Operation Mapping:**
| JSON Operation | XML Operation | Use Case |
|---------------|---------------|----------|
| `"POST"` | `"Create(POST)"` | Creating new records |
| `"GET"` | `"Query(GET)"` | Reading/querying data |
| `"PUT"` | `"Update(PUT)"` | Full record updates |
| `"PATCH"` | `"Update(PATCH)"` | Partial record updates |
| `"DELETE"` | `"Delete(DELETE)"` | Deleting records |

#### **XML Output (Enhanced Template):**
```xml
<!-- Service Task -->
<bpmn2:serviceTask id="create_opportunity" name="Create_Salesforce_Opportunity">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>activityType</key>
      <value>ExternalCall</value>
    </ifl:property>
    <ifl:property>
      <key>cmdVariantUri</key>
      <value>ctype::FlowstepVariant/cname::ExternalCall/version::1.0.4</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:serviceTask>

<!-- OData Participant (Fixed: EndpointReceiver not EndpointRecevier) -->
<bpmn2:participant id="Participant_create_opportunity" ifl:type="EndpointReceiver" name="Create_Salesforce_Opportunity_Receiver">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>ifl:type</key>
      <value>EndpointReceiver</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:participant>

<!-- OData Message Flow (Complete SAP Integration Suite Properties) -->
<bpmn2:messageFlow id="MessageFlow_create_opportunity" name="OData" sourceRef="create_opportunity" targetRef="Participant_create_opportunity">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>ComponentType</key>
      <value>HCIOData</value>  <!-- ✅ CRITICAL: HCIOData for OData operations -->
    </ifl:property>
    <ifl:property>
      <key>operation</key>
      <value>Create(POST)</value>  <!-- ✅ MAPPED: POST → Create(POST) -->
    </ifl:property>
    <ifl:property>
      <key>resourcePath</key>
      <value>/services/data/v52.0/sobjects/Opportunity</value>  <!-- ✅ FROM: receiver_adapter.endpoint -->
    </ifl:property>
    <ifl:property>
      <key>address</key>
      <value>https://mycompany.salesforce.com</value>
    </ifl:property>
    <ifl:property>
      <key>MessageProtocol</key>
      <value>OData V2</value>
    </ifl:property>
    <ifl:property>
      <key>TransportProtocol</key>
      <value>HTTP</value>
    </ifl:property>
    <ifl:property>
      <key>cmdVariantUri</key>
      <value>ctype::AdapterVariant/cname::sap:HCIOData/tp::HTTP/mp::OData V2/direction::Receiver/version::1.25.1</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:messageFlow>
```

#### **Template Method:** `templates.odata_request_reply_pattern()`
#### **🎯 Key Improvements:**
- ✅ **Fixed Typo**: `EndpointReceiver` (not `EndpointRecevier`)
- ✅ **Operation Mapping**: JSON `"POST"` → XML `"Create(POST)"`
- ✅ **Resource Path**: Automatically extracted from `receiver_adapter.endpoint`
- ✅ **Complete Properties**: All SAP Integration Suite required properties included
- ✅ **Import Ready**: Components visible after importing into SAP Integration Suite

---

### **2. Request-Reply with HTTP Adapter (REST APIs)**

#### **JSON Input:**
```json
{
  "type": "request_reply",
  "name": "Get_Stripe_Customer_Info",
  "id": "get_customer_info",
  "receiver_adapter": {
    "type": "http_adapter",
    "operation": "GET",
    "endpoint": "/v1/customers/{customer_id}",
    "connection": "stripe_api_connection"
  },
  "config": {
    "endpoint_path": "/v1/customers/{customer_id}",
    "method": "GET",
    "address": "https://api.stripe.com/v1"
  }
}
```

#### **XML Output (Enhanced Template):**
```xml
<!-- Service Task -->
<bpmn2:serviceTask id="get_customer_info" name="Get_Stripe_Customer_Info">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>activityType</key>
      <value>ExternalCall</value>
    </ifl:property>
    <ifl:property>
      <key>cmdVariantUri</key>
      <value>ctype::FlowstepVariant/cname::ExternalCall/version::1.0.4</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:serviceTask>

<!-- HTTP Participant (Fixed: EndpointReceiver not EndpointRecevier) -->
<bpmn2:participant id="Participant_get_customer_info" ifl:type="EndpointReceiver" name="Get_Stripe_Customer_Info_Receiver">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>ifl:type</key>
      <value>EndpointReceiver</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:participant>

<!-- HTTP Message Flow (Complete SAP Integration Suite Properties) -->
<bpmn2:messageFlow id="MessageFlow_get_customer_info" name="HTTP" sourceRef="get_customer_info" targetRef="Participant_get_customer_info">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>ComponentType</key>
      <value>HTTP</value>  <!-- ✅ HTTP for REST APIs -->
    </ifl:property>
    <ifl:property>
      <key>httpMethod</key>
      <value>GET</value>  <!-- ✅ MAPPED: receiver_adapter.operation → httpMethod -->
    </ifl:property>
    <ifl:property>
      <key>address</key>
      <value>https://api.stripe.com/v1</value>
    </ifl:property>
    <ifl:property>
      <key>TransportProtocol</key>
      <value>HTTP</value>
    </ifl:property>
    <ifl:property>
      <key>MessageProtocol</key>
      <value>None</value>
    </ifl:property>
    <ifl:property>
      <key>cmdVariantUri</key>
      <value>ctype::AdapterVariant/cname::sap:HTTP/tp::HTTP/mp::None/direction::Receiver/version::1.16.2</value>
    </ifl:property>
    <ifl:property>
      <key>httpRequestTimeout</key>
      <value>60000</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:messageFlow>
```

#### **Template Method:** `templates.http_request_reply_pattern()`
#### **🎯 Key Improvements:**
- ✅ **Enhanced Template**: Uses `http_request_reply_pattern()` instead of generic fallback
- ✅ **Complete Properties**: All SAP Integration Suite HTTP adapter properties
- ✅ **Method Mapping**: JSON `receiver_adapter.operation` → XML `httpMethod`
- ✅ **Timeout Configuration**: Proper `httpRequestTimeout` settings
- ✅ **Import Ready**: Components visible after importing into SAP Integration Suite

---

### **3. Request-Reply with SFTP Adapter**

#### **JSON Input:**
```json
{
  "type": "request_reply",
  "name": "Upload_File_SFTP",
  "id": "sftp_upload",
  "receiver_adapter": {
    "type": "sftp_adapter",
    "operation": "PUT",
    "host": "sftp.example.com",
    "path": "/uploads/"
  },
  "config": {
    "method": "PUT",
    "address": "sftp://sftp.example.com",
    "host": "sftp.example.com",
    "port": "22"
  }
}
```

#### **XML Output:**
```xml
<!-- SFTP Message Flow -->
<bpmn2:messageFlow id="MessageFlow_sftp_upload" name="SFTP" sourceRef="sftp_upload" targetRef="Participant_sftp_upload">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>ComponentType</key>
      <value>SFTP</value>  <!-- ✅ SFTP for file operations -->
    </ifl:property>
    <ifl:property>
      <key>host</key>
      <value>sftp.example.com</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:messageFlow>
```

#### **Template Method:** `templates.sftp_receiver_message_flow_template()`

---

## 🔧 **Enricher & Content Modifier Components**

### **1. Content Enricher**

#### **JSON Input:**
```json
{
  "type": "enricher",
  "name": "Set_Salesforce_Description",
  "id": "set_description",
  "config": {
    "content": "${get_customer_info.response.name} has subscribed to: ${get_product_info.response.name}"
  }
}
```

#### **XML Output:**
```xml
<bpmn2:callActivity id="set_description" name="Set_Salesforce_Description">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>activityType</key>
      <value>Enricher</value>
    </ifl:property>
    <ifl:property>
      <key>bodyContent</key>
      <value>${get_customer_info.response.name} has subscribed to: ${get_product_info.response.name}</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:callActivity>
```

#### **Template Method:** `templates.content_enricher_template()`

### **2. Content Modifier**

#### **JSON Input:**
```json
{
  "type": "content_modifier",
  "name": "Set_Request_Headers",
  "id": "content_modifier_1",
  "config": {
    "property_table": "<propertyTable><property><key>customer_id</key><value>${header.customer_id}</value></property></propertyTable>",
    "header_table": "<headerTable><header><key>Authorization</key><value>Bearer ${property.access_token}</value></header></headerTable>",
    "body_type": "expression",
    "body_content": "${body}"
  }
}
```

#### **XML Output:**
```xml
<bpmn2:callActivity id="content_modifier_1" name="Set_Request_Headers">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>activityType</key>
      <value>Enricher</value>
    </ifl:property>
    <ifl:property>
      <key>propertyTable</key>
      <value>&lt;propertyTable&gt;&lt;property&gt;&lt;key&gt;customer_id&lt;/key&gt;&lt;value&gt;${header.customer_id}&lt;/value&gt;&lt;/property&gt;&lt;/propertyTable&gt;</value>
    </ifl:property>
    <ifl:property>
      <key>headerTable</key>
      <value>&lt;headerTable&gt;&lt;header&gt;&lt;key&gt;Authorization&lt;/key&gt;&lt;value&gt;Bearer ${property.access_token}&lt;/value&gt;&lt;/header&gt;&lt;/headerTable&gt;</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:callActivity>
```

#### **Template Method:** `templates.content_modifier_template()`

---

## 📜 **Groovy Script Components**

#### **JSON Input:**
```json
{
  "type": "groovy_script",
  "name": "Map_To_Salesforce_Opportunity",
  "id": "map_to_opportunity",
  "config": {
    "script": "MapToSalesforceOpportunity.groovy"
  }
}
```

#### **XML Output:**
```xml
<bpmn2:callActivity id="map_to_opportunity" name="Map_To_Salesforce_Opportunity">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>activityType</key>
      <value>Script</value>
    </ifl:property>
    <ifl:property>
      <key>subActivityType</key>
      <value>GroovyScript</value>
    </ifl:property>
    <ifl:property>
      <key>script</key>
      <value>MapToSalesforceOpportunity.groovy</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:callActivity>
```

#### **Template Method:** `templates.groovy_script_template()`

---

## 🔀 **Router & Gateway Components**

### **1. Exclusive Gateway (Router)**

#### **JSON Input:**
```json
{
  "type": "router",
  "name": "Route_By_Customer_Type",
  "id": "customer_router",
  "config": {
    "conditions": [
      {
        "condition": "${property.customer_type} = 'Premium'",
        "target": "premium_flow"
      },
      {
        "condition": "${property.customer_type} = 'Standard'",
        "target": "standard_flow"
      }
    ]
  }
}
```

#### **XML Output:**
```xml
<bpmn2:exclusiveGateway id="customer_router" name="Route_By_Customer_Type">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>gatewayType</key>
      <value>Exclusive</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:exclusiveGateway>
```

#### **Template Method:** `templates.router_template()`

---

## 🔄 **Converter Components**

### **1. JSON to XML Converter**

#### **JSON Input:**
```json
{
  "type": "json_to_xml_converter",
  "name": "Convert_JSON_to_XML",
  "id": "json_converter",
  "config": {
    "add_root_element": "true",
    "root_element_name": "root"
  }
}
```

#### **XML Output:**
```xml
<bpmn2:callActivity id="json_converter" name="Convert_JSON_to_XML">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>activityType</key>
      <value>Converter</value>
    </ifl:property>
    <ifl:property>
      <key>converterType</key>
      <value>JSONtoXMLConverter</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:callActivity>
```

#### **Template Method:** `templates.json_to_xml_converter_template()`

---

## ⚠️ **Error Handling Components**

#### **JSON Input:**
```json
{
  "type": "exception_subprocess",
  "name": "Handle_Integration_Error",
  "id": "error_handler",
  "config": {
    "trigger": "any_error",
    "script": "LogErrorDetails.groovy"
  }
}
```

#### **XML Output:**
```xml
<bpmn2:subProcess id="error_handler" name="Handle_Integration_Error" triggeredByEvent="true">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>subProcessType</key>
      <value>Exception</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:subProcess>
```

#### **Template Method:** `templates.exception_subprocess_template()`

---

## 🎯 **Event Components**

### **1. Message Start Event**

#### **JSON Input:**
```json
{
  "type": "message_start_event",
  "name": "Start_Integration",
  "id": "start_event_1",
  "config": {
    "message_name": "StartMessage"
  }
}
```

#### **XML Output:**
```xml
<bpmn2:startEvent id="start_event_1" name="Start_Integration">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>componentVersion</key>
      <value>1.0</value>
    </ifl:property>
    <ifl:property>
      <key>cmdVariantUri</key>
      <value>ctype::FlowstepVariant/cname::MessageStartEvent/version::1.0</value>
    </ifl:property>
  </bpmn2:extensionElements>
  <bpmn2:outgoing>SequenceFlow_1</bpmn2:outgoing>
  <bpmn2:messageEventDefinition id="MessageEventDefinition_start_event_1"/>
</bpmn2:startEvent>
```

#### **Template Method:** `templates.message_start_event_template()`

### **2. Message End Event**

#### **JSON Input:**
```json
{
  "type": "message_end_event",
  "name": "End_Integration",
  "id": "end_event_1",
  "config": {
    "message_name": "EndMessage"
  }
}
```

#### **XML Output:**
```xml
<bpmn2:endEvent id="end_event_1" name="End_Integration">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>componentVersion</key>
      <value>1.0</value>
    </ifl:property>
  </bpmn2:extensionElements>
  <bpmn2:incoming>SequenceFlow_Last</bpmn2:incoming>
  <bpmn2:messageEventDefinition id="MessageEventDefinition_end_event_1"/>
</bpmn2:endEvent>
```

#### **Template Method:** `templates.message_end_event_template()`

### **3. Timer Start Event**

#### **JSON Input:**
```json
{
  "type": "timer_start_event",
  "name": "Scheduled_Start",
  "id": "timer_start_1",
  "config": {
    "schedule_key": "daily_schedule"
  }
}
```

#### **XML Output:**
```xml
<bpmn2:startEvent id="timer_start_1" name="Scheduled_Start">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>componentVersion</key>
      <value>1.0</value>
    </ifl:property>
    <ifl:property>
      <key>scheduleKey</key>
      <value>daily_schedule</value>
    </ifl:property>
  </bpmn2:extensionElements>
  <bpmn2:outgoing>SequenceFlow_1</bpmn2:outgoing>
  <bpmn2:timerEventDefinition id="TimerEventDefinition_timer_start_1"/>
</bpmn2:startEvent>
```

#### **Template Method:** `templates.timer_start_event_template()`

---

## 📝 **Logging Components**

### **1. Write to Log**

#### **JSON Input:**
```json
{
  "type": "write_to_log",
  "name": "Log_Request_Details",
  "id": "logger_1",
  "config": {
    "log_level": "Info",
    "message": "Processing request for customer: ${property.customer_id}"
  }
}
```

#### **XML Output:**
```xml
<bpmn2:callActivity id="logger_1" name="Log_Request_Details">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>activityType</key>
      <value>Script</value>
    </ifl:property>
    <ifl:property>
      <key>subActivityType</key>
      <value>WriteToLog</value>
    </ifl:property>
    <ifl:property>
      <key>logLevel</key>
      <value>Info</value>
    </ifl:property>
    <ifl:property>
      <key>logMessage</key>
      <value>Processing request for customer: ${property.customer_id}</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:callActivity>
```

#### **Template Method:** `templates.write_to_log_template()`

---

## 🗺️ **Message Mapping Components**

### **1. Message Mapping**

#### **JSON Input:**
```json
{
  "type": "message_mapping",
  "name": "Transform_Customer_Data",
  "id": "mapping_1",
  "config": {
    "source_type": "XML",
    "target_type": "JSON",
    "mapping_name": "CustomerTransformation.mmap"
  }
}
```

#### **XML Output:**
```xml
<bpmn2:callActivity id="mapping_1" name="Transform_Customer_Data">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>activityType</key>
      <value>Mapping</value>
    </ifl:property>
    <ifl:property>
      <key>sourceType</key>
      <value>XML</value>
    </ifl:property>
    <ifl:property>
      <key>targetType</key>
      <value>JSON</value>
    </ifl:property>
    <ifl:property>
      <key>mappingName</key>
      <value>CustomerTransformation.mmap</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:callActivity>
```

#### **Template Method:** `templates.message_mapping_template()`

---

## 📁 **SFTP Components**

### **1. SFTP Request-Reply**

#### **JSON Input:**
```json
{
  "type": "request_reply",
  "name": "Upload_File_SFTP",
  "id": "sftp_upload",
  "receiver_adapter": {
    "type": "sftp_adapter",
    "operation": "PUT",
    "host": "sftp.example.com",
    "path": "/uploads/",
    "filename": "customer_data.xml"
  },
  "config": {
    "address": "sftp://sftp.example.com",
    "method": "PUT",
    "host": "sftp.example.com",
    "port": "22"
  }
}
```

#### **XML Output:**
```xml
<!-- SFTP Participant -->
<bpmn2:participant id="Participant_sftp_upload" ifl:type="EndpointReceiver" name="SFTP_Server">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>ifl:type</key>
      <value>EndpointReceiver</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:participant>

<!-- SFTP Message Flow -->
<bpmn2:messageFlow id="MessageFlow_sftp_upload" name="SFTP" sourceRef="sftp_upload" targetRef="Participant_sftp_upload">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>ComponentType</key>
      <value>SFTP</value>
    </ifl:property>
    <ifl:property>
      <key>host</key>
      <value>sftp.example.com</value>
    </ifl:property>
    <ifl:property>
      <key>port</key>
      <value>22</value>
    </ifl:property>
    <ifl:property>
      <key>path</key>
      <value>/uploads/</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:messageFlow>
```

#### **Template Method:** `templates.sftp_receiver_message_flow_template()`

---

## 🏢 **SuccessFactors Components**

### **1. SuccessFactors Request-Reply**

#### **JSON Input:**
```json
{
  "type": "request_reply",
  "name": "Query_SuccessFactors_Users",
  "id": "sf_query",
  "receiver_adapter": {
    "type": "successfactors_adapter",
    "operation": "GET",
    "endpoint": "/odata/v2/User",
    "connection": "successfactors_connection"
  },
  "config": {
    "address": "https://api.successfactors.com",
    "method": "GET",
    "adapter_type": "ODATA"
  }
}
```

#### **XML Output:**
```xml
<!-- SuccessFactors Message Flow -->
<bpmn2:messageFlow id="MessageFlow_sf_query" name="SuccessFactors" sourceRef="sf_query" targetRef="Participant_sf_query">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>ComponentType</key>
      <value>SuccessFactors</value>
    </ifl:property>
    <ifl:property>
      <key>address</key>
      <value>https://api.successfactors.com/odata/v2/User</value>
    </ifl:property>
    <ifl:property>
      <key>operation</key>
      <value>Query(GET)</value>
    </ifl:property>
    <ifl:property>
      <key>authenticationMethod</key>
      <value>OAuth</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:messageFlow>
```

#### **Template Method:** `templates.successfactors_receiver_message_flow_template()`

---

## 🧼 **SOAP Components**

### **1. SOAP Request-Reply**

#### **JSON Input:**
```json
{
  "type": "request_reply",
  "name": "Call_SOAP_Service",
  "id": "soap_call",
  "receiver_adapter": {
    "type": "soap_adapter",
    "operation": "POST",
    "endpoint": "/soap/CustomerService",
    "connection": "soap_connection"
  },
  "config": {
    "address": "https://api.example.com/soap/CustomerService",
    "method": "POST",
    "soap_action": "getCustomerDetails"
  }
}
```

#### **XML Output:**
```xml
<bpmn2:messageFlow id="MessageFlow_soap_call" name="SOAP" sourceRef="soap_call" targetRef="Participant_soap_call">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>ComponentType</key>
      <value>SOAP</value>
    </ifl:property>
    <ifl:property>
      <key>address</key>
      <value>https://api.example.com/soap/CustomerService</value>
    </ifl:property>
    <ifl:property>
      <key>TransportProtocol</key>
      <value>HTTP</value>
    </ifl:property>
    <ifl:property>
      <key>cmdVariantUri</key>
      <value>ctype::AdapterVariant/cname::sap:SOAP/tp::HTTP/mp::Plain SOAP/direction::Receiver/version::1.9.0</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:messageFlow>
```

#### **Template Method:** `templates.soap_receiver_template()`

---

## 🔗 **ProcessDirect Components**

### **1. ProcessDirect Request-Reply**

#### **JSON Input:**
```json
{
  "type": "request_reply",
  "name": "Call_ProcessDirect",
  "id": "process_direct_call",
  "receiver_adapter": {
    "type": "process_direct_adapter",
    "operation": "POST",
    "endpoint": "/process/CustomerValidation",
    "connection": "process_direct_connection"
  },
  "config": {
    "address": "ProcessDirect://CustomerValidation",
    "method": "POST"
  }
}
```

#### **XML Output:**
```xml
<bpmn2:messageFlow id="MessageFlow_process_direct_call" name="ProcessDirect" sourceRef="process_direct_call" targetRef="Participant_process_direct_call">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>ComponentType</key>
      <value>ProcessDirect</value>
    </ifl:property>
    <ifl:property>
      <key>address</key>
      <value>ProcessDirect://CustomerValidation</value>
    </ifl:property>
    <ifl:property>
      <key>cmdVariantUri</key>
      <value>ctype::AdapterVariant/cname::sap:ProcessDirect/version::1.2.0</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:messageFlow>
```

#### **Template Method:** `templates.process_direct_template()`

---

## 📞 **Call Activity Components**

### **1. Call Activity**

#### **JSON Input:**
```json
{
  "type": "call_activity",
  "name": "Call_Sub_Process",
  "id": "call_activity_1",
  "config": {
    "activity_type": "Process",
    "called_element": "SubProcessValidation"
  }
}
```

#### **XML Output:**
```xml
<bpmn2:callActivity id="call_activity_1" name="Call_Sub_Process">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>activityType</key>
      <value>Process</value>
    </ifl:property>
    <ifl:property>
      <key>calledElement</key>
      <value>SubProcessValidation</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:callActivity>
```

#### **Template Method:** `templates.call_activity_template()`

---

## 🔄 **Additional Converter Components**

### **2. XML to JSON Converter**

#### **JSON Input:**
```json
{
  "type": "xml_to_json_converter",
  "name": "Convert_XML_to_JSON",
  "id": "xml_converter",
  "config": {
    "suppress_json_root": "false",
    "array_node_optional": "true"
  }
}
```

#### **XML Output:**
```xml
<bpmn2:callActivity id="xml_converter" name="Convert_XML_to_JSON">
  <bpmn2:extensionElements>
    <ifl:property>
      <key>activityType</key>
      <value>Converter</value>
    </ifl:property>
    <ifl:property>
      <key>converterType</key>
      <value>XMLtoJSONConverter</value>
    </ifl:property>
    <ifl:property>
      <key>suppressJsonRoot</key>
      <value>false</value>
    </ifl:property>
  </bpmn2:extensionElements>
</bpmn2:callActivity>
```

#### **Template Method:** `templates.xml_to_json_converter_template()`

---

## 🎯 **Critical Detection Rules (Enhanced)**

### **🔧 Primary Detection: Receiver Adapter Type**

| JSON receiver_adapter.type | XML ComponentType | Template Method | Operation Mapping |
|----------------------------|-------------------|-----------------|-------------------|
| `"odata_adapter"` | `HCIOData` | `odata_request_reply_pattern()` | `POST` → `Create(POST)` |
| `"http_adapter"` | `HTTP` | `http_request_reply_pattern()` | `GET` → `httpMethod: GET` |
| `"sftp_adapter"` | `SFTP` | `sftp_receiver_message_flow_template()` | `PUT` → `SFTP PUT` |
| `"successfactors_adapter"` | `SuccessFactors` | `successfactors_receiver_message_flow_template()` | `GET` → `Query(GET)` |
| `"soap_adapter"` | `SOAP` | `soap_receiver_template()` | `POST` → `SOAP Action` |
| `"process_direct_adapter"` | `ProcessDirect` | `process_direct_template()` | `POST` → `ProcessDirect` |

### **🔍 Secondary Detection: Address-Based Fallback**

| Address Pattern | Detected As | Template Used | Notes |
|----------------|-------------|---------------|-------|
| `"salesforce.com"` | OData | `odata_request_reply_pattern()` | Auto-detects Salesforce |
| `"sftp://"` | SFTP | `sftp_receiver_message_flow_template()` | Protocol-based detection |
| `"successfactors"` | SuccessFactors | `successfactors_receiver_message_flow_template()` | Domain-based detection |
| `"ProcessDirect://"` | ProcessDirect | `process_direct_template()` | Internal SAP calls |
| Other HTTPS | HTTP | `http_request_reply_pattern()` | Enhanced HTTP template |

### **⚡ Detection Logic Flow:**
```
1. Check receiver_adapter.type (PRIMARY)
   ├── odata_adapter → HCIOData template
   ├── http_adapter → HTTP template
   ├── sftp_adapter → SFTP template
   └── [other adapters] → Specific templates

2. If no receiver_adapter, check address (FALLBACK)
   ├── Contains "salesforce" → OData template
   ├── Contains "sftp://" → SFTP template
   └── Default → HTTP template

3. Map operations (JSON → XML)
   ├── POST → Create(POST) [OData] / httpMethod: POST [HTTP]
   ├── GET → Query(GET) [OData] / httpMethod: GET [HTTP]
   └── [other operations] → Appropriate XML format
```

---

## 📚 **Template Method Reference**

| Component Type | Template Method | File Location |
|---------------|----------------|---------------|
| **Request-Reply Patterns** | | |
| OData Request-Reply | `odata_request_reply_pattern()` | `enhanced_iflow_templates.py:1099` |
| HTTP Request-Reply | `request_reply_template()` | `enhanced_iflow_templates.py:1069` |
| SFTP Receiver | `sftp_receiver_message_flow_template()` | `enhanced_iflow_templates.py:1860` |
| SuccessFactors Receiver | `successfactors_receiver_message_flow_template()` | `enhanced_iflow_templates.py:1967` |
| SOAP Receiver | `soap_receiver_template()` | `enhanced_iflow_templates.py:441` |
| ProcessDirect | `process_direct_template()` | `enhanced_iflow_templates.py:549` |
| **Content Processing** | | |
| Content Enricher | `content_enricher_template()` | `enhanced_iflow_templates.py:728` |
| Content Modifier | `content_modifier_template()` | `enhanced_iflow_templates.py:673` |
| Groovy Script | `groovy_script_template()` | `enhanced_iflow_templates.py:1572` |
| Message Mapping | `message_mapping_template()` | `enhanced_iflow_templates.py:918` |
| **Flow Control** | | |
| Router/Gateway | `router_template()` | `enhanced_iflow_templates.py:783` |
| Call Activity | `call_activity_template()` | `enhanced_iflow_templates.py:814` |
| Exception Subprocess | `exception_subprocess_template()` | `enhanced_iflow_templates.py:841` |
| **Events** | | |
| Message Start Event | `message_start_event_template()` | `enhanced_iflow_templates.py:960` |
| Message End Event | `message_end_event_template()` | `enhanced_iflow_templates.py:979` |
| Timer Start Event | `timer_start_event_template()` | `enhanced_iflow_templates.py:998` |
| **Converters** | | |
| JSON to XML Converter | `json_to_xml_converter_template()` | `enhanced_iflow_templates.py:600+` |
| XML to JSON Converter | `xml_to_json_converter_template()` | `enhanced_iflow_templates.py:600+` |
| **Logging & Utilities** | | |
| Write to Log | `write_to_log_template()` | `enhanced_iflow_templates.py:878` |
| Participant | `participant_template()` | `enhanced_iflow_templates.py:81` |
| EDMX Metadata | `edmx_template()` | `enhanced_iflow_templates.py:242` |

---

## ✅ **Enhanced Validation Checklist**

When creating JSON components, ensure:

### **1. Request-Reply Components (CRITICAL):**
   - ✅ **Always include `receiver_adapter` object** - Required for proper template selection
   - ✅ **Set correct `receiver_adapter.type`** - Primary detection mechanism:
     - `"odata_adapter"` for Salesforce, SAP systems
     - `"http_adapter"` for REST APIs (Stripe, etc.)
     - `"sftp_adapter"` for file operations
   - ✅ **Include `receiver_adapter.operation`** - Maps to XML operation format
   - ✅ **Set `receiver_adapter.endpoint`** - Becomes XML `resourcePath`
   - ✅ **Include `config.address`** - Base URL for the service
   - ✅ **Match `config.method` with `receiver_adapter.operation`** - Consistency check

### **2. Operation Mapping Validation:**
   - ✅ **OData Operations:**
     - `"POST"` → `"Create(POST)"` for creating records
     - `"GET"` → `"Query(GET)"` for reading data
     - `"PUT"/"PATCH"` → `"Update(PUT/PATCH)"` for updates
     - `"DELETE"` → `"Delete(DELETE)"` for deletions
   - ✅ **HTTP Operations:**
     - `"GET"/"POST"/"PUT"/"DELETE"` → `"httpMethod: [OPERATION]"`

### **3. Component IDs & Naming:**
   - ✅ **Use unique IDs** across all components
   - ✅ **Follow naming convention:** `component_type_description`
   - ✅ **Avoid special characters** in IDs (use underscores)

### **4. Required Fields by Component Type:**
   - ✅ **All components:** `type`, `name`, `id`
   - ✅ **Request-reply:** `receiver_adapter`, `config` (with `address`)
   - ✅ **Scripts:** `config.script`
   - ✅ **Enrichers:** `config.content` or `config.property_table`
   - ✅ **Routers:** `config.conditions`

### **5. Template Compatibility:**
   - ✅ **Verify adapter type** matches intended system (OData for Salesforce, HTTP for REST)
   - ✅ **Check operation format** follows SAP Integration Suite conventions
   - ✅ **Ensure resource paths** are properly formatted
   - ✅ **Test import** into SAP Integration Suite to verify visibility

---

## 🔍 **Advanced Mapping Examples**

### **Complex Salesforce Integration Pattern**

#### **Complete JSON Flow:**
```json
{
  "process_name": "Stripe to Salesforce Integration",
  "endpoints": [
    {
      "method": "POST",
      "path": "/stripe-to-salesforce",
      "components": [
        {
          "type": "enricher",
          "name": "Set_Customer_Context",
          "id": "enricher_1",
          "config": {
            "content": "Processing customer: ${header.customer_id}"
          }
        },
        {
          "type": "request_reply",
          "name": "Get_Stripe_Customer",
          "id": "stripe_call",
          "receiver_adapter": {
            "type": "http_adapter",
            "operation": "GET",
            "endpoint": "/v1/customers/{id}",
            "connection": "stripe_connection"
          },
          "config": {
            "address": "https://api.stripe.com/v1",
            "method": "GET"
          }
        },
        {
          "type": "groovy_script",
          "name": "Transform_To_Salesforce",
          "id": "transform_1",
          "config": {
            "script": "StripeToSalesforceMapper.groovy"
          }
        },
        {
          "type": "request_reply",
          "name": "Create_Salesforce_Account",
          "id": "salesforce_call",
          "receiver_adapter": {
            "type": "odata_adapter",
            "operation": "POST",
            "endpoint": "/services/data/v52.0/sobjects/Account",
            "connection": "salesforce_odata_connection"
          },
          "config": {
            "address": "https://mycompany.salesforce.com",
            "method": "POST"
          }
        }
      ],
      "sequence": ["enricher_1", "stripe_call", "transform_1", "salesforce_call"]
    }
  ]
}
```

#### **Generated XML Components:**
1. **Enricher** → `content_enricher_template()` → `<bpmn2:callActivity activityType="Enricher">`
2. **Stripe Call** → Generic HTTP → `<bpmn2:messageFlow ComponentType="HTTP">`
3. **Transform** → `groovy_script_template()` → `<bpmn2:callActivity activityType="Script">`
4. **Salesforce Call** → `odata_request_reply_pattern()` → `<bpmn2:messageFlow ComponentType="HCIOData">`

---

## 🚨 **Common Pitfalls & Solutions**

### **❌ WRONG: Standalone OData Component**
```json
{
  "type": "odata",  // ❌ This will be auto-fixed but avoid
  "name": "Query_Salesforce",
  "config": {
    "address": "https://mycompany.salesforce.com",
    "operation": "Query(GET)"
  }
}
```

### **✅ CORRECT: Request-Reply with OData Adapter**
```json
{
  "type": "request_reply",  // ✅ Always use request_reply
  "name": "Query_Salesforce",
  "receiver_adapter": {     // ✅ Always include receiver_adapter
    "type": "odata_adapter",
    "operation": "GET"
  },
  "config": {
    "address": "https://mycompany.salesforce.com",
    "method": "GET"
  }
}
```

### **❌ WRONG: Missing Receiver Adapter**
```json
{
  "type": "request_reply",
  "name": "API_Call",
  "config": {              // ❌ Missing receiver_adapter
    "address": "https://api.example.com",
    "method": "POST"
  }
}
```

### **✅ CORRECT: Complete Request-Reply**
```json
{
  "type": "request_reply",
  "name": "API_Call",
  "receiver_adapter": {    // ✅ Required receiver_adapter
    "type": "http_adapter",
    "operation": "POST"
  },
  "config": {
    "address": "https://api.example.com",
    "method": "POST"
  }
}
```

---

## 🎯 **Template Selection Logic**

### **Decision Tree for Request-Reply Components:**

```
request_reply component
├── receiver_adapter.type == "odata_adapter"?
│   ├── YES → odata_request_reply_pattern() → HCIOData
│   └── NO → Check address/config
├── address contains "sftp://" OR protocol == "SFTP"?
│   ├── YES → sftp_receiver_message_flow_template() → SFTP
│   └── NO → Check for SuccessFactors
├── address contains "successfactors" OR adapter_type == "ODATA"?
│   ├── YES → successfactors_receiver_message_flow_template() → SuccessFactors
│   └── NO → Generic HTTP receiver → HTTP
```

---

## 📊 **Component Type Summary Table**

| JSON Type | Required Fields | Optional Fields | XML Template | ComponentType |
|-----------|----------------|-----------------|--------------|---------------|
| `request_reply` | `receiver_adapter`, `config.address` | `config.method` | Varies by adapter | `HCIOData`/`HTTP`/`SFTP`/`SuccessFactors` |
| `enricher` | `config.content` | `property_table` | `content_enricher_template()` | `Enricher` |
| `content_modifier` | - | `property_table`, `header_table` | `content_modifier_template()` | `Enricher` |
| `groovy_script` | `config.script` | `config.script_function` | `groovy_script_template()` | `Script` |
| `router` | `config.conditions` | `config.default_route` | `router_template()` | `ExclusiveGateway` |
| `json_to_xml_converter` | - | `config.root_element_name` | `json_to_xml_converter_template()` | `Converter` |
| `xml_to_json_converter` | - | `config.suppress_json_root` | `xml_to_json_converter_template()` | `Converter` |
| `exception_subprocess` | `config.trigger` | `config.script` | `exception_subprocess_template()` | `SubProcess` |
| `message_start_event` | - | `config.message_name` | `message_start_event_template()` | `StartEvent` |
| `message_end_event` | - | `config.message_name` | `message_end_event_template()` | `EndEvent` |
| `timer_start_event` | `config.schedule_key` | - | `timer_start_event_template()` | `StartEvent` |
| `write_to_log` | `config.log_level` | `config.message` | `write_to_log_template()` | `Script` |
| `message_mapping` | `config.mapping_name` | `config.source_type`, `config.target_type` | `message_mapping_template()` | `Mapping` |
| `call_activity` | `config.activity_type` | `config.called_element` | `call_activity_template()` | `CallActivity` |

---

## 🔧 **Developer Quick Reference**

### **For Salesforce Operations:**
```json
{
  "type": "request_reply",
  "receiver_adapter": {"type": "odata_adapter", "operation": "POST|GET|PUT|DELETE"},
  "config": {"address": "https://*.salesforce.com", "method": "POST|GET|PUT|DELETE"}
}
```
**→ Generates:** `HCIOData` message flow with OData participant

### **For REST API Calls:**
```json
{
  "type": "request_reply",
  "receiver_adapter": {"type": "http_adapter", "operation": "POST|GET|PUT|DELETE"},
  "config": {"address": "https://api.example.com", "method": "POST|GET|PUT|DELETE"}
}
```
**→ Generates:** `HTTP` message flow with generic participant

### **For File Operations:**
```json
{
  "type": "request_reply",
  "receiver_adapter": {"type": "sftp_adapter", "operation": "PUT|GET"},
  "config": {"address": "sftp://server.com", "host": "server.com", "port": "22"}
}
```
**→ Generates:** `SFTP` message flow with SFTP participant

---

## 🚀 **Recent Enhancements & Fixes**

### **✅ Fixed Issues (Based on d0a449df Analysis):**

1. **🔧 OData Adapter Detection Fixed**
   - **Problem**: `request_reply` components with `"receiver_adapter": {"type": "odata_adapter"}` were falling back to generic HTTP
   - **Solution**: Enhanced detection logic to properly identify `odata_adapter` type
   - **Result**: Salesforce operations now correctly generate `HCIOData` components

2. **🔧 Participant Typo Fixed**
   - **Problem**: Templates had typo `"EndpointRecevier"` instead of `"EndpointReceiver"`
   - **Solution**: Fixed all template participant types
   - **Result**: Proper SAP Integration Suite compatibility

3. **🔧 Operation Mapping Enhanced**
   - **Problem**: JSON `"operation": "POST"` was not mapping to correct OData format
   - **Solution**: Added operation mapping logic: `POST` → `Create(POST)`
   - **Result**: Correct OData operations in generated XML

4. **🔧 Resource Path Extraction**
   - **Problem**: `resourcePath` was empty in generated XML
   - **Solution**: Extract from `receiver_adapter.endpoint`
   - **Result**: Proper resource paths for OData operations

5. **🔧 Enhanced HTTP Template**
   - **Problem**: Generic HTTP receiver had minimal properties
   - **Solution**: Created `http_request_reply_pattern()` with complete SAP properties
   - **Result**: HTTP adapters now visible after import

### **📊 Template Improvements:**

| Template | Before | After |
|----------|--------|-------|
| **OData** | Basic properties, typo in participant | Complete SAP properties, correct operation mapping |
| **HTTP** | Generic fallback | Enhanced template with full HTTP adapter properties |
| **Detection** | Address-based only | Primary: receiver_adapter.type, Fallback: address |
| **Operations** | Static values | Dynamic mapping from JSON to XML format |

### **🎯 Verification Status:**

- ✅ **d0a449df Case**: All components now generate correctly
- ✅ **Import Testing**: Components visible in SAP Integration Suite after import
- ✅ **Operation Mapping**: JSON operations correctly map to XML format
- ✅ **Template Completeness**: All required SAP Integration Suite properties included

This comprehensive mapping ensures that your JSON components generate the correct SAP Integration Suite XML templates that are fully compatible with import and visible in the design environment! 🚀
