import pygame
import random


class PongGame:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pong Game")

        # Warna
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Objek Permainan
        self.paddle_width = 15
        self.paddle_height = 90
        self.ball_size = 15

        # Posisi Awal
        self.player1_x = 50
        self.player1_y = self.height // 2 - self.paddle_height // 2
        self.player2_x = self.width - 50 - self.paddle_width
        self.player2_y = self.height // 2 - self.paddle_height // 2

        # Bola
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.ball_dx = random.choice([-5, 5])
        self.ball_dy = random.choice([-5, 5])

        # Skor
        self.player1_score = 0
        self.player2_score = 0

        self.clock = pygame.time.Clock()

    def draw_objects(self):
        self.screen.fill(self.BLACK)

        # Menggambar Paddle
        pygame.draw.rect(self.screen, self.WHITE,
                         (self.player1_x, self.player1_y,
                          self.paddle_width, self.paddle_height))
        pygame.draw.rect(self.screen, self.WHITE,
                         (self.player2_x, self.player2_y,
                          self.paddle_width, self.paddle_height))

        # Menggambar Bola
        pygame.draw.rect(self.screen, self.WHITE,
                         (self.ball_x, self.ball_y,
                          self.ball_size, self.ball_size))

        pygame.display.flip()

    def move_ball(self):
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Pantulan dinding atas/bawah
        if self.ball_y <= 0 or self.ball_y >= self.height - self.ball_size:
            self.ball_dy *= -1

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            # Kontrol Paddle
            if keys[pygame.K_w] and self.player1_y > 0:
                self.player1_y -= 5
            if keys[pygame.K_s] and self.player1_y < self.height - self.paddle_height:
                self.player1_y += 5

            if keys[pygame.K_UP] and self.player2_y > 0:
                self.player2_y -= 5
            if keys[pygame.K_DOWN] and self.player2_y < self.height - self.paddle_height:
                self.player2_y += 5

            self.move_ball()
            self.draw_objects()
            self.clock.tick(60)

        pygame.quit()


# Menjalankan Game
if __name__ == "__main__":
    game = PongGame()
    game.run()