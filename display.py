import pygame
import math

class DetectDrowsy(object):
    def __init__(self, width=500, height=500):
        self.drowsy = False
        self.angle = 0
        self.auton = False
        self.width = width
        self.height = height
        self.frameRate = 5

    def timerFired(self):
        pass

    def redrawAll(self, screen):
        color = (0, 100, 100)
        pygame.draw.rect(screen, color, pygame.Rect(0, 0, self.width, self.height))

        path = "images/steering.png"
        image = pygame.transform.scale(pygame.image.load(path),(1024, 1024))  # rotate
        theta = self.angle * math.pi/180
        screen.blit(self.rot_center(image, self.angle),
            (self.width*.1,
            self.height*.2))
        """screen.blit(image,
            (self.width * .10 - ((724*math.sin(theta))/(math.sin((math.pi-theta)/2))*math.cos(math.pi/4)),
            self.height * .2 - ((724*math.sin(theta))/(math.sin((math.pi-theta)/2))*math.sin(math.pi/4))))"""

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_LEFT and self.angle < 60:
            self.angle += 5
        elif keyCode == pygame.K_RIGHT and self.angle > -60:
            self.angle -= 5

    def rot_center(self,image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    # def rot_center(image, rect, angle):
    #     """rotate an image while keeping its center"""
    #     rot_image = pygame.transform.rotate(image, angle)
    #     rot_rect = rot_image.get_rect(center=rect.center)
    #     return rot_image,rot_rect

    def mousePressed(self, x, y):
        pass

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        self.done = False
        while not self.done:
            time = clock.tick(self.frameRate)
            self.timerFired()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousePressed(*(event.pos))
                self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()

def main():
    drive = DetectDrowsy(1600, 1000)
    drive.run()

if __name__ == '__main__':
    main()
