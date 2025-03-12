import os
import json
import openai
from datetime import datetime
from dotenv import load_dotenv
from llm_calls import extract_action_steps, add_node_types, build_workflow_file
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


def main(transcript, output_path, workflow_platform):

    # Extract action steps from transcript
    action_steps_response_schema = json.load(open("structured_outputs/action_steps.json"))
    action_steps_response = extract_action_steps(open_ai_client, "gpt-4o-mini", transcript, action_steps_response_schema)
    print(f"Action steps:\n{json.dumps(action_steps_response, indent=2)}")

    # Format action steps
    action_steps = action_steps_response

    # Add uuids to action steps
    action_steps["trigger"]["uuid"] = str(uuid.uuid4())
    for action_step in action_steps:
        action_step["uuid"] = str(uuid.uuid4())

    # Map action steps to node types
    node_types_response_schema = json.load(open("structured_outputs/node_types.json"))
    node_types_response = add_node_types(open_ai_client, "gpt-4o-mini", action_steps, node_types_response_schema, load_node_types(workflow_platform))
    print(f"Action steps with node types:\n{json.dumps(action_steps, indent=2)}")
    
    # Add the node types to the action steps
    for action_step in action_steps:
        for node in node_types_response:
            if node["id"] == action_step["id"]:
                action_step["node_type"] = node["node_type"]
                action_step["node_name"] = node["node_name"]

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