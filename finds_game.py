import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.width = 1024
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Find-S Algorithm Game")
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        
        # Game state
        self.hypothesis = ['?', '?', '?', '?', '?', '?']  # Initial hypothesis
        self.attributes = ['Sky', 'Temp', 'Humid', 'Wind', 'Water', 'Forecast']
        self.examples = []
        self.font = pygame.font.Font(None, 36)
        
    def draw_text(self, text, x, y, color=None):
        if color is None:
            color = self.BLACK
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)
    
    def update_hypothesis(self, example):
        if example['label']:  # Positive example
            for i in range(len(self.hypothesis)):
                if self.hypothesis[i] == '?':
                    self.hypothesis[i] = example['features'][i]
                elif self.hypothesis[i] != example['features'][i]:
                    self.hypothesis[i] = '?'
    
    def draw(self):
        self.screen.fill(self.WHITE)
        
        # Draw title
        self.draw_text("Find-S Algorithm Learning Game", 20, 20)
        
        # Draw current hypothesis
        self.draw_text("Current Hypothesis:", 20, 80)
        for i, (attr, val) in enumerate(zip(self.attributes, self.hypothesis)):
            self.draw_text(f"{attr}: {val}", 20, 120 + i * 40)
        
        # Draw examples
        self.draw_text("Training Examples:", 400, 80)
        for i, example in enumerate(self.examples[-5:]):  # Show last 5 examples
            color = self.GREEN if example['label'] else self.RED
            features_str = ", ".join(example['features'])
            self.draw_text(f"Example {len(self.examples)-4+i}: {features_str}", 
                          400, 120 + i * 40, color)
        
        # Draw instructions
        self.draw_text("Press SPACE to add positive example", 20, 500)
        self.draw_text("Press N to add negative example", 20, 540)
        self.draw_text("Press Q to quit", 20, 570)
        
        pygame.display.flip()
    
    def generate_random_example(self):
        import random
        sky = random.choice(['Sunny', 'Rainy', 'Cloudy'])
        temp = random.choice(['Warm', 'Cold'])
        humid = random.choice(['High', 'Normal'])
        wind = random.choice(['Strong', 'Weak'])
        water = random.choice(['Warm', 'Cold'])
        forecast = random.choice(['Same', 'Change'])
        return [sky, temp, humid, wind, water, forecast]
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_SPACE:  # Add positive example
                        example = {
                            'features': self.generate_random_example(),
                            'label': True
                        }
                        self.examples.append(example)
                        self.update_hypothesis(example)
                    elif event.key == pygame.K_n:  # Add negative example
                        example = {
                            'features': self.generate_random_example(),
                            'label': False
                        }
                        self.examples.append(example)
            
            self.draw()
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()