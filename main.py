from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()



client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

server_params = StdioServerParameters(
    command="npx",  
    args=[
        "-y",
        "@openbnb/mcp-server-airbnb",
        "--ignore-robots-txt",
    ],  
    env=None,  
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            prompt = "I want to book an apartment in Paris for 2 nights. 17/04/2025 to 21/04/2025"
            await session.initialize()

            mcp_tools = await session.list_tools()

            tools = types.Tool(function_declarations=[
                {
                    "name":tool.name,
                    "description":tool.description,
                    "parameters":tool.inputSchema,
                }
                for tool in mcp_tools.tools
            ])
        

            # Send request with function declarations
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    tools=[tools],
                ),  
            )


            if response.candidates[0].content.parts[0].function_call:
                print(response.candidates[0])
                function_call = response.candidates[0].content.parts[0].function_call
                print(f"Function to call: {function_call.name}")
                print(f"Arguments: {function_call.args}")
            else:
                print("No function call found in the response.")
                print(response.text)

result = asyncio.run(run())
print(result)

