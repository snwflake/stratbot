import os
import logging
from enum import Enum
from typing import Optional, Literal

import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TEST_GUILD = discord.Object(id=os.getenv("__STRATBOT_GUILD_ID"))


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents) -> None:
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready() -> None:
    print(f"Logged in as {client.user} (ID: {client.user.id})")


class Modes(Enum):
    Skirmish6 = 6
    Skirmish8 = 8
    Skirmish10 = 10
    CW = 15


@client.tree.command()
@app_commands.describe(map="Which map are you looking for?", spawn="Which spawn?", mode="Which gamemode?")
async def strat(
    interaction: discord.Interaction,
    map: str,
    spawn: Literal["North", "South", "East", "West"],
    mode: Modes,
) -> None:
    pass


@client.tree.command()
@app_commands.describe(
    map="Name of the Map",
    spawn="Spawn",
    mode="Gamemode [skirmish: 6/8/10, cw/advance: 15]",
    strat="Please attach a file",
    image="Please attach an image",
)
async def add_strat(
    interaction: discord.Interaction,
    map: str,
    spawn: Literal["North", "South", "East", "West"],
    mode: Modes,
    strat: discord.Attachment,
    image: discord.Attachment,
) -> None:
    await interaction.response.defer()
    str = await strat.read()
    img = await image.to_file()
    await interaction.followup.send(
        f"Map: {map}\nspawn: {spawn}\nmode: {mode}\nstrat: {str.decode()}\nimage:", file=img
    )


handler = logging.FileHandler(filename="stratbot.log", encoding="utf-8", mode="w")
client.run(os.getenv("__STRATBOT_TOKEN"), log_handler=handler, log_level=logging.DEBUG)
