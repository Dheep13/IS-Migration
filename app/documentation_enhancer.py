"""Documentation enhancer using LLM services."""
import os
import sys
import logging
import json
from typing import Optional
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Try to import OpenAI and Anthropic, but don't fail if not installed
try:
    import openai
except ImportError:
    openai = None
    logger.warning("OpenAI package not installed. OpenAI-based enhancement will not be available.")

try:
    import anthropic
    import httpx
except ImportError:
    anthropic = None
    logger.warning("Anthropic package not installed. Claude-based enhancement will not be available.")

class DocumentationEnhancer:
    def __init__(self, selected_service='openai'):
        """Initialize documentation enhancer with specified LLM service.

        Args:
            selected_service: Service to use ('openai' or 'anthropic')
        """
        self.selected_service = selected_service

        # Load API keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

        # Initialize clients if possible
        self.openai_client = None
        self.anthropic_client = None

        if openai and self.openai_api_key:
            try:
                self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
                logger.info("OpenAI client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {str(e)}")

        if anthropic and self.anthropic_api_key:
            try:
                # Create a custom HTTP client with extended timeout (600 seconds instead of 300)
                http_client = httpx.Client(timeout=600.0)

                # Initialize Anthropic client with a custom http_client to avoid proxies issue
                self.anthropic_client = anthropic.Anthropic(
                    api_key=self.anthropic_api_key,
                    http_client=http_client
                )
                logger.info("Anthropic client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Anthropic client: {str(e)}")

    def enhance_documentation(self, base_documentation: str, generate_json: bool = True, output_dir: str = None) -> str:
        """Enhance documentation using the configured LLM service.

        Args:
            base_documentation: Base documentation to enhance

        Returns:
            Enhanced documentation or original if enhancement fails
        """
        # Modified to use a variable to track enhancement success
        enhancement_successful = False

        prompt = f"""You are a Dell Boomi and SAP Integration Suite specialist. Based on the following technical
    documentation, create comprehensive documentation that includes API details, flow logic,
    and detailed SAP Integration Suite visualization. Use SAP Integration Suite components and connections for
    the visualization.

    IMPORTANT:
    1. Do NOT make assumptions about adapters or systems not explicitly mentioned in the source documentation.
    2. Use ONLY the components and connections present in the original Dell Boomi process.
    3. When describing the SAP Integration Suite implementation, maintain the same integration pattern.
    4. If a connection type is unclear, mark it as a configuration decision.
    5. PRESERVE ALL TECHNICAL EXPRESSIONS EXACTLY AS WRITTEN, especially:
    - All HTTP connector configurations and endpoints
    - All Boomi Map/Transform field mappings and functions
    - All Document Properties and their source values
    - All connector parameters and operation configurations
    - DO NOT simplify, summarize, or rewrite any technical expressions

    CRITICAL BOOMI-SPECIFIC ANALYSIS REQUIREMENTS:
    6. ANALYZE BOOMI XML STRUCTURE THOROUGHLY:
    - Examine ALL <shape> elements and their shapetype attributes
    - Identify ALL <connectoraction> elements and their actionType, connectorType
    - Extract ALL <documentproperties> and their complex source value configurations
    - Analyze ALL <Map> elements with their <Mappings> and <Functions>
    - Identify ALL HTTP connector calls within Document Properties
    - Examine ALL operation configurations and parameters

    7. SEQUENCE OF EVENTS MUST BE ACCURATE:
    - Follow the <dragpoints> to determine the exact flow sequence
    - Map each shape's connections using toShape attributes
    - Preserve the exact order of operations as defined in the Boomi XML
    - Do NOT reorder or assume different sequences than what's in the XML

    8. CAPTURE COMPLEX BOOMI PATTERNS:
    - Document Properties with HTTP connector calls (GET operations to external APIs)
    - Dynamic property calculations using date functions, concatenations
    - Connector parameter mappings from profile elements
    - Field mappings in Map components with fromKey/toKey relationships
    - Function steps in transformations (DocumentPropertyGet, etc.)

    HANDLING LARGE DOCUMENTATION:
    1. First analyze the documentation size and structure. If you determine the content will exceed 20,000 tokens in your response, you should:
       - Focus on the most essential components and flows in your detailed analysis
       - Ensure all flows are at least mentioned, even if some details are summarized
       - Prioritize accuracy over comprehensive detail for very large applications
    2. Your final output must include a complete and accurate mapping of all components, even if you need to be more concise in your explanations.

    Here is the source documentation:

    {base_documentation}

    Please structure your response in Markdown with these sections:

    # [Descriptive Title Based on the API/Integration Purpose]

    ## Table of Contents
    Create a detailed table of contents with hyperlinks to all sections and subsections in the document. Use Markdown link syntax like [Section Name](#section-name) to create clickable links to each section. Include ALL sections and subsections.

    ## API Overview
    - Comprehensive description of what this API does and its business purpose
    - Base URL/endpoint pattern
    - Authentication mechanisms
    - Rate limiting information (if available)
    - General response format

    ## Endpoints
    For each endpoint, provide a detailed breakdown:
    - HTTP Method and full path
    - Purpose of the endpoint
    - Request parameters (path, query, headers) with detailed descriptions
    - Request body structure (if applicable) with field descriptions and data types
    - Response format and status codes with detailed descriptions
    - Example request/response if available
    - Error handling for this endpoint

    ## Current Dell Boomi Flow Logic
    ### Process Flow Overview
    Provide a high-level overview of the Dell Boomi process including:
    1. What triggers the process (Start Event configuration)
    2. Main processing steps and their purpose in sequence
    3. Data transformations that occur
    4. External system interactions
    5. Expected outcomes and error scenarios

    ### Step-by-Step Flow Description
    For each shape in the Boomi process, provide detailed analysis:
    1. **Start Event (shape1):**
       - Connector type and configuration
       - Listen operation details
       - Input profile and data format

    2. **Document Properties (if present):**
       - ALL dynamic document properties and their calculations
       - HTTP connector calls within properties (GET operations)
       - Source value configurations and parameter mappings
       - Date calculations and concatenation logic

    3. **Transform/Map Components:**
       - Input and output profiles
       - Field mappings (fromKey → toKey)
       - Function steps and their purposes
       - Default values and constants

    4. **Connector Actions:**
       - Connector type (Salesforce, HTTP, etc.)
       - Operation type (Send, Get, etc.)
       - Object actions and configurations
       - Field lists and parameter mappings

    5. **End Events:**
       - Stop configuration and continuation settings

    PAY SPECIAL ATTENTION to these technical details:
    - Include ALL HTTP connector endpoints and parameters
    - Show ALL Boomi Map field mappings with exact fromKey/toKey relationships
    - Preserve ALL Document Property source value configurations
    - Maintain ALL connector parameter mappings and profile element references
    - Document ALL function steps in transformations

    ## Boomi Transformations Explained
    For each Map/Transform component in the Boomi process:
    1. Provide a brief explanation of what the transformation is doing in plain language
    2. Explain the input profile format and expected output profile format
    3. Detail ALL field mappings with their source and target paths
    4. Explain any function steps used (DocumentPropertyGet, etc.)
    5. Include ALL default values and constants
    6. Show the complete mapping configuration from the XML

    ## SAP Integration Suite Implementation
    ### Component Mapping
    Map each Dell Boomi component to its SAP Integration Suite equivalent using this comprehensive mapping:

    **Core Boomi Components:**
    - Start Event (shapetype="start") → Start Message Event
    - Stop Event (shapetype="stop") → End Message Event
    - Connector Action (shapetype="connectoraction") → Request Reply with appropriate adapter
    - Map/Transform (shapetype="map") → Message Mapping or Groovy Script
    - Document Properties (shapetype="documentproperties") → Content Modifier (Set Properties)
    - Decision (shapetype="decision") → Router (Exclusive Gateway)
    - Branch → Parallel Gateway or Exclusive Gateway
    - Error Path → Exception Subprocess

    **Boomi Connector Types to SAP Adapters:**
    - connectorType="wss" (Web Services Server) → HTTPS Adapter (Receiver)
    - connectorType="http" → HTTPS Adapter (Sender)
    - connectorType="salesforce" → Salesforce Adapter or HTTPS Adapter
    - connectorType="sftp" → SFTP Adapter
    - connectorType="database" → JDBC Adapter
    - connectorType="odata" → OData Adapter

    **Mapping Components:**
    - Data Mapping → Message Mapping
    - XSLT Transform → XSLT Mapping
    - Operation Mapping → Operation Mapping

    **Processing Components:**
    - Content Enricher → Content Enricher (with lookup)
    - Filter → Filter
    - Script/Groovy → Groovy Script
    - XML Modifier → XML Modifier
    - Write Variables → Write Variables

    **Gateway Components:**
    - Parallel Processing → Sequential Multicast or Parallel Multicast
    - Join → Join (Parallel Gateway)
    - Exclusive Choice → Router (Exclusive Gateway)

    **Splitter Components:**
    - EDI Splitter → EDI Splitter
    - IDoc Splitter → IDoc Splitter
    - General Splitter → General Splitter

    **Storage Components:**
    - Database Select → Select (DB Storage)
    - Database Write → Write (DB Storage)
    - Database Get → Get (DB Storage)
    - Persist → Persist
    - ID Mapping → ID Mapping

    **Converter Components:**
    - JSON to XML → JSON to XML Converter
    - XML to CSV → XML to CSV Converter
    - CSV to XML → CSV to XML Converter
    - XML to JSON → XML to JSON Converter
    - Base64 Encode → Base64 Encoder
    - Base64 Decode → Base64 Decoder

    **Event Components:**
    - Timer/Scheduler → Timer Start Event
    - Error End → Error End Event
    - Process Call → Process Call

    **Aggregation Components:**
    - Aggregator → Aggregator
    - Gather → Gather

    **EDI Components:**
    - EDI Extractor → EDI Extractor
    - EDI Validator → EDI Validator

    **Adapter Components:**
    - OData Connector → OData Adapter
    - SFTP Connector → SFTP Adapter
    - SuccessFactors Connector → SuccessFactors Adapter
    - Salesforce Connector → Salesforce Adapter

    For each component mapping:
    - List each source component and its direct equivalent
    - Preserve the same connection types and patterns
    - Note any components that need configuration decisions
    - Document any potential gaps or differences in functionality

    ### Integration Flow Visualization

    IMPORTANT VISUALIZATION INSTRUCTIONS:
    1. Analyze the complexity of the flows first. If there are multiple complex flows with many endpoints, create separate diagrams. If the flows are simple or closely related, combine them into a single comprehensive diagram.
    2. Each diagram should have a clear, descriptive heading (e.g., "## Order Processing Flow Diagram" or "## Customer Data Integration Flow")
    3. For each diagram, provide a brief introduction explaining what the diagram represents
    4. Use your judgment to determine if multiple diagrams are needed - prefer fewer, more comprehensive diagrams when possible
    5. If you create multiple diagrams, ensure they are logically grouped and clearly labeled
    6. FOLLOW THE EXAMPLE DIAGRAM STRUCTURE PROVIDED BELOW - it shows the correct syntax and formatting

    Create a Mermaid diagram that accurately represents the flows, components, and connections found in the original Dell Boomi process. The diagram should follow this format:
    **IMPORTANT**: Your model output must be *only* the Mermaid code block (```mermaid …```) with no shell prompts or extra text.
    Use real line breaks in labels (or `<br/>`), not `\n` literals.

    STUDY THE EXAMPLE DIAGRAM BELOW CAREFULLY - it shows the proper way to structure your diagram with correct syntax for nodes, connections, and styling.

    ```mermaid
    flowchart TD
    %% Define node styles for Boomi/SAP Integration Suite components
    classDef httpAdapter fill:#87CEEB,stroke:#333,stroke-width:2px
    classDef contentModifier fill:#98FB98,stroke:#333,stroke-width:2px
    classDef mapping fill:#DDA0DD,stroke:#333,stroke-width:2px
    classDef adapter fill:#FFD700,stroke:#333,stroke-width:2px
    classDef event fill:#C0C0C0,stroke:#333,stroke-width:2px
    classDef errorHandler fill:#FFA07A,stroke:#333,stroke-width:2px

    %% Example Boomi diagram structure (use this as a reference)
    %% Start((Start)) --> StripeWebhook[HTTP Adapter: Stripe Webhook Receiver]:::httpAdapter
    %% StripeWebhook --> SetDynamicProps[Content Modifier: Set Dynamic Properties]:::contentModifier
    %% SetDynamicProps --> TransformData[Message Mapping: JSON to XML]:::mapping
    %% TransformData --> SalesforceCreate[Salesforce Adapter: Create Opportunity]:::adapter
    %% SalesforceCreate --> End((End)):::event

    %% %% Error Handling (if present in Boomi process)
    %% StripeWebhook -->|Error| ErrorHandler[(Exception Subprocess)]:::errorHandler
    %% ErrorHandler --> LogError[Write to Log: Error Details]:::contentModifier
    %% LogError --> ErrorEnd((Error End)):::event

    %% %% Document Properties Detail (if complex)
    %% subgraph DynamicProperties["Dynamic Properties Calculation"]
    %%     GetCustomer[HTTP GET: Customer Details]:::httpAdapter
    %%     GetProduct[HTTP GET: Product Details]:::httpAdapter
    %%     ConcatDescription[Concatenate: Customer + Product]:::contentModifier
    %%     CalcCloseDate[Calculate: Close Date - 3 months]:::contentModifier
    %% end

    %% YOUR ACTUAL DIAGRAM NODES AND CONNECTIONS GO HERE
    %% FOLLOW THE EXACT SEQUENCE FROM BOOMI XML DRAGPOINTS
    %% DO NOT INDENT THE FENCES — they must start at column 0

    ```

    %% Add styling based on component types
    class StripeWebhook,GetCustomer,GetProduct httpAdapter
    class SetDynamicProps,ConcatDescription,CalcCloseDate,LogError contentModifier
    class TransformData mapping
    class SalesforceCreate adapter
    class Start,End,ErrorEnd event
    class ErrorHandler errorHandler

    IMPORTANT MERMAID DIAGRAM RULES FOR BOOMI PROCESSES:
    1. Use TD (top-down) direction
    2. Include ALL style definitions exactly as shown above
    3. Group related flows with %% comments
    4. Use these exact node shapes:
       - ((name)) for Start/End events (Boomi Start/Stop shapes)
       - [name] for regular components (Connector Actions, Document Properties)
       - {"name"} for routers/decisions (IMPORTANT: use quotes inside the curly braces)
       - [(name)] for error handlers (Exception Subprocesses)
    5. Use these exact style classes based on Boomi component types:
       - :::httpAdapter for HTTP connectors, Web Services Server, OData adapters
       - :::contentModifier for Document Properties, Content Modifiers
       - :::mapping for Map/Transform components, Message Mappings
       - :::adapter for Salesforce, SFTP, Database connectors
       - :::event for Start/End events
       - :::errorHandler for error handling components
    6. Use -->|label| for labeled connections following Boomi dragpoint sequence
    7. Keep error handlers grouped together (if present in Boomi process)
    8. Maintain exact spacing and indentation as shown
    9. FOLLOW THE EXACT SEQUENCE from Boomi XML dragpoints (toShape attributes)
    10. Include ALL components from the Boomi process, even complex Document Properties
    11. For Document Properties with HTTP calls, show the external API interactions
    12. Use descriptive labels that reflect the actual Boomi component names and purposes

    ### Configuration Details
    For each component in the visualization, provide:
    - All required parameters
    - Default values
    - Placeholder values for missing configurations
    - Connection details between components

    ## Environment Configuration
    Provide a comprehensive breakdown of all configuration details:
    - Important configuration parameters (from source)
    - Environment variables (from source) with descriptions and example values
    - Dependencies on external systems (from source)
    - Security settings and certificates needed
    - Deployment considerations
    - Required resources (memory, CPU, etc.)

    ## API Reference
    Create a detailed API reference section that includes:
    - Complete list of all endpoints with their HTTP methods
    - Request and response schemas for each endpoint
    - Authentication requirements
    - Error codes and their meanings
    - Rate limiting information
    - Pagination details (if applicable)
    - Versioning information

    Make sure the final document has:
    1. A descriptive title that reflects the purpose of the Dell Boomi integration
    2. A comprehensive table of contents with hyperlinks to all sections
    3. Clear headings and subheadings for all sections
    4. Properly labeled Mermaid diagrams with descriptive headings that render correctly in HTML
    5. Complete process details including all Boomi components, configurations, and connections
    6. Detailed environment configuration information
    7. Accurate sequence of events based on Boomi XML dragpoint analysis
    8. All HTTP connector endpoints and parameters from Document Properties
    9. Complete field mappings from Boomi Map components
    10. All external system dependencies and API calls

    CRITICAL FINAL REMINDERS:
    - This is a DELL BOOMI process - use Boomi-specific terminology throughout
    - Analyze the XML structure thoroughly to capture ALL technical details
    - Maintain the exact sequence of operations as defined in the Boomi process
    - Include ALL Document Properties calculations and HTTP connector calls
    - Preserve ALL field mappings and transformation logic
    - Ensure Mermaid diagrams follow the exact component flow from the XML"""

        # Try to enhance with selected service
        enhanced_content = None
        if self.selected_service == 'openai':
            enhanced_content = self.enhance_with_openai(prompt)
            if enhanced_content:
                logger.info("Enhancement with OpenAI was successful")
                enhancement_successful = True
            else:
                logger.warning("Enhancement with OpenAI failed")

        elif self.selected_service in ['anthropic', 'claude']:  # Accept both names for compatibility
            enhanced_content = self.enhance_with_anthropic(prompt)
            if enhanced_content:
                logger.info("Enhancement with Anthropic was successful")
                enhancement_successful = True
            else:
                logger.warning("Enhancement with Anthropic failed")

        # Return enhanced content or original if enhancement fails
        if not enhancement_successful:
            logger.warning("LLM enhancement was not successful. Returning original documentation.")
            final_content = base_documentation
        else:
            final_content = enhanced_content

        # Generate JSON components if requested
        if generate_json and output_dir and enhancement_successful:
            try:
                self._generate_json_components(final_content, output_dir)
            except Exception as e:
                logger.warning(f"Failed to generate JSON components: {e}")

        return final_content

    def enhance_with_openai(self, prompt: str) -> Optional[str]:
        """Enhance documentation using OpenAI.

        Args:
            prompt: Prompt for OpenAI

        Returns:
            Enhanced documentation or None if failed
        """
        if not self.openai_client:
            logger.warning("OpenAI client not available. Cannot enhance documentation.")
            return None

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",  # Can be configured based on needs
                messages=[
                    {"role": "system", "content": "You are an expert integration specialist helping convert Dell Boomi processes to SAP Integration Suite."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=18000,
                timeout=600  # Set timeout to 600 seconds (increased from 300)
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error using OpenAI for enhancement: {str(e)}")
            return None

    def enhance_with_anthropic(self, prompt: str) -> Optional[str]:
        """Enhance documentation using Anthropic Claude.

        Args:
            prompt: Prompt for Claude

        Returns:
            Enhanced documentation or None if failed
        """
        if not self.anthropic_client:
            logger.error("Anthropic client not available. Cannot enhance documentation.")
            logger.error(f"API Key available: {bool(self.anthropic_api_key)}")
            logger.error(f"Anthropic module available: {bool(anthropic)}")
            return None

        try:
            # Log the API call attempt with prompt size
            logger.info(f"Starting Anthropic Claude API call with prompt size: {len(prompt)} characters")
            logger.info(f"Using model: claude-3-7-sonnet-20250219 with timeout: 600 seconds")
            logger.info(f"API Key (first 5 chars): {self.anthropic_api_key[:5]}...")

            import time
            start_time = time.time()

            try:
                # Use the Anthropic Messages API with the newer format
                response = self.anthropic_client.messages.create(
                    model="claude-3-7-sonnet-20250219",  # Using the latest model
                    max_tokens=20000,
                    temperature=0.2,
                    timeout=600,  # Set timeout to 600 seconds (increased from 300)
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                }
                            ]
                        }
                    ]
                )
            except Exception as api_error:
                logger.error(f"Anthropic API call failed with error: {str(api_error)}")
                logger.error(f"Error type: {type(api_error).__name__}")

                # Try with a different model as fallback
                logger.info("Trying fallback to claude-3-opus-20240229 model...")
                try:
                    response = self.anthropic_client.messages.create(
                        model="claude-3-opus-20240229",
                        max_tokens=20000,
                        temperature=0.2,
                        timeout=600,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": prompt
                                    }
                                ]
                            }
                        ]
                    )
                    logger.info("Fallback to claude-3-opus-20240229 model succeeded")
                except Exception as fallback_error:
                    logger.error(f"Fallback API call also failed: {str(fallback_error)}")
                    raise fallback_error

            elapsed_time = time.time() - start_time
            logger.info(f"Anthropic API call completed in {elapsed_time:.2f} seconds")

            # Get the content from the response - extract text from the first content item
            if hasattr(response, 'content') and len(response.content) > 0:
                # Check if content is a list with text items
                for item in response.content:
                    if hasattr(item, 'text'):
                        logger.info(f"Successfully extracted content from response, length: {len(item.text)} characters")
                        return item.text

                # Fallback for other response structures
                logger.warning("Unexpected response structure. Attempting to extract text directly.")
                if hasattr(response.content[0], 'text'):
                    logger.info(f"Extracted text directly from content[0], length: {len(response.content[0].text)} characters")
                    return response.content[0].text

                # Try to extract content as a string if it's not an object with a text attribute
                logger.warning("Could not find text attribute. Trying to convert content to string.")
                try:
                    content_str = str(response.content[0])
                    logger.info(f"Converted content to string, length: {len(content_str)} characters")
                    return content_str
                except Exception as str_error:
                    logger.error(f"Error converting content to string: {str(str_error)}")

            # Log the full response structure for debugging
            logger.warning("Could not extract text from Anthropic response")
            logger.warning(f"Response type: {type(response)}")
            logger.warning(f"Response attributes: {dir(response)}")
            logger.warning(f"Response content type: {type(response.content) if hasattr(response, 'content') else 'No content attribute'}")

            return None

        except Exception as e:
            logger.error(f"Error using Anthropic Claude for enhancement: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error traceback: {e.__traceback__}")
            return None

    def analyze_image_with_anthropic(self, prompt: str, image_data: str, mime_type: str) -> Optional[str]:
        """Analyze image using Anthropic Claude with vision capabilities.

        Args:
            prompt: Text prompt for image analysis
            image_data: Base64 encoded image data
            mime_type: MIME type of the image (e.g., 'image/png')

        Returns:
            Image analysis result or None if failed
        """
        if not self.anthropic_client:
            logger.error("Anthropic client not available. Cannot analyze image.")
            return None

        try:
            logger.info(f"Starting Anthropic vision analysis with image type: {mime_type}")

            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",  # Vision-capable model
                max_tokens=1000,
                timeout=300,  # 5 minutes for image analysis
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": mime_type,
                                    "data": image_data
                                }
                            }
                        ]
                    }
                ]
            )

            logger.info("Anthropic vision analysis completed successfully")
            return response.content[0].text

        except Exception as e:
            logger.error(f"Error using Anthropic for image analysis: {str(e)}")
            return None

    def _generate_json_components(self, enhanced_documentation: str, output_dir: str):
        """Generate JSON components for iFlow generation from enhanced documentation."""
        try:
            import os
            import json
            from datetime import datetime

            # Create a JSON generation prompt
            json_prompt = f"""Based on the following Dell Boomi documentation, generate a JSON structure that represents the SAP Integration Suite components needed for this integration.

CRITICAL: Respond with ONLY valid JSON in the exact format specified below. Do NOT include any explanations, markdown, or other text.

{enhanced_documentation}

Generate JSON in this exact format:
{{
    "process_name": "Name of the integration process",
    "description": "Description of what this integration does",
    "endpoints": [
        {{
            "method": "HTTP method (GET, POST, etc.)",
            "path": "Endpoint path",
            "purpose": "Purpose of this endpoint",
            "components": [
                {{
                    "type": "Component type (start_event, content_modifier, message_mapping, request_reply, end_event, etc.)",
                    "name": "Component name",
                    "id": "Unique component ID",
                    "config": {{
                        "endpoint_path": "For request_reply components",
                        "content": "For content_modifier components",
                        "script": "For groovy_script components"
                    }}
                }}
            ],
            "sequence": ["component_id_1", "component_id_2", "component_id_3"]
        }}
    ]
}}

RESPOND WITH ONLY JSON:"""

            # Generate JSON using enhanced logic with validation and retry
            components = self._generate_json_with_validation(json_prompt, output_dir)

            if components:
                # Apply the same enhancements as iFlow generation
                components = self._generate_transformation_scripts(components)
                components = self._create_intelligent_connections(components)

                # Save the enhanced JSON to file
                os.makedirs(output_dir, exist_ok=True)
                json_file = os.path.join(output_dir, "iflow_components.json")

                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(components, f, indent=2)

                logger.info(f"✅ Generated enhanced JSON components file: {json_file}")

                # Also save metadata
                metadata = {
                    "generated_at": datetime.now().isoformat(),
                    "source": "documentation_enhancer",
                    "llm_service": self.selected_service,
                    "documentation_length": len(enhanced_documentation),
                    "components_count": len(components.get("endpoints", [])),
                    "has_transformations": len(components.get("endpoints", [{}])[0].get("transformations", [])) > 0 if components.get("endpoints") else False,
                    "has_intelligent_connections": "sequence_flows" in str(components)
                }

                metadata_file = os.path.join(output_dir, "generation_metadata.json")
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2)

                logger.info(f"✅ Generated metadata file: {metadata_file}")
            else:
                logger.warning("Failed to generate JSON components")

        except Exception as e:
            logger.error(f"Error generating JSON components: {e}")
            raise

    def _generate_json_with_validation(self, json_prompt: str, output_dir: str, max_retries: int = 3):
        """Generate JSON with validation and retry logic."""
        import json

        for attempt in range(max_retries):
            try:
                logger.info(f"JSON generation attempt {attempt + 1}/{max_retries}")

                # Generate JSON response
                json_response = None
                if self.selected_service == 'anthropic' and self.anthropic_client:
                    json_response = self._call_anthropic_for_json(json_prompt)
                elif self.selected_service == 'openai' and self.openai_client:
                    json_response = self._call_openai_for_json(json_prompt)

                if not json_response:
                    logger.warning(f"Attempt {attempt + 1}: No response from LLM")
                    continue

                # Save debug response
                debug_dir = os.path.join(output_dir, "debug")
                os.makedirs(debug_dir, exist_ok=True)
                debug_file = os.path.join(debug_dir, f"json_response_attempt_{attempt + 1}.txt")
                with open(debug_file, 'w', encoding='utf-8') as f:
                    f.write(json_response)

                # Validate JSON
                is_valid, message = self._validate_json_response(json_response)
                if not is_valid:
                    logger.warning(f"Attempt {attempt + 1}: Invalid JSON - {message}")
                    continue

                # Parse JSON
                try:
                    components = json.loads(json_response)
                except json.JSONDecodeError as e:
                    logger.warning(f"Attempt {attempt + 1}: JSON decode error - {e}")
                    continue

                # Check for meaningful content
                if not self._has_meaningful_components(components):
                    logger.warning(f"Attempt {attempt + 1}: Components lack meaningful content")
                    continue

                logger.info(f"✅ Successfully generated valid JSON on attempt {attempt + 1}")
                return components

            except Exception as e:
                logger.error(f"Attempt {attempt + 1}: Error - {e}")
                continue

        logger.error(f"Failed to generate valid JSON after {max_retries} attempts")
        return None

    def _call_anthropic_for_json(self, prompt: str) -> str:
        """Call Anthropic API specifically for JSON generation."""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=8000,
                temperature=0.1,  # Lower temperature for more consistent JSON
                timeout=300,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )

            # Extract text from response
            if hasattr(response, 'content') and len(response.content) > 0:
                for item in response.content:
                    if hasattr(item, 'text'):
                        return item.text

            return None

        except Exception as e:
            logger.error(f"Error calling Anthropic for JSON: {e}")
            return None

    def _call_openai_for_json(self, prompt: str) -> str:
        """Call OpenAI API specifically for JSON generation."""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at converting Dell Boomi processes to SAP Integration Suite JSON configurations. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Lower temperature for more consistent JSON
                max_tokens=8000,
                timeout=300
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error calling OpenAI for JSON: {e}")
            return None

    def _validate_json_response(self, response: str):
        """Validate JSON response format."""
        try:
            import json
            import re

            # Try to extract JSON from response
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response)
            if json_match:
                json_str = json_match.group(1).strip()
            else:
                # Look for JSON structure
                start_brace = response.find('{')
                end_brace = response.rfind('}')
                if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
                    json_str = response[start_brace:end_brace + 1]
                else:
                    json_str = response.strip()

            # Parse JSON
            parsed_json = json.loads(json_str)

            # Check structure
            if not isinstance(parsed_json, dict):
                return False, "Response is not a JSON object"

            if "endpoints" not in parsed_json:
                return False, "Missing required 'endpoints' field"

            return True, "Valid JSON response"

        except Exception as e:
            return False, f"JSON validation error: {e}"

    def _has_meaningful_components(self, components):
        """Check if components contain meaningful content."""
        if not isinstance(components, dict):
            return False

        endpoints = components.get("endpoints", [])
        if not endpoints:
            return False

        # Check if at least one endpoint has components
        for endpoint in endpoints:
            endpoint_components = endpoint.get("components", [])
            if len(endpoint_components) >= 2:  # At least start and end
                return True

        return False

    def _generate_transformation_scripts(self, components):
        """Generate transformation scripts for components."""
        try:
            if not isinstance(components, dict) or "endpoints" not in components:
                return components

            for endpoint in components["endpoints"]:
                endpoint_components = endpoint.get("components", [])
                transformations = []

                for component in endpoint_components:
                    if component.get("type") == "message_mapping":
                        # Generate transformation script
                        transformation = {
                            "id": f"transform_{component.get('id', 'unknown')}",
                            "type": "groovy_script",
                            "name": f"Transform for {component.get('name', 'Unknown')}",
                            "script": self._generate_groovy_script(component)
                        }
                        transformations.append(transformation)

                if transformations:
                    endpoint["transformations"] = transformations

            return components

        except Exception as e:
            logger.warning(f"Error generating transformation scripts: {e}")
            return components

    def _generate_groovy_script(self, component):
        """Generate a basic Groovy script for transformation."""
        return """
// Auto-generated transformation script
import com.sap.gateway.ip.core.customdev.util.Message;

def Message processData(Message message) {
    // Get message body
    def body = message.getBody(java.lang.String);

    // Transform data here
    // Add your transformation logic

    message.setBody(body);
    return message;
}
""".strip()

    def _create_intelligent_connections(self, components):
        """Create intelligent connections between components."""
        try:
            if not isinstance(components, dict) or "endpoints" not in components:
                return components

            for endpoint in components["endpoints"]:
                endpoint_components = endpoint.get("components", [])
                sequence_flows = []

                # Create connections based on component sequence
                for i in range(len(endpoint_components) - 1):
                    current_comp = endpoint_components[i]
                    next_comp = endpoint_components[i + 1]

                    flow = {
                        "from": current_comp.get("id"),
                        "to": next_comp.get("id"),
                        "condition": None
                    }
                    sequence_flows.append(flow)

                if sequence_flows:
                    endpoint["sequence_flows"] = sequence_flows

            return components

        except Exception as e:
            logger.warning(f"Error creating intelligent connections: {e}")
            return components