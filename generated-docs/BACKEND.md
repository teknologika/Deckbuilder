<!--
IMPORTANT: The MCP client must fill in the content for each section below!
1. Write concise content for each section
2. Do not leave any sections empty
3. Use your analysis to create accurate content
4. If relevant, use AWS Diagram MCP Server to generate AWS architecture diagram in README.md
5. If relevant, use AWS Diagram MCP Server to generate data flow chart in BACKEND.md
-->

# Backend Architecture

<!-- MCP Client: Overview of the backend architecture -->

## Project Structure

<!-- MCP Client: Explain backend project structure -->

## Data Flow

<!-- MCP Client: Generate a data flow diagram using AWS Diagram MCP Server
This should be a diagram showing how data flows through the system components.
# Get the current workspace directory
workspace_dir = "project_directory"

# Create a data flow diagram
with Diagram("Data Flow", show=False, filename="data_flow_diagram"):
    # Define data sources
    api_gateway = APIGateway("API Gateway")
    # Define processing components
    processor = Custom("FastMCP Service")
    # Define data stores
    # Add messaging components if applicable
    queue = SQS("Message Queue")
    topic = SNS("Notification Topic")
    # Show data flow with labeled edges
    api_gateway >> Edge(label="JSON request") >> processor
    processor >> Edge(label="Query/Write") >> data_store
    processor >> Edge(label="Publish event") >> topic
    topic >> Edge(label="Notify") >> queue
```

After generating the data flow diagram with the AWS Diagram MCP Server, replace the image reference below with the path to the generated diagram.
-->

<!-- PLACEHOLDER: Replace this with a data flow diagram generated using AWS Diagram MCP Server -->
## Data Flow Diagram

```
This is a placeholder for the data flow diagram.
Use the awslabs.aws-diagram-mcp-server to generate a proper data flow diagram showing how data moves through the system.
- Backend (FastMCP)
- API Layer (Unknown)
```


<!-- Describe what this data flow diagram shows below -->

## Core Components

<!-- MCP Client: Detail the core backend components -->
