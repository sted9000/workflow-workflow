import openai
from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)  # Make sure to set OPENAI_API_KEY in your environment variables

def transcribe_audio(audio_file_path):
    """Transcribe audio file using OpenAI Whisper API"""
    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text

def get_action_steps(transcript):
    """Extract action steps from transcript using GPT"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts clear steps from text."},
            {"role": "user", "content": "Give me the action steps in the automation workflow from this transcript:\n\n" + transcript},
            {"role": "user", "content": "Note that the steps should reflect that we are not doing any navigation. Webhooks for all JobTread events will be captured and handled by the automation workflow."}
        ]
    )
    return response.choices[0].message.content

def create_n8n_workflow(action_steps):
    """Create n8n workflow from action steps"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert in creating n8n workflows. Create a valid n8n workflow JSON that implements the given action steps. Include appropriate nodes and connections."},
            {"role": "user", "content": f"Create an n8n workflow (no comments) JSON for these steps:\n{action_steps}"}
        ]
    )
    
    # Parse the JSON workflow from the response
    workflow_json = response.choices[0].message.content
    
    # Remove the code block markers
    workflow_json = workflow_json.replace("```json", "").replace("```", "")
    
    # Save the workflow
    workflow_path = Path("workflow.json")
    with open(workflow_path, "w") as f:
        f.write(workflow_json)
    
    return workflow_path

def main():
    # 1. Get audio file path from user
    audio_file_path = input("Enter the path to your audio file: ")
    
    # 2. Transcribe audio
    print("Transcribing audio...")
    transcript = transcribe_audio(audio_file_path)
    print("\nTranscription:")
    print(transcript)
    
    # 3. Extract action steps
    print("\nExtracting action steps...")
    action_steps = get_action_steps(transcript)
    print("\nAction Steps:")
    print(action_steps)
    
    # 4. Create n8n workflow
    print("\nCreating n8n workflow...")
    workflow_path = create_n8n_workflow(action_steps)
    print(f"\nWorkflow saved to: {workflow_path}")

if __name__ == "__main__":
    main()
