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

## Formatting Nodes into Valid Workflows
### Inputs
#### Prompt
> You are an expert at mapping text descriptions and details of workflow automations to their correct 

#### Trigger and Actions response (see above)

#### Automation platform
> You will be a {{workflow_platform}} workflow.

#### Documentation of node types
> 

#### Credentials for third party connections

### Output (Structured Output)
Valid workflow file


> You are an expert at engineering valid production quality workflow automation files when given a set of action steps. 