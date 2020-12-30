/** Connect Four
 *
 * Player 1 and 2 alternate turns. On each turn, a piece is dropped down a
 * column until a player gets four-in-a-row (horiz, vert, or diag) or until
 * board fills (tie)
 */

const WIDTH = 7;
const HEIGHT = 6;
let currPlayer = 1; // active player: 1 or 2
let board = []; // array of rows, each row is array of cells  (board[y][x])

/** makeBoard: create in-JS board structure:
 *    board = array of rows, each row is array of cells  (board[y][x])
 */

function makeBoard() {
  for (i = 0; i < HEIGHT; i++) {
    board.push(new Array(WIDTH));
  }
}

/** makeHtmlBoard: make HTML table and row of column tops. */

function makeHtmlBoard() {
  const htmlBoard = document.getElementById("board");

  /**makes the top table row for use as "buttons" for user to decide where
   * to drop their game piece*/
  const top = document.createElement("tr");
  top.setAttribute("id", "column-top");
  top.addEventListener("click", handleClick);

  /**creates the cells that go within the top table row
   * then adds the table row to the htmlBoard   */
  for (let x = 0; x < WIDTH; x++) {
    const headCell = document.createElement("td");
    headCell.setAttribute("id", x);
    top.append(headCell);
  }
  htmlBoard.append(top);

  /** creates all the rows and adds the cells to them  */
  for (let y = 0; y < HEIGHT; y++) {
    const row = document.createElement("tr");
    for (let x = 0; x < WIDTH; x++) {
      const cell = document.createElement("td");
      cell.setAttribute("id", `${y}-${x}`);
      row.append(cell);
    }
    htmlBoard.append(row);
  }
}

/** findSpotForCol: given column x, return top empty y (null if filled) */
function findSpotForCol(x) {
  for (i = 5; i > -1; i--) {
    if (board[i][x] === undefined) {
      return i;
    }
  }
  return null;
}

/** placeInTable: update DOM to place piece into HTML table of board */

function placeInTable(row, column) {
  // make a div and insert into correct table cell
  const piece = document.createElement("div");
  if (currPlayer === 1) {
    piece.className = "piece player1";
  } else {
    piece.className = "piece player2";
  }
  const dropLoc = document.getElementById(
    row.toString() + "-" + column.toString()
  );
  dropLoc.append(piece);
}

/** endGame: announce game end */
function endGame(msg) {
  /**pop up alert message saying who won */
  alert(msg);
}

/** handleClick: handle click of column top to play piece */
function handleClick(evt) {
  /** get x from ID of clicked cell */
  const x = +evt.target.id;
  let tieArray = [];

  /** get next spot in column (if none, ignore click) */
  const y = findSpotForCol(x);
  if (y === null) {
    return;
  }

  /** place piece in board and add to HTML table */
  placeInTable(y, x);
  board[y][x] = currPlayer;

  /** check for win */
  if (checkForWin()) {
    return endGame(`Player ${currPlayer} won!`);
  }

  /** check for tie */
  for (let y = 0; y < HEIGHT; y++) {
    for (let x = 0; x < WIDTH; x++) {
      const boardPosition = board[y][x];
      tieArray.push(boardPosition);
    }
  }
  if (_tie(tieArray)) {
    endGame("It's a tie!");
  }

  function _tie(cells) {
    return cells.every((el) => el === 1 || el === 2);
  }

  /** change to the other player's turn */
  if (currPlayer === 1 ? (currPlayer = 2) : (currPlayer = 1));
}

/** checkForWin: check board cell-by-cell for "does a win start here?" */
function checkForWin() {
  function _win(cells) {
    // Check four cells to see if they're all color of current player
    //  - cells: list of four (y, x) cells
    //  - returns true if all are legal coordinates & all match currPlayer

    return cells.every(
      ([y, x]) =>
        y >= 0 &&
        y < HEIGHT &&
        x >= 0 &&
        x < WIDTH &&
        board[y][x] === currPlayer
    );
  }

  // TODO: read and understand this code. Add comments to help you.

  for (let y = 0; y < HEIGHT; y++) {
    for (let x = 0; x < WIDTH; x++) {
      const horiz = [
        [y, x],
        [y, x + 1],
        [y, x + 2],
        [y, x + 3],
      ];
      const vert = [
        [y, x],
        [y + 1, x],
        [y + 2, x],
        [y + 3, x],
      ];
      const diagDR = [
        [y, x],
        [y + 1, x + 1],
        [y + 2, x + 2],
        [y + 3, x + 3],
      ];
      const diagDL = [
        [y, x],
        [y + 1, x - 1],
        [y + 2, x - 2],
        [y + 3, x - 3],
      ];

      if (_win(horiz) || _win(vert) || _win(diagDR) || _win(diagDL)) {
        return true;
      }
    }
  }
}

makeBoard();
makeHtmlBoard();
