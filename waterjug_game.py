import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 149, 255, 180)
DARK_BLUE = (0, 100, 200)
GRAY = (200, 200, 200)

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
        # Draw jug
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 3)
        
        # Draw water
        water_height = (self.current / self.capacity) * self.height
        if water_height > 0:
            water_rect = pygame.Rect(
                self.x, 
                self.y + self.height - water_height,
                self.width,
                water_height
            )
            pygame.draw.rect(screen, BLUE, water_rect)

        # Draw water particles
        for particle in self.water_particles:
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
        self.width = 60
        self.height = 40
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.water_particles = []

    def draw(self, screen):
        # Draw tap
        pygame.draw.rect(screen, WHITE, self.rect, 3)
        pygame.draw.rect(screen, WHITE, (self.x + 20, self.y + self.height, 20, 20))

class Drain:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        for i in range(4):
            pygame.draw.circle(screen, DARK_BLUE, 
                             (self.x + 20 * i + 10, self.y + 10), 5)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Water Jug Puzzle")
        self.clock = pygame.time.Clock()

        # Create game objects
        self.jug1 = WaterJug(200, 300, 3, 100, 160)  # 3L jug
        self.jug2 = WaterJug(500, 300, 5, 120, 200)  # 5L jug
        self.water_source = WaterSource(350, 100)
        self.drain = Drain(360, 500)

        self.selected_jug = None
        self.font = pygame.font.Font(None, 36)

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

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()