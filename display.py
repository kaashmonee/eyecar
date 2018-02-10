import pygame

class DetectDrowsy(object):
    def __init__(self, width=500, height=500):
        self.drowsy = False
        self.angle = 0
        self.auton = False

    def timerFired(self):
        pass

    def redrawAll(self, screen):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def run(self, server=None, serverMsg=None):
		pygame.init()
		clock = pygame.time.Clock()
		screen = pygame.display.set_mode((640,480),pygame.FULLSCREEN)
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
    drive = DetectDrowsy(width = 1200)
    game.run(server, serverMsg)

if __name__ == '__main__':
	main()
