# Agent Core Browser

This project demonstrates how to use the `bedrock-agentcore` and `browser-use` to perform browser automation tasks using natural language, exposed as a `AgentCore` service.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This project uses `uv` for package management. Make sure you have `uv` installed. If not, you can install it with:

```bash
pip install uv
```

You will also need to have Python 3.11 or higher installed.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/agent-core-browser.git
    cd agent-core-browser
    ```

2.  **Create a virtual environment and install dependencies:**

    `uv` will automatically create a virtual environment in the `.venv` directory and install the packages listed in `pyproject.toml`.

    ```bash
    uv pip install -r requirements.txt
    ```

3.  **Configure AWS Credentials:**

    Ensure your AWS credentials are configured correctly. The application uses `boto3` to interact with AWS services, so you can configure credentials via environment variables, a credentials file, or an IAM role.

    For example, using environment variables:

    ```bash
    export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
    export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
    export AWS_SESSION_TOKEN="YOUR_SESSION_TOKEN" # Optional
    export AWS_DEFAULT_REGION="us-east-1"
    ```

    Or using profile
    ```bash
    aws sso login --profile PowerUserAccess-YOUR_ACCOUNT
    ```

### Usage

The main script `browser.py` runs a web service that exposes the browser automation agent.

To run the service:

```bash
python browser.py
```

This will start a local server. You can then send requests to it to perform browser tasks.

### Invoking the service

You can use `curl` to send a prompt to the agent. The agent will then execute the browser task based on the prompt.

```bash
curl -X POST http://localhost:8080/invocations \
-H "Content-Type: application/json" \
-d '{"prompt": "Get me the uuid from the https://httpbin.org/uuid"}'
```

Expected output:

```
✅ Task completed successfully!

🔌 Closing browser session...
✅ Browser session closed

INFO     [bedrock_agentcore.tools.browser_client] Stopping browser session...
✅ Browser client stopped

The UUID from https://httpbin.org/uuid is: **dbd39a94-fddc-44d7-b0f2-3a9d99785087**

This endpoint returns a randomly generated UUID in JSON format, and I successfully extracted the UUID value for you.
✅ Strands Task completed successfully!

```
### How It Works

-   **`browser.py`**: The entry point of the application.
    -   It uses `BedrockAgentCoreApp` to create a web service.
    -   The `@app.entrypoint` decorator on `run_strands_agentcore` exposes it as the main endpoint.
    -   It initializes a `StrandsAgent` from the `strands` library.
    -   The `run_browser_task` function is defined as a tool that the `StrandsAgent` can use.
    -   Inside `run_browser_task`, it initializes a `BrowserClient` from `bedrock-agentcore` to manage the browser lifecycle.
    -   It uses `browser-use` to create and manage a persistent browser session for the automation task.
    -   An `Agent` from `browser-use` is created with a natural language task passed from the `StrandsAgent`.
    -   The agent uses a `ChatAnthropicBedrock` model to understand and execute the task.
-   **`pyproject.toml`**: Defines the project metadata and dependencies.
-   **`uv.lock`**: A lock file for reproducible builds.

## Dependencies

-   `bedrock-agentcore`: For managing the browser client and creating the web service.
-   `browser-use`: For browser automation with LLMs.
-   `rich`: For pretty-printing console output.
-   `strands`: For creating the main agent and managing tools.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
