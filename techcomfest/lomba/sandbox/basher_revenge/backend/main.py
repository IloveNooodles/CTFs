from src import Handler
import websockets
import asyncio
import sys

async def main():
    async with websockets.serve(Handler.handler, "", sys.argv[1]):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
