class Heuristic:
    def get_evaluation(self, state):
        pass


class ExampleHeuristic(Heuristic):
    def get_evaluation(self, state):
        return 0

class HammingHeuristic(Heuristic):
    def get_evaluation(self, state):
        sorted_state = list(range(1, len(state))) + [0]
        value = 0
        for st, goal in zip(state, sorted_state):
            if st != goal:
                value += 1
        return value

    
class ManhattanHeuristic(Heuristic):
    def get_evaluation(self, state):
        size = int(len(state) ** 0.5)
        value = 0
        for st in state:
            if st != 0: 
                st_row, st_col = divmod(state.index(st), size)
                goal_row, goal_col = divmod(st - 1, size)
                value += abs(st_row - goal_row) + abs(st_col - goal_col)
        return value
    
class NewHeuristic(Heuristic):
    def get_evaluation(self, state):
        sorted_state = list(range(1, len(state))) + [0]
        size = int(len(state) ** 0.5)
        value = 0
        for st, goal in zip(state, sorted_state):
            if st % size != goal % size:
                value += 1
        return value
    
class MaxSwapHeuristic(Heuristic):
    def get_evaluation(self, state):
        inversion_count = 0
        size = int(len(state) ** 0.5)

        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] > state[j] and state[i] != 0 and state[j] != 0:
                    inversion_count += 1

        return inversion_count
