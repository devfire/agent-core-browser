# Agent Core Browser

This project demonstrates how to use the `bedrock-agentcore` and `browser-use` libraries to perform browser automation tasks using natural language.

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

The main script `browser.py` initializes a browser session and runs a predefined task.

To run the script:

```bash
python browser.py
```

The default task is to "Search for a coffee maker on amazon.com and extract details of the first one". You can modify the `task` variable in `browser.py` to perform different actions:

```python
# in browser.py, line 87
task = "Your new browser task here"
```

## How It Works

-   **`browser.py`**: The entry point of the application.
    -   It initializes a `BrowserClient` from `bedrock-agentcore` to manage the browser lifecycle.
    -   It uses `browser-use` to create and manage a persistent browser session.
    -   An `Agent` from `browser-use` is created with a natural language task.
    -   The agent uses a `ChatAnthropicBedrock` model to understand and execute the task.
-   **`pyproject.toml`**: Defines the project metadata and dependencies.
-   **`uv.lock`**: A lock file for reproducible builds.

## Dependencies

-   `bedrock-agentcore`: For managing the browser client.
-   `browser-use`: For browser automation with LLMs.
-   `langchain-aws`: For interacting with Bedrock models.
-   `rich`: For pretty-printing console output.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.