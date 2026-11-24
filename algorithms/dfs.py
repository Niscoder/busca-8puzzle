from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        nodes_generated = 1
        nodes_expanded = 0

        if initial.is_goal:
            return SearchResult(initial, 0, nodes_generated, 1, initial.cost)

        if not initial.is_solvable:
            return SearchResult(None, 0, nodes_generated, 1, 0)

        stack = [initial]
        best_depth = {initial.tiles: 0}
        max_frontier_size = 1

        while stack:
            state = stack.pop()

            if best_depth[state.tiles] < state.cost:
                continue

            if state.cost >= self.depth_limit:
                continue

            nodes_expanded += 1

            for child in reversed(state.neighbors()):
                nodes_generated += 1

                if child.is_goal:
                    return SearchResult(
                        solution=child,
                        nodes_expanded=nodes_expanded,
                        nodes_generated=nodes_generated,
                        max_frontier_size=max_frontier_size,
                        depth=child.cost,
                    )

                known = best_depth.get(child.tiles)
                if known is not None and known <= child.cost:
                    continue
                best_depth[child.tiles] = child.cost
                stack.append(child)

            max_frontier_size = max(max_frontier_size, len(stack))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size, 0)
