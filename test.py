import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client


async def main():
    server_url = "http://127.0.0.1:8000/sse"

    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("Available tools:")
            for tool in tools.tools:
                print("-", tool.name)

            result = await session.call_tool(
                "get_service_records",
                arguments={
                    "app_service_name": "service_name1",
                    "start_time": "20250101",
                    "end_time": "20250102",
                    "status": "SUCCESS",
                },
            )

            print("\nResult:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
