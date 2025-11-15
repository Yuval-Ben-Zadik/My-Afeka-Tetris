import pygame
import sys
import os
import random
from tetromino_data import tetromino_shapes



def generate_bag():
    shapes = tetromino_shapes[:]
    random.shuffle(shapes)
    return shapes


bag = []


def get_next_tetromino():
    global bag
    if not bag:
        bag = generate_bag()
    return bag.pop(0)




class Tetromino:
    def __init__(self, shape_data, cell_size, start_x, start_y=0):
        self.blocks = shape_data["name"]
        self.rotations = shape_data["rotations"]
        self.color = shape_data["color"]
        self.rotation_index = 0
        self.cell_size = cell_size
        self.x = start_x # Starting x position in grid
        self.y = start_y # Starting y position in grid
        self.blocks = self.rotations[self.rotation_index]

    def draw(self, surface):
        for bx, by in self.blocks:
            real_pos_x = (self.x + bx) * self.cell_size # מיקום אופקי בפיקסלים
            real_pos_y = (self.y + by) * self.cell_size # מיקום אנכי בפיקסלים
            rect = pygame.Rect(real_pos_x, real_pos_y, self.cell_size, self.cell_size)
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, (30, 30, 30), rect, 1)  # Draw border

    def rotate(self):
        self.rotation_index = (self.rotation_index + 1) % len(self.rotations)
        self.blocks = self.rotations[self.rotation_index]






class TetrisGameWindow:
    def __init__(self, window_x=100, window_y=100, player_name=None):
        self.player_name = player_name
        os.environ['SDL_VIDEO_WINDOW_POS'] = f'{window_x},{window_y}'  # Set the window position
        pygame.init()

        self.width = 800
        self.height = 810
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tetris Game")

        self.grid_size_name = load_grid_size_setting()
        if self.grid_size_name == "small":
            self.one_cell_size = 30
        else:  # Large
            self.one_cell_size = 45

        self.rows = self.height // self.one_cell_size
        self.columns = 630 // self.one_cell_size
        self.grid = [[None for _ in range(self.columns)] for _ in range(self.rows)]
       
        self.bg_color = (0, 0, 0)  # black background
        self.grid_color = (50, 50, 50)  # gray grid lines

        self.clock = pygame.time.Clock()
        self.running = True

        num_cols = self.width // self.one_cell_size
        start_x = (num_cols - 2) // 2  # Center the grid horizontally

        self.current_piece = Tetromino(get_next_tetromino(), self.one_cell_size, start_x=start_x)
        self.next_piece_data = get_next_tetromino()

        self.last_move_time = pygame.time.get_ticks()
        self.fall_delay = 1000  # 1000 milliseconds = 1 second

        self.move_left = False
        self.move_right = False
        self.soft_drop = False
        self.move_delay = 100  # תזוזה רגילה
        self.last_drop_time = pygame.time.get_ticks()
        self.last_move_time = pygame.time.get_ticks()

        self.initial_move_delay = 200  # דיליי ראשוני לתזוזה רציפה
        self.last_horizontal_move = pygame.time.get_ticks()
        self.left_first_press = True
        self.right_first_press = True

        self.score = 0
        self.show_multiplier = False
        self.multiplier_timer = 0

        self.x2_image = pygame.image.load("x2_bonus.png").convert_alpha()
        self.x2_image = pygame.transform.scale(self.x2_image, (230, 230))  # Scale the image to fit the window

        self.score_font = pygame.font.SysFont("Arial", 32, bold=True)

        self.game_over = False

        self.snap_image = pygame.image.load("snapping_image.jpg").convert_alpha()
        self.snap_image = pygame.transform.scale(self.snap_image, (160, 160))
        self.snap_sound = pygame.mixer.Sound("finger_snap-_sound.mp3")
        self.snap_visible = False
        self.snap_timer = 0

        pygame.mixer.init()
        pygame.mixer.music.load("background_music1.mp3")
        self.load_volume_setting()
        if self.load_mute_setting():
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.play(-1)  # Play the music in a loop

        self.level = 1
        self.level_name = {1: "Basic", 2: "Advanced", 3: "Expert"}
        self.level_thresholds = {2: 150, 3: 300}
        self._level_image = {
            1: pygame.image.load("thanos_level1.jpg").convert_alpha(),
            2: pygame.image.load("thanos_level2.jpg").convert_alpha(),
            3: pygame.image.load("thanos_level3.jpg").convert_alpha()
        }
        self.thanos_image_width = 160
        self.thanos_image_height = 160
        for lvl in self._level_image:
            self._level_image[lvl] = pygame.transform.scale(self._level_image[lvl], (self.thanos_image_width, self.thanos_image_height))







    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.current_piece.x -= 1
                    if self.check_collision(self.current_piece):
                        self.current_piece.x += 1
                    self.move_left = True
                    self.left_first_press = True
                    self.last_horizontal_move = pygame.time.get_ticks()

                elif event.key == pygame.K_RIGHT:
                    self.current_piece.x += 1
                    if self.check_collision(self.current_piece):
                        self.current_piece.x -= 1
                    self.move_right = True
                    self.right_first_press = True
                    self.last_horizontal_move = pygame.time.get_ticks()

                elif event.key == pygame.K_DOWN:
                    self.current_piece.y += 1
                    if self.check_collision(self.current_piece):
                        self.current_piece.y -= 1
                    self.soft_drop = True

                elif event.key == pygame.K_UP:
                    self.current_piece.rotate()
                    if self.check_collision(self.current_piece):
                        for _ in range(3):
                            self.current_piece.rotate()
                
                elif event.key == pygame.K_SPACE:
                    self.hard_drop()
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.move_left = False
                    self.left_first_press = False
                
                elif event.key == pygame.K_RIGHT:
                    self.move_right = False
                    self.right_first_press = False

                elif event.key == pygame.K_DOWN:
                    self.soft_drop = False






    def draw_grid(self):
        self.screen.fill(self.bg_color)

        for row in range(self.rows):
            for col in range(self.columns):
                rect = pygame.Rect(col * self.one_cell_size, row * self.one_cell_size, self.one_cell_size, self.one_cell_size)
            
                # draw a locked piece
                if self.grid[row][col]:
                    pygame.draw.rect(self.screen, self.grid[row][col], rect)
                pygame.draw.rect(self.screen, self.grid_color, rect, 1)  # draw grid lines

        # check if there is a current piece and draw it
        if self.current_piece:
            self.current_piece.draw(self.screen)

        if self.show_multiplier:
            if pygame.time.get_ticks() - self.multiplier_timer < 2000:  # Show for 2 seconds
                center_x = (self.width - self.x2_image.get_width()) // 2
                center_y = (self.height - self.x2_image.get_height()) // 2 - 100
                self.screen.blit(self.x2_image, (center_x, center_y))
        else:
            self.show_multiplier = False

        # Draw the score
        score_text = self.score_font.render(f"Score: {self.score} xp", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # Draw the next piece
        self.draw_next_piece()

        # Draw the level image
        self.draw_level_boxes()
        self.draw_thanos_by_level()

        # show the snap image
        if self.snap_visible:
            if pygame.time.get_ticks() - self.snap_timer < 2000:  # Show for 2 second
                snap_x = 635
                snap_y = 600
                self.screen.blit(self.snap_image, (snap_x, snap_y))
            else:
                self.snap_visible = False




    def draw_next_piece(self):
        font = pygame.font.SysFont("Arial", 24, bold=True)
        next_label = font.render("Next Piece:", True, (255, 255, 255))
        self.screen.blit(next_label, (660, 20))

        if self.next_piece_data:
            shape = self.next_piece_data["rotations"][0]
            color = self.next_piece_data["color"]

            for bx, by in shape:
                x = 660 + bx * self.one_cell_size
                y = 60 + by * self.one_cell_size
                rect = pygame.Rect(x, y, self.one_cell_size, self.one_cell_size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (30, 30, 30), rect, 1)

    

    def draw_level_boxes(self):
        base_x = 660
        base_y = 250
        box_width = 120
        box_height = 25
        spacing = 10
        font = pygame.font.SysFont("Arial", 24, bold=True)

        for i in range(3):
            rect_y = base_y + i * (box_height + spacing)
            rect = pygame.Rect(base_x, rect_y, box_width, box_height)
            level_number = 3- i

            if self.level == level_number:
                pygame.draw.rect(self.screen, (255, 165, 0), rect) # Draw orange box for current level
            else:
                pygame.draw.rect(self.screen, (0, 0, 0), rect) # Draw black box for other levels
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)  # Draw border
            
            label = self.level_name[level_number]
            text_surface = font.render(label, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

        


    def draw_thanos_by_level(self):
        x = 635
        y = 370
        self.screen.blit(self._level_image[self.level], (x, y))







    def calculations(self):
        current_time = pygame.time.get_ticks()

        # Handle horizontal movement
        if self.move_left:
            if self.left_first_press:
                if current_time - self.last_horizontal_move > self.initial_move_delay:
                    self.current_piece.x -= 1
                    if self.check_collision(self.current_piece):
                        self.current_piece.x += 1
                    self.last_horizontal_move = current_time
                    self.left_first_press = False
            elif current_time - self.last_horizontal_move > self.move_delay:
                self.current_piece.x -= 1
                if self.check_collision(self.current_piece):
                    self.current_piece.x += 1
                self.last_horizontal_move = current_time

        if self.move_right:
            if self.right_first_press:
                if current_time - self.last_horizontal_move > self.initial_move_delay:
                    self.current_piece.x += 1
                    if self.check_collision(self.current_piece):
                        self.current_piece.x -= 1
                    self.last_horizontal_move = current_time
                    self.right_first_press = False
            elif current_time - self.last_horizontal_move > self.move_delay:
                self.current_piece.x += 1
                if self.check_collision(self.current_piece):
                    self.current_piece.x -= 1
                self.last_horizontal_move = current_time

        # Soft drop
        if self.soft_drop:
            if current_time - self.last_move_time > self.move_delay // 2:
                self.current_piece.y += 1
                if self.check_collision(self.current_piece):
                    self.current_piece.y -= 1
                    self.lock_piece()
                self.last_move_time = current_time

        # Automatic fall
        if not self.soft_drop and current_time - self.last_drop_time > self.fall_delay:
            self.current_piece.y += 1
            if self.check_collision(self.current_piece):
                self.current_piece.y -= 1
                self.lock_piece()
            self.last_drop_time = current_time








    def check_collision(self, tetromino, dx=0, dy=0):
        for bx, by in tetromino.blocks:
            block_x  = tetromino.x + bx + dx
            block_y = tetromino.y + by + dy
            
            # Check if the block is out of bounds
            if block_x  < 0 or block_x  >= self.columns or block_y >= self.rows:
                return True
            
            # Check if the block collides with an existing block in the grid
            if block_y >= 0 and self.grid[block_y][block_x] is not None:
                return True
        
        return False
    



    def hard_drop(self):
        while not self.check_collision(self.current_piece, dy=1):
            self.current_piece.y += 1
        self.lock_piece()



    

    def lock_piece(self):
        for bx, by in self.current_piece.blocks:
            gx = self.current_piece.x + bx
            gy = self.current_piece.y + by
            if 0 <= gx < self.columns and 0 <= gy < self.rows:
                self.grid[gy][gx] = self.current_piece.color

        self.clear_lines()

        num_cols = self.width // self.one_cell_size
        start_x = (num_cols - 2) // 2
        self.current_piece = Tetromino(self.next_piece_data, self.one_cell_size, start_x=start_x)
        self.next_piece_data = get_next_tetromino()

        if self.check_collision(self.current_piece):
            self.game_over = True




    
    def clear_lines(self):
        new_grid = []
        lines_cleared = 0

        for row in self.grid:
            is_full = True
            for cell in row:
                if cell is None:
                    is_full = False
                    break

            if not is_full:
                new_grid.append(row)
            else:
                lines_cleared += 1
        
        for _ in range(lines_cleared):
            empty_row = [None for _ in range(self.columns)]
            new_grid.insert(0, empty_row)
        
        self.grid = new_grid

        if lines_cleared > 0:
            self.snap_sound.play()
            self.snap_visible = True
            self.snap_timer = pygame.time.get_ticks()

            if lines_cleared > 1:
                self.score += (10 * lines_cleared) * 2
                self.show_multiplier = True
                self.multiplier_timer = pygame.time.get_ticks()
            else:
                self.score += 10

        for lvl, threshold in sorted(self.level_thresholds.items()):
            if self.score >= threshold:
                self.level = lvl
        if self.level == 1:
            self.fall_delay = 800
        elif self.level == 2:
            self.fall_delay = 500
        elif self.level == 3:
            self.fall_delay = 200

    



    def display_game_over(self):
        game_over_font = pygame.font.SysFont("Arial", 64, bold=True)
        text1 = game_over_font.render("Game Over!", True, (255, 255, 255))
        text_rect1 = text1.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.screen.blit(text1, text_rect1)

        text2 = game_over_font.render(f"Your Score: {self.score}", True, (255, 255, 255))
        text_rect2 = text2.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(text2, text_rect2)




    def load_volume_setting(self):
        if os.path.exists("settings.txt"):
            with open("settings.txt", "r") as f:
                for line in f:
                    if line.startswith("volume="):
                        volume = int(line.strip().split("=")[1])
                        pygame.mixer.music.set_volume(volume / 100)
                        

    def load_mute_setting(self):
        if os.path.exists("settings.txt"):
            with open("settings.txt", "r") as f:
                for line in f:
                    if line.startswith("mute="):
                        return line.strip().split("=")[1].lower() == "true"
        return False
    


    def run(self):
        while self.running:
            if self.game_over:
                self.display_game_over()
                pygame.display.flip()
                pygame.time.wait(3000)
                if self.player_name:
                    with open("all_scores.txt", "a") as f:
                        f.write(f"{self.player_name}-{self.score}\n")
                self.running = False
            self.handle_events()
            self.calculations()
            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.mixer.music.stop()  # Stop the music when the game ends
        pygame.quit()


def load_grid_size_setting():
    if os.path.exists("settings.txt"):
        with open("settings.txt", "r") as f:
            for line in f:
                if line.startswith("grid_size="):
                    return line.strip().split("=")[1].lower()
    return "small"  # ברירת מחדל





if __name__ == "__main__":
    grid_size = load_grid_size_setting()
    game = TetrisGameWindow(grid_size_name=grid_size, mute_music=False, music_volume=1)
    game.run()