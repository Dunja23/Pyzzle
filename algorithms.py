import random
import time
import heapq

import config


class Algorithm:
    def __init__(self, heuristic=None):
        self.heuristic = heuristic
        self.nodes_evaluated = 0
        self.nodes_generated = 0

    def get_legal_actions(self, state):
        self.nodes_evaluated += 1
        max_index = len(state)
        zero_tile_ind = state.index(0)
        legal_actions = []
        if 0 <= (up_ind := (zero_tile_ind - config.N)) < max_index:
            legal_actions.append(up_ind)
        if 0 <= (right_ind := (zero_tile_ind + 1)) < max_index and right_ind % config.N:
            legal_actions.append(right_ind)
        if 0 <= (down_ind := (zero_tile_ind + config.N)) < max_index:
            legal_actions.append(down_ind)
        if 0 <= (left_ind := (zero_tile_ind - 1)) < max_index and (left_ind + 1) % config.N:
            legal_actions.append(left_ind)
        return legal_actions

    def apply_action(self, state, action):
        self.nodes_generated += 1
        copy_state = list(state)
        zero_tile_ind = state.index(0)
        copy_state[action], copy_state[zero_tile_ind] = copy_state[zero_tile_ind], copy_state[action]
        return tuple(copy_state)

    def get_steps(self, initial_state, goal_state):
        pass

    def get_solution_steps(self, initial_state, goal_state):
        begin_time = time.time()
        solution_actions = self.get_steps(initial_state, goal_state)
        print(f'Execution time in seconds: {(time.time() - begin_time):.2f} | '
              f'Nodes generated: {self.nodes_generated} | '
              f'Nodes evaluated: {self.nodes_evaluated}')
        return solution_actions


class ExampleAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        solution_actions = []
        while state != goal_state:
            legal_actions = self.get_legal_actions(state)
            action = legal_actions[random.randint(0, len(legal_actions) - 1)]
            solution_actions.append(action)
            state = self.apply_action(state, action)
        return solution_actions
    

class BFSAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        queue = [(initial_state, [])]
        visited_states = set()

        while queue:
            current_state, current_actions = queue.pop(0)
            if current_state == goal_state:
                return current_actions
            if current_state not in visited_states:
                visited_states.add(current_state)
                legal_actions = self.get_legal_actions(current_state)
                for action in legal_actions:
                    next_state = self.apply_action(current_state, action)
                    next_actions = current_actions + [action]
                    queue.append((next_state, next_actions))

        return []
    

class BestFirstAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        priority_queue = [(self.heuristic.get_evaluation(initial_state), initial_state, [])]
        visited_states = set()

        while priority_queue:
            _, current_state, current_actions = heapq.heappop(priority_queue)
            if current_state == goal_state:
                return current_actions
            if current_state not in visited_states:
                legal_actions = self.get_legal_actions(current_state)
                for action in legal_actions:
                    next_state = self.apply_action(current_state, action)
                    next_actions = current_actions + [action]
                    priority = self.heuristic.get_evaluation(next_state)
                    heapq.heappush(priority_queue, (priority, next_state, next_actions))    
                visited_states.add(current_state)

        return []
    

class AStarAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        priority_queue = [(0 + self.heuristic.get_evaluation(initial_state), initial_state, 0, [])]
        visited_states = set()

        while priority_queue:
            _, current_state, cost, current_actions = heapq.heappop(priority_queue)
            if current_state == goal_state:
                return current_actions
            if current_state not in visited_states:
                visited_states.add(current_state)
                legal_actions = self.get_legal_actions(current_state)
                for action in legal_actions:
                    next_state = self.apply_action(current_state, action)
                    next_actions = current_actions + [action]
                    next_cost = cost + 1
                    heapq.heappush(priority_queue, (next_cost + self.heuristic.get_evaluation(next_state), next_state, next_cost, next_actions))

        return []
    
class BandBAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        priority_queue = [(0, initial_state, [])]
        visited_states = set()

        while priority_queue:
            cost, current_state, current_actions = heapq.heappop(priority_queue)
            if current_state == goal_state:
                return current_actions
            if current_state not in visited_states:
                visited_states.add(current_state)
                legal_actions = self.get_legal_actions(current_state)
                for action in legal_actions:
                    next_state = self.apply_action(current_state, action)
                    next_actions = current_actions + [action]
                    next_cost = cost + self.heuristic.get_evaluation(next_state)
                    heapq.heappush(priority_queue, (next_cost, next_state, next_actions))

        return []