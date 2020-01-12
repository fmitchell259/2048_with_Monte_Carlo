"""
    Next states function, returns a state object that has been
    scored based on the tiles that have been transformed.
    Returns a list of up, down, left and right slides.
"""


import copy
from state import State

def is_terminal(state):

    board = state.get_board_state()
    full_check = 0

    for r in range(len(board)):
        for s in range (len(board)):
            if board[r][s] != -1:
                full_check += 1

    if full_check == 16:

        check_states = next_states(state)
        if check_states is None:
            return True
        else:
            return False

    else:
        return False


def down_states(state):

    star = False

    # Set board value to 0 .Each board wil have a score associated with it.
    # This score is then added to the total score whenever a state is chosen.

    board_value = 0

    # Need a copy of the board to manipulate and create a fresh state with.

    board_state = copy.deepcopy(state.get_board_state())

    # Count so I can count backwards through the board.

    count = 0

    # We have a four check list so that if assigned True, the while loop
    # will skip any transformations in that column.

    # Top check is there in case I have three in a column and a different
    # number at the top. WHen set to True it stops an addition of the top
    # number if its equal to the transformation.

    four_check = [False, False, False, False]
    top_check = [False, False, False, False]

    # The while loop counts backwards through each row in the board.

    while count >= 0:

        # If we reach the top of the board then quit because numbers are all pushed
        # upwards, so by this point there is nothing left to do.

        if count == len(board_state) - 1:

            #
            break
        else:

            # The FOR loop deals with each column value in the row.

            for _ in range(len(board_state[0])):

                # Check to see if there is a number in this position.

                if board_state[count][_] != -1:

                    # Need the below clause to deal with four numbers in a row.

                    # Four_check allows the while loop to skip columns that have had
                    # four_number transformations, freezing this column
                    # in place.

                    if count == 0:
                        if board_state[count][_] == board_state[count + 1][_] == board_state[count + 2][_] == \
                                board_state[count + 3][_]:
                            board_state[count + 3][_] += board_state[count + 2][_]
                            board_state[count + 2][_] = -1
                            board_state[count + 1][_] = board_state[count + 3][_]
                            board_state[count][_] = -1
                            board_value += board_state[count + 3][_] * 2
                            four_check[_] = True
                            star = True

                            pass


                        # This checks if we have three in a row.
                        # The reason for the counter comparison is we only need to
                        # check for three in a column from row 3 and 2, otherwise
                        # its two in a row.

                        # Top check used here in case the top number is equal to the three_number
                        # transformation, again, freezing this column to avoid any further
                        # transformations throughout the WHILE loop.

                    if count <= 1:
                        if board_state[count][_] == board_state[count + 1][_] == board_state[count + 2][_]:
                            board_state[count + 2][_] += board_state[count + 1][_]
                            board_state[count + 1][_] = board_state[count][_]
                            board_state[count][_] = -1
                            board_value += board_state[count + 2][_]
                            top_check[_] = True

                            # Similiar to the check on up states at the bottom I
                            # also need to check here in down states if we are
                            # at the top of the list.

                            # This is to ensure that after a three transformation
                            # if a number exists ABOVE the three, that this number also
                            # slides down the board.

                            if count == 1:
                                board_state[count][_] = board_state[count - 1][_]
                                board_state[count - 1][_] = -1

                    # Below I check the space above the current tile is blank. I need the four check to avoid
                    # four numbers in a column continuing to be shifted after their transformation.

                    # I'm using the top_check below to stop numbers from being
                    # added together if I have transformed three and the transformation is
                    # equal to the top number.

                    if count <= 2:

                        if board_state[count + 1][_] == -1:
                            if four_check[_]:
                                pass
                            else:

                                if count <= 3:
                                    board_state[count + 1][_] = board_state[count][_]
                                    board_state[count][_] = board_state[count - 1][_]
                                    if count == 1:
                                        board_state[count - 1][_] = -1
                                    else:
                                        board_state[count - 1][_] = board_state[count - 2][_]
                                        board_state[count - 2][_] = -1
                                        top_check[count] = True


                        elif board_state[count + 1][_] == board_state[count][_]:
                            if top_check[_]:
                                pass
                            else:
                                if top_check[count]:
                                    pass
                                else:
                                    board_state[count + 1][_] += board_state[count][_]

                                    board_value += board_state[count + 1][_]

                                    board_state[count][_] = -1

                                    top_check[count] = True



                                # Again, just getting checks in place to ensure that
                                # after an addition takes place further down the board.

                                # That the rest of the numbers get shifted down as well.

                                if count == 2:
                                    if board_state[count][_] == board_state[count + 1][_]:
                                        board_state[count + 1][_] += board_state[count][_]
                                        board_state[count][_] = board_state[count - 1][_]
                                        board_state[count - 1][_] = board_state[count - 2][_]
                                        board_state[count - 2][_] = -1

            # Take one away from count to keep the while loop moving.

            count = count + 1

    # Only return a state if transformations have been applied.

    if board_state == state.get_board_state():
        return False
    else:
        state = State(board_state, board_value, move='DOWN')
        if star:
            state.set_star()
        else:
            pass
        return state

def up_states(state):

    star = False

    # Set board value to 0 .Each board will have a score associated with it.
    # This score is then added to the total score whenever a state is chosen.

    board_value = 0

    # Need a copy of the board to manipulate and create a fresh state with.

    board_state = copy.deepcopy(state.get_board_state())

    # Count so I can count backwards through the board.

    count = len(board_state) - 1

    # We have a four check list so that if assigned True, the while loop
    # will skip any transformations in that column.

    # Top check is there in case I have three in a column and a different
    # number at the top. WHen set to True it stops an addition of the top
    # number if its equal to the transformation.

    four_check = [False, False, False, False]
    top_check = [False, False, False, False]
    col_check = [False, False, False, False]

    # The while loop counts backwards through each row in the board.

    while count >= 0:

        # If we reach the top of the board then quit because numbers are all pushed
        # upwards, so by this point there is nothing left to do.

        if count == 0:
            break
        else:

            # The FOR loop deals with each column value in the row.

            for _ in range(len(board_state[0])):

                # Check to see if there is a number in this position.

                if board_state[count][_] != -1:

                    # Need the below clause to deal with four numbers in a row.

                    # Four_check allows the while loop to skip columns that have had
                    # four_number transformations, freezing this column
                    # in place.

                    if board_state[count][_] == board_state[count - 1][_] == board_state[count - 2][_] == \
                            board_state[count - 3][_]:
                        board_state[count - 3][_] += board_state[count - 2][_]
                        board_state[count - 2][_] = -1
                        board_state[count - 1][_] = board_state[count - 3][_]
                        board_state[count][_] = -1
                        board_value += board_state[count - 3][_] * 2
                        four_check[_] = True
                        star = True
                        pass
                    else:

                        # This checks if we have three in a row.
                        # The reason for the counter comparison is we only need to
                        # check for three in a column from row 3 and 2, otherwise
                        # its two in a row.

                        # Top check used here in case the top number is equal to the three_number
                        # transformation, again, freezing this column to avoid any further
                        # transformations throughout the WHILE loop.

                        if count >= 2:
                            if board_state[count][_] == board_state[count - 1][_] == board_state[count - 2][_]:
                                board_state[count - 2][_] += board_state[count - 1][_]
                                board_state[count - 1][_] = board_state[count][_]
                                board_state[count][_] = -1
                                board_value += board_state[count - 2][_]
                                top_check[_] = True

                        # Below I check the space above the current tile is blank. I need the four check to avoid
                        # four numbers in a column continuing to be shifted after their transformation.

                        # I'm using the top_check below to stop numbers from being
                        # added together if I have transformed three and the transformation is
                        # equal to the top number.

                        # Need a series of checks at the bottom and top fo the board to ensure
                        # numbers are moved and transformed correctly.

                        if board_state[count - 1][_] == -1:
                            if four_check[_]:
                                pass
                            else:
                                board_state[count - 1][_] = board_state[count][_]
                                if count == 3:
                                    board_state[count][_] = -1
                                else:
                                    board_state[count][_] = board_state[count + 1][_]
                                    board_state[count + 1][_] = -1
                                    if count == 1:
                                        board_state[count + 1][_] = board_state[count + 2][_]
                                        board_state[count + 2][_] = -1

                        elif board_state[count - 1][_] == board_state[count][_]:
                            if top_check[_]:
                                pass
                            elif board_state[count]:
                                pass
                            else:
                                board_state[count - 1][_] += board_state[count][_]
                                board_value += board_state[count - 1][_]
                                col_check[count - 1] = True

                                # Need this comparison check in case the two numbers
                                # that are the same sit at the bottom of the board.

                                # This ensures no index error when trying to shuffle
                                # numbers up the board.

                                if count != 3:
                                    board_state[count][_] = board_state[count + 1][_]
                                    board_state[count + 1][_] = -1
                                else:
                                    board_state[count][_] = -1

            # Take one away from count to keep the while loop moving.

            count = count - 1

    # Only return a state if transformations have been applied.

    if board_state == state.get_board_state():
        return False
    else:
        state = State(board_state, board_value, move="UP")
        if star:
            state.set_star()
        else:
            pass
        return state


def right_moves(state):

    star = False

    # Boar value gets set to 0, accumulated then added to total score
    # when the value is returned.

    board_value = 0

    add_flag_list = [False, False, False, False]

    # Need a copy of the board to manipulate and create a fresh state with.

    board_state = copy.deepcopy(state.get_board_state())

    for num, row in enumerate(board_state):

        # Just hard code the four here for the time being, this could do with an
        # adjustment later on.

        for col, val in enumerate(row):

            # Do the four check as soon as we pick up a row.

            # If we have four, do the transformation and jump out
            # of the FOR loop and onto the next row.


            if val != -1 and col == 0:

                if row[col] == row[col + 1] == row[col + 2] == row[col + 3]:
                    row[col + 3] += row[col + 2]
                    row[col + 1] += row[col]
                    row[col + 2] = -1
                    row[col] = -1
                    star = True
                    # Double the score we add here as we have added four
                    # numbers together in total.

                    board_value += row[col + 3] * 2
                    break

            # This checks when we reach the end of a row.
            # It checks to see if we have a number left to slide up

            # Also check here if we have two numbers to add.

            if col == len(board_state[0]) - 1:

                # if add_flag_list[col - 1] is True:
                #     break

                if row[col] == -1 and row[col - 1] != -1:
                    row[col] = row[col - 1]
                    row[col - 1] = row[col - 2]
                    row[col - 2] = row[col - 3]
                    row[col - 3] = -1
                    if row[col - 1] == -1:
                        row[col - 1] = row[col - 2]
                        row[col - 2] = -1
                        break
                    else:

                        break

                # Here just check if two numbers are the same and
                # if so add them.

                elif row[col] == row[col - 1] and val != -1:
                    if col > 0:
                        if add_flag_list[col - 1] == True:
                            pass
                        else:
                            row[col] += row[col - 1]
                            if col > 1:
                                row[col - 1] = row[col - 2]
                                row[col - 2] = -1
                                pass

                            board_value += row[col]

                            break



                # If we don't have a -1 next to our value and
                # the number is not the same as out value then
                # just pass with no move.

                else:
                    break

            elif col <= 1:

                if row[col] == row[col + 1] == row[col + 2] and val != -1:

                    row[col + 2] += val
                    row[col + 1] = val
                    row[col] = -1
                    board_value += row[col + 2]
                    break
                else:
                    # print(f"VAL IS {val}")
                    # print(f"row[col] {row[col]}")
                    # print(f"row[col + 1] {row[col + 1]}")
                    if val == row[col + 1] and row[col] != -1:

                        if add_flag_list[num] == True:
                            pass
                        else:
                            row[col + 1] += val
                            row[col] = row[col - 1]
                            row[col - 1] = -1
                            if num <= 2:
                                add_flag_list[col + 1] = True
                            board_value += row[col + 1]

                    elif row[col + 1] == -1:
                        row[col + 1] = val
                        row[col] = -1

                    else:
                        pass



    if board_state != state.get_board_state():
        state = State(board_state, board_value, move="RIGHT")

        if star == True:
            state.set_star()
        else:
            pass
        return state
    else:
        return False


def left_moves(state):

    star = False
    board = copy.deepcopy(state.get_board_state())

    board_value = 0

    add_flag = [False, False, False, False]

    for num, row in enumerate(board):

        counter = len(row) - 1

        while counter >= 0:

            if row[0] == row[1] == row[2] == row[3] and row[0] != -1:
                row[0] += row[1]
                row[2] += row[3]
                row[1] = -1
                row[3] = -1

                board_value += row[0] * 2

                star = True

                break

            if counter == 0:

                # Need a few catches here for when the loop reaches the
                # start of the list.

                if row[counter + 1] == -1 and row[counter + 2] != -1:

                    row[counter + 1] = row[counter + 2]
                    row[counter + 2] = -1

                if row[counter + 1] == -1 and row[counter + 2] == -1 and row[counter + 3] != -1:

                    row[counter + 1] = row[counter + 3]
                    row[counter + 3] = -1

                if row[counter + 2] == -1 and row[counter + 3] != -1:

                    row[counter + 2] = row[counter + 3]
                    row[counter + 3] = -1

                break

            else:

                if counter >= 2:

                    if row[counter] == row[counter - 1] == row[counter - 2] and row[counter] != -1:

                        row[counter - 2] += row[counter - 1]



                        row[counter] = - 1

                        board_value += row[counter - 2]

                        counter = counter - 1

                        continue

                if row[counter - 1] == -1:

                    row[counter - 1] = row[counter]

                    row[counter] = -1

                    counter = counter - 1

                    continue

                elif row[counter - 1] == row[counter] and row[counter] != -1:

                    if add_flag[counter] is True:

                        counter = counter - 1

                        continue

                    else:

                        row[counter - 1] += row[counter]

                        add_flag[counter - 1] = True

                        row[counter] = -1

                        board_value = row[counter - 1]

                        counter = counter - 1

                        continue

                else:

                    counter = counter - 1

                    continue

    if board != state.get_board_state():

        state = State(board, board_value, move="LEFT")

        if star == True:

            state.set_star()
        else:
            pass

        return state

    else:

        return False


def next_states(state):

    states = [up_states(state),
              down_states(state),
              right_moves(state),
              left_moves(state)]

    # I need next states to return a list of states.

    # I cant have it return a boolean value, if it returns
    # False then there are no moves to make.

    ret = [x for x in states if x is not False]

    if ret is None:

        return False

    else:
        return ret