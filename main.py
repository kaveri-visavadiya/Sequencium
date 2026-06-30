TURN_ORDER = ['R', 'B', 'B', 'R']


def create_board(m, n) -> list[list]:
    board = [['.' for _ in range(n)] for _ in range(m)]
    x = min(m, n) // 2

    for i in range(x):
        # Red player
        board[i][i] = [i+1, 'R']
        # Blue player
        board[m-1-i][n-1-i] = [i+1, 'B'] 

    return board


def is_terminal(board, m, n) -> bool:
        for i in range(m):
            for j in range(n):
                if board[i][j] == '.':
                    return False
        return True


def get_current_player(turn_idx: int) -> str:
    return TURN_ORDER[turn_idx % len(TURN_ORDER)]


def find_final_branch_length(board) -> dict:
    result = dict()
    for i, row in enumerate(board):
        for j, (number, player) in enumerate(row):
            if player not in result or number > result[player]:
                result[player] = number
    return result


def available_actions(board, m, n, current_player: str) -> list[list]:
    # find indices of current_player in board
    indices_of_player = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            # checking if board's cell is current player's cell
            if cell != '.' and cell[1] == current_player:
                indices_of_player.append([cell[0], (i, j)])
    indices_of_player.sort(key=lambda sublist: sublist[0], reverse=True)

    # given indices, find available actions around the indices for current_player
    actions = []
    marked = set()
    for (number, index) in indices_of_player:
        row, col = index
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                # skip center cell
                if (i, j) == (row, col):
                    continue
                # bounds check
                if not (0 <= i < m and 0 <= j < n):
                    continue
                # must be empty
                if board[i][j] != '.':
                    continue
                # already used
                if (i, j) in marked:
                    continue
                # add move
                actions.append([number + 1, (i, j)])
                marked.add((i, j))

    return actions


def play_game():
    # R = ai, B = you
    print("================= Sequencium =================")
    print("Turn order: ABBAABB...")
    print()

    while True:
        m, n = tuple(map(int, input("Enter the board size (M x N), separated by spaces: ").split()))
        if m < 1 or n < 1:
            print("Minimum size of board can be 3x3. Please try again.")
            continue 
        break

    board = create_board(m, n)
    for row in board:
        print(row)
    print()
    turn_idx = 0
    current_player = get_current_player(turn_idx)


    # play while board is not empty 
    while not is_terminal(board, m, n):

        if current_player == 'R':
            actions_1 = available_actions(board, m, n, current_player)
            if actions_1 == []:
                print("Player 1 has no moves. Passing turn.")
                turn_idx = 1            # B
                current_player = get_current_player(turn_idx)
                continue

            print("Player 1's action should be one of these numbers and a corresponding index: ", actions_1)
            while True:
                number_1 = int(input("Enter the number 1 wants to play: "))
                index_1 = tuple(map(int, input("Enter the index 1 wants to place it at, separated by spaces: ").split()))
                if [number_1, index_1] in actions_1:
                    break
                print("Invalid move. Try again.")
            print(f"Player 1's move: {number_1, index_1}")
            board[index_1[0]][index_1[1]] = [number_1, current_player]

            for row in board:
                print(row)
            print()


        else:
            actions_2 = available_actions(board, m, n, current_player)
            if actions_2 == []:
                print("Player 2 has no moves. Passing turn.")
                turn_idx = 3            # R
                current_player = get_current_player(turn_idx)
                continue

            print("Player 2's action should be one of these numbers and a corresponding index: ", actions_2)
            while True:
                number_2 = int(input("Enter the number you want to play: "))
                index_2 = tuple(map(int, input("Enter the index you want to place it at, separated by spaces: ").split()))
                if [number_2, index_2] in actions_2:
                    break
                print("Invalid move. Try again.")
            print(f"Player 2's move: {number_2, index_2}")
            board[index_2[0]][index_2[1]] = [number_2, current_player]

            for row in board:
                print(row)
            print()
        
        # change current player
        turn_idx = (turn_idx + 1) % 4
        current_player = get_current_player(turn_idx)

    
    # if board is full, check who winner is
    result = find_final_branch_length(board)
    if result['R'] == result['B']: print('Draw!')
    elif result['R'] > result['B']: print('Player 1 wins!')
    elif result['R'] < result['B']: print('Player 2 wins!')


if __name__ == "__main__":
    play_game()