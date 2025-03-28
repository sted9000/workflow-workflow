import os
import openai
import json
from dotenv import load_dotenv
load_dotenv() 
open_ai_client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)
"""
This script traverses the n8n documentation of different nodes, loads the documentation into an LLM which returns "When should I use this node?", and then saves the results in a structured way.
"""

base_dirs = ["./docs/integrations/builtin/app-nodes", "./docs/integrations/builtin/core-nodes", "./docs/integrations/builtin/trigger-nodes"]

def extract_node_docs(base_dir, file_name):
    if file_name.startswith("n8n-nodes-base") and file_name.endswith(".md"):
        with open(os.path.join(base_dir, file_name), "r") as f:
            return {"file_name": file_name.replace(".md", ""), "content": f.read()}
    # if it's a directory, traverse it
    if os.path.isdir(os.path.join(base_dir, file_name)):
        sub_dir = os.path.join(base_dir, file_name)
        for file in os.listdir(sub_dir):
            if file.startswith("index.md"):
                with open(os.path.join(sub_dir, file), "r") as f:
                    return {"file_name": file_name, "content": f.read()}
    

node_docs = []
for base_dir in base_dirs:
    for dir in os.listdir(base_dir):
        node_doc_file = extract_node_docs(base_dir, dir)
        if node_doc_file and node_doc_file["file_name"] and node_doc_file["content"]:
            node_docs.append(node_doc_file)


doc_summaries = []
for node_doc in node_docs:
    # Call OpenAI LLM for each node_doc and get a structured response
    response = open_ai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": "You are an expert summarizer of documentation."},
            {
                "role": "user", 
                "content": f"Please summarize the n8n node type documentation by answering the question 'When would you use this node type':\n\nNode type file name: {node_doc["file_name"]}\n\nDocumentation:\n{node_doc["content"]}"}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "node_summary",
                "schema": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "A summary of the node type documentation."
                        }
                    },
                    "required": ["summary"],
                    "strict": True
                }
            }
        }
    )
    
    content = json.loads(response.choices[0].message.content)
    doc_summaries.append({"file_name": node_doc["file_name"], "summary": content["summary"]})

# Determine if a node is a trigger or an action node by the file name
trigger_nodes = []
action_nodes = []
for doc_summary in doc_summaries:
    if "trigger" in doc_summary["file_name"]:
        trigger_nodes.append(doc_summary)
    else:
        action_nodes.append(doc_summary)

# Save the trigger and action nodes to a file in json format
# Use the file name as the key and the summary as the value
with open("trigger_nodes.json", "w") as f:
    json.dump(trigger_nodes, f)
with open("action_nodes.json", "w") as f:
    json.dump(action_nodes, f)

