# AG2 course

Five short scripts for AG2's classic `autogen` API.

| Script | What it shows |
|---|---|
| `01_tools.py` | `register_function`: an assistant calls a currency calculator that a user proxy executes |
| `02_converse.py` | Two `ConversableAgent`s (coder and reviewer) talking through `agent.run()` |
| `03_multiagent.py` | A group chat with `AutoPattern` and `run_group_chat` |
| `04_rag.py` | An `update_agent_state` hook that puts the current directory listing in the system message |
| `05_sequential_chat.py` | `initiate_chats`: three chats in a row, each summary carried into the next |

## Run

```bash
cd ag2-course
pip install -r requirements.txt
python 01_tools.py
```

Every script loads its model from `OAI_CONFIG_LIST.json` with `LLMConfig.from_json`. Before the first run, replace the placeholder `api_key` in that file with your OpenAI key, and don't commit the real key.

The config uses `gpt-5.4-mini`. The course was recorded with `gpt-4.1`, which OpenAI removes from the API on 2027-01-14 ([deprecations](https://developers.openai.com/api/docs/deprecations)). None of the scripts set `temperature` or `max_tokens`, so nothing else changes. `autogen` 0.14.1's price table has no `gpt-5.4-mini` entry, so you will see a "cost will be 0" warning; the chats still run.

## Which package

The requirements pin `autogen` 0.14.x. Since AG2 v1.0, `pip install ag2` installs a different framework (`import ag2`) that has no `autogen` module, so none of these scripts would import. The classic API these scripts use is maintained at [ag2ai/ag2classic](https://github.com/ag2ai/ag2classic) and published on PyPI as `autogen`.
