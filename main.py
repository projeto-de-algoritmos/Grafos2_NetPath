import pygame
import random


colors = [
    (0, 0, 0),  # Preto
    (255, 255, 255),  # Branco
    (255, 40, 0),  # Vermelho
    (139, 0, 0),  # Vermelho Escuro
    (0, 0, 255),  # Azul
    (0, 0, 139),  # Azul Escuro
    (0, 255, 0),  # Verde
    (255, 215, 0),  # Ouro
    (105, 105, 105),  # Cinza
    (240, 230, 140),  # Amarelo Khaki
    (255, 140, 0),  # Laranja Escuro
    (255, 165, 0),  # Laranja
    (255, 69, 0),  # Laranja Avermelhado
]

nodesCenterPositions = {
    'A': (70, 300),
    'B': (220, 450),
    'C': (230, 150),
    'D': (330, 300),
    'E': (400, 150),
    'F': (430, 450),
    'G': (530, 200),
    'H': (730, 400)
}

edgesDirectionsIndication = [
    (206, 435), (216, 165), (317, 282), (317, 317), (380, 150), (392, 167),
    (403, 170), (410, 450), (418, 432), (510, 193), (710, 402), (715, 385)
]


class Game:
    def __init__(self, resolution, display, running, screens):
        self.resolution = resolution
        self.display = display
        self.running = running
        self.screens = screens
        self.isWeightsChoicesDone = False

        self.edgesWeights = {
            'A': {'B': 0, 'C': 0},
            'B': {'D': 0, 'F': 0},
            'C': {'D': 0, 'E': 0},
            'D': {'E': 0, 'F': 0},
            'E': {'G': 0},
            'F': {'E': 0, 'H': 0},
            'G': {'H': 0},
            'H': {}
        }

        self.edges = {}

    def initialPage(self):
        icon = pygame.image.load('./assets/media/icon.png')
        self.display.blit(
            pygame.transform.scale(icon, (200, 200)),
            (int(self.resolution[0]/2 - 100), 40)
        )

        titleFont = pygame.font.Font('./assets/fonts/Roboto-Bold.ttf', 40)
        title = titleFont.render('dPath', True, colors[1])
        titleArea = title.get_rect()
        titleArea.center = (
            int(self.resolution[0]/2),
            int(title.get_height()/2) + 200 + 40 + 40
        )
        self.display.blit(title, titleArea)

        buttonsTextFont = pygame.font.Font(
            './assets/fonts/Roboto-Bold.ttf', 20
        )
        quitButtonText = buttonsTextFont.render('SAIR', True, colors[1])
        quitButtonText_W = quitButtonText.get_width()
        quitButtonText_H = quitButtonText.get_height()

        mouse = pygame.mouse.get_pos()

        quitStart_X = (
            int(self.resolution[0]/2 - quitButtonText_W/2 - 20)
        )
        quitStart_Y = (
            self.resolution[1] - 40 - quitButtonText_H - 20
        )
        if (
            quitStart_X <= mouse[0] <= quitStart_X + quitButtonText_W + 40
            and quitStart_Y <= mouse[1] <= quitStart_Y + quitButtonText_H + 20
        ):
            pygame.draw.rect(
                self.display, colors[3],
                (
                    quitStart_X, quitStart_Y,
                    quitButtonText_W + 40, quitButtonText_H + 20
                )
            )
        else:
            pygame.draw.rect(
                self.display, colors[2],
                (
                    quitStart_X, quitStart_Y,
                    quitButtonText_W + 40, quitButtonText_H + 20
                )
            )

        self.display.blit(quitButtonText, (quitStart_X + 20, quitStart_Y + 10))

        startButtonText = buttonsTextFont.render(
            'ENCONTRAR MENOR CAMINHO', True, colors[1]
        )
        sButtonText_W = startButtonText.get_width()
        sButtonText_H = startButtonText.get_height()

        sButtonStart_X = int(
            self.resolution[0]/2 - sButtonText_W/2 - 20
        )
        sButtonStart_Y = (
            177 + 40 + 40 + title.get_height() + 40
        )
        if (
            sButtonStart_X <= mouse[0] <= sButtonStart_X + sButtonText_W + 40
            and
            sButtonStart_Y <= mouse[1] <= sButtonStart_Y + sButtonText_H + 20
        ):
            pygame.draw.rect(
                self.display, colors[5],
                (
                    sButtonStart_X, sButtonStart_Y,
                    sButtonText_W + 40, sButtonText_H + 20
                )
            )
        else:
            pygame.draw.rect(
                self.display, colors[4],
                (
                    sButtonStart_X, sButtonStart_Y,
                    sButtonText_W + 40, sButtonText_H + 20
                )
            )

        self.display.blit(
            startButtonText, (sButtonStart_X + 20, sButtonStart_Y + 10)
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                quit_H = quitButtonText_H
                quit_W = quitButtonText_W
                if (
                    quitStart_X <= mouse[0] <= quitStart_X + quit_W + 40
                    and quitStart_Y <= mouse[1] <= quitStart_Y + quit_H + 20
                ):
                    print("Encerrando o programa...")

                    self.running = False

                start_W = sButtonText_W
                start_H = sButtonText_H
                if (
                    sButtonStart_X <= mouse[0] <= sButtonStart_X + start_W + 40
                    and
                    sButtonStart_Y <= mouse[1] <= sButtonStart_Y + start_H + 20
                ):
                    print("Alterando tela...")

                    self.screens['initialPage'] = 0
                    self.screens['shortestPathPreviewPage'] = 0
                    self.screens['shortestPathFindPage'] = 1

    def dijkstra(self, startNode, endNode):
        print("Iniciando Dijkstra...")

        distances = {str(i): 2000 for i in self.edgesWeights}
        distances[startNode] = 0

        self.edges = {str(i): (None, 2000) for i in self.edgesWeights}
        self.edges[startNode] = (None, 0)

        while distances:
            nearestNode = min(distances.keys(), key=(lambda k: distances[k]))
            distances.pop(nearestNode)

            pygame.draw.circle(
                self.display, colors[10],
                nodesCenterPositions[nearestNode], 20
            )
            pygame.display.update()
            pygame.time.delay(200)

            for i in self.edgesWeights[nearestNode]:

                pygame.draw.circle(
                    self.display, colors[10],
                    nodesCenterPositions[i], 20
                )
                pygame.display.update()
                pygame.time.delay(200)

                edgeWeight = self.edgesWeights[nearestNode][i]
                d = self.edges[nearestNode][1] + edgeWeight
                if d < self.edges[i][1]:
                    distances[i] = d
                    self.edges[i] = (nearestNode, d)

                if i == 'H':
                    pygame.draw.circle(
                        self.display, colors[7],
                        nodesCenterPositions[i], 20
                    )
                else:
                    pygame.draw.circle(
                        self.display, colors[9],
                        nodesCenterPositions[i], 20
                    )
                pygame.display.update()
                pygame.time.delay(200)

            if nearestNode == 'A':
                pygame.draw.circle(
                    self.display, colors[6],
                    nodesCenterPositions[nearestNode], 20
                )
            else:
                pygame.draw.circle(
                    self.display, colors[9],
                    nodesCenterPositions[nearestNode], 20
                )
            pygame.display.update()
            pygame.time.delay(200)

        print("Finalizando algoritmo...")

        self.screens['initialPage'] = 0
        self.screens['shortestPathFindPage'] = 0
        self.screens['shortestPathPreviewPage'] = 1

    def shortestPathFindPage(self):
        titleFont = pygame.font.Font('./assets/fonts/Roboto-Bold.ttf', 35)
        title = titleFont.render(
            'Aplicando Dijkstra no Grafo', True, colors[11]
        )
        titleArea = title.get_rect()
        titleArea.center = (
            int(self.resolution[0]/2),
            int(title.get_height()/2) + 40
        )
        self.display.blit(title, titleArea)

        for i in nodesCenterPositions:
            for j in self.edgesWeights[i]:
                pygame.draw.line(
                    self.display, colors[8],
                    nodesCenterPositions[i], nodesCenterPositions[j], 3
                )

                if i > j:
                    pygame.draw.circle(
                        self.display, colors[9], nodesCenterPositions[j], 20
                    )

                if not self.isWeightsChoicesDone:
                    print("Construido grafo na tela...")
                    print("Gerando peso de aresta aleatoriamente...")

                    self.edgesWeights[i][j] = random.choice(range(100))
                    pygame.display.update()
                    pygame.time.delay(100)

                textFont = pygame.font.Font(
                    './assets/fonts/Roboto-Bold.ttf', 20
                )
                weight = textFont.render(
                    str(self.edgesWeights[i][j]), True, colors[0]
                )
                weightArea = weight.get_rect()

                w_W = nodesCenterPositions[i][0] + nodesCenterPositions[j][0]
                w_H = nodesCenterPositions[i][1] + nodesCenterPositions[j][1]
                weightArea.center = (int(w_W/2), int(w_H/2))

                pygame.draw.rect(
                    self.display, colors[1],
                    (
                        int(w_W/2) - int(weight.get_width()/2) - 5,
                        int(w_H/2) - int(weight.get_height()/2) - 5,
                        weight.get_width() + 10, weight.get_height() + 10
                    )
                )

                self.display.blit(weight, weightArea)

                if not self.isWeightsChoicesDone:
                    pygame.display.update()
                    pygame.time.delay(100)

            if i == 'A':
                pygame.draw.circle(
                    self.display, colors[6], nodesCenterPositions[i], 20
                )
            elif i == 'H':
                pygame.draw.circle(
                    self.display, colors[7], nodesCenterPositions[i], 20
                )
            else:
                pygame.draw.circle(
                    self.display, colors[9], nodesCenterPositions[i], 20
                )

            if not self.isWeightsChoicesDone:
                pygame.display.update()
                pygame.time.delay(100)

        for i in edgesDirectionsIndication:
            pygame.draw.circle(self.display, colors[0], i, 5)
            pygame.display.update()
            pygame.time.delay(100)

        self.isWeightsChoicesDone = True

        self.dijkstra('A', 'H')

    def shortestPathPreviewPage(self):
        print("Iniciando apresentação do menor caminho...")

        titleFont = pygame.font.Font('./assets/fonts/Roboto-Bold.ttf', 35)
        title = titleFont.render('Menor Caminho', True, colors[12])
        titleArea = title.get_rect()
        titleArea.center = (
            int(self.resolution[0]/2),
            int(title.get_height()/2) + 40
        )
        self.display.blit(title, titleArea)

        for i in nodesCenterPositions:
            for j in self.edgesWeights[i]:
                pygame.draw.line(
                    self.display, colors[8],
                    nodesCenterPositions[i], nodesCenterPositions[j], 3
                )

                if i > j:
                    pygame.draw.circle(
                        self.display, colors[9],
                        nodesCenterPositions[j], 20
                    )
                if i == 'A':
                    pygame.draw.circle(
                        self.display, colors[6], nodesCenterPositions[i], 20
                    )
                elif j == 'H':
                    pygame.draw.circle(
                        self.display, colors[9], nodesCenterPositions[i], 20
                    )
                    pygame.draw.circle(
                        self.display, colors[7], nodesCenterPositions[j], 20
                    )
                else:
                    pygame.draw.circle(
                        self.display, colors[9], nodesCenterPositions[i], 20
                    )

                textFont = pygame.font.Font(
                    './assets/fonts/Roboto-Bold.ttf', 20
                )
                weight = textFont.render(
                    str(self.edgesWeights[i][j]), True, colors[0]
                )
                weightArea = weight.get_rect()

                w_W = nodesCenterPositions[i][0] + nodesCenterPositions[j][0]
                w_H = nodesCenterPositions[i][1] + nodesCenterPositions[j][1]
                weightArea.center = (int(w_W/2), int(w_H/2))

                pygame.draw.rect(
                    self.display, colors[1],
                    (
                        int(w_W/2) - int(weight.get_width()/2) - 5,
                        int(w_H/2) - int(weight.get_height()/2) - 5,
                        weight.get_width() + 10, weight.get_height() + 10
                    )
                )

                self.display.blit(weight, weightArea)

        for i in edgesDirectionsIndication:
            pygame.draw.circle(self.display, colors[0], i, 5)

        shortestPath = []
        edge = 'H'
        while edge != 'A':
            shortestPath.append((self.edges[edge][0], edge))
            edge = self.edges[edge][0]

        for i in shortestPath:
            pygame.draw.circle(
                self.display, colors[6],
                nodesCenterPositions[i[1]], 20
            )
            pygame.display.update()
            pygame.time.delay(400)

            pygame.draw.line(
                self.display, colors[6],
                nodesCenterPositions[i[0]], nodesCenterPositions[i[1]], 3
            )

            textFont = pygame.font.Font(
                './assets/fonts/Roboto-Bold.ttf', 20
            )
            weight = textFont.render(
                str(self.edgesWeights[i[0]][i[1]]), True, colors[0]
            )
            weightArea = weight.get_rect()

            w_W = nodesCenterPositions[i[0]][0] + nodesCenterPositions[i[1]][0]
            w_H = nodesCenterPositions[i[0]][1] + nodesCenterPositions[i[1]][1]
            weightArea.center = (int(w_W/2), int(w_H/2))

            pygame.draw.rect(
                self.display, colors[1],
                (
                    int(w_W/2) - int(weight.get_width()/2) - 5,
                    int(w_H/2) - int(weight.get_height()/2) - 5,
                    weight.get_width() + 10, weight.get_height() + 10
                )
            )
            self.display.blit(weight, weightArea)

            pygame.display.update()
            pygame.time.delay(400)

            pygame.draw.circle(
                self.display, colors[6],
                nodesCenterPositions[i[0]], 20
            )

            pygame.display.update()
            pygame.time.delay(400)

        print("Apresentação do menor caminho finalizada.")
        print("Voltando para a tela inicial...")

        for i in edgesDirectionsIndication:
            pygame.draw.circle(self.display, colors[0], i, 5)

        pygame.display.update()
        pygame.time.delay(1454)

        self.screens['initialPage'] = 1
        self.screens['shortestPathFindPage'] = 0
        self.screens['shortestPathPreviewPage'] = 0


def main():
    pygame.init()

    resolution = (800, 600)

    pygame.display.set_caption("dPath")

    icon = pygame.image.load('./assets/media/icon.png')
    pygame.display.set_icon(icon)

    display = pygame.display.set_mode(resolution)

    screens = {
        'initialPage': 1, 'shortestPathFindPage': 0,
        'shortestPathPreviewPage': 0
    }

    newGame = Game(resolution, display, True, screens)

    while newGame.running:
        if newGame.screens['initialPage']:
            display.fill(colors[0])
            newGame.initialPage()
        elif newGame.screens['shortestPathFindPage']:
            display.fill(colors[1])
            newGame.shortestPathFindPage()
        elif newGame.screens['shortestPathPreviewPage']:
            display.fill(colors[1])
            newGame.shortestPathPreviewPage()

        pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.quit()
    quit()
