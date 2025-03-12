# Automated Workflow Generator
Generate Workflows from client call transcripts

## Background
Creating automated workflows for a clients from scratch is tedious and labor intensive -- very ironic.

## Generating Workflow Triggers and Actions (we'll call them nodes from now on) from audio transcripts
### Inputs
#### Prompt
> You are an expert at designing workflow automations. Take the transcript a call with my client and return the steps in a workflow. The steps should be english, not contain code, and should include relevant details that would help an intern build the workflow. The structured response should include a single trigger and a list of ordered action steps for the workflow.

#### Example
> Here is an example of a well structured response: 
{"trigger": {"description": "New Job Created", "details": "When a new job is created in JobTread the workflow automation will be triggered by a webhook." 
}, "actions": [{"order": 0, "description": "Send Email to Client", "details": Send an email to the client with GMail. The title should be 'Welcome to Your New Job -- Acme Construction'. The body of the email should be a short message about the details of the job (found in the webhook body) and should provide a link the job details." }]

#### Transcript of client call

### Output (Structured Output)
A single trigger and a list of actions
```
{
  "trigger": {
    "description": str,
    "details": [str]
  },
  "actions" [
    {
      "order": int
      "description": str,
      "details": [str]
    }
  ]
}
```

## Add "Node Types"
### Inputs
#### Prompt
> You are an expert at mapping text descriptions and details of workflow automations to their correct node types

#### Transcription to Nodes Response
#### Homemade docs for node types

### Output (Structured Output)
The same output as the Transcript-to-Node call + the node names
```
{
  "trigger": {
    "description": str,
    "details": [str],
    "node_type": str
  },
  "actions" [
    {
      "order": int
      "description": str,
      "details": [str],
      "node_type"
    }
  ]
}
```

## Generate Valid Workflow Files
### Inputs
#### Prompt
> You are an expert workflow automation software engineer. From the following data, documentation, and examples create a valid {{platform_name}} workflow file. 

#### Response to "Add Node Types" Query
#### Comprehensive docs and node types for each of the node types
#### An example valid workflow document

### Output (Structured Output)
Valid workflow file