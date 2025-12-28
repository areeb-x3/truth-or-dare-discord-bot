# Future Scope

This documentation discusses possible features that can be implemented in this script. These features may or may not coded in the final version but will act as building blocks to make a robust discord bot.

## 1. Better Player Selection System
**Credit: Priyanshi-2006**

The current implementation of `/pick_player` uses random module to pick a player. This however, sometimes repeats previous players that have already been picked before, Current Implementation randomly picks a player from the `player` set and puts them in `picked` set. When `player` set becomes empty, all the players from `picked` set are moved back to `player` set and the process repeats again.

However, a better approach is to use a simple for loop to select a player sequentially. This implementation is better than using a random function (Yeah my bad :|). The players IDs must be stored in list instead of a set. Inside `current` store the index for the player that is picked. (Default=1, start from a player not overseer). When `/pick_player` is executed, increment the `current` pointer by 1. If `current` is equal to length of `player` list, set it back to 1.
