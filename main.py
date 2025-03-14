import os
import json
import openai
from datetime import datetime
from dotenv import load_dotenv
from llm_calls import extract_action_steps, match_node_types, build_workflow_file
import uuid
load_dotenv()

# Set llm clients
open_ai_client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)
local_llm_client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="http://localhost:1234/v1"
)


def load_node_types(workflow_platform):
    node_types = json.load(open(f"context/{workflow_platform}/node_types.json"))
    return node_types


def load_workflow_docs(workflow_platform):
    node_docs = json.load(open(f"context/{workflow_platform}/node_docs.json"))
    return node_docs


def load_workflow_examples(workflow_platform):
    workflow_examples = json.load(open(f"context/{workflow_platform}/workflow_examples.json"))
    return workflow_examples


def load_workflow_response_schema(workflow_platform):
    workflow_response_schema = json.load(open(f"structured_outputs/{workflow_platform}/workflow.json"))
    return workflow_response_schema


def main(transcript_path, output_path, workflow_platform):

    # Extract action steps from transcript
    # transcript = open(transcript_path).read()

    # action_steps_response_schema = json.load(open("structured_outputs/action_steps.json"))
    # action_steps = extract_action_steps(open_ai_client, "gpt-4o-mini", transcript, action_steps_response_schema)
    # print(f"Action steps response:\n{json.dumps(action_steps_response, indent=2)}")
    
    action_steps = [
        {
        "order": 1,
        "type": "trigger",
        "action_step_description": "Detect job status change in JobTread",
        "action_step_details": [
            "Set up a webhook in JobTread to monitor changes in job statuses.",
            "The trigger should activate when a job status changes from 'lead' to 'proposal'."
        ]
        },
        {
        "order": 2,
        "type": "action",
        "action_step_description": "Send a confirmation email to the customer",
        "action_step_details": [
            "Use Gmail API to send an email.",
            "The email subject should indicate that a proposal has been sent.",
            "Include the following body text: 'Thank you for working with us. We just sent over a proposal and we'd love for your feedback and review. Let us know if you have any questions or concerns.'",
            "Ensure the email is sent to the customer's email address stored in JobTread."
        ]
        }
    ]
    
    # Add ids to action steps
    for action_step in action_steps:
        action_step["id"] = str(uuid.uuid4())

    action_steps = [
  {
    "order": 1,
    "type": "trigger",
    "action_step_description": "Detect job status change in JobTread",
    "action_step_details": [
      "Set up a webhook in JobTread to monitor changes in job statuses.",
      "The trigger should activate when a job status changes from 'lead' to 'proposal'."
    ],
    "id": "8db90c60-a616-44fb-bf24-3e4d3fa4696c"
  },
  {
    "order": 2,
    "type": "action",
    "action_step_description": "Send a confirmation email to the customer",
    "action_step_details": [
      "Use Gmail API to send an email.",
      "The email subject should indicate that a proposal has been sent.",
      "Include the following body text: 'Thank you for working with us. We just sent over a proposal and we'd love for your feedback and review. Let us know if you have any questions or concerns.'",
      "Ensure the email is sent to the customer's email address stored in JobTread."
    ],
    "id": "8c080201-fc4a-4ff5-bdf1-02aebf9199a6"
  }
]
    

    # Map action steps to node types
    # node_types_response_schema = json.load(open("structured_outputs/node_types.json"))
    # node_types_response = match_node_types(open_ai_client, "gpt-4o-mini", action_steps, node_types_response_schema, load_node_types(workflow_platform))
    # print(f"Node types response:\n{json.dumps(node_types_response, indent=2)}")

    node_types_response = {
  "matched_node_types": [
    {
      "input_object_id": "8db90c60-a616-44fb-bf24-3e4d3fa4696c",
      "node_id": "n8n-trigger-jobthread-job-status-change"
    },
    {
      "input_object_id": "8c080201-fc4a-4ff5-bdf1-02aebf9199a6",
      "node_id": "n8n-action-send-email"
    }
  ]
}

    node_types = node_types_response["matched_node_types"]
    
    # Add the node types to the action steps
    for action_step in action_steps:
        for node in node_types:
            if action_step["id"] == node["input_object_id"]:
                action_step["node_id"] = node["node_id"]
                

    # Build workflow file
    workflow_response = build_workflow_file(open_ai_client, "gpt-4o-mini", action_steps, load_workflow_response_schema(workflow_platform), load_workflow_docs(workflow_platform), load_workflow_examples(workflow_platform), workflow_platform)
    print(f"Workflow:\n{json.dumps(workflow_response, indent=2)}")
    
    # Save workflow
    with open(output_path, "w") as f:
        json.dump(workflow_response, f, indent=2)

    print(f"Successfully created {workflow_platform} workflow: {output_path}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert audio to n8n workflow")
    parser.add_argument("--transcript", default="./transcripts/test.txt", help="Path to the transcript file")
    parser.add_argument("--output", default=f"./output/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json", help="Path to save the generated workflow")
    
    args = parser.parse_args()
    
    main(args.transcript, args.output, "n8n")