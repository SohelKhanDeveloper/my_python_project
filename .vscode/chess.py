import sys
def create_board():
    return [
        list("rnbqkbnr"),  # 8
        list("pppppppp"),  # 7
        list("........"),  # 6
        list("........"),  # 5   
        list("........"),  # 4
        list("........"),  # 3
        list("PPPPPPPP"),  # 2
        list("RNBQKBNR"),  # 1   
    ]
FILES = "abcdefgh"

def print_board(board):
    print()
    print("   a b c d e f g h")
    print("  +" + "--"*8 + "+")
    for row_idx, row in enumerate(board):
        rank = 8 - row_idx
        row_str = f"{rank} |" + " ".join(c if c != '.' else '.' for c in row) + " |"
        print(row_str + f" {rank}")
    print("  +" + "--"*8 + "+")
    print("   a b c d e f g h")
    print()
def parse_move_input(s):
    # Accept "e2 e4" or "e2e4"
    s = s.strip()
    s = s.replace('-', '').replace('>', '').replace(',', '')
    if ' ' in s:
        parts = s.split()
        if len(parts) != 2:
            return None
        return parts[0], parts[1]
    if len(s) == 4:
        return s[:2], s[2:]
    return None

def algebraic_to_index(square):
    # square like 'e2' -> (row, col)
    if len(square) != 2:
        return None
    file, rank = square[0], square[1]
    if file not in FILES or not rank.isdigit():
        return None
    col = FILES.index(file)
    r = int(rank)
    if r < 1 or r > 8:
        return None
    row = 8 - r
    return (row, col)

def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8

def is_white(piece):
    return piece.isupper()

def is_black(piece):
    return piece.islower()

def same_color(a, b):
    if a == '.' or b == '.':
        return False
    return (is_white(a) and is_white(b)) or (is_black(a) and is_black(b))

def valid_pawn_move(board, r1, c1, r2, c2, piece):
    dir_forward = -1 if is_white(piece) else 1  # white moves up (row decreases)
    start_row = 6 if is_white(piece) else 1
    # simple forward one
    if c1 == c2:
        if r2 == r1 + dir_forward and board[r2][c2] == '.':
            return True
        # two-square from start
        if r1 == start_row and r2 == r1 + 2*dir_forward:
            mid_r = r1 + dir_forward
            if board[mid_r][c1] == '.' and board[r2][c2] == '.':
                return True
        return False
    # capture diagonally
    if abs(c2 - c1) == 1 and r2 == r1 + dir_forward:
        if board[r2][c2] != '.' and not same_color(piece, board[r2][c2]):
            return True
    return False

def valid_knight_move(r1, c1, r2, c2):
    dr = abs(r2 - r1)
    dc = abs(c2 - c1)
    return (dr, dc) in [(1, 2), (2, 1)]

def path_clear(board, r1, c1, r2, c2):
    # For sliding pieces: rook, bishop, queen
    dr = r2 - r1
    dc = c2 - c1
    step_r = 0 if dr == 0 else (1 if dr > 0 else -1)
    step_c = 0 if dc == 0 else (1 if dc > 0 else -1)
    r, c = r1 + step_r, c1 + step_c
    while (r, c) != (r2, c2):
        if board[r][c] != '.':
            return False
        r += step_r
        c += step_c
    return True

def valid_bishop_move(board, r1, c1, r2, c2):
    if abs(r2 - r1) == abs(c2 - c1):
        return path_clear(board, r1, c1, r2, c2)
    return False

def valid_rook_move(board, r1, c1, r2, c2):
    if r1 == r2 or c1 == c2:
        return path_clear(board, r1, c1, r2, c2)
    return False

def valid_queen_move(board, r1, c1, r2, c2):
    # combination of rook and bishop
    if r1 == r2 or c1 == c2:
        return path_clear(board, r1, c1, r2, c2)
    if abs(r2 - r1) == abs(c2 - c1):
        return path_clear(board, r1, c1, r2, c2)
    return False

def valid_king_move(r1, c1, r2, c2):
    return max(abs(r2 - r1), abs(c2 - c1)) == 1


def is_valid_move(board, src, dst, turn):
        # turn: 'white' or 'black'
    r1, c1 = src
    r2, c2 = dst
    if not (in_bounds(r1, c1) and in_bounds(r2, c2)):
        return False, "Out of bounds."
    piece = board[r1][c1]
    if piece == '.':
        return False, "No piece at source square."
    if turn == 'white' and not is_white(piece):
        return False, "That's not your piece (white to move)."
    if turn == 'black' and not is_black(piece):
        return False, "That's not your piece (black to move)."
    target = board[r2][c2]
    if target != '.' and same_color(piece, target):
        return False, "Can't capture your own piece."
    p = piece.lower()
    valid = False
    reason = "Illegal move for that piece."
    if p == 'p':
        valid = valid_pawn_move(board, r1, c1, r2, c2, piece)
    elif p == 'n':
        valid = valid_knight_move(r1, c1, r2, c2)
    elif p == 'b':
        valid = valid_bishop_move(board, r1, c1, r2, c2)
    elif p == 'r':
        valid = valid_rook_move(board, r1, c1, r2, c2)
    elif p == 'q':
        valid = valid_queen_move(board, r1, c1, r2, c2)
    elif p == 'k':
        valid = valid_king_move(r1, c1, r2, c2)
    else:
        valid = False
    if not valid:
        return False, reason
    return True, None

def apply_move(board, src, dst):
    r1, c1 = src
    r2, c2 = dst
    piece = board[r1][c1]
    captured = board[r2][c2]
    board[r2][c2] = piece
    board[r1][c1] = '.'
    # Pawn promotion: if pawn reaches last rank -> promote to Queen
    if piece == 'P' and r2 == 0:
        board[r2][c2] = 'Q'
        print("White pawn promoted to Queen!")
    if piece == 'p' and r2 == 7:
        board[r2][c2] = 'q'
        print("Black pawn promoted to Queen!")
    return captured

def main():
    print("Simple Console Chess (no castling / en passant / check detection)")
    print("Enter moves like: e2 e4  or  e7e5. Type 'quit' to exit.\n")
    board = create_board()
    print_board(board)   
    turn = 'white'
    move_num = 1
    while True:
        print_board(board)
        prompt = f"{turn.capitalize()} to move (move {move_num}): "
        user_input = input(prompt).strip()
        if user_input.lower() in ('quit','exit'):
            print("Game ended.")
            sys.exit(0)
        if user_input.lower() in ('help','?'):
            board = create_board()
            print("Enter moves like 'e2 e4' or 'g8f6'. 'quit' to exit.")
            continue
        parsed = parse_move_input(user_input)
        if not parsed:
            print("Can't parse move. Use format like 'e2 e4' or 'e2e4'.")
            continue
        s_from, s_to = parsed
        src=algebraic_to_index(s_from)
        dst=algebraic_to_index(s_to)
        if src is None or dst is None:
            print("Invalid square name. Use a-h and 1-8 (e.g. e2).")
            continue
        valid, reason = is_valid_move(board, src, dst, turn)
        if not valid:
            print("Invalid move:", reason)
            continue
        captured = apply_move(board, src, dst)
        if captured != '.':
            print(f"Captured {captured}!")
        # swap turn
        if turn == 'white':
            turn = 'black'
        else:
            turn = 'white'
            move_num += 1  # increment move number after Black moves

if __name__ == "__main__":
    main()