import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

GOAL_POSITIONS = {tile: divmod(i, 3) for i, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distance = 0
        for i, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            row, col = divmod(i, 3)
            goal_row, goal_col = GOAL_POSITIONS[tile]
            distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        nodes_generated = 1
        nodes_expanded = 0

        if not initial.is_solvable:
            return SearchResult(None, 0, nodes_generated, 1, 0)

        tie = count()
        h0 = self.heuristic(initial)
        frontier = [(initial.cost + h0, h0, next(tie), initial)]
        best_g = {initial.tiles: initial.cost}
        explored = set()
        max_frontier_size = 1

        while frontier:
            _, _, _, state = heapq.heappop(frontier)

            if state.tiles in explored:
                continue

            if state.is_goal:
                return SearchResult(
                    solution=state,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=state.cost,
                )

            explored.add(state.tiles)
            nodes_expanded += 1

            for child in state.neighbors():
                nodes_generated += 1
                if child.tiles in explored:
                    continue
                if child.cost >= best_g.get(child.tiles, float("inf")):
                    continue
                best_g[child.tiles] = child.cost
                h = self.heuristic(child)
                heapq.heappush(frontier, (child.cost + h, h, next(tie), child))

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size, 0)
