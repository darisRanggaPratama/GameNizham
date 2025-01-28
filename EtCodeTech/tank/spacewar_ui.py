# spacewar_ui.py
import pygame


class GameUI:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.SysFont(None, 36)
        self.large_font = pygame.font.SysFont(None, 72)

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

    def format_time(self, milliseconds):
        """Convert milliseconds to MM:SS format"""
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def draw_game_stats(self, player, start_time, current_time):
        """Draw in-game statistics including health, score, shots fired and elapsed time"""
        elapsed_time = current_time - start_time

        # Render text surfaces
        health_text = self.font.render(f"Health: {player.health}", True, self.RED)
        score_text = self.font.render(f"Score: {player.score}", True, self.WHITE)
        shots_text = self.font.render(f"Shots Fired: {player.shots_fired}", True, self.BLUE)
        time_text = self.font.render(f"Time: {self.format_time(elapsed_time)}", True, self.WHITE)

        # Position and draw text
        self.screen.blit(health_text, (20, 20))
        self.screen.blit(score_text, (20, 60))
        self.screen.blit(shots_text, (20, 100))
        self.screen.blit(time_text, (20, 140))

    def show_game_over(self, player, start_time, end_time):
        """Display game over screen with final statistics"""
        self.screen.fill(self.BLACK)

        # Calculate total play time
        total_time = end_time - start_time
        time_str = self.format_time(total_time)

        # Determine game outcome
        if player.health <= 0:
            main_text = "Game Over! You Lost!"
            color = self.RED
        else:  # score >= 100
            main_text = "Congratulations! You Won!"
            color = self.GREEN

        # Render all text surfaces
        game_over_text = self.large_font.render(main_text, True, color)
        final_score_text = self.font.render(f"Final Score: {player.score}", True, self.WHITE)
        shots_fired_text = self.font.render(f"Total Shots: {player.shots_fired}", True, self.WHITE)
        time_text = self.font.render(f"Total Time: {time_str}", True, self.WHITE)
        restart_text = self.font.render("Game will restart in 3 seconds...", True, self.WHITE)

        # Calculate positions (centered horizontally)
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        game_over_pos = ((screen_width - game_over_text.get_width()) // 2,
                         screen_height // 2 - 100)
        score_pos = ((screen_width - final_score_text.get_width()) // 2,
                     game_over_pos[1] + 80)
        shots_pos = ((screen_width - shots_fired_text.get_width()) // 2,
                     score_pos[1] + 40)
        time_pos = ((screen_width - time_text.get_width()) // 2,
                    shots_pos[1] + 40)
        restart_pos = ((screen_width - restart_text.get_width()) // 2,
                       time_pos[1] + 80)

        # Draw all text elements
        self.screen.blit(game_over_text, game_over_pos)
        self.screen.blit(final_score_text, score_pos)
        self.screen.blit(shots_fired_text, shots_pos)
        self.screen.blit(time_text, time_pos)
        self.screen.blit(restart_text, restart_pos)

        # Update display
        pygame.display.flip()
