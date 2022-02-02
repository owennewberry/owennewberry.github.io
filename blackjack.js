const readlineSync = require("readline-sync");
const line = "-".repeat(process.stdout.columns);
const chalk = require("chalk");

var playerTotal, dealerTotal, card, id, playerAces, dealerAces, textPlayer, textDealer, num, text1, answer, resp, stakeTemp, stake, playerCardNum, double, split, splitVal, playerBust, originalStake, payout;
var bank = 0, playerCards = [];

//Number set for cards
const count = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11];
//Secondary number sets for debugging high scores
//const count = [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11];

//Possiblities for number 10
const ten = ["Jack", "Queen", "King"];

//Start the round by resetting variables from last round, setting stakes, showing dealer's first card, and drawing 2 player cards
function play() {
  resetRound();
  askStake();
  //dealer's first card
  id = Math.floor(Math.random() * 13);
  dealerFirstCard = count[id];
  dealerTotal += dealerFirstCard;
  if (dealerFirstCard == 11) {
    dealerAces++;
    dealerFirstCard = "ace"
  }
  else if (dealerFirstCard == 10) {
    id = Math.floor(Math.random() * 3);
    dealerFirstCard = ten[id];
  }
  console.log("Dealer's first card is: " + chalk.blue(dealerFirstCard));
  //Start the player's move by drawing 2 cards
  playerDrawCard(2);
}

//------------------------------------------------------------------------------------------------------------------------
//Player's move, getes drawn 2 cards and told total, chooses to hit, stand, double down or split where applicable
//Hit draws another card and option is repeated
//Stand moves on to the dealer move
function playerDrawCard(a) {
  for (let i = 0; i < a; i++) {
    textPlayer = "";
    playerCardNum++;
    id = Math.floor(Math.random() * 13);
    card = count[id];
    playerTotal = playerTotal + card;
    if (card == 11) {
      playerAces++;
      card = "ace"
    }
    else if (card == 10) {
      id = Math.floor(Math.random() * 3);
      card = ten[id];
    }
    playerCards[playerCardNum - 1] = card;
    console.log(chalk.blue(card));
  }
  if (playerTotal > 21) {
    if (playerAces > 0) {
      playerAces--;
      playerTotal -= 10;
    }
  }

  for (i = 0; i < playerAces; i++) {
    num = playerTotal - 10 * (i + 1);
    text1 = " or " + chalk.blue(num.toString());
    textPlayer += text1;
  }
  //Print the player's total including string formed above if there are aces
  console.log("Current total is: " + chalk.blue(playerTotal) + textPlayer + ".");

  if (playerTotal > 21) {
    if (playerAces > 0) {
      playerAces--;
      playerTotal -= 10;
    }
    else if (playerAces == 0) {
      console.log("You went bust!");
      playerBust = true;
      playerLose();
    }
  }
  else if (double == true) {
    if (split == 2 && playerBust == false) {
      dealerStand()
    }
    else {
      dealerPlay();
    }
  }
  else if (playerTotal < 21) {
    answer = ["hit", "stand"];
    if (stake <= bank && playerCardNum == 2) {
      if (playerCards[0] == playerCards[1] && split == 0) {
        answer.push("double down", "split");
      }
      else if (playerCards[0] != playerCards[1] || (playerCards[0] == playerCards[1] && split != 0)) {
        answer.push("double down");
      }
    }
    index = readlineSync.keyInSelect(answer, "Move?");
    if (answer[index] == "hit") {
      playerDrawCard(1);
    }
    else if (answer[index] == "stand") {
      if (split == 2 && playerBust == false) {
        dealerStand()
      }
      else {
        dealerPlay();
      }