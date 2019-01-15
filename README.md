# FISH-Bot

FISH bot is a generic chat bot that is a sequentional model build using a Bidirection Recurring Neural Netowrk. This chatbot is developed from [Daniel Kukiela](https://github.com/daniel-kukiela/nmt-chatbot). Changes have been made to few files to make it domain specific aswell. 

## ChatBot Conservations

#### Example 1:
![Conservation 1](https://github.com/tarunkolla/FISHBot/blob/master/res/convo1.png)
#### Example 2:
![Conservation 2](https://github.com/tarunkolla/FISHBot/blob/master/res/convo2.png)
#### Example 3:
![Conservation 3](https://github.com/tarunkolla/FISHBot/blob/master/res/convo3.png)
#### Example 4:
![Conservation 4](https://github.com/tarunkolla/FISHBot/blob/master/res/convo4.png)

## Othr info:

Model trained on Linux machine with 8GB RAM, 8GB P4000 Nvedia GPU and 8 core processor.
Total number of steps trained: 75K
2.5M pairs of conservations from reddit May 2018 comments.
1.25M vocab size.
Domain specific bot trained from data in [convo](https://github.com/tarunkolla/FISHBot/tree/master/nmt-chatbot/convo) folder.
