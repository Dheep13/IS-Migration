#!/usr/bin/env python3
"""
gemma_chat_fixed.py

Enhanced chat against a RunPod vLLM Serverless Endpoint (Gemma model),
with extended timeouts and better error handling for cold starts.

Requirements:
    pip install openai python-dotenv

Usage:
    1. Create a `.env` file in the same folder with:
           RUNPOD_API_KEY=your_runpod_api_key
           RUNPOD_ENDPOINT_ID=your_endpoint_id
           MODEL_NAME=google/gemma-3n-e4b-it
    2. Run:
           python gemma_chat_fixed.py
"""

import os
import sys
import time
from dotenv import load_dotenv
from openai import OpenAI

# Load .env
load_dotenv()

# --- Enhanced Config --------------------------------------------------------
ENDPOINT   = os.getenv("RUNPOD_ENDPOINT_ID", "yap1wc04ci8b5d").strip()
API_KEY    = os.getenv("RUNPOD_API_KEY", "rpa_PC6SLEQEY1SD4PSJXZLV5RBFTKTJIIWRT461NHCB1ekzyh").strip()
MODEL_NAME = os.getenv("MODEL_NAME", "google/gemma-3-4b-it").strip()  # Updated to match your preference

# Extended timeouts for RunPod cold starts and complex prompts
TIMEOUT_SHORT = 600    # 10 minutes for simple prompts
TIMEOUT_LONG  = 1200   # 20 minutes for complex prompts
MAX_TOKENS_DEFAULT = 4096  # Increased default token limit for better iFlow generation

if not ENDPOINT or not API_KEY:
    print("❌ ERROR: Missing RUNPOD_ENDPOINT_ID or RUNPOD_API_KEY in .env", file=sys.stderr)
    sys.exit(1)

# Use OpenAI-compatible endpoint as per RunPod documentation
BASE_URL = f"https://api.runpod.ai/v2/{ENDPOINT}/openai/v1"

# Initialize client with extended timeout
client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    timeout=TIMEOUT_LONG,  # Use longer timeout by default
)

def detect_prompt_complexity(prompt: str) -> bool:
    """Detect if prompt is complex and needs longer timeout"""
    complex_keywords = [
        "generate", "create", "write", "explain", "tutorial", "guide", 
        "code", "example", "detailed", "comprehensive", "step by step",
        "iflow", "integration", "xml", "bpmn", "sap"
    ]
    
    # Long prompts or complex keywords indicate need for longer timeout
    is_long = len(prompt) > 500
    has_complex_keywords = any(keyword in prompt.lower() for keyword in complex_keywords)
    
    return is_long or has_complex_keywords

def chat_once(prompt: str, max_tokens: int = MAX_TOKENS_DEFAULT) -> str:
    """Single, non-streamed completion with adaptive timeout."""

    # Determine timeout based on prompt complexity
    is_complex = detect_prompt_complexity(prompt)
    timeout = TIMEOUT_LONG if is_complex else TIMEOUT_SHORT

    print(f"⏳ Processing {'complex' if is_complex else 'simple'} prompt (timeout: {timeout//60} minutes)...")

    try:
        start_time = time.time()

        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            top_p=0.8,
            max_tokens=max_tokens,
            timeout=timeout,
        )

        elapsed_time = time.time() - start_time

        # Debug: Print response structure
        print(f"🔍 Response type: {type(resp)}")
        if hasattr(resp, 'choices'):
            print(f"🔍 Choices length: {len(resp.choices) if resp.choices else 'None'}")
            if resp.choices and len(resp.choices) > 0:
                choice = resp.choices[0]
                print(f"🔍 Choice type: {type(choice)}")
                if hasattr(choice, 'message'):
                    print(f"🔍 Message type: {type(choice.message)}")
                    if hasattr(choice.message, 'content'):
                        response_text = choice.message.content.strip() if choice.message.content else "[Empty response]"
                        print(f"✅ Response received in {elapsed_time:.1f} seconds ({len(response_text)} characters)")
                        return response_text
                    else:
                        print("❌ No content in message")
                        return "[Error] No content in response message"
                else:
                    print("❌ No message in choice")
                    return "[Error] No message in response choice"
            else:
                print("❌ No choices in response")
                return "[Error] No choices in response"
        else:
            print("❌ No choices attribute in response")
            return "[Error] Invalid response structure"

    except Exception as e:
        elapsed_time = time.time() - start_time
        error_msg = str(e)

        print(f"🔍 Full error: {repr(e)}")

        if "timeout" in error_msg.lower():
            print(f"⏰ Timeout after {elapsed_time:.1f} seconds. Try a simpler prompt or check RunPod status.")
        elif "model" in error_msg.lower() and "not exist" in error_msg.lower():
            print(f"❌ Model '{MODEL_NAME}' not found. Check your RunPod endpoint configuration.")
        else:
            print(f"❌ Error after {elapsed_time:.1f} seconds: {error_msg}")

        return f"[Error] {error_msg}"

def chat_stream(prompt: str, max_tokens: int = MAX_TOKENS_DEFAULT):
    """Streamed completion with adaptive timeout."""
    
    is_complex = detect_prompt_complexity(prompt)
    timeout = TIMEOUT_LONG if is_complex else TIMEOUT_SHORT
    
    print(f"⏳ Streaming {'complex' if is_complex else 'simple'} prompt (timeout: {timeout//60} minutes)...")
    
    try:
        start_time = time.time()
        token_count = 0
        
        for chunk in client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            top_p=0.8,
            max_tokens=max_tokens,
            stream=True,
            timeout=timeout,
        ):
            delta = chunk.choices[0].delta.content
            if delta:
                print(delta, end="", flush=True)
                token_count += len(delta.split())
        
        elapsed_time = time.time() - start_time
        print(f"\n✅ Stream completed in {elapsed_time:.1f} seconds (~{token_count} tokens)")
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        error_msg = str(e)
        
        if "timeout" in error_msg.lower():
            print(f"\n⏰ Stream timeout after {elapsed_time:.1f} seconds.")
        else:
            print(f"\n❌ Stream error after {elapsed_time:.1f} seconds: {error_msg}")

def test_model_names():
    """Test different model names to find the working one"""
    global MODEL_NAME

    possible_models = [
        "google/gemma-3-4b-it",      # Your preferred model
        "google/gemma-7b-it",        # From RunPod documentation
        "google/gemma-2b-it",        # Alternative
        "google/gemma-3n-e4b-it",    # Previous attempt
        "gemma-3-4b-it",             # Without google/ prefix
        "gemma-7b-it",               # Without google/ prefix
        "gemma-2b-it"                # Without google/ prefix
    ]

    test_prompt = "Hello! What is 2+2?"

    print("🔍 Testing different model names...")

    for model in possible_models:
        print(f"🧪 Trying model: {model}")

        # Temporarily change the model name
        original_model = MODEL_NAME
        MODEL_NAME = model

        try:
            # Create a new client with the test model
            test_client = OpenAI(
                base_url=BASE_URL,
                api_key=API_KEY,
                timeout=60,  # Short timeout for testing
            )

            resp = test_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": test_prompt}],
                temperature=0.1,
                max_tokens=50,
                timeout=60,
            )

            if resp and resp.choices and len(resp.choices) > 0:
                content = resp.choices[0].message.content
                if content:
                    print(f"✅ SUCCESS! Model '{model}' works!")
                    print(f"   Response: {content.strip()[:100]}...")
                    MODEL_NAME = model  # Keep the working model
                    return True

        except Exception as e:
            error_msg = str(e)
            if "not exist" in error_msg.lower():
                print(f"❌ Model not found: {model}")
            else:
                print(f"❌ Error with {model}: {error_msg}")

        # Restore original model name for next iteration
        MODEL_NAME = original_model

    print("❌ No working model found!")
    return False

def test_connection():
    """Test connection with a simple prompt"""
    print("🔍 Testing connection...")
    test_prompt = "Hello! What is 2+2?"
    response = chat_once(test_prompt, max_tokens=50)

    if "[Error]" not in response:
        print("✅ Connection test successful!")
        return True
    else:
        print("❌ Connection test failed!")
        print("🔄 Trying different model names...")
        return test_model_names()

def test_iflow_generation():
    """Test iFlow generation with extended timeout"""
    print("\n🧪 Testing iFlow generation (this may take several minutes)...")
    
    iflow_prompt = """You are an expert SAP Integration Suite developer. Generate a complete SAP Integration Suite iFlow project structure based on the following requirements:

Requirements:
1. Create a fully functional iFlow with proper BPMN2 XML structure
2. Include HTTP listener, data mapping, and HTTP connector
3. Generate complete project files including MANIFEST.MF and .project
4. Ensure proper error handling and logging components

Generate a complete iFlow project for: TestFlow_SalesforceToSAP

IMPORTANT: Structure your response with clear file separators:

=== FILE: src/main/resources/scenarioflows/integrationflow/TestFlow_SalesforceToSAP.iflw ===
[Generate the main iFlow XML content here]

=== FILE: META-INF/MANIFEST.MF ===
[Generate the manifest file content here]

Generate the complete structured response with all files:"""
    
    response = chat_once(iflow_prompt, max_tokens=8192)
    
    if "=== FILE:" in response:
        file_count = response.count("=== FILE:")
        print(f"✅ iFlow generation successful! Generated {file_count} files.")
        print(f"📊 Response length: {len(response)} characters")
        return True
    else:
        print("❌ iFlow generation failed - no file structure found")
        print(f"📊 Response length: {len(response)} characters")
        return False

def verify_runpod_setup():
    """Verify RunPod setup matches documentation"""
    print("🔍 Verifying RunPod Setup...")
    print(f"📡 Endpoint ID: {ENDPOINT}")
    print(f"� API Key: {API_KEY[:20]}...")
    print(f"🌐 Base URL: {BASE_URL}")
    print(f"🤖 Model: {MODEL_NAME}")
    print()

    # Check if endpoint format is correct
    expected_format = f"https://api.runpod.ai/v2/{ENDPOINT}/openai/v1"
    if BASE_URL == expected_format:
        print("✅ Endpoint URL format is correct (OpenAI-compatible)")
    else:
        print(f"⚠️  Endpoint URL format: {BASE_URL}")
        print(f"   Expected format: {expected_format}")

    print()

def main():
    print(f"�🚀 Enhanced Gemma Chat with Extended Timeouts")
    print(f"📋 Based on RunPod vLLM Worker Documentation")
    print()

    # Verify setup first
    verify_runpod_setup()

    print(f"⏱️  Timeouts: {TIMEOUT_SHORT//60}min (simple) / {TIMEOUT_LONG//60}min (complex)")
    print(f"🎯 Max tokens: {MAX_TOKENS_DEFAULT}")
    print()
    
    # Test connection first
    if not test_connection():
        print("❌ Exiting due to connection failure")
        return
    
    print("\nCommands:")
    print("  'test' - Test iFlow generation")
    print("  'exit' or 'quit' - Exit")
    print("  'stream' - Toggle streaming mode")
    print("  'tokens <number>' - Set max tokens")
    print()
    
    streaming_mode = False
    current_max_tokens = MAX_TOKENS_DEFAULT
    
    try:
        while True:
            prompt = input("User: ").strip()
            
            if prompt.lower() in {"exit", "quit"}:
                print("👋 Bye!")
                break
            elif prompt.lower() == "test":
                test_iflow_generation()
                continue
            elif prompt.lower() == "stream":
                streaming_mode = not streaming_mode
                print(f"🔄 Streaming mode: {'ON' if streaming_mode else 'OFF'}")
                continue
            elif prompt.lower().startswith("tokens "):
                try:
                    new_tokens = int(prompt.split()[1])
                    current_max_tokens = min(max(new_tokens, 50), 16384)  # Clamp between 50-16384
                    print(f"🎯 Max tokens set to: {current_max_tokens}")
                except:
                    print("❌ Invalid token count. Use: tokens <number>")
                continue
            elif not prompt:
                continue
            
            print("Assistant: ", end="" if streaming_mode else "\n")
            
            if streaming_mode:
                chat_stream(prompt, current_max_tokens)
            else:
                reply = chat_once(prompt, current_max_tokens)
                print(reply)
            
            print()  # Extra newline for readability

    except KeyboardInterrupt:
        print("\n👋 Interrupted, bye!")

if __name__ == "__main__":
    main()
