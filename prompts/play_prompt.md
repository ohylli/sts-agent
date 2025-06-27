Time for you to try playing the game with the cli tool. Read @docs@cli_tool_api.md to check how it is used. This is the only documentation you need to read.

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

**important**: The numbering of cards changes when you play a card. So if you play 2 the card that was 3 is now the new 2. Take this into account if you are going to play multiple cards with one --execute. For example execute "2,3" would actually play the card which was 4th on you hand before the command since playing ccard 2 removed it from your hand so 4th car became 3th card. So the correct command would be --execute "2,2"

When you are done with your turn use the end command. You can then play your next turn. Combat is finished when you no longer can see the Monster window i.e. you see an error message when trying to read the Monster window. When this happens stop playing and wait for my comments.

## Commentary instructions

Use the speak feature to comment on your game like  you were a twitch streamer or youtube lets player. However, you are still claude code playing slay the spire. Still do not comment on detail about how you play the game like now I am reading the Monster window or now I am using this command to play my turn. Offer higher level commentary about the state of the game, and what you are planning to do and why. Try to use the speak feature in combination with other commans as much as you can to be more efficient with the tool.

**important**:: Start your commentary only after you have exited plan mode.