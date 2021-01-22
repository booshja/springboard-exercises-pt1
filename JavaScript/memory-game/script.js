const gameContainer = document.getElementById("game");
const currentScore = document.getElementById("current-score");
const lowScore = document.getElementById("low-score");
let clickCount = 0;
let cardOne = {};
let cardTwo = {};
let cardOneColor = "";
let cardTwoColor = "";
let moves = 0;
let numMatches = 0;
let divs = [];
let noClick = false;

const COLORS = [
  "red",
  "blue",
  "green",
  "orange",
  "purple",
  "red",
  "blue",
  "green",
  "orange",
  "purple",
];

// here is a helper function to shuffle an array
// it returns the same array with values shuffled
// it is based on an algorithm called Fisher Yates if you want ot research more
function shuffle(array) {
  let counter = array.length;
  // While there are elements in the array
  while (counter > 0) {
    // Pick a random index
    let index = Math.floor(Math.random() * counter);
    // Decrease counter by 1
    counter--;
    // And swap the last element with it
    let temp = array[counter];
    array[counter] = array[index];
    array[index] = temp;
  }
  return array;
}

let shuffledColors = shuffle(COLORS);
// when the DOM loads
window.addEventListener("DOMContentLoaded", function () {
  createDivsForColors(shuffledColors);
});

// this function loops over the array of colors
// it creates a new div and gives it a class with the value of the color
// it also adds an event listener for a click for each card
function createDivsForColors(colorArray) {
  for (let color of colorArray) {
    // create a new div
    const newDiv = document.createElement("div");
    // give it a class attribute for the value we are looping over
    newDiv.classList.add(color);
    // call a function handleCardClick when a div is clicked on
    newDiv.addEventListener("click", handleCardClick);
    // append the div to the element with an id of game
    gameContainer.append(newDiv);
  }
  if (JSON.stringify(localStorage.getItem("lowScore"))) {
    const low = JSON.stringify(localStorage.getItem("lowScore")).substring(
      1,
      3
    );
    lowScore.innerText = "Lowest Score: " + low;
  }
}

// TODO: Implement this function!
function handleCardClick(e) {
  if (noClick) return;
  if (e.target.classList.contains("done")) {
    alert("This card has already been matched!");
  } else {
    if (e.target.style.backgroundColor !== "") {
      alert("You already clicked on this card!");
    } else {
      if (clickCount === 0) {
        noClick = true;
        clickCount++;
        cardOne = e.target;
        cardOneColor = cardOne.className;
        cardOne.style.backgroundColor = cardOneColor;
        noClick = false;
      } else if (clickCount === 1) {
        noClick = true;
        clickCount++;
        cardTwo = e.target;
        cardTwoColor = cardTwo.className;
        cardTwo.style.backgroundColor = cardTwoColor;
        moves++;
        currentScore.innerText = "Current Score: " + moves;
      }
      if (clickCount === 2) {
        if (cardOneColor !== cardTwoColor) {
          setTimeout(function () {
            cardsReset();
          }, 1000);
        } else {
          cardOne.classList.replace(cardOneColor, "done");
          cardTwo.classList.replace(cardTwoColor, "done");
          cardOne = {};
          cardTwo = {};
          clickCount = 0;
          numMatches++;
          noClick = false;
          if (numMatches === 5) {
            JSON.stringify(localStorage.setItem("lowScore", moves));
            if (moves < JSON.parse(localStorage.getItem("lowScore"))) {
              lowScore.innerText = "Lowest Score: " + moves;
              alert("New Low Score! Congrats!");
            }
            setTimeout(function () {
              alert("Game over!");
            }, 500);
          }
        }
      }
    }
  }
}

function cardsReset() {
  cardOne.style.backgroundColor = "";
  cardTwo.style.backgroundColor = "";
  cardOne = {};
  cardTwo = {};
  clickCount = 0;
  noClick = false;
}
