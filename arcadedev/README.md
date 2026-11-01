# Arcade.dev examples

Scripts that call [Arcade](https://docs.arcade.dev) tools directly, from CrewAI, and from the OpenAI Agents SDK. `claude.md` is a reference sheet of Arcade docs for your coding assistant, and `mcp_server/` is an MCP server scaffolded with the Arcade CLI.

| Script | What it does | Install |
| --- | --- | --- |
| `00_simple_tool_call.py` | Runs the hosted `Math.Sqrt` tool. | `pip install arcadepy python-dotenv` |
| `01_simple_auth_tool.py` | Authorizes and runs `GitHub.SetStarred` (opens an auth link the first time). | `pip install arcadepy python-dotenv` |
| `02_framework_tool.py` | CrewAI agent with Arcade Gmail tools via `crewai-arcade`. | see the note below |
| `03_mcp_toolkit.py` | OpenAI Agents SDK agent with the Arcade Gmail toolkit. | `pip install arcadepy agents-arcade "openai-agents~=0.24" python-dotenv` |
| `04_crewai_mcp_gateway.py` | CrewAI agent that reaches Gmail through an Arcade MCP Gateway. | `pip install "crewai>=1.15,<2" python-dotenv` |

Install 03 and 04 in separate virtual environments: openai-agents 0.24 needs `openai>=3`, and crewai 1.15 needs `openai<3`.

Create a `.env` in this folder:

```bash
ARCADE_API_KEY=arc_...
OPENAI_API_KEY=sk-...
```

The scripts hardcode the course's Arcade user id (an email address). Replace it with your own before you run them. `04_crewai_mcp_gateway.py` also points at the course's gateway URL; create your own gateway in the Arcade dashboard and use its URL.

## Models

03 and 04 use `gpt-5.4-mini`. They used `gpt-4.1`, which OpenAI removes from the API on January 14, 2027 ([deprecations](https://developers.openai.com/api/docs/deprecations)).

## Note on 02_framework_tool.py

Arcade has deprecated `crewai-arcade`. The current release, 2.0.1, is an empty package that only prints a deprecation warning, so `from crewai_arcade import ArcadeToolManager` fails after a plain `pip install crewai-arcade`. To run the script as written, install the last working release, which pulls in CrewAI 0.x and needs Python 3.10 to 3.12:

```bash
pip install "crewai-arcade==0.1.1" python-dotenv
```

That script still uses `gpt-4.1` and is kept as written. For new CrewAI projects, use the MCP Gateway approach in `04_crewai_mcp_gateway.py`.
