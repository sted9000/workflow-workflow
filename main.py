import os
import json
import openai
from datetime import datetime
from dotenv import load_dotenv
from llm_calls import transcribe_audio, extract_action_steps, map_action_steps_to_nodes, generate_n8n_workflow
from utils import save_workflow

load_dotenv()

# Set llm clients
open_ai_client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)
local_llm_client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="http://localhost:1234/v1"
)


def main(transcript_path, workflow_platform, output_path):

    # Step 1: Extract action steps
    action_steps = extract_action_steps(open_ai_client, "gpt-4o-mini", transcript_path)

    
    # Step 3: Load n8n node documentation
    # node_docs = load_n8n_node_docs()
    # print(f"Loaded documentation for {len(node_docs)} node types")
    
    # Step 4: Map action steps to node types
    node_docs = json.load(open("context/node_types.json"))
    mappings = map_action_steps_to_nodes(open_ai_client, "gpt-4o-mini", action_steps, node_docs)
    print(f"Created {len(mappings)} mappings between action steps and node types")
    
    # Step 5: Generate n8n workflow
    workflow = generate_n8n_workflow(open_ai_client, "gpt-4o-mini", mappings)

    # # Step 6: Lint the workflow
    # linted_workflow = lint_workflow(workflow)
    
    # Step 7: Save workflow
    save_workflow(workflow, output_path)
    
    print(f"Successfully created n8n workflow: {output_path}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert audio to n8n workflow")
    parser.add_argument("--audio_file", default="./audio/test.m4a", help="Path to the audio file")
    parser.add_argument("--output", default=f"./output/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json", help="Path to save the generated workflow")
    
    args = parser.parse_args()
    
    main(args.audio_file, args.output)