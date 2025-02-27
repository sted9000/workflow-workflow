import json
from pathlib import Path

def load_n8n_node_docs(docs_path):
    """
    Load n8n node documentation from a local directory.
    
    Args:
        docs_path (str): Path to the n8n nodes documentation directory
        
    Returns:
        dict: Dictionary of node documentation
    """
    print(f"Loading n8n node documentation from: {docs_path}")
    
    node_docs = {}
    docs_dir = Path(docs_path)
    
    if not docs_dir.exists():
        print(f"Warning: Documentation directory {docs_path} not found")
        return node_docs
    
    for file_path in docs_dir.glob("**/*.json"):
        try:
            with open(file_path, "r") as f:
                node_info = json.load(f)
                node_name = file_path.stem
                node_docs[node_name] = node_info
        except Exception as e:
            print(f"Error loading node documentation from {file_path}: {e}")
    
    return node_docs


def save_workflow(workflow, output_path):
    """
    Save the generated n8n workflow to a JSON file.
    
    Args:
        workflow (dict): n8n workflow JSON
        output_path (str): Path to save the workflow file
        
    Returns:
        None
    """
    print(f"Saving workflow to: {output_path}")
    
    with open(output_path, "w") as f:
        json.dump(workflow, f, indent=2)
