from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

# print(bool(os.getenv("GEMINI_API_KEY")))

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

server_params = StdioServerParameters(
    command="npx",  # Executable
    args=[
        "-y",
        "@openbnb/mcp-server-airbnb",
        "--ignore-robots-txt",
    ],  # Optional command line arguments
    env=None,  # Optional environment variables
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            prompt = "I want to book an apartment in Paris for 2 nights. 17/04/2025 to 21/04/2025"
            await session.initialize()

            mcp_tools = await session.list_tools()
            # print()
            # print()
            # for tool in mcp_tools.tools:
            #     print(tool)
            print("123456")
            tools = types.Tool(function_declarations=[
                {
                    "name":tool.name,
                    "description":tool.description,
                    "parameters":tool.inputSchema,
                }
                for tool in mcp_tools.tools
            ])
            # print("\n\n*-*-*-*-*-*-*-*-*-*-*-*-*-*\n\n")
            # print(tools)
            # print("\n\n*-*-*-*-*-*-*-*-*-*-*-*-*-*\n\n")

            # Send request with function declarations
            print(1234567)
            response = client.models.generate_content(
                model="gemini-2.0-flash",  # Or your preferred model supporting function calling
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    tools=[tools],
                ),  # Example other config
            )

            print("\n\n*-*-*-*-*-*-*-*-*-*-*-*-*-*\n\n")
            print(response)
            print("\n\n*-*-*-*-*-*-*-*-*-*-*-*-*-*\n\n")
            await run()
            # return response

result = asyncio.run(run())
print(result)

