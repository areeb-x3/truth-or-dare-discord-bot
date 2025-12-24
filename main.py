import config
import discord
import random
from discord import app_commands

TOKEN = config.API_KEY

TRUTHS = [
    "What's your biggest fear?",
    "Who was your first crush?",
    "What's a secret no one knows?",
    "Have you ever lied to your best friend?",
    "What's the most embarrassing thing you've done?",
    "Who do you have a crush on right now?",
    "What's your guilty pleasure?",
    "Have you ever cheated on a test?"
]

DARES = [
    "Send your last used emoji 10 times",
    "Change your nickname to something embarrassing for 5 minutes",
    "Say 'I love this server' in all caps 3 times",
    "Do 10 pushups and post proof",
    "Send a voice message singing your favorite song",
    "Change your profile picture to something funny",
    "Compliment every person online right now"
]

games = {}

class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Enable message content intent
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self):
        # Sync commands globally
        await self.tree.sync()
        print("Commands synced!")

client = MyClient()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    print(f'Bot is in {len(client.guilds)} guilds')

# ---------------- START GAME ----------------
@client.tree.command(name="start_game", description="Start a truth or dare game")
async def start_game(interaction: discord.Interaction):
    if not interaction.guild:
        return await interaction.response.send_message("❌ This command only works in servers.", ephemeral=True)
    
    gid = interaction.guild.id
    games[gid] = {
        "overseer": interaction.user.id,
        "players": set(),
        "current": None
    }
    await interaction.response.send_message(
        f"🎮 **Truth or Dare Game Started!**\n"
        f"👑 Overseer: **{interaction.user.name}**\n"
        f"Use `/join_game` to join the game!"
    )

# ---------------- JOIN GAME ----------------
@client.tree.command(name="join_game", description="Join the truth or dare game")
async def join_game(interaction: discord.Interaction):
    if not interaction.guild:
        return await interaction.response.send_message("❌ This command only works in servers.", ephemeral=True)
    
    gid = interaction.guild.id
    if gid not in games:
        return await interaction.response.send_message("❌ No active game. Use `/start_game` first!", ephemeral=True)
    
    games[gid]["players"].add(interaction.user.id)
    player_count = len(games[gid]["players"])
    await interaction.response.send_message(
        f"✅ **{interaction.user.name}** joined the game!\n"
        f"👥 Players: {player_count}"
    )

# ---------------- PICK PLAYER ----------------
@client.tree.command(name="pick", description="Pick a random player (overseer only)")
async def pick(interaction: discord.Interaction):
    if not interaction.guild:
        return await interaction.response.send_message("❌ This command only works in servers.", ephemeral=True)
    
    gid = interaction.guild.id
    game = games.get(gid)
    
    if not game:
        return await interaction.response.send_message("❌ No active game.", ephemeral=True)
    
    if interaction.user.id != game["overseer"]:
        return await interaction.response.send_message("❌ Only the overseer can pick players.", ephemeral=True)
    
    if not game["players"]:
        return await interaction.response.send_message("❌ No players have joined yet!")
    
    chosen = random.choice(list(game["players"]))
    game["current"] = chosen
    user = interaction.guild.get_member(chosen)
    
    await interaction.response.send_message(
        f"🎯 **{user.mention}** has been chosen!\n"
        f"Choose your fate: `/truth` or `/dare`"
    )

# ---------------- TRUTH ----------------
@client.tree.command(name="truth", description="Choose truth")
async def truth(interaction: discord.Interaction):
    if not interaction.guild:
        return await interaction.response.send_message("❌ This command only works in servers.", ephemeral=True)
    
    gid = interaction.guild.id
    game = games.get(gid)
    
    if not game:
        return await interaction.response.send_message("❌ No active game.", ephemeral=True)
    
    if game["current"] is None:
        return await interaction.response.send_message("❌ No one has been picked yet!", ephemeral=True)
    
    if interaction.user.id != game["current"]:
        return await interaction.response.send_message("❌ It's not your turn!", ephemeral=True)
    
    selected_truth = random.choice(TRUTHS)
    game["current"] = None  # Reset current player
    
    await interaction.response.send_message(
        f"🧠 **Truth for {interaction.user.mention}:**\n"
        f">>> {selected_truth}\n\n"
        f"Overseer can use `/pick` for the next player!"
    )

# ---------------- DARE ----------------
@client.tree.command(name="dare", description="Choose dare")
async def dare(interaction: discord.Interaction):
    if not interaction.guild:
        return await interaction.response.send_message("❌ This command only works in servers.", ephemeral=True)
    
    gid = interaction.guild.id
    game = games.get(gid)
    
    if not game:
        return await interaction.response.send_message("❌ No active game.", ephemeral=True)
    
    if game["current"] is None:
        return await interaction.response.send_message("❌ No one has been picked yet!", ephemeral=True)
    
    if interaction.user.id != game["current"]:
        return await interaction.response.send_message("❌ It's not your turn!", ephemeral=True)
    
    selected_dare = random.choice(DARES)
    game["current"] = None  # Reset current player
    
    await interaction.response.send_message(
        f"🔥 **Dare for {interaction.user.mention}:**\n"
        f">>> {selected_dare}\n\n"
        f"Overseer can use `/pick` for the next player!"
    )

# ---------------- END GAME ----------------
@client.tree.command(name="end_game", description="End the current game (overseer only)")
async def end_game(interaction: discord.Interaction):
    if not interaction.guild:
        return await interaction.response.send_message("❌ This command only works in servers.", ephemeral=True)
    
    gid = interaction.guild.id
    game = games.get(gid)
    
    if not game:
        return await interaction.response.send_message("❌ No active game.", ephemeral=True)
    
    if interaction.user.id != game["overseer"]:
        return await interaction.response.send_message("❌ Only the overseer can end the game.", ephemeral=True)
    
    player_count = len(game["players"])
    del games[gid]
    
    await interaction.response.send_message(
        f"🎮 **Game Ended!**\n"
        f"Thanks for playing! Total players: {player_count}"
    )

# ---------------- VIEW PLAYERS ----------------
@client.tree.command(name="players", description="View all players in the current game")
async def players(interaction: discord.Interaction):
    if not interaction.guild:
        return await interaction.response.send_message("❌ This command only works in servers.", ephemeral=True)
    
    gid = interaction.guild.id
    game = games.get(gid)
    
    if not game:
        return await interaction.response.send_message("❌ No active game.", ephemeral=True)
    
    if not game["players"]:
        return await interaction.response.send_message("❌ No players have joined yet!")
    
    player_list = []
    for player_id in game["players"]:
        member = interaction.guild.get_member(player_id)
        if member:
            player_list.append(member.name)
    
    overseer = interaction.guild.get_member(game["overseer"])
    
    await interaction.response.send_message(
        f"👥 **Current Players ({len(player_list)}):**\n"
        f"{', '.join(player_list)}\n\n"
        f"👑 **Overseer:** {overseer.name if overseer else 'Unknown'}"
    )

client.run(TOKEN)