Time for you to play the game with the cli tool. Read @docs@cli_tool_api.md to check how it is used. This is the only documentation you need to read.

## You goal

You are in the begining of a combat encounter. You goal is to play this combat encounter as best you can while offering commentary using the --speak feature. 

## How to play

First to asses the current state you can check the following windows:

- Player
- Monster
- Hand
- Deck
- Discard
- Relic

To play a card from your hand simply execute its number as a command. So 2 to play the second card from your hand. 

**important** Hand Reordering: When you play a card, it's removed and all cards shift left. To play multiple cards:
- Method 1 (When order doesn't matter): Play right-to-left (e.g., to play three Strikes at positions 1, 2, 5, use "5,2,1")
- Method 2 (When order matters): Recalculate positions after each play (e.g., to play Bash then Strike at positions 2 and 4, use "2,3" since Strike shifts from 4 to 3)
- Example: Hand is [1:Strike, 2:Bash, 3:Defend, 4:Strike]. To play Bash→Strike: use "2,3" (Strike shifts left after Bash is played)

When you are done with your turn use the end command. You can then play your next turn. Combat is finished when you no longer can see the Monster window i.e. you see an error message when trying to read the Monster window. When this happens stop playing and wait for my comments.

## Commentary instructions

Use the speak feature to comment on your game like  you were a twitch streamer or youtube lets player. However, you are still claude code playing slay the spire. Still do not comment on detail about how you play the game like now I am reading the Monster window or now I am using this command to play my turn. Offer higher level commentary about the state of the game, and what you are planning to do and why. Try to use the speak feature in combination with other commans as much as you can to be more efficient with the tool.

**important**:: Start your commentary only after you have exited plan mode.