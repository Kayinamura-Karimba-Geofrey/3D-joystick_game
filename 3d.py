import serial, pygame, math, time
from pygame.locals import *

BT_PORT = "COM5"
BAUD_RATE = 9600

bt = serial.Serial(BT_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bluetooth 3D Control Demo")

cube_color = (0, 255, 0)
clock = pygame.time.Clock()

pitch = roll = 0

def draw_cube(surface, x, y, size, pitch, roll):
    cx, cy = x + size // 2, y + size // 2
    angle_x = math.radians(pitch)
    angle_y = math.radians(roll)

    offset_x = math.sin(angle_y) * 100
    offset_y = math.sin(angle_x) * 100

    pygame.draw.rect(surface, cube_color, (cx + offset_x - 50, cy + offset_y - 50, 100, 100))

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    line = bt.readline().decode('utf-8').strip()
    if line:
        try:
            pitch, roll = map(float, line.split(','))
        except ValueError:
            pass

    draw_cube(screen, 350, 250, 100, pitch, roll)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
bt.close()
