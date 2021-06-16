# Author: Ethan Lopez
# Date: 3/3/2021
# Description: Represents a Janngi gameboard with all the playable pieces. Moves are made through the utilization of
# algebraic notation which represent each grid on the game board. Each piece has a method that provides the rules of each
# piece and designates the rows and columns it can move on the board. All possible movement are made into move object
# which is later used to distinguish between valid and possible movements for a player, which helps in distinguishing
# when a player is in check.

class Move:
    """
    Represents a movement a piece makes. Interacts with the main JanggiGame class where potential moves, valid moves,
    and user moves are all converted into movement objects. These movement objects will be used to compare valid moves
    and user made moves as well as make it easier to obtain information such as starting coordinates and values as well
    as ending coordinate values.
    """

    def __init__(self, startSq, endSq, board):
        """Initializes a Move object with a given starting coordinate, ending coordinate, and a board. These values are
        utilized to store starting piece and ending piece of a space as well."""
        self._startRow = startSq[0]
        self._startCol = startSq[1]
        self._endRow = endSq[0]
        self._endCol = endSq[1]
        self._pieceMoved = board[self._startRow][self._startCol]
        self._pieceCaptured = board[self._endRow][self._endCol]

    def __repr__(self):
        """Returns the piece captured in place of a move object"""
        return self._pieceCaptured

    def get_start_row(self):
        """Returns the first index coordinate of the starting coordinate"""
        return self._startRow

    def get_start_col(self):
        """Returns the second index coordinate of the starting coordinate"""
        return self._startCol

    def get_end_row(self):
        """Returns the first index coordinate of the ending coordinate"""
        return self._endRow

    def get_end_col(self):
        """Returns the second index coordinate of the ending coordinate"""
        return self._endCol

    def get_piece_moved(self):
        """Returns the piece on the starting row and col square."""
        return self._pieceMoved

    def get_piece_captured(self):
        """Returns the piece on the ending row and col square."""
        return self._pieceCaptured


class JanggiGame:
    """
    Represents a Game object, which includes a board, pieces represented as strings. Responsible for providing methods
    that help user make moves as well as provides methods that validate all possible movement of pieces as well as
    determines if the general is in a checkmated position and listing whether the game is finished or not. Also, interacts
    with the Move class by using methods that help in converting data it was presented into move objects.
    """
    def __init__(self):
        """Initializes game board as well as the pieces which are represented as strings. Also contains attributes that
        indicate the state of the game as well as whose turn it is."""

        self._board = [["RR", "RE", "RH", "RG", "--", "RG", "RE", "RH", "RR"],  # 0
                       ["--", "--", "--", "--", "RK", "--", "--", "--", "--"],  # 1
                       ["--", "RC", "--", "--", "--", "--", "--", "RC", "--"],  # 2
                       ["RP", "--", "RP", "--", "RP", "--", "RP", "--", "RP"],  # 3
                       ["--", "--", "--", "--", "--", "--", "--", "--", "--"],  # 4
                       ["--", "--", "--", "--", "--", "--", "--", "--", "--"],  # 5
                       ["BP", "--", "BP", "--", "BP", "--", "BP", "--", "BP"],  # 6
                       ["--", "BC", "--", "--", "--", "--", "--", "BC", "--"],  # 7
                       ["--", "--", "--", "--", "BK", "--", "--", "--", "--"],  # 8
                       ["BR", "BE", "BH", "BG", "--", "BG", "BE", "BH", "BR"],  # 9
                       ]
        self._game_state = "UNFINISHED"
        self._moveLog = []
        self._player_turn = "RED"
        self._checkmate = False
        self._player_red = None
        self._player_blue = None

    def get_move_log(self):
        return self._moveLog

    def get_game_state(self):
        """Returns the game state"""
        return self._game_state

    def set_game_state(self,state):
        """Sets the game state"""
        self._game_state = state

    def set_checkmate(self, value):
        """Sets the status of checkmate"""
        self._checkmate = value

    def get_checkmate(self):
        """Returns the value of checkmate"""
        return self._checkmate

    def get_board(self):
        """Returns the board"""
        return self._board

    def get_player_turn(self):
        """Returns the current player's turn"""
        return self._player_turn

    def set_player_turn(self):
        """Set player's turn to the opposite of what player's turn is."""
        if self.get_player_turn() == "RED":
            self._player_turn = "BLUE"
        else:
            self._player_turn = "RED"

    def get_player_red(self):
        """Returns whether player red's king is in check"""
        return self._player_red

    def set_player_red(self, value):
        """Sets true or false if player red's king is in check"""
        self._player_red = value

    def get_player_blue(self):
        """Returns whether player blue's king is in check"""
        return self._player_blue

    def set_player_blue(self, value):
        """Sets true or false if player blue's king is in check"""
        self._player_blue = value


    def convert_to_coords(self, pos_str):
        """Convert the algorithmic notation to actual coordinates that can be used for index processing. This function
        takes a algebraic notated coordinate and converts it into a tuple with coordinate readjusted for the board.
        Returns a tuple with those coordinates for make_move"""
        col_code = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        col = pos_str[0]
        row = pos_str[1:]
        if col in col_code:
            c = col_code.index(col)
            r = int(row) - 1
            coord_pos = (r, c)
            return coord_pos
    
    def convert_to_algebraic(self, xcor, ycor):
        col_code = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        ax_cor = col_code[xcor]
        ay_cor = ycor + 1
        return (ax_cor, ay_cor)


    def test_move(self, start_cor, end_cor):
        """Is called by getValidMoves to test each possible move, to see if that move places their king into check or leaves
        their king in check."""
        board = self.get_board()
        moves_list = self.get_all_possible_moves()
        if start_cor == end_cor:
            self.set_player_turn()
            return True
        for move in moves_list:
            if move.get_start_row() == start_cor[0] and move.get_start_col() == start_cor[1]:
                if move.get_end_row() == end_cor[0] and move.get_end_col() == end_cor[1]:
                    board[move.get_start_row()][move.get_start_col()] = "--"
                    board[move.get_end_row()][move.get_end_col()] = move.get_piece_moved()
                    self.set_player_turn()
                    return True
        return False

    def undo_move(self):
        if len(self._moveLog) != 0:
            move = self._moveLog.pop()
            self._board[move._startRow][move._startCol] = move._pieceMoved
            self._board[move._endRow][move._endCol] = move._pieceCaptured
            self.set_player_turn()
        


    def make_move(self, xcor, ycor):
        """Given a algebraic notated coordinate, uses convert_to_coords to retrieve list friendly coordinates
        and creates a move object with those positions and readjusts the board state to readjust the pieces on the board."""
        print("Attempting: ", xcor, "->", ycor)
        moves_list = self.get_valid_moves()
        start = xcor
        end = ycor
        board = self.get_board()
        moveLog = self.get_move_log()
        if self.get_game_state() == "UNFINISHED":
            if xcor == ycor:
                self.set_player_turn()
                return True
            for move in moves_list:
                if move.get_start_row() == start[0] and move.get_start_col() == start[1]:
                    if move.get_end_row() == end[0] and move.get_end_col() == end[1]:
                        board[move.get_start_row()][move.get_start_col()] = "--"
                        board[move.get_end_row()][move.get_end_col()] = move.get_piece_moved()
                        moveLog.append((move))
                        self.set_player_turn()

                        opp_moves = self.get_valid_moves()
                        if len(opp_moves) == 0:
                            if self.in_check():
                                self.set_checkmate(True)
                            else:
                                self.set_checkmate(False)
                        else:
                            self.set_checkmate(False)

                        if self.get_checkmate() == True:
                            if self.get_player_turn() == 'RED':
                                self.set_game_state("BLUE_WON")
                            else:
                                self.set_game_state("RED_WON")
                        else:
                            self.set_player_turn()
                        self.set_player_turn()
                        return True
            return False
        return False

    def get_valid_moves(self):
        """Given a list of all possible moves, checks every possible move and checks to see if that move is valid by testing
        it on the board and seeing if that move puts the king is in check or puts it into check and deletes those
        moves from all possible moves. """
        moves = self.get_all_possible_moves()
        board = self.get_board()
        for i in range(len(moves)-1, -1, -1):
            move = moves[i]
            end = move.get_piece_captured()
            start = move.get_piece_moved()
            start_cor = (move.get_start_row(), move.get_start_col())
            end_cor = (move.get_end_row(), move.get_end_col())
            self.test_move(start_cor, end_cor)
            self.set_player_turn()
            if self.in_check() is True:
                moves.remove(move)
            board[start_cor[0]][start_cor[1]] = start
            board[end_cor[0]][end_cor[1]] = end
        return moves

    def get_all_possible_moves(self):
        """Scans the board for each piece and provides their row, col, and a list of moves to
        a their specific call function. Returns a list of all the possible moves a piece can make on the board when
        called."""
        moves = []
        board = self.get_board()
        for r in range(0, 10):
            for c in range(0, 9):
                turn = board[r][c][0]
                if turn == "R" and self.get_player_turn() == 'RED' or turn == 'B' and self.get_player_turn() == 'BLUE':
                    piece = board[r][c][1]
                    if piece == 'P':
                        self.get_pawn_moves(r, c, moves)
                    if piece == 'R':
                        self.get_rook_moves(r, c, moves)
                    if piece == 'H':
                        self.get_horse_moves(r, c, moves)
                    if piece == 'C':
                        self.get_cannon_moves(r, c, moves)
                    if piece == 'E':
                        self.get_elephant_moves(r,c,moves)
                    if piece == 'G':
                        self.get_guards_moves(r,c,moves)
                    if piece == 'K':
                        self.get_general_moves(r,c,moves)
        return moves

    def is_in_check(self, team):
        """Given a team, scans the board to check if that team's king is currently in a check position."""
        board = self.get_board()
        if team == 'red':
            for r in range(0, 10):
                for c in range(0, 9):
                    piece = board[r][c]
                    if piece == 'RK':
                        return self.square_under_attack(r, c)
        elif team == 'blue':
            for r in range(0,10):
                for c in range(0,9):
                    piece = board[r][c]
                    if piece == 'BK':
                        return self.square_under_attack(r, c)


    def in_check(self):
        """Called by getValidMoves to verify if the king is under attack by the opponent and returns true or false
        to getValidMoves"""
        board = self.get_board()
        for r in range(0, 10):
            for c in range(0, 9):
                piece = board[r][c]
                if piece == 'RK':
                    if self.get_player_turn() == 'RED':
                        self.set_player_red(self.square_under_attack(r, c))
                        return self.get_player_red()
                elif piece == 'BK':
                    if self.get_player_turn() == 'BLUE':
                        self.set_player_blue(self.square_under_attack(r, c))
                        return self.get_player_blue()

    def square_under_attack(self, r, c):
        """Called by in_check to verify if any opponent pieces have a check on the main player's king"""
        self.set_player_turn()
        oppMoves = self.get_all_possible_moves()
        self.set_player_turn()
        for move in oppMoves:
            if move.get_end_row() == r and move.get_end_col() == c:
                return True
        return False

    def get_pawn_moves(self, row, col, moves):
        """Given a row, col, and move list, iterates through each movement a pawn can make on the board and creates an
         Move object which is then appended into a the move list"""
        board = self.get_board()
        diagnolCor = ((-1, -1), (1, -1), (-1, 1), (1, 1))
        diagonalPos = ((0, 3), (2, 3), (0, 5), (2, 5), (1, 4))
        if self.get_player_turn() == "RED":
            if 0 <= row + 1 <= 9:
                if board[row + 1][col] == "--":
                    moves.append(Move((row, col), (row + 1, col), board))
                elif board[row + 1][col][0] == "B":
                    moves.append(Move((row, col), (row + 1, col), board))
            if 0 <= col + 1 <= 8:
                if board[row][col + 1] == '--':
                    moves.append(Move((row, col), (row, col + 1), board))
                elif board[row][col + 1][0] == "B":
                    moves.append(Move((row, col), (row, col + 1), board))
            if 0 <= col - 1 <= 8:
                if board[row][col - 1] == '--':
                    moves.append(Move((row, col), (row, col - 1), board))
                elif board[row][col - 1][0] == "B":
                    moves.append(Move((row, col), (row, col - 1), board))
            for i in diagonalPos:
                if row == i[0] and col == i[1]:
                    for c in diagnolCor:
                        dRow = row + c[0]
                        dCol = col + c[1]
                        if 7 <= dRow <= 9 and 3 <= dCol <= 5 :
                            diagPiece = board[dRow][dCol]
                            if diagPiece == '--':
                                moves.append(Move((row, col), (dRow, dCol), board))
                            if diagPiece[0] == 'B':
                                moves.append(Move((row, col), (dRow, dCol), board))
        else:
            diagonalPos = ((9, 3), (7, 3), (9, 5), (7, 5), (8, 4))
            if 0 <= row - 1 <= 9:
                if board[row - 1][col] == "--":
                    moves.append(Move((row, col), (row - 1, col), board))
                elif board[row - 1][col][0] == "R":
                    moves.append(Move((row, col), (row - 1, col), board))
            if 0 <= col + 1 <= 8:
                if board[row][col + 1] == '--':
                    moves.append(Move((row, col), (row, col + 1), board))
                elif board[row][col + 1][0] == "R":
                    moves.append(Move((row, col), (row, col + 1), board))
            if 0 <= col - 1 <= 8:
                if board[row][col - 1] == '--':
                    moves.append(Move((row, col), (row, col - 1), board))
                elif board[row][col - 1][0] == "R":
                    moves.append(Move((row, col), (row, col - 1), board))
            for i in diagonalPos:
                if row == i[0] and col == i[1]:
                    for c in diagnolCor:
                        dRow = row + c[0]
                        dCol = col + c[1]
                        if 0 <= dRow <= 2 and 3 <= dCol <= 5:
                            diagPiece = board[dRow][dCol]
                            if diagPiece == '--':
                                moves.append(Move((row, col), (dRow, dCol), board))
                            if diagPiece[0] == 'R':
                                moves.append(Move((row, col), (dRow, dCol), board))

    def get_rook_moves(self, row, col, moves):
        """Given a row, col, and move list, iterates through each movement a rook can makes on the board and appends that
        data into a the move list """
        board = self.get_board()
        directions = ((1, 0), (-1, 0), (0, -1), (0, 1))
        diagonalPos = ((9, 3), (7, 3), (9, 5), (7, 5), (8, 4), (0, 3), (2, 3), (0, 5), (2, 5), (1, 4))
        diagnolCor = ((-1, -1), (1, -1), (-1, 1), (1, 1))

        if self.get_player_turn() == "RED":
            for d in directions:
                mark = 0
                for i in range(1, 10):
                    endRow = row + d[0] * i
                    endCol = col + d[1] * i
                    if 0 <= endRow <= 9 and 0 <= endCol <= 8:
                        endPiece = board[endRow][endCol]
                        if mark == 0:
                            if endPiece[0] == "R":
                                mark = 1
                            elif endPiece == '--':
                                moves.append(Move((row, col), (endRow, endCol), board))
                            elif endPiece[0] == "B":
                                moves.append(Move((row, col), (endRow, endCol), board))
                                mark = 1
                for i in diagonalPos:
                    if row == i[0] and col == i[1]:
                        for c in diagnolCor:
                            dRow = row + c[0]
                            dCol = col + c[1]
                            if 7 <= dRow <= 9 and 3 <= dCol <= 5 or 0 <= dRow <= 2 and 3 <= dCol <= 5:
                                diagPiece = board[dRow][dCol]
                                if diagPiece == '--':
                                    moves.append(Move((row, col), (dRow, dCol), board))
                                if diagPiece[0] == 'B':
                                    moves.append(Move((row, col), (dRow, dCol), board))
        elif self.get_player_turn() == "BLUE":
            for d in directions:
                mark = 0
                for i in range(1, 10):
                    endRow = row + d[0] * i
                    endCol = col + d[1] * i
                    if 0 <= endRow <= 9 and 0 <= endCol <= 8:
                        endPiece = board[endRow][endCol]
                        if mark == 0:
                            if endPiece[0] == "B":
                                mark = 1
                            elif endPiece == '--':
                                moves.append(Move((row, col), (endRow, endCol), board))
                            elif endPiece[0] == "R":
                                moves.append(Move((row, col), (endRow, endCol), board))
                                mark = 1
            for i in diagonalPos:
                if row == i[0] and col == i[1]:
                    for c in diagnolCor:
                        dRow = row + c[0]
                        dCol = col + c[1]
                        if 7 <= dRow <= 9 and 3 <= dCol <= 5 or 0 <= dRow <= 2 and 3 <= dCol <= 5:
                            diagPiece = board[dRow][dCol]
                            if diagPiece == '--':
                                moves.append(Move((row, col), (dRow, dCol), board))
                            if diagPiece[0] == 'R':
                                moves.append(Move((row, col), (dRow, dCol), board))

    def get_horse_moves(self, row, col, moves):
        """Given a row, col, and move list, iterates through each movement a horse can makes on the board and appends that
        data into a the move list"""
        board = self.get_board()
        directions = ((1, 0), (-1, 0), (0, -1), (0, 1))
        check_directions = ((1,-1), (-1,-1), (1,-1), (-1,1))
        right_directions = ((1,1), (-1, 1), (-1,-1), (1,1))
        i = 0
        if self.get_player_turn() == "RED":
            for d in directions:
                mark = 0
                endRow = row + d[0]
                endCol = col + d[1]
                if 0 <= endRow <= 9 and 0 <= endCol <= 8:
                    endPiece = board[endRow][endCol]
                    if endPiece[0] != '-':
                        mark = 3
                    if mark == 0:
                        left_row = check_directions[i][0]
                        left_col = check_directions[i][1]
                        if 0 <= endRow + left_row <= 9 and 0 <= endCol + left_col <= 8:
                            checkPiece = board[endRow + left_row][endCol + left_col]
                            if mark == 0 and checkPiece[0] != 'R':
                                    moves.append(Move((row, col), (endRow + left_row, endCol + left_col), board))
                        mark = 0
                        right_row = right_directions[i][0]
                        right_col = right_directions[i][1]
                        if 0 <= endRow + right_row <= 9 and 0 <= endCol + right_col <= 8:
                            nextPiece = board[endRow + right_row][endCol + right_col]
                            if mark == 0 and nextPiece[0] != 'R':
                                moves.append(Move((row,col),(endRow+right_row,endCol+right_col), board))
                i += 1
        else:
            for d in directions:
                mark = 0
                endRow = row + d[0]
                endCol = col + d[1]
                if 0 <= endRow <= 9 and 0 <= endCol <= 8:
                    endPiece = board[endRow][endCol]
                    if endPiece[0] != '-':
                        mark = 3
                    if mark == 0:
                        left_row = check_directions[i][0]
                        left_col = check_directions[i][1]
                        if 0 <= endRow + left_row <= 9 and 0 <= endCol + left_col <= 8:
                            checkPiece = board[endRow + left_row][endCol + left_col]
                            if mark == 0 and checkPiece[0] != 'B':
                                    moves.append(Move((row, col), (endRow + left_row, endCol + left_col), board))
                        mark = 0
                        right_row = right_directions[i][0]
                        right_col = right_directions[i][1]
                        if 0 <= endRow + right_row <= 9 and 0 <= endCol + right_col <= 8:
                            nextPiece = board[endRow + right_row][endCol + right_col]
                            if mark == 0 and nextPiece[0] != 'B':
                                moves.append(Move((row,col), (endRow+right_row,endCol+right_col), board))
                i += 1

    def get_cannon_moves(self, row, col, moves):
        """Given a row, col, and move list, iterates through each movement a cannon can makes on the board and appends that
        data into a the move list"""
        board = self.get_board()
        directions = ((1, 0), (-1, 0), (0, -1), (0, 1))
        diagonalPos = ((9, 3), (7, 3), (9, 5), (7, 5), (8, 4), (0, 3), (2, 3), (0, 5), (2, 5), (1, 4))
        diagnolCor = ((-1, -1), (1, -1), (-1, 1), (1, 1))
        if self.get_player_turn() == "RED":
            for d in directions:
                mark = 0
                for i in range(1, 10):
                    endRow = row + d[0] * i
                    endCol = col + d[1] * i
                    if 0 <= endRow <= 9 and 0 <= endCol <= 8:
                        endPiece = board[endRow][endCol]
                        if endPiece[0] != "-" and mark == 0:
                            if endPiece[1] == 'C':
                                mark = 3
                            else:
                                mark = 1
                        elif endPiece == '--' and mark == 0:
                            mark = 0
                        elif mark == 1 and endPiece == '--':
                            moves.append(Move((row,col),(endRow,endCol), board))
                        elif mark == 1 and endPiece[0] == 'B':
                            moves.append(Move((row,col), (endRow,endCol), board))
                            mark = 3
                        elif mark == 1 and endPiece[0] == 'R':
                            mark = 3
            for i in diagonalPos:
                if row == i[0] and col == i[1]:
                    for c in diagnolCor:
                        dRow = row + c[0]
                        dCol = col + c[1]
                        if 7 <= dRow <= 9 and 3 <= dCol <= 5 or 0 <= dRow <= 2 and 3 <= dCol <= 5:
                            diagPiece = board[dRow][dCol]
                            if diagPiece != '--':
                                dRow2 = row + c[0] * 2
                                dCol2 = col + c[1] * 2
                                if 7 <= dRow2 <= 9 and 3 <= dCol2 <= 5 or 0 <= dRow2 <= 2 and 3 <= dCol2 <= 5:
                                    dPiece = board[dRow2][dCol2]
                                    if dPiece[0] != 'R':
                                        moves.append(Move((row, col), (dRow2, dCol2), board))
        elif self.get_player_turn() == "BLUE":
            for d in directions:
                mark = 0
                for i in range(1, 10):
                    endRow = row + d[0] * i
                    endCol = col + d[1] * i
                    if 0 <= endRow <= 9 and 0 <= endCol <= 8:
                        endPiece = board[endRow][endCol]
                        if endPiece[0] != "-" and mark == 0:
                            if endPiece[1] == 'C':
                                mark = 3
                            else:
                                mark = 1
                        elif endPiece == '--' and mark == 0:
                            mark = 0
                        elif mark == 1 and endPiece == '--':
                            moves.append(Move((row,col),(endRow,endCol), board))
                        elif mark == 1 and endPiece[0] == 'R':
                            moves.append(Move((row,col), (endRow,endCol), board))
                            mark = 3
                        elif mark == 1 and endPiece[0] == 'B':
                            mark = 3
            for i in diagonalPos:
                if row == i[0] and col == i[1]:
                    for c in diagnolCor:
                        dRow = row + c[0]
                        dCol = col + c[1]
                        if 7 <= dRow <= 9 and 3 <= dCol <= 5 or 0 <= dRow <= 2 and 3 <= dCol <= 5:
                            diagPiece = board[dRow][dCol]
                            if diagPiece != '--':
                                dRow2 = row + c[0] * 2
                                dCol2 = col + c[1] * 2
                                if 7 <= dRow2 <= 9 and 3 <= dCol2 <= 5 or 0 <= dRow2 <= 2 and 3 <= dCol2 <= 5:
                                    dPiece = board[dRow2][dCol2]
                                    if dPiece[0] != 'B':
                                        moves.append(Move((row, col), (dRow2, dCol2), board))


    def get_elephant_moves(self, row, col, moves):
        """Given a row, col, and move list, iterates through each movement a elephant can makes on the board and appends that
        data into a the move list"""
        board = self.get_board()
        directions = ((1, 0), (-1, 0), (0, -1), (0, 1))
        check_directions = ((1,-1), (-1,-1), (1,-1), (-1,1))
        right_directions = ((1,1), (-1, 1), (-1,-1), (1,1))
        i = 0

        if self.get_player_turn() == "RED":
            for d in directions:
                mark = 0
                endRow = row + d[0]
                endCol = col + d[1]
                if 0 <= endRow <= 9 and 0 <= endCol <= 8:
                    endPiece = board[endRow][endCol]
                    if endPiece[0] != '-':
                        mark = 3
                    if mark == 0:
                        left_row = check_directions[i][0]
                        left_col = check_directions[i][1]
                        if 0 <= endRow + left_row <= 9 and 0 <= endCol + left_col <= 8:
                            checkPiece = board[endRow + left_row][endCol + left_col]
                            if checkPiece != '--':
                                mark = 3
                            if 0 <= endRow + left_row <= 9 and 0 <= endCol + left_col <= 8:
                                if mark == 0 and board[endRow + left_row][endCol + left_col][0] == 'R' or board[endRow + left_row][endCol + left_col][0] == 'B':
                                    mark = 3
                                if 0 <= endRow + (left_row * 2) <= 9 and 0 <= endCol + (left_col * 2) <= 8:
                                    if mark == 0 and board[endRow + (left_row*2)][endCol + (left_col*2)][0] != 'R':
                                        moves.append(Move((row, col), (endRow + left_row*2, endCol + left_col*2), board))
                        mark = 0
                        right_row = right_directions[i][0]
                        right_col = right_directions[i][1]
                        if 0 <= endRow + right_row <= 9 and 0 <= endCol + right_col <= 8:
                            nextPiece = board[endRow + right_row][endCol + right_col]
                            if nextPiece != '--':
                                mark = 3
                            if 0 <= endRow + right_row <= 9 and 0 <= endCol + right_col <= 8:
                                if mark == 0 and board[endRow + right_row][endCol + right_col][0] == 'R' or board[endRow+right_row][endCol + right_col][0] == 'B':
                                    mark = 3
                                if 0 <= endRow + (right_row*2) <= 9 and 0 <= endCol + (right_col*2) <= 8:
                                    if mark == 0 and board[endRow + (right_row*2)][endCol + (right_col*2)][0] != 'R':
                                        moves.append(Move((row,col),(endRow+right_row*2,endCol+right_col*2), board))
                i += 1
        else:
            check_directions = ((1, -1), (-1, -1), (1, -1), (-1, 1))
            right_directions = ((1, 1), (-1, 1), (-1, -1), (1, 1))
            for d in directions:
                mark = 0
                endRow = row + d[0]
                endCol = col + d[1]
                if 0 <= endRow <= 9 and 0 <= endCol <= 8:
                    endPiece = board[endRow][endCol]
                    if endPiece[0] != '-':
                        mark = 3
                    if mark == 0:
                        left_row = check_directions[i][0]
                        left_col = check_directions[i][1]
                        if 0 <= endRow + left_row <= 9 and 0 <= endCol + left_col <= 8:
                            checkPiece = board[endRow + left_row][endCol + left_col]
                            if checkPiece != '--':
                                mark = 3
                            if 0 <= endRow + left_row <= 9 and 0 <= endCol + left_col <= 8:
                                if mark == 0 and board[endRow + left_row][endCol + left_col][0] == 'R' or board[endRow + left_row][endCol + left_col][0] == 'B':
                                    mark = 3
                                if 0 <= endRow + (left_row * 2) <= 9 and 0 <= endCol + (left_col * 2) <= 8:
                                    if mark == 0 and board[endRow + (left_row*2)][endCol + (left_col*2)][0] != 'B':
                                        moves.append(Move((row, col), (endRow + left_row*2, endCol + left_col*2), board))
                        mark = 0
                        right_row = right_directions[i][0]
                        right_col = right_directions[i][1]
                        if 0 <= endRow + right_row <= 9 and 0 <= endCol + right_col <= 8:
                            nextPiece = board[endRow + right_row][endCol + right_col]
                            if nextPiece != '--':
                                mark = 3
                            if 0 <= endRow + right_row <= 9 and 0 <= endCol + right_col <= 8:
                                if mark == 0 and board[endRow + right_row][endCol + right_col][0] == 'R' or board[endRow+right_row][endCol + right_col][0] == 'B':
                                    mark = 3
                                if 0 <= endRow + (right_row*2) <= 9 and 0 <= endCol + (right_col*2) <= 8:
                                    if mark == 0 and board[endRow + (right_row*2)][endCol + (right_col*2)][0] != 'B':
                                        moves.append(Move((row,col),(endRow+right_row*2,endCol+right_col*2), board))
                i += 1

    def get_guards_moves(self, row, col, moves):
        """Given a row, col, and move list, iterates through each movement a guards can makes on the board and appends that
        data into a the move list"""
        board = self.get_board()
        directions = ((1, 0), (-1, 0), (0, -1), (0, 1))
        diagonalPos = ((0,3),(2,3),(0,5),(2,5),(1,4))
        diagnolCor = ((-1,-1), (1,-1), (-1,1), (1,1))
        if self.get_player_turn() == "RED":
            for d in directions:
                endRow = row + d[0]
                endCol = col + d[1]
                if 0 <= endRow <= 2 and 3 <= endCol <= 5:
                    endPiece = board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((row, col), (endRow, endCol), board))
                    elif endPiece[0] == "B":
                        moves.append(Move((row, col), (endRow, endCol), board))
            for i in diagonalPos:
                if row == i[0] and col == i[1]:
                    for c in diagnolCor:
                        dRow = row + c[0]
                        dCol = col + c[1]
                        if 0 <= dRow <= 2 and 3 <= dCol <= 5:
                            diagPiece = board[dRow][dCol]
                            if diagPiece == '--':
                                moves.append(Move((row,col),(dRow, dCol), board))
                            if diagPiece[0] == 'B':
                                moves.append(Move((row,col), (dRow, dCol), board))
        else:
            diagonalPos = ((9, 3), (7, 3), (9, 5), (7, 5), (8, 4))
            for d in directions:
                endRow = row + d[0]
                endCol = col + d[1]
                if 7 <= endRow <= 9 and 3 <= endCol <= 5:
                    endPiece = board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((row, col), (endRow, endCol), board))
                    elif endPiece[0] == "R":
                        moves.append(Move((row, col), (endRow, endCol), board))
            for i in diagonalPos:
                if row == i[0] and col == i[1]:
                    for c in diagnolCor:
                        dRow = row + c[0]
                        dCol = col + c[1]
                        if 7 <= dRow <= 9 and 3 <= dCol <= 5:
                            diagPiece = board[dRow][dCol]
                            if diagPiece == '--':
                                moves.append(Move((row, col), (dRow, dCol), board))
                            if diagPiece[0] == 'R':
                                moves.append(Move((row, col), (dRow, dCol), board))

    def get_general_moves(self, row, col, moves):
        """Given a row, col, and move list, iterates through each movement a general can makes on the board and appends that
        data into a the move list"""
        board = self.get_board()
        directions = ((1, 0), (-1, 0), (0, -1), (0, 1))
        diagonalPos = ((0, 3), (2, 3), (0, 5), (2, 5), (1, 4))
        diagnolCor = ((-1, -1), (1, -1), (-1, 1), (1, 1))
        if self.get_player_turn() == "RED":
            for d in directions:
                endRow = row + d[0]
                endCol = col + d[1]
                if 0 <= endRow <= 2 and 3 <= endCol <= 5:
                    endPiece = board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((row, col), (endRow, endCol), board))
                    elif endPiece[0] == "B":
                        moves.append(Move((row, col), (endRow, endCol), board))
            for i in diagonalPos:
                if row == i[0] and col == i[1]:
                    for c in diagnolCor:
                        dRow = row + c[0]
                        dCol = col + c[1]
                        if 0 <= dRow <= 2 and 3 <= dCol <= 5:
                            diagPiece = board[dRow][dCol]
                            if diagPiece == '--':
                                moves.append(Move((row, col), (dRow, dCol), board))
                            if diagPiece[0] == 'B':
                                moves.append(Move((row, col), (dRow, dCol), board))
        else:
            diagonalPos = ((9, 3), (7, 3), (9, 5), (7, 5), (8, 4))
            for d in directions:
                endRow = row + d[0]
                endCol = col + d[1]
                if 7 <= endRow <= 9 and 3 <= endCol <= 5:
                    endPiece = board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((row, col), (endRow, endCol), board))
                    elif endPiece[0] == "R":
                        moves.append(Move((row, col), (endRow, endCol), board))
            for i in diagonalPos:
                if row == i[0] and col == i[1]:
                    for c in diagnolCor:
                        dRow = row + c[0]
                        dCol = col + c[1]
                        if 7 <= dRow <= 9 and 3 <= dCol <= 5:
                            diagPiece = board[dRow][dCol]
                            if diagPiece == '--':
                                moves.append(Move((row, col), (dRow, dCol), board))
                            if diagPiece[0] == 'R':
                                moves.append(Move((row, col), (dRow, dCol), board))

    def display(self):
        """Displays the board"""
        for space in self._board:
            print(space)

