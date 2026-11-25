import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        # distância de Manhattan: soma das distâncias de cada peça até sua posição final
        # (o espaço vazio não entra na conta, por isso a heurística é admissível)
        distancia = 0
        for i, peca in enumerate(state.tiles):
            if peca == 0:
                continue
            destino = peca - 1
            distancia += abs(i // 3 - destino // 3) + abs(i % 3 - destino % 3)
        return distancia

    def search(self, initial: State) -> SearchResult:
        expandidos = 0
        gerados = 1
        max_fronteira = 1

        if not initial.is_solvable:
            return SearchResult(None, expandidos, gerados, max_fronteira, 0)

        contador = 0  # desempate entre nós com o mesmo f
        fronteira = [(self.heuristic(initial), contador, initial)]
        melhor_g = {initial.tiles: 0}
        fechados = set()

        while fronteira:
            _, _, atual = heapq.heappop(fronteira)

            if atual.tiles in fechados:
                continue

            if atual.is_goal:
                return SearchResult(atual, expandidos, gerados, max_fronteira, atual.cost)

            fechados.add(atual.tiles)
            expandidos += 1

            for filho in atual.neighbors():
                gerados += 1
                if filho.tiles in fechados:
                    continue
                if filho.cost < melhor_g.get(filho.tiles, float("inf")):
                    melhor_g[filho.tiles] = filho.cost
                    contador += 1
                    f = filho.cost + self.heuristic(filho)
                    heapq.heappush(fronteira, (f, contador, filho))

            max_fronteira = max(max_fronteira, len(fronteira))

        return SearchResult(None, expandidos, gerados, max_fronteira, 0)
