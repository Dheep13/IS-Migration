# Enhanced Process Flow Example

This shows how the new enhanced process flow formatting will look:

---

## **Process Flow Overview**

### **Flow Steps**

---

#### **Step 5: Transform SAP Response to SF Update (shape10)**

**Component Type:** Map/Transform

**Purpose:** Transforms the SAP BAPI response JSON into Salesforce Account update XML format, mapping SAP customer number to Salesforce Account fields for the update operation.

**Configuration Details:**

- **Input Profile:** SAP BAPI Customer Creation Response
- **Output Profile:** Salesforce Account Update Request
- **Transformation Logic:** Maps SAP customer number to Salesforce Account fields
- **Function Steps:** Data type conversions and field mapping transformations

**Input Data Structure:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| CustomerNumber | String | SAP-generated customer number from BAPI response |
| CreationStatus | String | Success/failure status of customer creation |
| ResponseMessage | String | Detailed response message from SAP |

**Output Data Structure:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| Account.Id | String | Salesforce Account unique identifier |
| Account.CustomerNumber__c | String | Custom field to store SAP customer number |
| Account.SAPStatus__c | String | Integration status tracking field |

**Field Mappings:**

| Source Field | Target Field | Data Type | Business Purpose |
|--------------|--------------|-----------|------------------|
| Customer.CompanyName | BAPI_CUSTOMER.NAME | String | Maps company name from Salesforce to SAP customer master |
| Customer.BillingStreet | BAPI_CUSTOMER.STREET | String | Maps billing street address for customer creation |
| Customer.BillingCity | BAPI_CUSTOMER.CITY | String | Maps billing city for customer address |
| Customer.BillingState | BAPI_CUSTOMER.REGION | String | Maps billing state/region for customer address |
| Customer.BillingPostalCode | BAPI_CUSTOMER.POSTAL_CODE | String | Maps billing postal code for customer address |
| Customer.BillingCountry | BAPI_CUSTOMER.COUNTRY | String | Maps billing country for customer address |

**Data Flow:**

- **Input:** SAP BAPI response JSON containing customer number and status
- **Processing:** Field mapping and data transformation from JSON to XML format
- **Output:** Salesforce Account update XML with mapped customer data

---

#### **Step 6: Check If New Account (shape25)**

> **Component Type:** Decision

**Purpose:** Evaluates if the account is new based on account status and routes flow accordingly to either create new account or update existing account.

**Configuration Details:**
- **Decision Criteria:** Account status field evaluation
- **Branch Logic:** Routes to create path for new accounts, update path for existing
- **Routing Rules:** Based on account existence and status flags

**Data Flow:**
- **Input:** Transformed Salesforce update data with account information
- **Processing:** Decision logic applied to determine account status
- **Output:** Routing decision directing flow to appropriate next step

---

#### **Step 7a: Update Salesforce Account (shape5)**

> **Component Type:** Connector Action

**Purpose:** Updates existing Salesforce Account with SAP customer number and integration status information.

**Configuration Details:**
- **Connector Type:** Salesforce
- **Operation:** Update
- **Target Object:** Account
- **Authentication:** OAuth 2.0 with refresh token
- **Error Handling:** Retry logic with exponential backoff

**Data Flow:**
- **Input:** Salesforce Account update XML with customer data
- **Processing:** Salesforce update operation performed via REST API
- **Output:** Salesforce update response with success/failure status

---

#### **Step 7b: Handle Existing Account (shape21)**

> **Component Type:** Information

**Purpose:** Handles the case when account already exists, providing information about existing account and logging the duplicate scenario.

**Configuration Details:**
- **Information Type:** Account existence notification
- **Logging Level:** INFO
- **Message Format:** Structured log entry with account details

**Data Flow:**
- **Input:** Account data for existing account scenario
- **Processing:** Information logging and duplicate handling logic
- **Output:** Information message and process continuation signal

---

#### **Step 8: End Events (shape4 and shape22)**

> **Component Type:** End Event

**Purpose:** Completes the process flow with appropriate success or failure handling based on the integration outcome.

**Configuration Details:**
- **Completion Type:** Multiple end points based on flow path
- **Final Actions:** Process completion logging and cleanup
- **Continuation Settings:** Process stops with status indication

**Data Flow:**
- **Input:** Final processed data from previous steps
- **Processing:** Completion actions and final status determination
- **Output:** Process completion with success/failure status

---

## Key Improvements:

1. **Clear Purpose Statements** - Each step explains what it accomplishes
2. **Detailed Configuration** - Specific technical details organized clearly
3. **Enhanced Data Flow** - Input/Processing/Output clearly defined
4. **Visual Separation** - Horizontal rules and blockquotes for better readability
5. **Professional Formatting** - Clean, business-appropriate presentation
6. **Comprehensive Context** - Full understanding of each step's role

---

## Field Mappings: Before vs After

### ❌ **BEFORE (Broken Format):**
```
Field Mappings: | Source Field | Target Field | Type | Notes | |--------------|--------------|------|-------| | 5 | IMPORT/Object/I_PI_COMPANYDATA/Object/NAME | profile | Company name | | 9 | IMPORT/Object/I_PI_COMPANYDATA/Object/STREET | profile | Street address |
```

### ✅ **AFTER (Enhanced Format):**

**Field Mappings:**

| Source Field | Target Field | Data Type | Business Purpose |
|--------------|--------------|-----------|------------------|
| Customer.CompanyName | BAPI_CUSTOMER.NAME | String | Maps company name from Salesforce to SAP customer master |
| Customer.BillingStreet | BAPI_CUSTOMER.STREET | String | Maps billing street address for customer creation |
| Customer.BillingCity | BAPI_CUSTOMER.CITY | String | Maps billing city for customer address |
| Customer.BillingState | BAPI_CUSTOMER.REGION | String | Maps billing state/region for customer address |

### 🎯 **Key Field Mapping Improvements:**
- **Readable Field Names** - "Customer.CompanyName" instead of "5" or long XML paths
- **Proper Table Format** - Multi-line markdown table instead of single-line text
- **Business Context** - "Business Purpose" column explains the mapping logic
- **Clean Target Fields** - "BAPI_CUSTOMER.NAME" instead of "IMPORT/Object/I_PI_COMPANYDATA/Object/NAME"
- **Proper Data Types** - "String", "Integer", "Date" instead of generic "profile"

---

## Input/Output Profiles: Before vs After

### ❌ **BEFORE (Technical XML Paths):**
```
Input Profile: SF Account QUERY Response XML
- Account Name: Salesforce account name (String)
- Account Street: Street address (String)

Output Profile: Boomi for SAP BAPI_CUSTOMER_CREATEFROMDATA1 FUNCTION Request JSON
- IMPORT/Object/I_PI_COMPANYDATA/Object/NAME: Company name (String)
- IMPORT/Object/I_PI_COMPANYDATA/Object/STREET: Street address (String)
- IMPORT/Object/I_PI_COMPANYDATA/Object/CITY: City (String)
```

### ✅ **AFTER (Clean, Business-Friendly Format):**

**Input Data Structure:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| Account.Name | String | Salesforce account name |
| Account.BillingStreet | String | Primary billing street address |
| Account.BillingCity | String | Billing address city |

**Output Data Structure:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| CompanyName | String | SAP customer company name |
| Street | String | Customer street address |
| City | String | Customer city |

### 🎯 **Key Profile Improvements:**
- **Clean Field Names** - "CompanyName" instead of "IMPORT/Object/I_PI_COMPANYDATA/Object/NAME"
- **Structured Tables** - Easy-to-scan table format instead of bullet lists
- **Business Descriptions** - Clear, business-friendly field descriptions
- **Logical Grouping** - Related fields grouped together (e.g., address fields)
- **Professional Presentation** - Clean, scannable format for technical documentation
