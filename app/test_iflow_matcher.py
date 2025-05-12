#!/usr/bin/env python3
"""
Test script for the iFlow matcher functionality.
This script creates a sample markdown file and tests the iFlow matcher.
"""

import os
import sys
import tempfile
import json
from main import process_markdown_for_iflow

def create_sample_markdown():
    """Create a sample markdown file for testing"""
    sample_content = """# MuleSoft API Documentation

## API Overview

This API provides REST endpoints for managing customer accounts and transactions.
It supports creating, updating, and retrieving account information.

## Endpoints

### GET /accounts/{accountId}

Retrieves account information for the specified account ID.

**Request:**
```
GET /accounts/12345 HTTP/1.1
Host: api.example.com
Authorization: Bearer {token}
```

**Response:**
```json
{
  "accountId": "12345",
  "name": "John Doe",
  "balance": 1000.00,
  "status": "active"
}
```

### POST /accounts

Creates a new account.

**Request:**
```
POST /accounts HTTP/1.1
Host: api.example.com
Authorization: Bearer {token}
Content-Type: application/json
```

```json
{
  "name": "Jane Smith",
  "initialBalance": 500.00
}
```

**Response:**
```json
{
  "accountId": "67890",
  "name": "Jane Smith",
  "balance": 500.00,
  "status": "active"
}
```

## Current MuleSoft Flow Logic

**Trigger**: GET request to `/accounts/{accountId}`

**Processing Steps**:
1. Validate the account ID
2. Query the account database
3. Transform the response using `account-transform.dwl`
4. Return the account information

**Error Handling**:
- If account not found, return 404
- If validation fails, return 400
- If system error, return 500

## Authentication

The API uses OAuth 2.0 for authentication. Clients must include a valid Bearer token in the Authorization header.

## Rate Limiting

The API is rate limited to 100 requests per minute per client.
"""

    # Create a temporary file
    fd, temp_path = tempfile.mkstemp(suffix=".md")
    with os.fdopen(fd, 'w') as f:
        f.write(sample_content)
    
    return temp_path

def test_iflow_matcher():
    """Test the iFlow matcher functionality"""
    print("Creating sample markdown file...")
    markdown_path = create_sample_markdown()
    
    print(f"Sample markdown file created at: {markdown_path}")
    
    # Create output directory
    output_dir = os.path.join(tempfile.gettempdir(), "iflow_test_output")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Output directory: {output_dir}")
    
    # Process the markdown file
    print("Processing markdown file...")
    result = process_markdown_for_iflow(
        markdown_file_path=markdown_path,
        output_dir=output_dir
    )
    
    # Check the result
    if result["status"] == "success":
        print("Test successful!")
        print(f"Report: {result['files']['report']}")
        print(f"Summary: {result['files']['summary']}")
        
        # Print summary content
        with open(result['files']['summary'], 'r') as f:
            summary = json.load(f)
            print("\nTop matches:")
            for match in summary.get("top_matches", [])[:3]:
                print(f"- {match.get('name')}: {match.get('score'):.2f}")
                print(f"  {match.get('description')}")
                print(f"  URL: {match.get('url')}")
                print()
    else:
        print(f"Test failed: {result['message']}")
    
    # Clean up
    os.unlink(markdown_path)
    
    return result

if __name__ == "__main__":
    test_iflow_matcher()
