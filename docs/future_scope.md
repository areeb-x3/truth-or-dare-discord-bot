# Future Scope

This documentation discusses possible features that can be implemented in this script. These features may or may not coded in the final version but will act as building blocks to make a robust discord bot.

## 1. Better Player Selection System
**Credit: Priyanshi-2006**

The current implementation of `/pick_player` uses random module to pick a player. This however, sometimes repeats previous players that have already been picked before, Current Implementation randomly picks a player from the `player` set and puts them in `picked` set. When `player` set becomes empty, all the players from `picked` set are moved back to `player` set and the process repeats again.

However, a better approach is to use a simple for loop to select a player sequentially. This implementation is better than using a random function (Yeah my bad :|). The players IDs must be stored in list instead of a set. Inside `current` store the index for the player that is picked. (Default=1, start from a player not overseer). When `/pick_player` is executed, increment the `current` pointer by 1. If `current` is equal to length of `player` list, set it back to 1.

## 2. Overseer as a Player

The Overseer cannot participate in Truth and Dare, missing out on fun with their friends (or enjoying them suffer(?)). To solve this issue, the overseer will included in `player` list. The `overseer` key will be removed. When a new game is created, The overseer is the first player in the `player` list. The index position 0 will be reserved for the overseer. When an overseer leaves, the next player automatically becomes the overseer. Game does not end unless the Overseer executes `/end` command.

Another command that must be implemented alongside is `/kick` command. The overseer will be able to kick player. (This helps in removing AFK players.)

## 3. Developer Mode & Commands

Currently, the `/debug` command displays the `games` dictionary. This is not ideal for a developer (us). Create an Embed that shows information relevant to a developer. (BotID, Guilds Joined, etc). Currently this feature hasn't be thought through.

When executing the main script, A `debug` argument will be used to enable the debug mode. By default its false.

```bash
python main.py --debug=true
```

The debug mode will expose all the available debug commands.

## 4. Using SQLite Database

Data is stored in primary memory when the script is executed. This means persistent storage is not possible when script is terminated. A database can store large amounts of data, remain persistent and quickly insert/delete/access data. This will change previous implementations of joining/leaving of players, creating new games etc. The SQLite Table Schemas can be defined as..

- games(game_id*, guild_id)
- players(player_id*, game_id)
- truth_statements(truth_id*, statement)
- dare_statements(dare_id*, statement)
- picked_truth_statement(guild_id, truth_id)
- picked_dare_statement(guild_id, dare_id)

When the script runs, the database will automatically fetch truth and statements from `statements.json` file. Statements will be fetched randomly from `truth_statements` and `dare_statements` tables and their id will be stored in `picked_truth_statement` and `picked_dare_statement` respectively. This ensures the server/guild does not receive repeating truths and dares.

The `games` table only stores game_id and in which server/guild it belongs to. The `players` table stores the player_id and their corresponding game_id. The Overseer and player selection logic will change. However, I haven't worked on a solution for this.