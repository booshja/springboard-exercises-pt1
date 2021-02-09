let currentScore = 0;
const wordsEntered = [];
let clickable = true;

/** Creates the message displayed when a word is entered, appends it to the DOM */
function makeFeedback(result) {
  success = " Your word is a real word, and is on the boggle board!";
  boardFail = " Looks like your word is not on the boggle board, try again!";
  wordFail = " Your word isn't a real word according to our list, try again!";
  emptyFail = " You must enter a word to guess!";
  span = "<span class=''></span>";

  if (result === "ok") {
    return (
      span.slice(0, 13) +
      "success" +
      span.slice(13, 15) +
      "Points!" +
      span.slice(15) +
      success
    );
  } else if (result === "not-on-board") {
    return (
      span.slice(0, 13) +
      "oops" +
      span.slice(13, 15) +
      "Oops!" +
      span.slice(15) +
      boardFail
    );
  } else if (result === "not-word") {
    return (
      span.slice(0, 13) +
      "oops" +
      span.slice(13, 15) +
      "Oh no!" +
      span.slice(15) +
      wordFail
    );
  } else if (result === "empty") {
    return (
      span.slice(0, 13) +
      "oops" +
      span.slice(13, 15) +
      "Oh shucks!" +
      span.slice(15) +
      emptyFail
    );
  }
}

/** Adds current score to the running total, updates the DOM */
function updateScore(wordScore) {
  currentScore += Number(wordScore);
  $("#score").text(currentScore);
}

/** When timer runs out:
 * -Stop the setInterval function
 * -Disable the Submit button
 * -Display message to user with:
 *    -Current game score
 *    -High score
 *    -Number of games the user has played
 */
async function endGame(timer) {
  clearInterval(timer);
  clickable = false;

  const resp = await axios.post("http://127.0.0.1:5000/game/update", {
    score: currentScore,
  });
  const record = resp.data.new_record;

  $("#results").html(
    "<span class='success'>Game Over!</span> Your score was " +
      `${currentScore}! <br>`
  );
  if (record === true) {
    $("#results").append("This is a new high score!");
  }
}

/** Runs the timer
 * -Counts down every second, appends to DOM
 * -At end of timer:
 *    -Stop the function from repeating
 *    -Show a message that the game is over
 */
$(document).ready(function () {
  let timeLeft = 60;

  const timer = setInterval(function () {
    $("#timer").text(timeLeft.toString());
    timeLeft--;
    if (timeLeft < 0) {
      endGame(timer);
    }
  }, 1000);
});

/** Handles the submit button
 * -Makes an AJAX request
 *   -Sends the word to the server
 *   -The server checks if the word is on the words list
 *   -The server checks if the word is on the board
 * -Takes the response from the server, displays feedback to user
 */
$("#word-submit").on("click", async function (e) {
  e.preventDefault();
  if (clickable === true) {
    $word = $("#word-guess").val().toLowerCase();
    if ($word) {
      if (wordsEntered.indexOf($word) === -1) {
        wordsEntered.push($word);
        $("#word-guess").val("");
        const res = await axios
          .get("http://127.0.0.1:5000/game/word-guess", {
            params: { word: $word },
          })
          .then(function (response) {
            return response.data;
          });

        $("#results").html(makeFeedback(res.result));

        if (res.result === "ok") {
          $("#found-words").append(" " + $word);
          updateScore($word.length);
        }
      } else {
        $("#results").html(makeFeedback("empty"));
      }
    }
  }
});
