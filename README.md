# FAQ Generator using AWS Bedrock

## Overview

This project is an Intelligent FAQ Assistant that processes FAQ data stored in an S3 bucket, generates responses using AWS Bedrock, and stores the results back in S3. It uses Jinja2 for dynamic prompt generation.

## Architecture

1. An S3 event triggers the Lambda function.
2. The Lambda function reads the FAQ data from the input S3 bucket.
3. The function generates responses using AWS Bedrock.
4. The responses are stored in the output S3 bucket.

## Files

- `lambda_function.py`: The main code for the Lambda function.
- `requirements.txt`: Lists the dependencies.
- `prompt_template.txt`: Template for generating prompts.
- `sample_input.json`: Example input file for testing.
- `sample_output.json`: Example output file showing the expected result.

## Setup

1. Deploy the Lambda function.
2. Ensure the required permissions for S3 and Bedrock are configured.
3. Upload FAQ data to the input S3 bucket to trigger the function.

## Running Locally

To test the function locally:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the function with a sample event:
   ```bash
   python lambda_function.py
   ```

## Example

Input FAQ data:

```json
{
  "faqs": [
    {
      "question": "What is the return policy?",
      "context": "Customer support"
    },
    {
      "question": "How can I track my order?",
      "context": "Shipping information"
    }
  ]
}
```
