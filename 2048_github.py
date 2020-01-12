from next_states import next_states, is_terminal
import os
from state import State
import random, time
import pandas as pd


class MonteCarlo:

    def __init__(self, start_state, rollout_iter, t, depth):

        self.start_state = start_state
        self.tree = {self.start_state: next_states(self.start_state)}
        self.rollout_iter = rollout_iter
        self.time = t
        self.depth = depth
        self.best_move = None

    def __repr__(self):

        return "Monte Carlo Search Object"

    def get_tree(self):

        return self.tree

    def set_best_move(self, move):

        self.best_move = move

    def reset_search(self, current_state):

        # This resets my search tree after it has been built
        # up over a number of iterations in order to deduce the
        # best move.

        self.tree.clear()
        next = next_states(current_state)
        self.tree[current_state] = next

    def search(self):

        time = self.time
        best_move = self.traverse_tree(time, self.start_state)
        if best_move == False:
            return False
        else:
            return best_move

    def are_you_leaf(self, state):

        # This for loop iterates through the tree
        # If it finds the state as a key it means
        # this is not a leaf.

        # If it does not find the state as a key (a parent)
        # Then we are deffo at a leaf.

        for parent, child in self.tree.items():

            if state == parent:
                return False
            else:
                return True

    def get_best_move(self, state):

        child_list = self.tree[state]
        val_list = [s.get_node_value() for s in child_list]
        if val_list == []:
            return False

        else:
            best_move_index = val_list.index(max(val_list))
            print(f"MOVE: {child_list[best_move_index].move}")
            time.sleep(0.25)
            return child_list[best_move_index]

    def traverse_tree(self, time, state):

        # So we fist set the starting state.

        # Then we count down the time variable, allowing for
        # as many roll-outs as we have time on the clock.

        while time > 0:

            current_state = state

            # First check in Monte Carlo is to check if we have leaf node.

            is_leaf = self.are_you_leaf(current_state)

            # If not, then we need to traverse the tree until we find a leaf node.

            while not is_leaf:

                # Now this while loop needs to find a leaf.

                # We do this by comparing UCB values.

                # First lets grab the children of the current node.
                # We KNOW this node is not a leaf and is therefore inside
                # the tree, so we can grab its child list by accessing the tree
                # directly.

                child_list = self.tree[current_state]

                if child_list == []:
                    return False

                # print(child_list)

                # Once we have a child list we need to se the UCB1 value
                # for each of the children.

                for ch in child_list:
                    ch.set_ucb_1(current_state.get_node_visits())

                # Now we create a ucb value list and take the state
                # from our child list that corresponds to the maximmum
                # index in our ucb list.

                ucb_val_list = [s.get_ucb_1() for s in child_list]

                # Now it's time to expand so lets choose the highest ucb
                # value.
                # We pick up the correct index from our ucb val list

                child_index = ucb_val_list.index(max(ucb_val_list))

                # Then using this index we pick up a child from our child list.

                current_state = child_list[child_index]

                # Finally we check if this is a leaf in order to try and
                # jump out of the WHILE loop.

                is_leaf = self.are_you_leaf(current_state)

            # So we finally have found a leaf, there are a few more checks to complete
            # before rolling out.

            # First we need to check if it has been visited before, if not we simply
            # rollout straight away, if so then we need to add this to the tree, along
            # with its children, slowly building up a picture of the search space using
            # simulated rollouts.

            total_state_visits = current_state.get_node_visits()

            if total_state_visits == 0:

                rollout_count = self.rollout_iter

                value = 0

                # Because this leaf has not been visited before we can just rollout
                # straight away.

                while rollout_count > 0:
                    value += self.rollout(current_state)

                    rollout_count = rollout_count - 1

                self.back_propogate(current_state, value / self.rollout_iter)

                # state.set_node_value(value)

                time = time - 1

                continue

            elif total_state_visits > 0:

                rollout_count = self.rollout_iter

                value = 0

                # Here we need to add the node to the tree.

                self.tree[current_state] = next_states(current_state)

                # Now we simply select the first available child to rollout
                # from.

                next_s = self.tree[current_state]

                if next_s:
                    current_state = next_s[0]
                else:
                    current_state = current_state

                # Now we have a rollout state we simply rollout!

                while rollout_count > 0:
                    value += self.rollout(current_state)

                    rollout_count = rollout_count - 1

                self.back_propogate(current_state, value / self.rollout_iter)

                # state.set_node_value(value)

                time = time - 1

                continue

        best_move = self.get_best_move(self.start_state)

        # Then we set the best move

        self.best_move = best_move

        return best_move

    def back_propogate(self, current_state, value):

        # Don't forget first we need to adjust the current nodes
        # value as we are updating the keys within the dictionary

        current_state.set_node_value(value)

        for parent, child in self.tree.items():

            if child == current_state:

                parent.set_node_value(value)

                current_state = parent

    def rollout(self, state):

        depth_limit = self.depth
        depth = 0

        # Here the rollout will simulate a randomly moved
        # game all the way to the end.

        # This final game value is passed back up the tree
        # adjusting the number of visits and the value of
        # each node.

        # We back-propagate this value to let the MCTS search
        # know which are the best nodes to visit.

        # Exploitation vs Exploration.

        total_score = state.get_board_value()

        rand_child = state

        while not is_terminal(rand_child):

            if depth == depth_limit:
                return total_score
            else:

                children = next_states(rand_child)

                if children == []:
                    total_score += rand_child.get_board_value()
                    return total_score
                else:
                    total_score += rand_child.get_board_value()
                    rand_child = random.choice(children)
                    depth += 1
                    rand_child.drop_tile()
                    continue


def simulate_full_game():

    start_board = [[-1, -1, -1, -1],
                   [-1, -1, -1, -1],
                   [-1, -1, -1, -1],
                   [-1, -1, -1, -1]]

    state = State(start_board, 0)

    t_score = state.get_board_value()

    while True:

        t_score += state.get_board_value()

        state.drop_tile()

        next_s = next_states(state)
        rand_move = False

        false_states = 0
        for s in next_s:
            if s is False:
                false_states += 1

        if false_states == 4:
            break
        else:

            while rand_move == False:
                rand_move = random.choice(next_s)

        state = rand_move


def agent_play(rollout_iter, t, depth, roll_count, dec_time, game_no):

    time_elapsed = 0

    move_list = []

    total_score = 0

    total_moves = 0

    start_board = [[-1, -1, -1, -1],
                   [-1, -1, -1, -1],
                   [-1, -1, -1, -1],
                   [-1, -1, -1, -1]]

    state = State(start_board, 0)

    state.drop_tile()
    state.drop_tile()

    terminal = is_terminal(state)

    monte_carlo = MonteCarlo(state, rollout_iter, t, depth)

    while not terminal:

        st = time.time()

        # time.sleep(0.5)

        os.system("clear")

        print("State after dropping tile.\n")

        for r in state.get_board_state():

            print(r)

        print('\n')

        print(f"\nScore before move {total_score}\n")
        print(f"Rollout's from single node {roll_count}")
        print(f"NUmber of total rollouts {dec_time}")
        print(f"Depth {depth}\n")
        print(f"Game Number: {game_no + 1}")
        print(f"Time elapsed {(time_elapsed / 60)} minutes")

        monte_carlo.reset_search(state)

        monte_carlo.start_state = state

        move = monte_carlo.search()

        if move == False:

            top_tile = find_top_tile(state)


            return total_score, move_list, total_moves, top_tile

        else:

            # time.sleep(0.5)

            os.system("clear")

            print("Move after monte carlo...\n")

            for r in move.get_board_state():

                print(r)

            print('\n')

            move_list.append(move.move)

            total_score += move.get_board_value()

            print(f"\nScore after move {total_score}\n")

            terminal = is_terminal(state)

            state = move

            state.drop_tile()

            total_moves += 1

            end = time.time() - st
            time_elapsed += end


def find_top_tile(state):

    top_tile = 0

    board = state.get_board_state()

    for _ in range(len(board[0])):

        for _1 in range(len(board[0])):

            if board[_][_1] > top_tile:

                top_tile = board[_][_1]

    return top_tile


def main():

    output = None

    rollout_count = 200
    depth = 4
    decision_time = 6

    rows_list = []

    for _ in range(20):

        game_frame = {}

        start = time.time()
        score, move_list, total_moves, top_tile = agent_play(rollout_count,
                                                             decision_time,
                                                             depth,
                                                             rollout_count,
                                                             decision_time,
                                                             _)
        end = (time.time() - start) / 60

        print(f"\nGame Over.\nTotal Score: {score}")
        print(f"Total time to play full game: {end} minutes")
        print(f"Top tile: {top_tile}")
        print(f"Total Number of Moves {total_moves}")
        print(f"Search Depth Limit {depth}")
        print(f"Time for Decision {decision_time}")
        print(f"Rollout from individual node {rollout_count}")
        print("All moves through game.\n")

        game_frame['Game'] = _ + 1
        game_frame['Rollout Iterations'] = rollout_count
        game_frame['Time for decision'] = decision_time
        game_frame['Search Depth Limit'] = depth
        game_frame['Total Score'] = score
        game_frame['Total Moves'] = total_moves
        game_frame['Time To Play (minutes)'] = end
        game_frame['Top Tile'] = top_tile

        up = 0
        down = 0
        right = 0
        left = 0
        for move in move_list:
            if move == "UP":
                up += 1

            elif move == "DOWN":
                down += 1

            elif move == "RIGHT":
                right += 1

            elif move == "LEFT":
                left += 1

        print(f"\nUP: {up}")
        print(f"DOWN: {down}")
        print(f"LEFT {left}")
        print(f"RIGHT: {right}\n")

        # game_frame['GAME UP'] = up
        # game_frame['GAME DOWN'] = down
        # game_frame['GAME RIGHT'] = right
        # game_frame['GAME LEFT'] = left

        rows_list.append(game_frame)

    output_row = pd.DataFrame(rows_list)

    output_row.to_csv("masb_r500_d4_t4.csv")



main()