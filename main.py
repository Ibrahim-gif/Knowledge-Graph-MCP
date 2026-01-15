from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
from openai import AsyncAzureOpenAI
from agents import Agent, Runner, set_default_openai_client, OpenAIChatCompletionsModel
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
import asyncio
import logfire

os.environ["OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"] = "http://localhost:4318/v1/traces"

logfire.configure(
    service_name="opentelemetry-instrumentation-openai-agents-logfire",
    send_to_logfire=False,
)
logfire.instrument_openai_agents()

# Setup tracing to console
span_exporter = ConsoleSpanExporter()
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(span_exporter))
trace.set_tracer_provider(tracer_provider)

async def run_main():
    load_dotenv(override=True)
    env = dict(os.environ) 
    env["LIBSQL_URL"] = "file:./memory/ed.db"

    params = {"command": "npx","args": ["-y", "mcp-memory-libsql"]}

    async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as server:
        mcp_tools = await server.list_tools()

    print(f"Available MCP Tools: {mcp_tools}")

    instructions = "You use your entity tools as a persistent memory to store and recall information about your conversations."
    request = "I love cheeesecakes. Can you remember that for me?"
    model = "gpt-4.1-mini"

    async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as mcp_server:
        agent = initialize_agent(name="agent", instructions=instructions, model=model, mcp_servers=[mcp_server])

        # Start tracing
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("Adding Memory"):
            result = await Runner.run(agent, request)
        print(result.final_output)

    async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as mcp_server:
        agent = initialize_agent(name="agent", instructions=instructions, model=model, mcp_servers=[mcp_server])
        with tracer.start_as_current_span("conversation"):
            result = await Runner.run(agent, "My name's Ed. What do you know about me?")
        print(result.final_output)

def initialize_agent(name, instructions, model, mcp_servers):
    from agents import set_tracing_disabled
    set_tracing_disabled(True)

    client = AsyncAzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment ="gpt-4.1",  # your deployment name here
        api_version="2024-10-21"  # or newer supported version
    )
    model = OpenAIChatCompletionsModel(model=model, openai_client=client)
    set_default_openai_client(client)

    agent = Agent(
        name=name,
        instructions=instructions,
        model=model,
        mcp_servers=mcp_servers
    )
    return agent

if __name__ == "__main__":
    print("starting main.py")
    asyncio.run(run_main())