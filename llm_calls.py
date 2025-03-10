import json


def transcribe_audio(client, model,audio_file_path):
    """
    Transcribe an audio file using OpenAI's Whisper model.
    
    Args:
        audio_file_path (str): Path to the audio file
        
    Returns:
        str: The transcribed text
    """
    print(f"Transcribing audio file: {audio_file_path}")
    
    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model=model
        )
    
    return transcript.text


def extract_action_steps(client, model, transcript):

    """
    Use an LLM to extract action steps from a transcript.
    
    Args:
        transcript (str): The transcribed text
        
    Returns:
        list: List of action step descriptions
    """
    print("Extracting action steps from transcript...")
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": "You are an assistant that identifies actionable steps from transcripts. Extract clear, concrete actions that could be automated in a workflow."},
            {
                "role": "user", 
                "content": f"Extract a list of actionable steps from this transcript. Format your response as a JSON array of strings, with each string being a clear and detailed action step:\n\n{transcript}"}
        ],
        response_format={"type": "json_object"}
    )
    
    action_steps = json.loads(response.choices[0].message.content).get("action_steps", [])
    return action_steps


def map_action_steps_to_nodes(client, model, action_steps, node_docs):
    """
    Map action steps to appropriate n8n node types using an LLM and node documentation.
    
    Args:
        action_steps (list): List of action step descriptions
        node_docs (dict): Dictionary of node documentation
        
    Returns:
        list: List of dictionaries mapping action steps to node types
    """
    
    
    # Use the LLM to map action steps to nodes
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an assistant that helps map action steps to appropriate n8n node types."},
            {"role": "user", "content": f"""
I have the following action steps that need to be implemented in an n8n workflow:

{json.dumps(action_steps, indent=2)}


Map each action step to the most appropriate n8n node type. For each action step, provide:
1. The original action step
2. The recommended n8n node type
3. A brief explanation of why this node is appropriate

Format your response as a JSON object with an array called 'mappings', where each item contains 'action_step_description' and  'node_type', 'explanation'. Below is the documentation for the node types:

{json.dumps(node_docs, indent=2)}
"""}
        ],
        response_format={"type": "json_object"}
    )
    
    mappings = json.loads(response.choices[0].message.content).get("mappings", [])
    return mappings


def generate_n8n_workflow(client, model, mappings):
    """
    Generate an n8n workflow based on the mapped action steps and node types.
    
    Args:
        mappings (list): List of dictionaries mapping action steps to node types
        
    Returns:
        dict: n8n workflow JSON
    """
    print("Generating n8n workflow...")
    
    # Use the LLM to create the actual workflow JSON
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an assistant that creates n8n workflows. Generate a complete, valid n8n workflow JSON based on the provided node mappings. You should use the tools to pull in examples of specific node types and their structure."},
            {"role": "user", "content": f"""
Create a complete n8n workflow JSON based on these node mappings:

{json.dumps(mappings, indent=2)}

The workflow should:
1. Start with a proper trigger node
2. Connect all nodes in a logical sequence
3. Include all necessary configuration parameters
4. Use proper n8n workflow syntax and structure by referencing the examples provided in the tools

Format your response as a valid JSON object representing an n8n workflow.
"""}
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_node_example",
                    "description": "Get an example of a specific n8n node type",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "node_type": {
                                "type": "string",
                                "description": "The name of the n8n node type to get an example for"
                            }
                        },
                        "required": ["node_type"]
                    }
                }
            }
        ],
        
        
        response_format={"type": "json_object"}
    )
    
    # workflow = json.loads(response.choices[0].message.content)
    print(response.choices[0].message.tool_calls)
    exit()
    # return workflow