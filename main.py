import math
import copy
import pygame
import time

# =================================================================
# Function to determine if a game is over
def is_game_over(board):
    # Check rows and columns for a win
    for i in range(4):
        if board[i][0] == board[i][1] == board[i][2] == board[i][3] != '':
            return True
        if board[0][i] == board[1][i] == board[2][i] == board[3][i] != '':
            return True

    # Check diagonals for a win
    if board[0][0] == board[1][1] == board[2][2] == board[3][3] != '':
        return True
    if board[0][3] == board[1][2] == board[2][1] == board[3][0] != '':
        return True

    # Check if the board is full
    for i in range(4):
        for j in range(4):
            if board[i][j] == '':
                return False

    return True

# =================================================================
def get_best_move(board, player_sign, depth):
    best_score = float('-inf')
    best_move = None

    for i in range(4):
        for j in range(4):
            if board[i][j] == '':
                # Make a copy of the board for each move
                temp_board = copy.deepcopy(board)
                temp_board[i][j] = player_sign

                # Evaluate the current board and find the best move
                score = minimax(temp_board, depth, alpha=best_score, beta=float('inf'), maximizing_player=False)

                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

# =================================================================
# Function to determine the best move for the AI player
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_game_over(board):
        return evaluate_board(board)

    if maximizing_player:
        alpha = -math.inf
        for i in range(4):
            for j in range(4):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    eval = minimax(board, depth - 1, alpha, beta, False)
                    alpha = max(alpha, eval)
                    board[i][j] = ''
                    if beta <= alpha:
                        continue
        return alpha

    else:
        beta = math.inf
        for i in range(4):
            for j in range(4):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    eval = minimax(board, depth - 1, alpha, beta, True)
                    beta = min(beta, eval)
                    board[i][j] = ''
                    if beta <= alpha:
                        continue
        return beta

# =================================================================
def evaluate_board(board):
    score = 0
    winning_combinations = [
        # Rows
        [(i, j) for j in range(4)] for i in range(4)
    ] + [
        # Columns
        [(i, j) for i in range(4)] for j in range(4)
    ] + [
        # Diagonals
        [(i, i) for i in range(4)],
        [(i, 3 - i) for i in range(4)]
    ]

    for combination in winning_combinations:
        # Count the number of Xs and Os in each combination
        num_Xs = sum(1 for i, j in combination if board[i][j] == 'X')
        num_Os = sum(1 for i, j in combination if board[i][j] == 'O')

        # Assign a score based on the combination
        if num_Xs == 4:
            score -= 1000000
        elif num_Xs == 3 and num_Os == 1:
            score -= 10000
        elif num_Xs == 2 and num_Os == 2:
            score -= 100
        elif num_Os == 4:
            score += 1000000
        elif num_Os == 3 and num_Xs == 1:
            score += 10000
        elif num_Os == 2 and num_Xs == 2:
            score += 100

    return score
# Function to evaluate the board for the AI player
# def evaluate_board(board):
#     ai_sign = 'O'
#     user_sign = 'X'
#     score = 0
#     columns	 = []
#     for i in range(4):
#         columns.append([row[i] for row in board])
#     for column in columns:
#         if user_sign not in column:
#             score += 1 + column.count(ai_sign)
 
#     for row in board:
#         if user_sign not in row:
#             score += 1 + row.count(ai_sign) 
           

#     main_diag = [(0,0),(1,1),(2,2),(3,3)]
#     counter_diag = [(0,3),(1,2),(2,1),(3,0)]
#     mdiag = [board[x][y] for x,y in main_diag]
#     cdiag = [board[x][y] for x,y in counter_diag]
#     if user_sign not in mdiag:
#         score += 1 + mdiag.count(ai_sign)
#     if user_sign not in cdiag:
#         score += 1 + cdiag.count(ai_sign)
# #==================================================================
#     for column in columns:
#         if ai_sign not in column:
#             score -= 1 - column.count(user_sign)
 
#     for row in board:
#         if ai_sign not in row:
#             score -= 1 - row.count(user_sign) 
    
#     if ai_sign not in mdiag:
#         score -= 1 - mdiag.count(user_sign)
#     if ai_sign not in cdiag:
#         score += 1 + cdiag.count(user_sign)
#     return score


# =================================================================
def end(board):
    # Check rows and columns for a win
    for i in range(4):
        if board[i][0] == board[i][1] == board[i][2] == board[i][3] == 'X':
            return 'X'
        if board[i][0] == board[i][1] == board[i][2] == board[i][3] == 'O':
            return 'O'
        if board[0][i] == board[1][i] == board[2][i] == board[3][i] == 'X':
            return 'X'
        if board[0][i] == board[1][i] == board[2][i] == board[3][i] == 'O':
            return 'O'

    # Check diagonals for a win
    if board[0][0] == board[1][1] == board[2][2] == board[3][3] == 'X':
        return 'X'
    if board[0][0] == board[1][1] == board[2][2] == board[3][3] == 'O':
        return 'O'
    if board[0][3] == board[1][2] == board[2][1] == board[3][0] == 'X':
        return 'X'
    if board[0][3] == board[1][2] == board[2][1] == board[3][0] == 'O':
        return 'O'

    # Check if the board is full
    flag = True
    for i in range(4):
        for j in range(4):
            if board[i][j] == '':
                flag=False
    if flag:
          return 'T'

# =================================================================
def AI_player(board):
    if end(board) == 'X':
        return 'X'
    elif end(board) == 'O':
        return 'O'
    elif end(board) == 'T':
        return 'T'
    else:
        return get_best_move(board, 'O', depth =2)

# =================================================================
def handle_click(x, y):
	if 40 < x < 135 and 150 < y < 260: # first row
		return (0, 0)
	elif 143 < x < 242 and 150 < y < 260:
		return (0, 1)
	elif 250 < x < 350 and 150 < y < 260:
		return (0, 2)
	elif 353 < x < 462 and 150 < y < 260:
		return (0, 3)

	elif 40 < x < 135 and 265 < y < 370: # second row
		return (1, 0)
	elif 143 < x < 242 and 265 < y < 370:
		return (1, 1)
	elif 250 < x < 350 and 265 < y < 370:
		return (1, 2)
	elif 353 < x < 462 and 265 < y < 370:
		return (1, 3)

	elif 40 < x < 135 and 375 < y < 475: # third row
		return (2, 0)
	elif 143 < x < 242 and 375 < y < 475:
		return (2, 1)
	elif 250 < x < 350 and 375 < y < 475:
		return (2, 2)
	elif 353 < x < 462 and 375 < y < 475:
		return (2, 3)

	elif 40 < x < 135 and 480 < y < 570: # last row
		return (3, 0)
	elif 143 < x < 242 and 480 < y < 570:
		return (3, 1)
	elif 250 < x < 350 and 480 < y < 570:
		return (3, 2)
	elif 353 < x < 462 and 480 < y < 570:
		return (3, 3)

	else:
		return ()


# =================================================================
def draw_game_win(win, bot_score, player_score, board, extra):
	win.fill(WITHE)
	win.blit(game_map, (0, 0))
	match_score_p = setting_score.render(f"Player                  Bot", 1, BLACK_M)
	match_score_b = setting_score.render(f" {player_score}                       {bot_score}", 1, BLACK_M)
	win.blit(match_score_p, (55, 10))
	win.blit(match_score_b, (60,  60))
	for ind, i in enumerate(board):
		for jnd, j in enumerate(i):
			if j == "X":
				win.blit(X_image, (45+(100*jnd)+(jnd*5), 160+(100*ind)+(ind*6)))
			elif j == "O":
				win.blit(O_image, (45+(100*jnd)+(jnd*5), 160+(100*ind)+(ind*6)))

	# ------------------------------------------------
	pygame.display.update()

	if extra:
		time.sleep(0.1)
		final_ressult = setting_finish.render(extra[0], 1, PERPEL)
		win.blit(final_ressult, (150, 270))
		pygame.display.update()
		time.sleep(1)

# =================================================================
def validation(res, board):
	if res:
		if board[res[0]][res[1]] == "":
			return True
	return False
# =================================================================
def main(win, board, bot_score, player_score):
    run = True
    exit = False
    bot_turn = False
    extra = []
    while run:
        clock.tick(FPS)

        if bot_turn:

            res = AI_player(board)

            if res == "X":
                player_score += 1
                extra = ["You Win"]
            elif res == "O":
                bot_score += 1
                extra = ["Bot Win"]
            elif res == "T":
                extra = ["Its a Tie"]
            else:
                board[res[0]][res[1]] = "O"
                res = AI_player(board)
                if res == "X":
                    player_score += 1
                    extra = ["You Win"]
                elif res == "O":
                    bot_score += 1
                    extra = ["Bot Win"]
                elif res == "T":
                    extra = ["Its a Tie"]

            bot_turn = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                res = handle_click(mouse[0], mouse[1])
                val = validation(res, board)
                if val:
                    board[res[0]][res[1]] = "X"
                    bot_turn = True

        if exit:
            break

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_q]:
            break

        draw_game_win(win, bot_score, player_score, board, extra)
        if extra:
            extra = []
            board = [['', '', '', ''],['', '', '', ''],['', '', '', ''],['', '', '', '']]

# =================================================================
if __name__ == "__main__":
	board = [['', '', '', ''],['', '', '', ''],['', '', '', ''],['', '', '', '']]
	# act = [['','','',''],['','','',''],['','','',''],['','','','']]
	pygame.font.init()
	clock = pygame.time.Clock()
	FPS = 15
	WITHE = (255, 255, 255)
	BLACK_M = (18, 18, 18)
	PERPEL = (255, 0, 255)
	WIDTH, HEIGHT = 500, 605
	bot_score, player_score = 0, 0

	win = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Tick Tack Toe")
	# change in win
	game_map = pygame.image.load("./assets/final.png")
	O_image = pygame.image.load("./assets/O.png")
	X_image = pygame.image.load("./assets/X.png")
	setting_score = pygame.font.SysFont("comicsans", 30, bold=True, italic=False)
	setting_finish = pygame.font.SysFont("comicsans", 50, bold=True, italic=False)
	setting_reset = pygame.font.SysFont("comicsans", 25, bold=False, italic=False)

	main(win, board, bot_score, player_score)
