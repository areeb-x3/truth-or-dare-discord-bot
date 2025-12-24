import config
import discord
import random
from discord import app_commands

TOKEN = config.API_KEY

TRUTHS = [
    "What's your biggest fear?",
    "Who was your first crush?",
    "What's a secret no one knows?"
]

DARES = [
    "Send your last used emoji",
    "Change your nickname for 5 minutes",
    "Say 'I love this server' in chat"
]

games = {}

class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient()

# ---------------- START GAME ----------------
@client.tree.command(name="start_game", description="Start a truth or dare game")
async def start_game(interaction: discord.Interaction):
    gid = interaction.guild.id
    games[gid] = {
        "overseer": interaction.user.id,
        "players": set(),
        "current": None
    }
    await interaction.response.send_message(
        f"🎮 Game started by **{interaction.user.name}**!\nUse `/join_game` to join."
    )

# ---------------- JOIN GAME ----------------
@client.tree.command(name="join_game", description="Join the truth or dare game")
async def join_game(interaction: discord.Interaction):
    gid = interaction.guild.id
    if gid not in games:
        return await interaction.response.send_message("❌ No active game.", ephemeral=True)

    games[gid]["players"].add(interaction.user.id)
    await interaction.response.send_message(f"✅ {interaction.user.name} joined the game!")

# ---------------- PICK PLAYER ----------------
@client.tree.command(name="pick", description="Pick a random player (overseer only)")
async def pick(interaction: discord.Interaction):
    gid = interaction.guild.id
    game = games.get(gid)

    if not game or interaction.user.id != game["overseer"]:
        return await interaction.response.send_message("❌ Only overseer can do this.", ephemeral=True)

    if not game["players"]:
        return await interaction.response.send_message("❌ No players joined.")

    chosen = random.choice(list(game["players"]))
    game["current"] = chosen

    user = interaction.guild.get_member(chosen)
    await interaction.response.send_message(
        f"🎯 **{user.mention}** was chosen!\nTruth or Dare? (`/truth` or `/dare`)"
    )

# ---------------- TRUTH ----------------
@client.tree.command(name="truth", description="Choose truth")
async def truth(interaction: discord.Interaction):
    gid = interaction.guild.id
    game = games.get(gid)

    if not game or interaction.user.id != game["current"]:
        return await interaction.response.send_message("❌ Not your turn.", ephemeral=True)

    await interaction.response.send_message(
        f"🧠 **Truth:** {random.choice(TRUTHS)}"
    )

# ---------------- DARE ----------------
@client.tree.command(name="dare", description="Choose dare")
async def dare(interaction: discord.Interaction):
    gid = interaction.guild.id
    game = games.get(gid)

    if not game or interaction.user.id != game["current"]:
        return await interaction.response.send_message("❌ Not your turn.", ephemeral=True)

    await interaction.response.send_message(
        f"🔥 **Dare:** {random.choice(DARES)}"
    )

client.run(TOKEN)
