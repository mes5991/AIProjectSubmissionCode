import xlrd
import numpy as np
import pygame
file_location = 'C:/Users/Matthew/Documents/WPI/Spring 16/AI/Project/AI-Project/map.xlsx'
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)
data=[]
data=np.zeros((100,100))
for col in range (sheet.ncols):
        for row in range (sheet.nrows):
            data[row,col]=int(sheet.cell_value(row,col))
print(data)

print(data)
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()

# Set the width and height of the screen [width, height]
M = 1000
size = (M, M)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("World Map")
done = False
k = 1

# set the scaling factor based on screen size
z = M/100

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
screen.fill(BLACK)

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True# Flag that we are done so we exit this loop
    while k == 1:
        # Drawing code
        for i in range(100):
            for j in range(100):
                if data[i,j] == 1.0:
                    m = i * z
                    n = j * z
                    pygame.draw.rect(screen, BLACK, [m, n, z, z])
                elif data[i,j] == 2.0:
                    m = i * z
                    n = j * z
                    pygame.draw.rect(screen, GREEN, [m, n, 50, 50])
                else:
                    m = i * z
                    n = j * z
                    pygame.draw.rect(screen, WHITE, [m, n, z, z])
        k = 0
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
