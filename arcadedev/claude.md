# Arcade.dev Development Guide

## Table of Contents

- [What is Arcade.dev?](#what-is-arcadedev)
- [Step 1: Arcade's Hosted Tools Quickstart](#step-1-arcades-hosted-tools-quickstart)
- [Step 2: Build MCP Server](#step-2-build-mcp-server-01_framework_toolpy)
- [Step 3: MCP Toolkit](#step-3-mcp-toolkit-02_mcp_toolkitpy)
- [Step 4: MCP Gateways](#step-4-mcp-gateways-03_crewai_mcp_gatewaypy)

---

## What is Arcade.dev?

### The Big Picture Problem

AI agents today face a **critical limitation**: they can chat, answer questions, and provide recommendations, but they **can't actually DO things** on behalf of users. Why?

#### The Authentication Challenge:
- Most APIs require OAuth tokens or API keys
- AI agents traditionally can't securely authenticate as individual users
- Developers must build custom OAuth flows for each service
- Managing secrets, tokens, and user permissions is complex and risky
- Enterprise security requirements (SOC 2, encryption) are hard to meet

#### The Integration Nightmare:
- Every integration (Gmail, Slack, GitHub, etc.) requires custom code
- Different frameworks require different implementations
- No standardized way to share tools across projects
- Testing and evaluating tool reliability is manual and time-consuming

### What Arcade.dev Does

Arcade.dev is an **AI tool-calling platform** that acts as the **"SSO for AI Agents"** - it's infrastructure that lets AI agents securely take actions on behalf of users across 100+ services.

**Think of it as:**
- **For AI Agents**: What Stripe is for payments
- **Authentication Layer**: OAuth management for AI
- **Tool Marketplace**: Pre-built integrations + SDK for custom tools
- **Production Platform**: Complete runtime, registry, and evaluation suite

### Core Value Propositions

#### 1. Secure Authentication (Agent Auth)
- **OAuth flows managed for you**: No need to build authorization logic
- **30+ auth providers**: Google, GitHub, Slack, Reddit, LinkedIn, etc.
- **User-level permissions**: AI acts as the user, not as a "bot"
- **Token security**: Encrypted storage, SOC 2 compliant
- **LLMs never see tokens**: Secrets injected at runtime via context
- **Remember authorization**: Users don't re-auth unless they revoke

**Why this matters**: Your AI agent can send emails from a user's Gmail, post to their Slack, or update their CRM - all with proper permissions and security.

#### 2. Pre-Built Tool Library (Hosted Tools)
- **100+ integrations ready to use**: Gmail, Slack, GitHub, Salesforce, Notion, etc.
- **Call with one line of code**: No need to build API wrappers
- **Always up-to-date**: Arcade maintains the integrations
- **Multi-framework support**: Works with LangChain, CrewAI, OpenAI Agents, Vercel AI

**Example use cases**:
- Email automation (read, send, draft responses)
- Calendar management (schedule meetings, check availability)
- CRM updates (Salesforce, HubSpot)
- Team collaboration (Slack messages, GitHub PRs)
- Content creation (Notion pages, Google Docs)

#### 3. Model Context Protocol (MCP) Leadership

**What's MCP?**
Model Context Protocol is an open standard for connecting AI agents to external tools and data sources.

**The MCP Problem:**
- 99% of MCP servers are single-user only
- Designed for local resources (files, databases)
- No authentication mechanism for multi-user scenarios
- Can't handle OAuth for third-party services
- Not production-ready for enterprise

**Arcade's MCP Solution:**
- First to support MCP with multi-user auth
- Build MCP servers with `arcade-mcp` framework
- Deploy MCP servers with OAuth built-in
- **MCP Gateways**: Federate tools from multiple MCP servers
- **Streamable HTTP transport**: Real-time tool execution
- **Contributing to MCP spec**: Helping standardize authentication

**Why this matters**: You can build custom MCP tools once and use them across Claude Desktop, Cursor, VS Code, and any MCP client - with secure user authentication.

#### 4. Custom Tool SDK (Build Your Own)
- **Framework-agnostic**: Build once, use anywhere
- **Secrets management**: Built-in `.env` support
- **Auth decorators**: Add OAuth with `@app.tool(requires_auth=...)`
- **Type-safe**: Annotated parameters for LLM understanding
- **Deploy anywhere**: Cloud, VPC, on-premises (Docker, K8s)

#### 5. Tool Evaluations & Testing
- **Automated benchmarking**: Test how well LLMs use your tools
- **Reliability metrics**: Track success rates, errors, latency
- **Continuous improvement**: Identify and fix tool issues before production

#### 6. Production Infrastructure
- **Monitoring & logging**: Track agent behavior and tool usage
- **Error handling**: Graceful failures with retry logic
- **Rate limiting**: Protect APIs from abuse
- **Multi-tenancy**: Isolate user data and permissions
- **SOC 2 compliant**: Enterprise-grade security

### Who Benefits from Arcade.dev?

#### 1. AI Engineers & Developers
- Build production agents 10x faster
- No need to reinvent OAuth for each integration
- Focus on agent logic, not infrastructure
- Test and evaluate tools systematically

#### 2. Startups Building AI Products
- Ship AI features quickly without building integrations from scratch
- Scale to enterprise customers with security compliance
- Reduce maintenance burden (Arcade updates integrations)

#### 3. Enterprises
- Deploy secure, authenticated agents across the organization
- Control which tools agents can access
- Audit trail for agent actions
- On-premises deployment option for sensitive data

#### 4. AI Agent Framework Maintainers
- Integrate Arcade for instant tool access
- Provide users with 100+ pre-built integrations
- Support for LangChain, CrewAI, OpenAI Agents, etc.

### Real-World Use Cases

**Customer Support Automation:**
- Agent reads support tickets (Zendesk, Intercom)
- Searches knowledge base (Notion, Confluence)
- Drafts personalized responses
- Updates CRM with interaction notes (Salesforce)
- Sends follow-up emails (Gmail)

**Sales Automation:**
- Monitor leads (Salesforce, HubSpot)
- Research prospects (LinkedIn, Clearbit)
- Schedule discovery calls (Google Calendar)
- Send personalized outreach (Gmail, Slack)
- Update deal stages automatically

**Internal Operations:**
- Summarize daily emails and prioritize
- Schedule team meetings based on availability
- Update project management tools (Jira, Linear)
- Post status updates to Slack
- Generate reports from multiple data sources

**Personal Assistant:**
- Manage email inbox (archive, label, respond)
- Schedule appointments
- Track expenses (Mint, Plaid)
- Control smart home (IoT integrations)
- Aggregate information from multiple services

### The Vision: "SSO for AI Agents"

Just like **Stripe** made payments infrastructure invisible so developers could focus on their product...

**Arcade.dev makes tool-calling infrastructure invisible** so developers can focus on building powerful AI agents.

**Their Mission:**
> "Unlock anyone trying to build an agent that does more than just information retrieval"

**The Outcome:**
AI agents that don't just chat - they **get work done**.

### Quick Stats

- **$12M Series A** funding (2025)
- **30+ auth providers** supported
- **100+ pre-built integrations**
- **SOC 2 Type II** compliant
- **Multi-framework** support (LangChain, CrewAI, Agents, etc.)
- **Open source** MCP framework (`arcade-mcp`)

---

## Step 1: Arcade's Hosted Tools Quickstart

Arcade gives your AI agents the power to act. With Arcade's Hosted Tools, your AI can send Gmail, update Notion, message in Slack, and more.

### Outcomes

Install and use the Arcade client to call Arcade Hosted Tools.

### You will Learn

- Install the Arcade client
- Execute your first tool using the Arcade client
- Authorize a tool to star a GitHub repository on your behalf

### Prerequisites

- An Arcade account
- An Arcade API key
- The `uv` package manager

### Install the Arcade client

In your terminal, run the following command to install the Python client package `arcadepy`:

```bash
uv pip install arcadepy
```

### Instantiate and use the client

Create a new script called `example.py`:

```python
from arcadepy import Arcade

# You can also set the `ARCADE_API_KEY` environment variable instead of passing it as a parameter.
client = Arcade(api_key="{arcade_api_key}")

# Arcade needs a unique identifier for your application user (this could be an email address, a UUID, etc).
# In this example, use the email you used to sign up for Arcade.dev:
user_id = "tylerreedytlearning@gmail.com"

# Let's use the `Math.Sqrt` tool from the Arcade Math MCP Server to get the square root of a number.
response = client.tools.execute(
    tool_name="Math.Sqrt",
    input={"a": '625'},
    user_id=user_id,
)

print(f"The square root of 625 is {response.output.value}")

# Now, let's use a tool that requires authentication to star a GitHub repository
auth_response = client.tools.authorize(
    tool_name="GitHub.SetStarred",
    user_id=user_id,
)

if auth_response.status != "completed":
    print(f"Click this link to authorize: `{auth_response.url}`. The process will continue once you have authorized the app.")
    # Wait for the user to authorize the app
    client.auth.wait_for_completion(auth_response.id)

response = client.tools.execute(
    tool_name="GitHub.SetStarred",
    input={
        "owner": "ArcadeAI",
        "name": "arcade-mcp",
        "starred": True,
    },
    user_id=user_id,
)

print(response.output.value)
```

### Run the code

```bash
uv run example.py
```

Expected output:
```
> The square root of 625 is 25
> Successfully starred the repository ArcadeAI/arcade-mcp
```


## Step 2: Build MCP Server (`01_framework_tool.py`)

Creating an MCP server, configuring it for Cursor, and demonstrating usage with agents.

### Build MCP Server QuickStart

#### Outcomes

Build and run an MCP Server with tools that you create.

#### You will Learn

- Install `arcade-mcp`, the secure framework for building MCP servers
- Start your MCP server and connect to it from your favorite MCP client
- Call a simple tool
- Call a tool that requires a secret
- Create an Arcade account
- Call a tool that requires auth

#### Prerequisites

- Python 3.10 or higher
- The `uv` package manager

### Install the Arcade CLI

In your terminal, run the following command to install the `arcade-mcp` package - Arcade's CLI:

```bash
uv tool install arcade-mcp
```

This will install the Arcade CLI as a uv tool, making it available system-wide.

### Create Your Server

In your terminal, run the following command to scaffold a new MCP Server called `my_server`:

```bash
arcade new my_server
cd my_server/src/my_server
```

This generates a Python module with the following structure:

```
my_server/
├── src/
│   └── my_server/
│       ├── __init__.py
│       ├── .env.example
│       └── server.py
└── pyproject.toml
```

**File descriptions:**
- `server.py` - Entrypoint file with MCPApp and example tools
- `pyproject.toml` - Dependencies and project configuration
- `.env.example` - Example .env file containing a secret required by one of the generated tools in server.py

`server.py` includes proper structure with command-line argument handling. It creates an MCPApp with three sample tools:

- **greet**: This tool has a single argument, the name of the person to greet. It requires no secrets or auth
- **whisper_secret**: This tool requires no arguments, and will output the last 4 characters of a `MY_SECRET_KEY` secret that you can define in your `.env` file
- **get_posts_in_subreddit**: This tool has a single argument, a subreddit, and will return the latest posts on that subreddit. It requires the user to authorize the tool to perform a read operation on their behalf

> **Note:** If you're having issues with the `arcade` command, please see the Troubleshooting section.

### Setup the secrets in your environment

Secrets are sensitive strings like passwords, API keys, or other tokens that grant access to a protected resource or API. Arcade includes the "whisper_secret" tool that requires a secret key to be set in your environment. If the secret is not set, the tool will return an error.

You can create a `.env` file at the same directory as your entrypoint file (`server.py`) and add your secret:

```env
MY_SECRET_KEY="my-secret-value"
```

The generated project includes a `.env.example` file with the secret key name and example value. You can rename it to `.env` to start using it:

```bash
mv .env.example .env
```

### Connect to Arcade to unlock authorized tool calling

Since the Reddit tool accesses information only available to your Reddit account, you'll need to authorize it. For this, you'll need to create an Arcade account and connect to it from the terminal:

```bash
arcade login
```

Follow the instructions in your browser, and once you've finished, your terminal will be connected to your Arcade account.

### Run your MCP Server

Run your MCP Server using one of the following commands in your terminal:

```bash
uv run server.py stdio
```

> **Note:** When using the stdio transport, MCP clients typically launch the MCP server as a subprocess. Because of this, the server may run in a different environment and not have access to secrets defined in your local `.env` file. Please refer to the create a tool with secrets guide for more information.

You should see output like this in your terminal:

```
2025-11-03 13:46:11.041 | DEBUG    | arcade_mcp_server.mcp_app:add_tool:242 - Added tool: greet
2025-11-03 13:46:11.042 | DEBUG    | arcade_mcp_server.mcp_app:add_tool:242 - Added tool: whisper_secret
2025-11-03 13:46:11.043 | DEBUG    | arcade_mcp_server.mcp_app:add_tool:242 - Added tool: get_posts_in_subreddit
INFO     | 13:46:11 | arcade_mcp_server.mcp_app:299 | Starting my_server v1.0.0 with 3 tools
```

### Configure your MCP Client(s)

Now you can connect MCP Clients to your MCP server:

```bash
# Configure Cursor to use your MCP server with the default transport (stdio)
arcade configure cursor

# Configure Cursor to use your MCP server with the http transport
arcade configure cursor --transport http
```

### Try it out!

Try calling your tool inside your assistant. Here's some prompts you can try:

- "Get some posts from the r/mcp subreddit"
- "What's the last 4 characters of my secret key?"
- "Greet me as Supreme MCP Master"

### Troubleshooting

#### `arcade` command not found or not working

If you're getting issues with the `arcade` command, please make sure you did not install it outside of your virtual environment. For example, if your system-wide Python installation older than 3.10, you may need to uninstall arcade from that Python installation in order for the terminal to recognize the `arcade` command installed in your virtual environment.

#### The Reddit tool is not working

Ensure you run `arcade login` and follow the instructions in your browser to connect to your Arcade account.

#### The Whisper Secret tool is not working

Ensure you have set the environment variable in your terminal or `.env` file, and that it matches the secret key defined in the `@app.tool` decorator. If you are using the stdio transport, then ensure the environment variable is set in the MCP client's configuration file.


## Step 3: MCP Toolkit (`02_mcp_toolkit.py`)

Look for any toolkit, and you can add it in this example with authorization.

---

## Step 4: MCP Gateways (`03_crewai_mcp_gateway.py`)

### Overview

MCP Gateways are a way to connect multiple MCP Servers to your agent, application, or IDE. MCP Gateways allow you to federate the tools from multiple MCP Servers into a single collection for easier management, control, and access. You can mix and match tools from different MCP Servers in the same project, and not all tools from a MCP server need to be available to the same LLM.

### Configure MCP Gateways

To configure an MCP Gateway, go to the [MCP Gateways dashboard](https://api.arcade.dev/mcp) and click on the "Create MCP Gateway" button.

When configuring an MCP Gateway, you can select the tools you want to include in the Gateway from any MCP Servers available to the project.

#### MCP Gateway Configuration Options

The options available when configuring an MCP Gateway are:

- **Name**: The name of the MCP Gateway. Informative only.
- **Description**: The description of the MCP Gateway. If set, this information will be returned to the LLM to hint at the purpose of the tools within the MCP Gateway.
- **Slug**: The slug of the MCP Gateway. This is the URL slug that will be used to access the MCP Gateway. It must be unique.
- **Allowed Tools**: If set, only the tools in the MCP Servers that are selected will be available to the MCP Gateway. If left blank, all tools from the MCP Servers available to the project will be available through the MCP Gateway.

### How to use MCP Gateways

Any MCP client that supports the Streamable HTTP transport can use an Arcade MCP Gateway. To use an Arcade MCP Gateway, you can use the following URL in your MCP client:

```
https://api.arcade.dev/mcp/<YOUR-GATEWAY-SLUG>
```

Learn how to use MCP Gateways with:

- Cursor
- Claude Desktop
- Visual Studio Code