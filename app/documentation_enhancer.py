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

    def enhance_documentation(self, base_documentation: str) -> str:
        """Enhance documentation using the configured LLM service.

        Args:
            base_documentation: Base documentation to enhance

        Returns:
            Enhanced documentation or original if enhancement fails
        """
        # Modified to use a variable to track enhancement success
        enhancement_successful = False

        prompt = f"""You are a MuleSoft and SAP Integration Suite specialist. Based on the following technical
    documentation, create comprehensive documentation that includes API details, flow logic,
    and detailed SAP Integration Suite visualization. Use SAP Integration Suite components and connections for
    the visualization.

    IMPORTANT:
    1. Do NOT make assumptions about adapters or systems not explicitly mentioned in the source documentation.
    2. Use ONLY the components and connections present in the original MuleSoft flow.
    3. When describing the SAP Integration Suite implementation, maintain the same integration pattern.
    4. If a connection type is unclear, mark it as a configuration decision.
    5. PRESERVE ALL TECHNICAL EXPRESSIONS EXACTLY AS WRITTEN, especially:
    - All OData query parameters like $filter, $select, $expand
    - All DataWeave transformations including variables, functions, and operators
    - All conditions, regex patterns, and logical expressions
    - DO NOT simplify, summarize, or rewrite any technical expressions

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

    ## Current MuleSoft Flow Logic
    1. What triggers each flow
    2. Main processing steps and their purpose
    3. Data transformations that occur
    4. Expected outcomes and error scenarios
    5. PAY SPECIAL ATTENTION to these technical details:
    - Include ALL query parameters with their EXACT filter expressions (like $filter, $select)
    - Show ALL DataWeave transformations in full, using code blocks with triple backticks
    - Preserve ALL variable names, field references, and operator syntax exactly as found
    - Maintain ALL conditional expressions and pattern matching logic

    ## DataWeave Transformations Explained
    For each DataWeave transformation in the flow:
    1. Provide a brief explanation of what the transformation is doing in plain language
    2. Explain the input format and expected output format
    3. Highlight any important functions or operations used (e.g., map, filter, groupBy)
    4. Explain any complex logic or conditional statements
    5. Include the full original DataWeave code in a code block

    ## SAP Integration Suite Implementation
    ### Component Mapping
    Map each MuleSoft component to its SAP Integration Suite equivalent:
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

    Create a Mermaid diagram that accurately represents the flows, components, and connections found in the original MuleSoft application. The diagram should follow this format:
    **IMPORTANT**: Your model output must be *only* the Mermaid code block (```mermaid …```) with no shell prompts or extra text.
    Use real line breaks in labels (or `<br/>`), not `\n` literals.

    STUDY THE EXAMPLE DIAGRAM BELOW CAREFULLY - it shows the proper way to structure your diagram with correct syntax for nodes, connections, subgraphs, and styling.

    ```mermaid
    flowchart TD
    %% Define node styles
    classDef httpAdapter fill:#87CEEB,stroke:#333,stroke-width:2px
    classDef contentModifier fill:#98FB98,stroke:#333,stroke-width:2px
    classDef router fill:#FFB6C1,stroke:#333,stroke-width:2px
    classDef mapping fill:#DDA0DD,stroke:#333,stroke-width:2px
    classDef exception fill:#FFA07A,stroke:#333,stroke-width:2px
    classDef processCall fill:#F0E68C,stroke:#333,stroke-width:2px

    %% Example diagram structure (use this as a reference)
    %% Start([Start]) --> HttpListener[HTTP Listener /products]
    %% HttpListener --> GetProductsFlow[Get Products Flow]
    %% GetProductsFlow --> ResponseHeaders[Set Response Headers]
    %% ResponseHeaders --> End([End])

    %% %% Error Handling
    %% HttpListener -->|Error| ErrorHandler[(Global Error Handler)]
    %% ErrorHandler --> SetErrorResponse[Set Error Response]
    %% SetErrorResponse --> SetErrorHeaders[Set Error Headers]
    %% SetErrorHeaders --> ErrorEnd([Error End])

    %% %% Get Products Flow
    %% subgraph GetProductDetailsFlow["Get Product Details Flow"]
    %%     SubflowStart([Subflow Start]) --> ValidateProduct[Validate Product ID\nGroovy Script]
    %%     ValidateProduct --> ProductRouter{"Is Valid Product?"}
    %%     ProductRouter -->|Yes| LogValidRequest[Log Valid Request]
    %%     LogValidRequest --> BuildODataQuery[Build OData Query\n$filter and $select]
    %%     BuildODataQuery --> ODataRequest[OData Request to SAP HANA]
    %%     ODataRequest --> TransformResponse[Transform Response\nto JSON]
    %%
    %%     ProductRouter -->|No| LogInvalidRequest[Log Invalid Request]
    %%     LogInvalidRequest --> BuildErrorResponse[Build Error Response\nPRODUCT_NOT_FOUND]
    %% end

    %% YOUR ACTUAL DIAGRAM NODES AND CONNECTIONS GO HERE
    %% DO NOT INDENT THE FENCES — they must start at column 0

    ```

    %% Add styling
    class HttpListener,ODataRequest httpAdapter
    class ResponseHeaders,LogValidRequest,LogInvalidRequest,SetErrorResponse,SetErrorHeaders contentModifier
    class ProductRouter router
    class ValidateProduct,BuildODataQuery,TransformResponse,BuildErrorResponse mapping
    class ErrorHandler exception
    class GetProductsFlow processCall

    IMPORTANT MERMAID DIAGRAM RULES:
    1. Use TD (top-down) direction
    2. Include ALL style definitions exactly as shown above
    3. Group related flows with %% comments
    4. Use these exact node shapes:
       - ((name)) for Start/End events
       - [name] for regular components
       - {"name"} for routers (IMPORTANT: use quotes inside the curly braces)
       - [[name]] for process calls
       - [(name)] for error handlers
    5. Use these exact style classes:
       - :::httpAdapter for HTTP components
       - :::contentModifier for content modifiers
       - :::router for routers
       - :::mapping for transformations
       - :::exception for error handlers
       - :::processCall for process calls
    6. Use -->|label| for labeled connections
    7. Keep error handlers grouped together
    8. Maintain exact spacing and indentation as shown
    9. AVOID using special characters like curly braces in node labels or connection labels - replace path parameters like '{{accountId}}' with plain text (e.g., 'accountId')
    10. For API endpoints with path parameters, use simplified formats like '/InvestmentAccounts/accountId/Retrieve' instead of '/InvestmentAccounts/{{accountId}}/Retrieve'

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
    1. A descriptive title that reflects the purpose of the API/integration
    2. A comprehensive table of contents with hyperlinks to all sections
    3. Clear headings and subheadings for all sections
    4. Properly labeled diagrams with descriptive headings
    5. Complete API details including endpoints, parameters, and examples
    6. Detailed environment configuration information"""

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
            return base_documentation

        return enhanced_content

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
                    {"role": "system", "content": "You are an expert integration specialist helping convert MuleSoft applications to SAP Integration Suite."},
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