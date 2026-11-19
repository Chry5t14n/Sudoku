const puzzles = {
  easy: [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
  ],
  medium: [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 0, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 0],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 0, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
  ],
  hard: [
    [5, 0, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 9, 0, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 6, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 4, 0, 0, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
  ]
};

const boardElement = document.querySelector("#board");
const difficultyElement = document.querySelector("#difficulty");
const numberPadElement = document.querySelector("#number-pad");
const statusElement = document.querySelector("#status");
const clearElement = document.querySelector("#clear");
const restartElement = document.querySelector("#restart");

let board = [];
let fixedCells = new Set();
let selectedCell = null;

function copyPuzzle(difficulty) {
  return puzzles[difficulty].map((row) => [...row]);
}

function setStatus(message, type = "") {
  statusElement.textContent = message;
  statusElement.className = `status${type ? ` ${type}` : ""}`;
}

function hasConflict(row, column) {
  const value = board[row][column];
  if (!value) return false;

  for (let currentColumn = 0; currentColumn < 9; currentColumn += 1) {
    if (currentColumn !== column && board[row][currentColumn] === value) return true;
  }
  for (let currentRow = 0; currentRow < 9; currentRow += 1) {
    if (currentRow !== row && board[currentRow][column] === value) return true;
  }

  const boxRow = Math.floor(row / 3) * 3;
  const boxColumn = Math.floor(column / 3) * 3;
  for (let currentRow = boxRow; currentRow < boxRow + 3; currentRow += 1) {
    for (let currentColumn = boxColumn; currentColumn < boxColumn + 3; currentColumn += 1) {
      if ((currentRow !== row || currentColumn !== column)
        && board[currentRow][currentColumn] === value) {
        return true;
      }
    }
  }
  return false;
}

function isWinningBoard() {
  if (board.flat().includes(0)) return false;
  const expected = new Set([1, 2, 3, 4, 5, 6, 7, 8, 9]);

  for (let index = 0; index < 9; index += 1) {
    if (new Set(board[index]).size !== 9) return false;
    if (new Set(board.map((row) => row[index])).size !== 9) return false;
  }
  for (let boxRow = 0; boxRow < 9; boxRow += 3) {
    for (let boxColumn = 0; boxColumn < 9; boxColumn += 3) {
      const values = [];
      for (let row = boxRow; row < boxRow + 3; row += 1) {
        for (let column = boxColumn; column < boxColumn + 3; column += 1) {
          values.push(board[row][column]);
        }
      }
      if (new Set(values).size !== 9
        || values.some((value) => !expected.has(value))) return false;
    }
  }
  return true;
}

function isValidMove(row, column, number) {
  if (fixedCells.has(`${row}-${column}`)) return false;
  if (number < 1 || number > 9) return false;

  const original = board[row][column];
  board[row][column] = number;
  const valid = !hasConflict(row, column);
  board[row][column] = original;
  return valid;
}

function enterNumber(number) {
  if (!selectedCell) {
    setStatus("Selecione uma casa vazia primeiro.", "error");
    return;
  }

  const [row, column] = selectedCell.split("-").map(Number);
  if (!isValidMove(row, column, number)) {
    setStatus("Jogada inválida: o número já está na linha, coluna ou quadrante.", "error");
    renderBoard();
    return;
  }

  board[row][column] = number;
  if (isWinningBoard()) {
    renderBoard();
    setStatus("Parabéns! Você completou o Sudoku!", "success");
  } else {
    setStatus("Jogada aplicada.");
    renderBoard();
  }
}

function clearSelectedCell() {
  if (!selectedCell) {
    setStatus("Selecione uma casa vazia primeiro.", "error");
    return;
  }
  const [row, column] = selectedCell.split("-").map(Number);
  if (fixedCells.has(selectedCell)) {
    setStatus("Esta casa já está fixa.", "error");
    return;
  }
  board[row][column] = 0;
  setStatus("Casa limpa.");
  renderBoard();
}

function renderBoard() {
  boardElement.replaceChildren();

  board.forEach((rowValues, row) => {
    rowValues.forEach((value, column) => {
      const cell = document.createElement("button");
      const key = `${row}-${column}`;
      cell.type = "button";
      cell.className = "cell";
      cell.textContent = value || "";
      cell.dataset.row = row;
      cell.dataset.column = column;
      cell.setAttribute("aria-label", `Linha ${row + 1}, coluna ${column + 1}`);

      if (fixedCells.has(key)) {
        cell.classList.add("fixed");
      } else {
        cell.classList.add("editable");
        if (value) cell.classList.add("entered");
      }
      if (selectedCell === key) cell.classList.add("selected");
      if (value && hasConflict(row, column)) cell.classList.add("conflict");

      cell.addEventListener("click", () => {
        if (fixedCells.has(key)) {
          setStatus("Esta casa já está fixa.", "error");
          return;
        }
        selectedCell = key;
        setStatus(`Casa selecionada: linha ${row + 1}, coluna ${column + 1}.`);
        renderBoard();
      });
      boardElement.appendChild(cell);
    });
  });
}

function startGame(difficulty = difficultyElement.value) {
  board = copyPuzzle(difficulty);
  fixedCells = new Set();
  board.forEach((row, rowIndex) => {
    row.forEach((value, columnIndex) => {
      if (value) fixedCells.add(`${rowIndex}-${columnIndex}`);
    });
  });
  selectedCell = null;
  setStatus("Selecione uma casa vazia e escolha um número.");
  renderBoard();
}

numberPadElement.addEventListener("click", (event) => {
  const button = event.target.closest("[data-number]");
  if (!button) return;
  const number = Number(button.dataset.number);
  enterNumber(number);
});

clearElement.addEventListener("click", () => {
  clearSelectedCell();
});

document.addEventListener("keydown", (event) => {
  if (event.key >= "1" && event.key <= "9") {
    event.preventDefault();
    enterNumber(Number(event.key));
  } else if (event.key === "Backspace" || event.key === "Delete") {
    event.preventDefault();
    clearSelectedCell();
  } else if (event.key === "Escape") {
    selectedCell = null;
    setStatus("Seleção removida.");
    renderBoard();
  }
});

difficultyElement.addEventListener("change", () => startGame());
restartElement.addEventListener("click", () => startGame());

startGame("easy");
