import pygame
import sys

# Inisialisasi pygame
pygame.init()

# Konstanta untuk ukuran jendela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visualisasi Bangun Ruang")

# Warna
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


# Class Dasar
class Shape:
    def __init__(self, color):
        self.color = color

    def area(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def perimeter(self):
        raise NotImplementedError("Subclass must implement abstract method")


# Class Turunan
class Square(Shape):
    def __init__(self, side, color):
        super().__init__(color)
        self.side = side

    def area(self):
        return self.side ** 2

    def perimeter(self):
        return 4 * self.side


class Rectangle(Shape):
    def __init__(self, width, height, color):
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, base, height, color):
        super().__init__(color)
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

    def perimeter(self):
        # Asumsi segitiga sama sisi untuk kesederhanaan
        return 3 * self.base


class Circle(Shape):
    def __init__(self, radius, color):
        super().__init__(color)
        self.radius = radius

    def area(self):
        return 3.14 * (self.radius ** 2)

    def perimeter(self):
        return 2 * 3.14 * self.radius


# Fungsi untuk menggambar bangun ruang
def draw_shapes(shapes):
    screen.fill(WHITE)
    y_offset = 50

    for shape in shapes:
        if isinstance(shape, Square):
            pygame.draw.rect(screen, shape.color, (100, y_offset, shape.side, shape.side))
            text = f"Square: Area={shape.area()}, Perimeter={shape.perimeter()}"
        elif isinstance(shape, Rectangle):
            pygame.draw.rect(screen, shape.color, (300, y_offset, shape.width, shape.height))
            text = f"Rectangle: Area={shape.area()}, Perimeter={shape.perimeter()}"
        elif isinstance(shape, Triangle):
            pygame.draw.polygon(screen, shape.color, [(400, y_offset + shape.height), (400 - shape.base // 2, y_offset),
                                                      (400 + shape.base // 2, y_offset)])
            text = f"Triangle: Area={shape.area()}, Perimeter={shape.perimeter()}"
        elif isinstance(shape, Circle):
            pygame.draw.circle(screen, shape.color, (600, y_offset + shape.radius), shape.radius)
            text = f"Circle: Area={shape.area()}, Perimeter={shape.perimeter()}"

        # Tampilkan teks
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (50, y_offset + 20))
        y_offset += 100

    pygame.display.flip()


# Contoh penggunaan
shapes = [
    Square(100, RED),
    Rectangle(150, 80, BLUE),
    Triangle(100, 80, GREEN),
    Circle(50, YELLOW)
]


# Loop utama
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_shapes(shapes)


# Menjalankan program
if __name__ == "__main__":
    main()
