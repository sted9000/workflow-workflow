import json


def extract_action_steps(client, model, transcript, response_format):

    """
    Use an LLM to extract action steps from a transcript.
    
    Args:
        client (OpenAI): The OpenAI client
        model (str): The model to use for the LLM call
        transcript (str): The transcribed text
        response_format (dict): The response format to use for the LLM call
        
    Returns:
        action step (obj)
    """
    print("Extracting action steps from transcript...")
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": "You are an expert at designing workflow automations from transcripts of conversations between myself and a client who want to automate a process in their business. The steps your response should be english, not contain code, and should include relevant details that would help an intern build the workflow. Each step should be numbered as to its position in the workflow. Each step should be a descrete action that can be represented as a workflow node. The structured of the response should JSON, include a single trigger that will be used to start the workflow, and a list of ordered action steps for the workflow."},
            {
                "role": "user", 
                "content": f"Extract a list of descrete, clear, and detailed action steps from this transcript that will later be used by an intern to build a workflow automation.:\n\n{transcript}"}
        ],
        response_format=response_format
    )
    
    action_steps = json.loads(response.choices[0].message.content)
    print(action_steps)
    return action_steps


def match_node_types(client, model, action_steps, response_format, docs):
    """
    Use LLM to add node types to action steps.
    
    Args:
        client (OpenAI): The OpenAI client
        model (str): The model to use for the LLM call
        action_steps (list): List of action step descriptions
        response_format (dict): The response format to use for the LLM call
        docs (dict): Dictionary of node documentation
        
    Returns:
        list: List of dictionaries mapping action steps to node types
    """
    print("Matching node types to action steps...")
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert at mapping text descriptions and details of workflow automations to their correct node types. You will be given a list of action steps and documentation of node types. You will need to match each action step to the most appropriate node type."},
            {"role": "user", "content": f"I have the following action steps that need to be implemented in a workflow by an intern: {json.dumps(action_steps, indent=2)}\n\nHere is the documentation for the node types: {json.dumps(docs, indent=2)}"}    
        ],
        response_format=response_format
    )
    
    mappings = json.loads(response.choices[0].message.content)
    print(mappings)
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