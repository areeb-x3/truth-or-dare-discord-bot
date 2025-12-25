from tod import TodStatements
import discord

statements = TodStatements()

# ---------------- JOIN GAME BUTTONS ----------------
class GameControlView(discord.ui.View):
    def __init__(self, guild_id: int, games: dict):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.games = games

    @discord.ui.button(
        style=discord.ButtonStyle.success,
        emoji="➕"
    )
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        gid = self.guild_id
        game = self.games.get(gid)

        if not game:
            return await interaction.response.send_message(
                "❌ No active game.",
                ephemeral=True
            )

        if interaction.user.id == game["overseer"]:
            return await interaction.response.send_message(
                "❌ Overseer cannot join as a player.",
                ephemeral=True
            )

        if interaction.user.id in game["players"]:
            return await interaction.response.send_message(
                "⚠️ You already joined the game.",
                ephemeral=True
            )

        game["players"].add(interaction.user.id)

        await interaction.response.send_message(
            f"✅ You joined the game!\n"
            f"👥 Players: {len(game['players'])}",
            ephemeral=True
        )

    @discord.ui.button(
        style=discord.ButtonStyle.danger,
        emoji="➖"
    )
    async def quit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        gid = self.guild_id
        game = self.games.get(gid)

        if not game:
            return await interaction.response.send_message(
                "❌ No active game.",
                ephemeral=True
            )

        user_id = interaction.user.id

        # Overseer quits → end game
        if user_id == game["overseer"]:
            del games[gid]
            return await interaction.response.send_message(
                "🛑 Overseer quit. Game ended.",
                ephemeral=True
            )

        if user_id not in game["players"]:
            return await interaction.response.send_message(
                "❌ You are not in the game.",
                ephemeral=True
            )

        game["players"].remove(user_id)

        if game["current"] == user_id:
            game["current"] = None

        await interaction.response.send_message(
            f"🚪 You quit the game.\n"
            f"👥 Players remaining: {len(game['players'])}",
            ephemeral=True
        )

# ---------------- SELECT T/D BUTTONS ----------------
class GameTurnView(discord.ui.View):
    def __init__(self, guild_id: int, games: dict):
        super().__init__(timeout=None)
        self.guild_id = guild_id
        self.games = games

    # -------- TRUTH --------
    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="❔", label="Truth")
    async def truth_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        gid = self.guild_id
        game = self.games.get(gid)

        if not game or game["current"] is None:
            return await interaction.response.send_message("❌ No active turn.", ephemeral=True)

        if interaction.user.id != game["current"]:
            return await interaction.response.send_message("❌ Not your turn.", ephemeral=True)

        question = statements.get_truth()
        game["current"] = None

        await interaction.response.send_message(
            f"🧠 **Truth:**\n>>> {question}",
            ephemeral=False
        )

    # -------- DARE --------
    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="❗", label="Dare")
    async def dare_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        gid = self.guild_id
        game = self.games.get(gid)

        if not game or game["current"] is None:
            return await interaction.response.send_message("❌ No active turn.", ephemeral=True)

        if interaction.user.id != game["current"]:
            return await interaction.response.send_message("❌ Not your turn.", ephemeral=True)

        challenge = statements.get_dare()
        game["current"] = None

        await interaction.response.send_message(
            f"🔥 **Dare:**\n>>> {challenge}",
            ephemeral=False
        )
    
    # -------- JOIN --------
    @discord.ui.button(
        style=discord.ButtonStyle.success,
        emoji="➕"
    )
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        gid = self.guild_id
        game = self.games.get(gid)

        if not game:
            return await interaction.response.send_message(
                "❌ No active game.",
                ephemeral=True
            )

        if interaction.user.id == game["overseer"]:
            return await interaction.response.send_message(
                "❌ Overseer cannot join as a player.",
                ephemeral=True
            )

        if interaction.user.id in game["players"]:
            return await interaction.response.send_message(
                "⚠️ You already joined the game.",
                ephemeral=True
            )

        game["players"].add(interaction.user.id)

        await interaction.response.send_message(
            f"✅ You joined the game!\n"
            f"👥 Players: {len(game['players'])}",
            ephemeral=True
        )
    
    # -------- QUIT --------
    @discord.ui.button(
        style=discord.ButtonStyle.danger,
        emoji="➖"
    )
    async def quit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        gid = self.guild_id
        game = self.games.get(gid)

        if not game:
            return await interaction.response.send_message(
                "❌ No active game.",
                ephemeral=True
            )

        user_id = interaction.user.id

        # Overseer quits → end game
        if user_id == game["overseer"]:
            del games[gid]
            return await interaction.response.send_message(
                "🛑 Overseer quit. Game ended.",
                ephemeral=True
            )

        if user_id not in game["players"]:
            return await interaction.response.send_message(
                "❌ You are not in the game.",
                ephemeral=True
            )

        game["players"].remove(user_id)

        if game["current"] == user_id:
            game["current"] = None

        await interaction.response.send_message(
            f"🚪 You quit the game.\n"
            f"👥 Players remaining: {len(game['players'])}",
            ephemeral=True
        )