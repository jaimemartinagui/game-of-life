"""
                               --------------
                              | Game of Life |
                               --------------

    - A dead cell with exactly 3 living neighboring cells is born.
    - A living cell with 2 or 3 living neighboring cells is still alive, otherwise it dies.
"""

import time
from math import floor

import pygame
import numpy as np

from game_variables import game_variables


class GameOfLife:
    """Class for the game. The main funtion is run_game_of_life()."""

    def __init__(self, board_size, bg_color, n_cells_x, n_cells_y, time_frame):

        # Board configuration
        self.board_size = board_size
        self.bg_color = bg_color

        # Number of horizontal and vertical cells
        self.n_cells_x, self.n_cells_y = n_cells_x, n_cells_y

        # Size of each cell
        self.size_x = (self.board_size[0] - 1) / self.n_cells_x
        self.size_y = (self.board_size[1] - 1) / self.n_cells_y

        self.time_frame = time_frame

    def run_game_of_life(self):
        """Main function to run the game."""

        pygame.init()
        # Initialize the board
        screen = pygame.display.set_mode(self.board_size, pygame.RESIZABLE)
        game_state = np.zeros((self.n_cells_x, self.n_cells_y))
        pause = True
        while True:
            new_game_state = np.copy(game_state)
            # Mouse and keyboard events
            pause, new_game_state = self._interaction(pause, new_game_state)
            # Clear the board to draw the new state of the game
            screen.fill(self.bg_color)
            for y in range(0, self.n_cells_y):
                for x in range(0, self.n_cells_x):
                    if not pause:
                        n_alive_neighs = self._count_alive_neighs(game_state, x, y)
                        # A dead cell with exactly 3 living neighboring cells is born
                        if game_state[x, y] == 0 and n_alive_neighs == 3:
                            new_game_state[x, y] = 1
                        # A living cell with 2 or 3 living neighbors will survive, otherwise it dies
                        if game_state[x, y] == 1 and n_alive_neighs not in [2, 3]:
                            new_game_state[x, y] = 0
                    vertices = self._generate_vertices(x, y)
                    # Draw black (dead) or white (alive) cells
                    pygame.draw.polygon(screen, (255, 255, 255), vertices, int(1-new_game_state[x, y]))
            # Update the game status
            game_state = new_game_state
            time.sleep(self.time_frame)
            pygame.display.flip()
        pygame.quit()

    def _interaction(self, pause, new_game_state):
        """Interact with the game via mouse or keyboard."""

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                pause = not pause
            mouse_click = pygame.mouse.get_pressed()
            if sum(mouse_click) > 0:
                pos_x, pos_y = pygame.mouse.get_pos()
                if 0 < pos_x < self.board_size[0]-1 and 0 < pos_y < self.board_size[1]-1:
                    cell_x = floor(pos_x/self.size_x)
                    cell_y = floor(pos_y/self.size_y)
                    new_game_state[cell_x, cell_y] = mouse_click[0] and not mouse_click[2]
        return pause, new_game_state

    def _count_alive_neighs(self, game_state, x, y):
        """Count the number of alive neighbors for a given position and game state."""

        n_alive_neighs = sum([game_state[(x-1) % self.n_cells_x, (y-1) % self.n_cells_y],
                              game_state[(x)   % self.n_cells_x, (y-1) % self.n_cells_y],
                              game_state[(x+1) % self.n_cells_x, (y-1) % self.n_cells_y],
                              game_state[(x-1) % self.n_cells_x, (y)   % self.n_cells_y],
                              game_state[(x+1) % self.n_cells_x, (y)   % self.n_cells_y],
                              game_state[(x-1) % self.n_cells_x, (y+1) % self.n_cells_y],
                              game_state[(x)   % self.n_cells_x, (y+1) % self.n_cells_y],
                              game_state[(x+1) % self.n_cells_x, (y+1) % self.n_cells_y]])
        return n_alive_neighs

    def _generate_vertices(self, x, y):
        """Generate the vertices of a given position on the board."""

        vertices = [(x     * self.size_x, y     * self.size_y),
                    ((x+1) * self.size_x, y     * self.size_y),
                    ((x+1) * self.size_x, (y+1) * self.size_y),
                    (x     * self.size_x, (y+1) * self.size_y)]
        vertices = [tuple(map(int, v)) for v in vertices]
        return vertices


if __name__ == "__main__":

    GOL = GameOfLife(game_variables['board_size'],
                     game_variables['bg_color'],
                     game_variables['n_cells_x'],
                     game_variables['n_cells_y'],
                     game_variables['time_frame'])

    GOL.run_game_of_life()
