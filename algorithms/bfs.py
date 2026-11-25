from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        expandidos = 0
        gerados = 1
        max_fronteira = 1

        if not initial.is_solvable:
            return SearchResult(None, expandidos, gerados, max_fronteira, 0)

        if initial.is_goal:
            return SearchResult(initial, expandidos, gerados, max_fronteira, initial.cost)

        fronteira = deque([initial])
        visitados = {initial.tiles}

        while fronteira:
            atual = fronteira.popleft()
            expandidos += 1

            for filho in atual.neighbors():
                gerados += 1
                if filho.tiles in visitados:
                    continue

                # teste de objetivo na geração: a BFS já garante o menor caminho
                if filho.is_goal:
                    return SearchResult(filho, expandidos, gerados, max_fronteira, filho.cost)

                visitados.add(filho.tiles)
                fronteira.append(filho)

            max_fronteira = max(max_fronteira, len(fronteira))

        return SearchResult(None, expandidos, gerados, max_fronteira, 0)
