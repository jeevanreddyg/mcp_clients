import asyncio
from mcp.client.sse import sse_client
from mcp import ClientSession
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_core.messages.utils import get_buffer_string
from langchain.chat_models import init_chat_model

async def main():
    
    load_dotenv()
    
    # Initialize the model
    model = init_chat_model("llama3.2", model_provider="ollama")
    
    async with sse_client("http://127.0.0.1:3003/sse") as streams:
        async with ClientSession(streams[0], streams[1]) as session:
            await session.initialize()
            
            tools = await load_mcp_tools(session)
            
            agent = create_react_agent(model, tools)
            
            query = "What is sum 1 and 2?"
            print(f"User Query: {query}")
            
            response = await agent.ainvoke({"messages": query})
            print(f"AI Response: {get_buffer_string(response['messages'])}")
    
if __name__ == "__main__":
    asyncio.run(main())    