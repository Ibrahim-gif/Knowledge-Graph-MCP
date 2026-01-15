# Copilot Instructions for MCP - part 2

## Project Overview
- This project demonstrates usage of the `openai-agents` library with Azure OpenAI, persistent memory via MCP, and OpenTelemetry tracing.
- Main entry points: `main.py` (hello world), `main.py` (core agent logic, tracing, memory, and MCP integration).

## Key Components
- **Agents**: Defined and run in `main.py` using the `openai-agents` library. Agents are initialized with Azure OpenAI models and MCP memory tools.
- **MCP Integration**: Uses `MCPServerStdio` to provide persistent memory for agents. Example: storing and recalling user preferences.
- **Tracing**: OpenTelemetry and Logfire are configured for tracing agent operations and OpenAI calls. Tracing is output to the console.
- **Async/Await**: All agent and server operations are asynchronous.

## Developer Workflows
- **Run main**: `python main.py` (prints hello world)
- **Run agent demo**: `python main.py` (runs agent with memory and tracing)
- **Dependencies**: Install with `pip install -e .` (requires Python 3.11+)
- **Environment**: Set `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT` in a `.env` file for Azure OpenAI access.
- **MCP Memory**: Requires `npx -y mcp-memory-libsql` (Node.js) for local memory server. Ensure Node.js is installed.

## Patterns & Conventions
- **Agent Initialization**: See `initialize_agent` in `main.py` for the standard pattern.
- **Tracing**: Always use OpenTelemetry for new agent operations. See `run_main` for span usage.
- **Environment Variables**: Use `python-dotenv` to load `.env`.
- **Model Selection**: Default is `gpt-4.1-mini` for agent, with deployment name set in `initialize_agent`.

## Integration Points
- **Azure OpenAI**: All completions use Azure endpoints and deployments.
- **MCP Memory**: Agents interact with MCP memory via `MCPServerStdio`.
- **OpenTelemetry**: Tracing is enabled for both agent logic and OpenAI calls.

## Example: Adding a New Agent
- Copy the `initialize_agent` and `Runner.run` pattern from `main.py`.
- Use async/await for all agent and MCP operations.
- Add tracing spans for new workflows.

## References
- `main.py`: Full example of agent, memory, and tracing integration.
- `pyproject.toml`: Dependency management.
- `.env`: Required for Azure OpenAI credentials (not checked in).

---
If any section is unclear or missing details, please provide feedback for further refinement.
