from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        expandidos = 0
        gerados = 1
        max_fronteira = 1

        if not initial.is_solvable:
            return SearchResult(None, expandidos, gerados, max_fronteira, 0)

        pilha = [initial]
        # guarda a menor profundidade em que cada estado já foi alcançado,
        # assim um estado só é revisitado se for por um caminho mais curto
        melhor_profundidade = {initial.tiles: 0}

        while pilha:
            atual = pilha.pop()

            if atual.is_goal:
                return SearchResult(atual, expandidos, gerados, max_fronteira, atual.cost)

            # estado já foi alcançado depois por um caminho mais curto
            if atual.cost > melhor_profundidade[atual.tiles]:
                continue

            if atual.cost >= self.depth_limit:
                continue

            expandidos += 1

            # empilha ao contrário para expandir na ordem UP, DOWN, LEFT, RIGHT
            for filho in reversed(atual.neighbors()):
                gerados += 1
                prof = melhor_profundidade.get(filho.tiles)
                if prof is not None and prof <= filho.cost:
                    continue
                melhor_profundidade[filho.tiles] = filho.cost
                pilha.append(filho)

            max_fronteira = max(max_fronteira, len(pilha))

        return SearchResult(None, expandidos, gerados, max_fronteira, 0)
