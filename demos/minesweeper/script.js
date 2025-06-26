document.addEventListener('DOMContentLoaded', () => {
    const boardSizeSelect = document.getElementById('boardSize');
    const minesInput = document.getElementById('mines');
    const resetButton = document.getElementById('resetButton');
    const gameBoard = document.getElementById('game-board');
    const minesCountSpan = document.getElementById('mines-count');
    const timerSpan = document.getElementById('timer');
    const messageDiv = document.getElementById('message');

    let boardSize = 9;
    let minesCount = 10;
    let board = [];
    let revealedCells = 0;
    let flaggedCells = 0;
    let timer;
    let time = 0;
    let gameOver = false;

    function initGame() {
        boardSize = parseInt(boardSizeSelect.value);
        minesCount = parseInt(minesInput.value);
        
        if (minesCount >= boardSize * boardSize) {
            alert("地雷數量必須小於棋盤總格數！");
            return;
        }

        gameOver = false;
        revealedCells = 0;
        flaggedCells = 0;
        time = 0;
        messageDiv.textContent = '';
        minesCountSpan.textContent = `地雷: ${minesCount}`;
        timerSpan.textContent = `時間: ${time}`;
        clearInterval(timer);
        timer = setInterval(() => {
            time++;
            timerSpan.textContent = `時間: ${time}`;
        }, 1000);

        createBoard();
        plantMines();
        calculateNumbers();
        renderBoard();
    }

    function createBoard() {
        board = Array(boardSize).fill(null).map(() => Array(boardSize).fill(null).map(() => ({ mine: false, revealed: false, flagged: false, number: 0 })));
    }

    function plantMines() {
        let plantedMines = 0;
        while (plantedMines < minesCount) {
            const row = Math.floor(Math.random() * boardSize);
            const col = Math.floor(Math.random() * boardSize);
            if (!board[row][col].mine) {
                board[row][col].mine = true;
                plantedMines++;
            }
        }
    }

    function calculateNumbers() {
        for (let row = 0; row < boardSize; row++) {
            for (let col = 0; col < boardSize; col++) {
                if (board[row][col].mine) continue;
                let count = 0;
                for (let i = -1; i <= 1; i++) {
                    for (let j = -1; j <= 1; j++) {
                        const newRow = row + i;
                        const newCol = col + j;
                        if (newRow >= 0 && newRow < boardSize && newCol >= 0 && newCol < boardSize && board[newRow][newCol].mine) {
                            count++;
                        }
                    }
                }
                board[row][col].number = count;
            }
        }
    }

    function renderBoard() {
        gameBoard.innerHTML = '';
        gameBoard.style.gridTemplateColumns = `repeat(${boardSize}, 30px)`;
        for (let row = 0; row < boardSize; row++) {
            for (let col = 0; col < boardSize; col++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                cell.dataset.row = row;
                cell.dataset.col = col;

                if (board[row][col].revealed) {
                    cell.classList.add('revealed');
                    if (board[row][col].mine) {
                        cell.textContent = '💣';
                        cell.classList.add('mine');
                    } else if (board[row][col].number > 0) {
                        cell.textContent = board[row][col].number;
                    }
                } else if (board[row][col].flagged) {
                    cell.textContent = '🚩';
                    cell.classList.add('flagged');
                }

                cell.addEventListener('click', () => handleCellClick(row, col));
                cell.addEventListener('contextmenu', (e) => {
                    e.preventDefault();
                    handleCellRightClick(row, col);
                });

                gameBoard.appendChild(cell);
            }
        }
    }

    function handleCellClick(row, col) {
        if (gameOver || board[row][col].revealed || board[row][col].flagged) return;

        revealCell(row, col);

        if (board[row][col].mine) {
            endGame(false);
        } else {
            checkWinCondition();
        }
    }

    function handleCellRightClick(row, col) {
        if (gameOver || board[row][col].revealed) return;

        board[row][col].flagged = !board[row][col].flagged;
        if (board[row][col].flagged) {
            flaggedCells++;
        } else {
            flaggedCells--;
        }
        minesCountSpan.textContent = `地雷: ${minesCount - flaggedCells}`;
        renderBoard();
    }

    function revealCell(row, col) {
        if (row < 0 || row >= boardSize || col < 0 || col >= boardSize || board[row][col].revealed) return;

        board[row][col].revealed = true;
        revealedCells++;

        if (board[row][col].number === 0 && !board[row][col].mine) {
            for (let i = -1; i <= 1; i++) {
                for (let j = -1; j <= 1; j++) {
                    revealCell(row + i, col + j);
                }
            }
        }
        renderBoard();
    }

    function endGame(win) {
        gameOver = true;
        clearInterval(timer);
        if (win) {
            messageDiv.textContent = '恭喜你，你贏了！';
            messageDiv.style.color = 'green';
        } else {
            messageDiv.textContent = '遊戲結束，你踩到地雷了！';
            messageDiv.style.color = 'red';
            // Reveal all mines
            for (let row = 0; row < boardSize; row++) {
                for (let col = 0; col < boardSize; col++) {
                    if (board[row][col].mine) {
                        board[row][col].revealed = true;
                    }
                }
            }
            renderBoard();
        }
    }

    function checkWinCondition() {
        if (revealedCells === boardSize * boardSize - minesCount) {
            endGame(true);
        }
    }

    resetButton.addEventListener('click', initGame);
    boardSizeSelect.addEventListener('change', initGame);
    minesInput.addEventListener('change', initGame);

    initGame();
});
