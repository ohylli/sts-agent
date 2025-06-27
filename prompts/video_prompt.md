I am recording a youtube video of you playing the game. Read @docs@cli_tool_api.md to check how the tool for playing  is used. This is the only documentation you need to read.

## Your goal

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

**important**: Start your commentary only after you have exited plan mode.

## Video structure

The structure of the video we are making should be as follows:

- First introduce yourself and explain shortly what you are
- Next make a joke about needing a break from all the coding you have been doing and having some fun by playing slay the spire
- Next very shortly tell what slay the spire is
- Then shortly explain how you are able to speak and to play the game: the text the spire mod and the tool you use to interact with it.
- Then play the combat encounter as described above offering commentary
- After the encounter present a short summary and analysis of it.
- Then tell the viewers that if they want to know more about how you are doing this or try it themselves, they can check the github repository linked in the video description.
- Finally finish the video by doing a typical youtuber outro.