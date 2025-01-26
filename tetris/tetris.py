import pygame
import random
import math

# Inisialisasi pygame
pygame.init()

# Konstanta
CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 30
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT

# Warna-warna (RGB)
COLORS = [
    (255, 0, 0),  # Merah
    (0, 255, 0),  # Hijau
    (0, 0, 255),  # Biru
    (255, 255, 0),  # Kuning
    (255, 165, 0),  # Oranye
    (128, 0, 128),  # Ungu
    (0, 255, 255)  # Cyan
]

# Bentuk-bentuk Tetromino
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]


class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Tetris Berkilau')
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.glow_counter = 0

    def new_piece(self):
        # Membuat piece baru dengan posisi dan warna random
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return {
            'shape': shape,
            'color': color,
            'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
            'y': 0
        }

    def valid_move(self, piece, x, y):
        for i in range(len(piece['shape'])):
            for j in range(len(piece['shape'][0])):
                if piece['shape'][i][j]:
                    new_x = x + j
                    new_y = y + i
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True

    def merge_piece(self):
        for i in range(len(self.current_piece['shape'])):
            for j in range(len(self.current_piece['shape'][0])):
                if self.current_piece['shape'][i][j]:
                    if self.current_piece['y'] + i < 0:
                        self.game_over = True
                        return
                    self.grid[self.current_piece['y'] + i][self.current_piece['x'] + j] = self.current_piece['color']

    def clear_lines(self):
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(self.grid[y]):
                lines_cleared += 1
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            else:
                y -= 1
        self.score += lines_cleared * 100

    def rotate_piece(self):
        new_shape = list(zip(*reversed(self.current_piece['shape'])))
        new_piece = {
            'shape': new_shape,
            'color': self.current_piece['color'],
            'x': self.current_piece['x'],
            'y': self.current_piece['y']
        }
        if self.valid_move(new_piece, new_piece['x'], new_piece['y']):
            self.current_piece = new_piece

    def draw(self):
        self.screen.fill((0, 0, 0))

        # Menggambar grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    color = self.grid[y][x]
                    # Efek berkilau
                    glow = abs(math.sin(self.glow_counter / 20)) * 50
                    glowed_color = tuple(min(255, c + glow) for c in color)
                    pygame.draw.rect(self.screen, glowed_color,
                                     (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                     (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        # Menggambar piece yang sedang jatuh
        if not self.game_over:
            for i in range(len(self.current_piece['shape'])):
                for j in range(len(self.current_piece['shape'][0])):
                    if self.current_piece['shape'][i][j]:
                        x = (self.current_piece['x'] + j) * CELL_SIZE
                        y = (self.current_piece['y'] + i) * CELL_SIZE
                        # Efek berkilau untuk piece yang sedang jatuh
                        glow = abs(math.sin(self.glow_counter / 20)) * 50
                        color = self.current_piece['color']
                        glowed_color = tuple(min(255, c + glow) for c in color)
                        pygame.draw.rect(self.screen, glowed_color, (x, y, CELL_SIZE, CELL_SIZE))
                        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, CELL_SIZE, CELL_SIZE), 1)

        # Menampilkan Game Over
        if self.game_over:
            font = pygame.font.Font(None, 48)
            game_over_text = font.render('GAME OVER', True, (255, 0, 0))
            score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2,
                                              WINDOW_HEIGHT // 2 - game_over_text.get_height()))
            self.screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2,
                                          WINDOW_HEIGHT // 2 + score_text.get_height()))

        pygame.display.flip()

    def run(self):
        fall_time = 0
        fall_speed = 50  # Semakin kecil nilainya, semakin cepat

        while True:
            self.glow_counter += 1
            fall_time += self.clock.get_rawtime()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if not self.game_over:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            if self.valid_move(self.current_piece,
                                               self.current_piece['x'] - 1,
                                               self.current_piece['y']):
                                self.current_piece['x'] -= 1
                        if event.key == pygame.K_RIGHT:
                            if self.valid_move(self.current_piece,
                                               self.current_piece['x'] + 1,
                                               self.current_piece['y']):
                                self.current_piece['x'] += 1
                        if event.key == pygame.K_DOWN:
                            if self.valid_move(self.current_piece,
                                               self.current_piece['x'],
                                               self.current_piece['y'] + 1):
                                self.current_piece['y'] += 1
                        if event.key == pygame.K_UP:
                            self.rotate_piece()
                        if event.key == pygame.K_SPACE:
                            while self.valid_move(self.current_piece,
                                                  self.current_piece['x'],
                                                  self.current_piece['y'] + 1):
                                self.current_piece['y'] += 1

            if not self.game_over:
                if fall_time >= fall_speed:
                    fall_time = 0
                    if self.valid_move(self.current_piece,
                                       self.current_piece['x'],
                                       self.current_piece['y'] + 1):
                        self.current_piece['y'] += 1
                    else:
                        self.merge_piece()
                        self.clear_lines()
                        if not self.game_over:
                            self.current_piece = self.new_piece()

            self.draw()


if __name__ == '__main__':
    game = Tetris()
    game.run()