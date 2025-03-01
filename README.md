# Automated Workflow Generator
A tool to create n8n workflows from a audio description using LLMs.

## Background
I have been creating workflows for a client. It's tedious and inefficient to create the workflows manually.

Our current process is as follows:
1. They have a meeting with a customer to discuss the process they want to automate
2. They write the actions steps out in a text file
3. They have a meeting with a MAXX Appretice to discuss the workflow
4. The MAXX Appretice manually creates a workflow in a sandbox
5. The client reviews the workflow, approves it, and moves it to a production environment

This project is a proof of concept to show that we can use LLMs to generate the workflows from an audio description. Potentially, this could save the us multiple hours per workflow!


## Features
- OpenAI's Whisper Model
- Locally hosted LLM so build can include credentials and secrets

## Usage
```
pip install -r requirements.txt
```

```
# .env
OPENAI_API_KEY=your_openai_api_key
```

```
python main.py --audio_file <path_to_audio_file> --output <path_to_output_file>
```

## Finding
With just the scafolding the workflow is ok, but still not great.
```json
{
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "job-created",
        "responseMode": "onReceived"
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        250,
        300
      ]
    },
    {
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "field": "json.start_date",
              "operation": "notExists"
            }
          ]
        }
      },
      "name": "Check Start Date",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [
        450,
        300
      ]
    },
    {
      "parameters": {
        "functionCode": "const startDate = '2023-01-01'; // example arbitrary start date\nreturn { query: `start_date=${startDate}` };"
      },
      "name": "Format API Query",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        650,
        200
      ]
    },
    {
      "parameters": {
        "url": "https://api.jobtread.com/job",
        "method": "GET",
        "queryParameters": {
          "start_date": "={{$json[\"query\"]}}"
        }
      },
      "name": "Send API Request",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 1,
      "position": [
        850,
        300
      ]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [
        [
          {
            "node": "Check Start Date",
            "type": "default",
            "index": 0
          }
        ]
      ]
    },
    "Check Start Date": {
      "main": [
        [
          {
            "node": "Format API Query",
            "type": "default",
            "index": 0
          }
        ],
        []
      ]
    },
    "Format API Query": {
      "main": [
        [
          {
            "node": "Send API Request",
            "type": "default",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

However, let's see what happens when the LLM is given context -- in the form of tools -- for n8n nodes, JobTread Jobs, and JobTread's API endpoints.

## TODO
- [ ] Linting n8n workflow for errors and best practices
- [ ] Tool use for more specific docs and context
- [ ] Structured Output for more precise n8n node structure
