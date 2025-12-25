# Local Modules
import config
from views import GameControlView, GameTurnView
from tod import TodStatements

# Built-in/Installed Modules
import discord, random
from discord import app_commands

# -----------------------------------------------------------------------
# MAIN ENGINE OF THE DISCORD BOT
# -----------------------------------------------------------------------
class TodBotClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Enable message content intent
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self):
        # Sync commands globally
        await self.tree.sync()
        print("Commands synced!")

statements = TodStatements()
client = TodBotClient()
games = {}

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    print(f'Bot is in {len(client.guilds)} guilds')

# -----------------------------------------------------------------------
# BOT COMMANDS
# -----------------------------------------------------------------------

# START GAME
@client.tree.command(name="start_game", description="Start a truth or dare game")
async def start_game(interaction: discord.Interaction):
    if not interaction.guild:
        return await interaction.response.send_message(
            "❌ This command only works in servers.",
            ephemeral=True
        )

    gid = interaction.guild.id

    if gid in games:
        overseer = interaction.guild.get_member(games[gid]["overseer"])
        return await interaction.response.send_message(
            f"❌ A game is already running.\n"
            f"👑 Overseer: **{overseer.name if overseer else 'Unknown'}**",
            ephemeral=True
        )

    games[gid] = {
        "overseer": interaction.user.id,
        "players": set(),
        "current": None
    }

    embed = discord.Embed(
        title="🎮 Truth or Dare Game Started!",
        description="Use the buttons below to join or quit.",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="Overseer",
        value=interaction.user.mention,
        inline=False
    )

    view = GameControlView(guild_id=gid, games=games)

    await interaction.response.send_message(
        embed=embed,
        view=view
    )

# JOIN GAME
@client.tree.command(name="join_game", description="Join the truth or dare game")
async def join_game(interaction: discord.Interaction):
    if not interaction.guild:
        return await interaction.response.send_message("❌ This command only works in servers.", ephemeral=True)
    
    gid = interaction.guild.id
    if gid not in games:
        return await interaction.response.send_message("❌ No active game. Use `/start_game` first!", ephemeral=True)
    
    game = games.get(gid)
    # BLOCK OVERSEER FROM JOINING
    if interaction.user.id == game["overseer"]:
        return await interaction.response.send_message(
            "❌ The overseer cannot join the game as a player.",
            ephemeral=True
        )

    # OPTIONAL: prevent duplicate joins
    if interaction.user.id in game["players"]:
        return await interaction.response.send_message(
            "⚠️ You have already joined the game.",
            ephemeral=True
        )
    
    games[gid]["players"].add(interaction.user.id)
    player_count = len(games[gid]["players"])
    await interaction.response.send_message(
        f"✅ **{interaction.user.name}** joined the game!\n"
        f"👥 Players: {player_count}"
    )

# QUIT GAME
@client.tree.command(name="quit_game", description="Quit the current truth or dare game")
async def quit_game(interaction: discord.Interaction):
    if not interaction.guild:
        return await interaction.response.send_message(
            "❌ This command only works in servers.",
            ephemeral=True
        )

    gid = interaction.guild.id
    game = games.get(gid)

    if not game:
        return await interaction.response.send_message(
            "❌ No active game to quit.",
            ephemeral=True
        )

    user_id = interaction.user.id

    if user_id == game["overseer"]:
        player_count = len(game["players"])
        del games[gid]
        return await interaction.response.send_message(
            f"🛑 **Overseer has quit the game.**\n"
            f"🎮 Game ended. Total players were: {player_count}"
        )

    if user_id not in game["players"]:
        return await interaction.response.send_message(
            "❌ You are not part of the current game.",
            ephemeral=True
        )

    game["players"].remove(user_id)


    if game["current"] == user_id:
        game["current"] = None

    await interaction.response.send_message(
        f"🚪 **{interaction.user.name}** has quit the game.\n"
        f"👥 Players remaining: {len(game['players'])}"
    )

# PICK PLAYER
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
    user = await interaction.guild.fetch_member(chosen)
    
    embed = discord.Embed(
        title="🎯 Player Selected",
        description=f"**{user.mention}** has been chosen!",
        color=discord.Color.gold()
    )

    embed.add_field(
        name="Next Step",
        value="Choose `/truth` or `/dare`",
        inline=False
    )

    embed.set_footer(text="Players can still join or quit below")

    view = GameTurnView(guild_id=gid, games=games)

    await interaction.response.send_message(
        embed=embed,
        view=view
    )

# TRUTH
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
    
    selected_truth = statements.get_truth()
    game["current"] = None  # Reset current player
    
    await interaction.response.send_message(
        f"🧠 **Truth for {interaction.user.mention}:**\n"
        f">>> {selected_truth}\n\n"
        f"Overseer can use `/pick` for the next player!"
    )

# DARE
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
    
    selected_dare = statements.get_dare()
    game["current"] = None  # Reset current player
    
    await interaction.response.send_message(
        f"🔥 **Dare for {interaction.user.mention}:**\n"
        f">>> {selected_dare}\n\n"
        f"Overseer can use `/pick` for the next player!"
    )

# END GAME 
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

# VIEW PLAYERS
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

# DEBUG COMMANDS
@client.tree.command(name="debug", description="Debug")
async def debug(interaction: discord.Interaction):
    await interaction.response.send_message(f"{games}")

# -----------------------------------------------------------------------
# RUNNING THE BOT
# -----------------------------------------------------------------------
client.run(config.API_KEY)