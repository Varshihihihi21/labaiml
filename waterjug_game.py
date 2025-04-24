import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 149, 255, 180)
DARK_BLUE = (0, 100, 200)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (100, 100, 100)
METALLIC = (192, 192, 192)
METALLIC_DARK = (128, 128, 128)
GOLD = (255, 215, 0)
PASTEL_GREEN = (119, 221, 119)

class WaterJug:
    def __init__(self, x, y, capacity, width, height):
        self.x = x
        self.y = y
        self.capacity = capacity
        self.current = 0
        self.width = width
        self.height = height
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.rect = pygame.Rect(x, y, width, height)
        self.water_particles = []

    def draw(self, screen):
        # Calculate water height once at the beginning
        water_height = (self.current / self.capacity) * (self.height - 20)
        
        # Determine outline color based on water level
        outline_color = BLUE if water_height > 0 else WHITE
        
        # Draw jug body with curved bottom and shading
        # Main body shadow
        pygame.draw.rect(screen, DARK_GRAY, (self.x + 3, self.y + 3, self.width, self.height - 20))
        pygame.draw.ellipse(screen, DARK_GRAY, (self.x + 3, self.y + self.height - 17, self.width, 40))
        
        # Main body highlight
        pygame.draw.rect(screen, LIGHT_GRAY, (self.x, self.y, self.width - 3, self.height - 20))
        pygame.draw.ellipse(screen, LIGHT_GRAY, (self.x, self.y + self.height - 20, self.width - 3, 40))
        
        # Jug outline
        pygame.draw.rect(screen, outline_color, (self.x, self.y, self.width, self.height - 20), 3)
        pygame.draw.ellipse(screen, outline_color, (self.x, self.y + self.height - 20, self.width, 40), 3)
        
        # Draw handle with shading
        handle_width = 25
        pygame.draw.arc(screen, DARK_GRAY, (self.x + self.width + 3, self.y + 43, handle_width, 60), -1.57, 1.57, 5)
        pygame.draw.arc(screen, WHITE, (self.x + self.width, self.y + 40, handle_width, 60), -1.57, 1.57, 3)
        
        # Draw spout with shading
        spout_points = [
            (self.x + self.width - 20, self.y + 20),
            (self.x + self.width + 15, self.y),
            (self.x + self.width + 15, self.y + 30)
        ]
        shadow_points = [(x + 3, y + 3) for x, y in spout_points]
        pygame.draw.polygon(screen, DARK_GRAY, shadow_points)
        pygame.draw.polygon(screen, LIGHT_GRAY, spout_points)
        pygame.draw.polygon(screen, WHITE, spout_points, 3)
        
        # Draw water with shading and curved bottom
        if water_height > 0:
            # Water shadow
            shadow_rect = pygame.Rect(
                self.x + 3,
                self.y + self.height - 17 - water_height,
                self.width,
                water_height
            )
            pygame.draw.rect(screen, DARK_BLUE, shadow_rect)
            
            # Main water body
            water_rect = pygame.Rect(
                self.x,
                self.y + self.height - 20 - water_height,
                self.width - 3,
                water_height
            )
            pygame.draw.rect(screen, BLUE, water_rect)
            
            # Curved water bottom
            water_bottom = pygame.Rect(self.x, self.y + self.height - 20, self.width, 40)
            pygame.draw.ellipse(screen, BLUE, water_bottom)
                
        # Draw water particles with glow effect
        for particle in self.water_particles:
            pygame.draw.circle(screen, DARK_BLUE, (int(particle[0] + 2), int(particle[1] + 2)), 3)
            pygame.draw.circle(screen, BLUE, (int(particle[0]), int(particle[1])), 2)

    def update_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class WaterSource:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 120
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.water_particles = []

    def draw(self, screen):
        # Draw main tap body
        pygame.draw.rect(screen, METALLIC, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, METALLIC_DARK, (self.x, self.y, self.width, self.height), 2)
        
        # Draw tap handle
        handle_width = 30
        handle_height = 15
        pygame.draw.rect(screen, METALLIC, (self.x - handle_width + 10, self.y + 20, handle_width, handle_height))
        pygame.draw.rect(screen, METALLIC_DARK, (self.x - handle_width + 10, self.y + 20, handle_width, handle_height), 2)
        
        # Draw spout
        spout_points = [
            (self.x + self.width, self.y + self.height - 40),
            (self.x + self.width + 15, self.y + self.height - 40),
            (self.x + self.width + 15, self.y + self.height - 20)
        ]
        pygame.draw.polygon(screen, METALLIC, spout_points)
        pygame.draw.polygon(screen, METALLIC_DARK, spout_points, 2)

class Drain:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 30
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, screen):
        # Draw main drain body
        pygame.draw.rect(screen, METALLIC, self.rect)
        pygame.draw.rect(screen, METALLIC_DARK, self.rect, 2)
        
        # Draw grate lines
        for i in range(5):
            x_pos = self.x + (i + 1) * (self.width / 6)
            pygame.draw.line(screen, METALLIC_DARK, (x_pos, self.y), (x_pos, self.y + self.height), 2)
            
        # Draw horizontal grate lines
        for i in range(2):
            y_pos = self.y + (i + 1) * (self.height / 3)
            pygame.draw.line(screen, METALLIC_DARK, (self.x, y_pos), (self.x + self.width, y_pos), 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Water Jug Puzzle")
        self.clock = pygame.time.Clock()

        # Create game objects
        self.jug1 = WaterJug(300, 400, 3, 100, 160)  # 3L jug
        self.jug2 = WaterJug(600, 400, 5, 120, 200)  # 5L jug
        self.water_source = WaterSource(100, 300)  # Moved to left side
        self.drain = Drain(800, 600)  # Moved to bottom right

        self.selected_jug = None
        self.font = pygame.font.Font(None, 36)
        self.has_won = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if clicked on either jug
                for jug in [self.jug1, self.jug2]:
                    if jug.rect.collidepoint(mouse_pos):
                        self.selected_jug = jug
                        jug.dragging = True
                        jug.drag_offset_x = jug.x - mouse_pos[0]
                        jug.drag_offset_y = jug.y - mouse_pos[1]

            if event.type == pygame.MOUSEBUTTONUP:
                if self.selected_jug:
                    # Check if jug is over water source
                    if self.water_source.rect.colliderect(self.selected_jug.rect):
                        self.selected_jug.current = self.selected_jug.capacity
                    
                    # Check if jug is over drain
                    if self.drain.rect.colliderect(self.selected_jug.rect):
                        self.selected_jug.current = 0

                    # Check if jugs are close to each other for transfer
                    if self.jug1.rect.colliderect(self.jug2.rect):
                        if self.selected_jug == self.jug1:
                            self.transfer_water(self.jug1, self.jug2)
                        else:
                            self.transfer_water(self.jug2, self.jug1)

                    self.selected_jug.dragging = False
                    self.selected_jug = None

            if event.type == pygame.MOUSEMOTION:
                if self.selected_jug and self.selected_jug.dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    self.selected_jug.update_position(
                        mouse_pos[0] + self.selected_jug.drag_offset_x,
                        mouse_pos[1] + self.selected_jug.drag_offset_y
                    )

        return True

    def transfer_water(self, from_jug, to_jug):
        space_available = to_jug.capacity - to_jug.current
        amount_to_transfer = min(from_jug.current, space_available)
        from_jug.current -= amount_to_transfer
        to_jug.current += amount_to_transfer
        self.check_win_condition()

    def check_win_condition(self):
        if self.jug1.current == 4 or self.jug2.current == 4:
            self.has_won = True

    def draw(self):
        self.screen.fill((110, 142, 251))  # Background color

        # Draw game objects
        self.water_source.draw(self.screen)
        self.drain.draw(self.screen)
        self.jug1.draw(self.screen)
        self.jug2.draw(self.screen)

        # Draw jug labels and current volumes
        jug1_text = self.font.render(f"{self.jug1.current}L / {self.jug1.capacity}L", True, WHITE)
        jug2_text = self.font.render(f"{self.jug2.current}L / {self.jug2.capacity}L", True, WHITE)
        self.screen.blit(jug1_text, (self.jug1.x, self.jug1.y - 30))
        self.screen.blit(jug2_text, (self.jug2.x, self.jug2.y - 30))

        # Draw goal text
        goal_text = self.font.render("Goal: Measure 4 liters of water", True, WHITE)
        self.screen.blit(goal_text, (WINDOW_WIDTH//2 - 150, 30))

        # Draw victory message if won
        if self.has_won:
            # Create gradient background for victory message
            gradient_surface = pygame.Surface((400, 100))
            for i in range(100):
                alpha = 255 - (i * 2)
                if alpha < 0: alpha = 0
                color = (*PASTEL_GREEN[:3], alpha)
                pygame.draw.rect(gradient_surface, color, (0, i, 400, 1))
            
            victory_font = pygame.font.Font(None, 72)
            victory_text = victory_font.render("Congratulations! You Won!", True, GOLD)
            text_rect = victory_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            
            # Draw gradient background
            gradient_rect = gradient_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            gradient_surface.set_alpha(180)
            self.screen.blit(gradient_surface, gradient_rect)
            
            # Draw text with golden color
            self.screen.blit(victory_text, text_rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        return True

if __name__ == "__main__":
    game = Game()
    game.run()