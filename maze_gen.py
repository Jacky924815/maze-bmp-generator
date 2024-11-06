import cv2
import numpy as np
import random
from PIL import Image

class MazeGenerator:
    def __init__(self, row, column):
        self.__row = row
        self.__column = column
        
        self.__maze = np.zeros((row, column), dtype='uint8')
        
    
    def reset(self):
        self.__maze[:,:] = 0;
        
        
    def __check_x_bound(self, x):
        return x >= 0 and x < self.__row
    
    
    def __check_y_bound(self, y):
        return y >= 0 and y < self.__column
    
    
    def generate(self):
        DIR_VECTOR = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        visited = np.zeros((self.__row, self.__column), dtype='bool')
        queue = [(0, 0)]
        
        self.reset()
        
        while not queue == []:
            x, y = queue.pop(0)
            visited[x][y] = True
            
            check_pass = False            
            while not check_pass:
                self.__maze[x][y] = random.randint(1,15)
                
                # close up
                if x == 0:
                    self.__maze[x][y] &= 0x0B
                # close down
                elif x == self.__row-1:
                    self.__maze[x][y] &= 0x07
                    
                # close left
                if y == 0:
                    self.__maze[x][y] &= 0x0E
                # close right
                elif y == self.__column-1:
                    self.__maze[x][y] &= 0x0D
                    
                # check if at least 1 direction is open
                if self.__maze[x][y] != 0x00:
                    check_pass = True
            
                
            for i in range(4):
                dx, dy = DIR_VECTOR[i]
                if not self.__check_x_bound(x+dx) or not self.__check_y_bound(y+dy):
                    continue
                if visited[x+dx][y+dy]:
                    # checked connection
                    # open if should connect
                    connected = (self.__maze[x+dx][y+dy] >> (i//2*2+(1-i%2)) & 0x01 == 0x01)
                    if connected:
                        if i == 0:
                            self.__maze[x][y] |= 0x01
                        elif i == 1:
                            self.__maze[x][y] |= 0x02
                        elif i == 2:
                            self.__maze[x][y] |= 0x04
                        elif i == 3:
                            self.__maze[x][y] |= 0x08
                    # close if need
                    else:
                        if i == 0:
                            self.__maze[x][y] &= 0x0E
                        elif i == 1:
                            self.__maze[x][y] &= 0x0D
                        elif i == 2:
                            self.__maze[x][y] &= 0x0B
                        elif i == 3:
                            self.__maze[x][y] &= 0x07
                else:
                    if (self.__maze[x][y] >> i & 0x01) == 0x01 and (x+dx, y+dy) not in queue:
                        queue.append((x+dx, y+dy))
                    
        # check the maze can be slove (start (0,0), goal (r-1, c-1))
        # 1. maze[0][0] and maze[r-1][c-1] are not 0
        # 2. number of non-0 grather than 90%
        count = np.count_nonzero(self.__maze)
        if not (count / (self.__row * self.__column) >= 0.9 and 
                self.__maze[0][0] != 0 and
                self.__maze[self.__row-1][self.__column-1] != 0):
            self.generate()
        else:
            self.__maze[0][0] |= 0x01
            self.__maze[self.__row-1][self.__column-1] |= 0x02


    def print_maze(self):
        print(self.__maze)
        
        
    def make_bmp(self):
        bmp = np.zeros((8*self.__row, 8*self.__column), dtype='uint8')
        
        for x in range(self.__row):
            for y in range(self.__column):
                if self.__maze[x][y] != 0x00:
                    bmp[x*8+1:x*8+7, y*8+1:y*8+7] = 0xFF
                    
                    if self.__maze[x][y] & 0x01 == 0x01:
                        bmp[x*8+1:x*8+7, y*8] = 0xFF
                        
                    if self.__maze[x][y] & 0x02 == 0x02:
                        bmp[x*8+1:x*8+7, y*8+7] = 0xFF
                        
                    if self.__maze[x][y] & 0x04 == 0x04:
                        bmp[x*8, y*8+1:y*8+7] = 0xFF
                        
                    if self.__maze[x][y] & 0x08 == 0x08:
                        bmp[x*8+7, y*8+1:y*8+7] = 0xFF
        
        return bmp
    
    
    def show_maze(self, title='maze'):
        bmp = self.make_bmp()
        cv2.imshow(title, bmp)
        cv2.waitKey(0)
        
        
    def save_bmp(self, title='maze'):
        bmp = self.make_bmp()
        bmp = Image.fromarray(bmp)
        bmp = bmp.convert('1')
        bmp.save(f'output/image/{title}.bmp', format='BMP')

    
    def save_text(self, title='maze'):
        with open(f'output/data/{title}.txt', 'w') as f:
            for i in range(self.__row):
                for j in range(self.__column):
                    f.write(hex(self.__maze[i][j]).upper()[-1])
                f.write('\n')
                
    
        
if __name__ == '__main__':
    maze_gen = MazeGenerator(8, 16)
    
    for i in range(1, 63):
        maze_gen.generate()
        maze_gen.save_bmp(f'maze-{i}')
        maze_gen.save_text(f'maze-{i}')
