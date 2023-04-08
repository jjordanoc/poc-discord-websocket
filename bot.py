import asyncio
from asyncio import Task
from typing import Union

import discord
import websockets
from discord.ext import commands

CHANNEL_ID = 1094347509238857828
BOT_TOKEN = "MTA5MzcwMjY2ODg3NjI1OTQxOQ.G0uhqh.zlJWzddo-7qS6DB1PrxdkOIr2MbzlfR5U2mhLE"

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
loop = asyncio.get_event_loop()
websocket_server_task: Union[Task, None] = None


@client.event
async def on_ready():
    print("Hello! Study bot is ready!")
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("Hello, send data bot is ready!")


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


if __name__ == "__main__":
    websocket_server_task = None
    loop.create_task(client.start(BOT_TOKEN))
    loop.run_forever()
