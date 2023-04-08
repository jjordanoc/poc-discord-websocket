import asyncio
import os
from asyncio import Task
from typing import Optional

import discord
import websockets
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
CHANNEL_ID: int = int(os.getenv("CHANNEL_ID"))
BOT_TOKEN: str = os.getenv("TOKEN")

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
loop = asyncio.get_event_loop()
websocket_server_task: Optional[Task] = None


@client.command()
async def hello(ctx):
    await ctx.send("Hello")


@client.command()
async def start(ctx):
    print("WebSocket server started")
    await send_to_discord("Listening at ws://localhost:8000")
    global websocket_server_task
    websocket_server_task = loop.create_task(start_server())


@client.command()
async def stop(ctx):
    print("WebSocket server stopped")
    await send_to_discord("Stopping server at ws://localhost:8000")
    if websocket_server_task is not None:
        websocket_server_task.cancel()


async def send_to_discord(message):
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(message)


async def receive_data(websocket, path):
    async for message in websocket:
        await send_to_discord(f"Received data: {message}")


async def start_server():
    async with websockets.serve(receive_data, "localhost", 8000):
        await asyncio.Future()


@client.event
async def on_ready():
    print("Logged in as", client.user)
    await send_to_discord("Bot started")

if __name__ == "__main__":
    websocket_server_task = None
    loop.create_task(client.start(BOT_TOKEN))
    loop.run_forever()
