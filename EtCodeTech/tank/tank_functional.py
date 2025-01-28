import math
import random
import sys
from dataclasses import dataclass
from typing import Tuple, Dict, List

import pygame as pg

# Configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TANK_SPEED = 5
BULLET_SPEED = 10


@dataclass
class Position:
    x: float
    y: float


@dataclass
class GameState:
    tank1_pos: Position
    tank2_pos: Position
    tank1_health: int
    tank2_health: int
    tank1_score: int
    tank2_score: int
    bullets: List[dict]
    game_over: bool


def create_initial_state() -> GameState:
    """Create the initial game state"""
    return GameState(
        tank1_pos=Position(50, SCREEN_HEIGHT - 100),
        tank2_pos=Position(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100),
        tank1_health=100,
        tank2_health=100,
        tank1_score=0,
        tank2_score=0,
        bullets=[],
        game_over=False
    )


def load_assets() -> Dict:
    """Load game assets"""
    return {
        'background': pg.transform.scale(
            pg.image.load("assets/background.jpeg"),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        ),
        'tank1': pg.image.load("assets/tanker64.png").convert_alpha(),
        'tank2': pg.image.load("assets/tankers64.png").convert_alpha(),
        'move_sound': pg.mixer.Sound("assets/tank-engine.mp3"),
        'shoot_sound': pg.mixer.Sound("assets/tank-shots.mp3"),
        'explosion_sound': pg.mixer.Sound("assets/tank-hits.mp3")
    }


def create_bullet(pos: Position, direction: int) -> dict:
    """Create a new bullet with the given position and direction"""
    return {
        'pos': Position(
            pos.x + (64 if direction == 1 else 0),
            pos.y + 32
        ),
        'direction': direction,
        'color': (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    }


def update_bullet_position(bullet: dict) -> dict:
    """Update bullet position based on its direction"""
    return {
        **bullet,
        'pos': Position(
            bullet['pos'].x + (BULLET_SPEED * bullet['direction']),
            bullet['pos'].y
        )
    }


def update_bullet_color(bullet: dict, frame: int) -> dict:
    """Update bullet color for glow effect"""
    intensity = abs(math.sin(frame / 10)) * 200 + 55
    return {
        **bullet,
        'color': (int(intensity), random.randint(50, 255), random.randint(50, 255))
    }


def clamp_position(pos: Position) -> Position:
    """Clamp position within screen boundaries"""
    return Position(
        max(0, min(pos.x, SCREEN_WIDTH - 64)),
        max(0, min(pos.y, SCREEN_HEIGHT - 64))
    )


def update_tank_positions(tank1_pos: Position, tank2_pos: Position, keys: List[bool]) -> Tuple[Position, Position]:
    """Update tank positions based on keyboard input"""
    new_tank1_pos = Position(tank1_pos.x, tank1_pos.y)
    new_tank2_pos = Position(tank2_pos.x, tank2_pos.y)

    # Tank 1 movement (WASD)
    if keys[pg.K_a]:
        new_tank1_pos = Position(new_tank1_pos.x - TANK_SPEED, new_tank1_pos.y)
    if keys[pg.K_d]:
        new_tank1_pos = Position(new_tank1_pos.x + TANK_SPEED, new_tank1_pos.y)
    if keys[pg.K_w]:
        new_tank1_pos = Position(new_tank1_pos.x, new_tank1_pos.y - TANK_SPEED)
    if keys[pg.K_s]:
        new_tank1_pos = Position(new_tank1_pos.x, new_tank1_pos.y + TANK_SPEED)

    # Tank 2 movement (Arrow keys)
    if keys[pg.K_LEFT]:
        new_tank2_pos = Position(new_tank2_pos.x - TANK_SPEED, new_tank2_pos.y)
    if keys[pg.K_RIGHT]:
        new_tank2_pos = Position(new_tank2_pos.x + TANK_SPEED, new_tank2_pos.y)
    if keys[pg.K_UP]:
        new_tank2_pos = Position(new_tank2_pos.x, new_tank2_pos.y - TANK_SPEED)
    if keys[pg.K_DOWN]:
        new_tank2_pos = Position(new_tank2_pos.x, new_tank2_pos.y + TANK_SPEED)

    return clamp_position(new_tank1_pos), clamp_position(new_tank2_pos)


def check_collision(bullet_pos: Position, tank_pos: Position) -> bool:
    """Check if bullet collides with tank"""
    bullet_rect = pg.Rect(bullet_pos.x, bullet_pos.y, 10, 10)
    tank_rect = pg.Rect(tank_pos.x, tank_pos.y, 64, 64)
    return bullet_rect.colliderect(tank_rect)


def update_game_state(state: GameState, keys: List[bool], frame: int) -> GameState:
    """Update game state based on inputs and current frame"""
    if state.game_over:
        return state

    # Update tank positions
    new_tank1_pos, new_tank2_pos = update_tank_positions(state.tank1_pos, state.tank2_pos, keys)

    # Update bullets
    new_bullets = []
    new_tank1_health = state.tank1_health
    new_tank2_health = state.tank2_health
    new_tank1_score = state.tank1_score
    new_tank2_score = state.tank2_score

    for bullet in state.bullets:
        updated_bullet = update_bullet_position(update_bullet_color(bullet, frame))

        # Check collisions
        if bullet['direction'] > 0:
            if check_collision(updated_bullet['pos'], state.tank2_pos):
                new_tank2_health -= 20
                new_tank1_score += 1
                continue
        else:
            if check_collision(updated_bullet['pos'], state.tank1_pos):
                new_tank1_health -= 20
                new_tank2_score += 1
                continue

        # Keep bullet if still on screen
        if (0 < updated_bullet['pos'].x < SCREEN_WIDTH):
            new_bullets.append(updated_bullet)

    # Check game over condition
    game_over = new_tank1_health <= 0 or new_tank2_health <= 0

    return GameState(
        tank1_pos=new_tank1_pos,
        tank2_pos=new_tank2_pos,
        tank1_health=new_tank1_health,
        tank2_health=new_tank2_health,
        tank1_score=new_tank1_score,
        tank2_score=new_tank2_score,
        bullets=new_bullets,
        game_over=game_over
    )


def render_game(screen: pg.Surface, state: GameState, assets: Dict):
    """Render the current game state"""
    # Draw background
    screen.blit(assets['background'], (0, 0))

    # Draw tanks
    screen.blit(assets['tank1'], (state.tank1_pos.x, state.tank1_pos.y))
    screen.blit(assets['tank2'], (state.tank2_pos.x, state.tank2_pos.y))

    # Draw bullets
    for bullet in state.bullets:
        pg.draw.circle(screen, bullet['color'],
                       (int(bullet['pos'].x), int(bullet['pos'].y)), 5)
        # Draw glow effect
        glow_surface = pg.Surface((30, 30), pg.SRCALPHA)
        pg.draw.circle(glow_surface, (*bullet['color'], 100), (15, 15), 15)
        screen.blit(glow_surface, (int(bullet['pos'].x - 15), int(bullet['pos'].y - 15)))

    # Draw HUD
    font = pg.font.Font(None, 36)
    tank1_stats = font.render(f"Tank 1: {state.tank1_health}% | Score: {state.tank1_score}", True, (0, 0, 0))
    tank2_stats = font.render(f"Tank 2: {state.tank2_health}% | Score: {state.tank2_score}", True, (0, 0, 0))
    screen.blit(tank1_stats, (10, 10))
    screen.blit(tank2_stats, (SCREEN_WIDTH - 300, 10))

    if state.game_over:
        winner = "Tank 1 Wins!" if state.tank2_health <= 0 else "Tank 2 Wins!"
        game_over_text = font.render(winner, True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

    pg.display.flip()


def main():
    pg.init()
    pg.mixer.init()

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Tank Battle")
    clock = pg.time.Clock()

    try:
        assets = load_assets()
        pg.mixer.music.load("assets/adventure.mp3")
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)
    except FileNotFoundError as e:
        print(f"Error loading assets: {e}")
        return

    state = create_initial_state()
    running = True

    while running:
        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and not state.game_over:
                if event.key == pg.K_SPACE:
                    assets['shoot_sound'].play()
                    new_bullet = create_bullet(state.tank1_pos, 1)
                    state = GameState(**{**state.__dict__,
                                         'bullets': state.bullets + [new_bullet]})
                elif event.key == pg.K_RETURN:
                    assets['shoot_sound'].play()
                    new_bullet = create_bullet(state.tank2_pos, -1)
                    state = GameState(**{**state.__dict__,
                                         'bullets': state.bullets + [new_bullet]})

        # Get current keyboard state and update game
        keys = pg.key.get_pressed()
        frame = pg.time.get_ticks() // 50
        state = update_game_state(state, keys, frame)

        # Render
        render_game(screen, state, assets)

        # Reset game if game over
        if state.game_over:
            pg.mixer.music.stop()
            assets['shoot_sound'].stop()
            assets['explosion_sound'].stop()
            pg.time.delay(3000)
            state = create_initial_state()
            pg.mixer.music.play(-1)

        clock.tick(60)

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
