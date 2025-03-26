import random
import pygame
from tkinter import messagebox
pygame.init()

class Paddle:
	def __init__(self, root, x, y):
		self.x = x
		self.y = y
		self.root = root
		self.vel = 10

	def update(self):
		pygame.draw.rect(self.root, (255, 255, 255), (self.x, self.y, 20, 140))

	def move_up(self):
		if self.y - self.vel >= 0:
			self.y -= self.vel

	def move_down(self):
		if self.y + self.vel <= 400:
			self.y += self.vel

	def returnRect(self):
		return pygame.Rect(self.x, self.y, 25, 145)

class Ball:
	def __init__(self, root):
		self.x = 485
		self.y = 270
		self.vel_x = 11
		self.vel_y = 10
		self.radius = 15
		self.root = root

	def update(self):
		pygame.draw.circle(self.root, (200, 200, 200), (self.x, self.y), self.radius)

	def move(self):
		self.x += self.vel_x
		self.y += self.vel_y

		if (self.y - self.radius <= 0) or (self.y + self.radius >= 540):
			self.vel_y *= -1

		if (self.x <= 0) or (self.x >= 970):
			self.reset()

	def collision(self, paddle):
		ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
		if ball_rect.colliderect(paddle.returnRect()):
			self.vel_x *= -1

	def reset(self):
		self.x, self.y = 485, 270 
		self.vel_x = random.choice([-1, 1]) * (10 + random.randint(-2, 2))
		self.vel_y = random.choice([-1, 1]) * (10 + random.randint(-2, 2))

def draw_center_line(window):
	for y in range(0, 540, 40): 
		if y % 60 == 0:
			pygame.draw.line(window, (255, 255, 255), (485, y), (485, y+40), 3) 

def main():
	window = pygame.display.set_mode((970, 540))
	pygame.display.set_caption("Python Ping Pong")
	font = pygame.font.SysFont('comicsans', 50)
	adminfont = pygame.font.SysFont('arial', 20)

	player_score = opponent_score = 0
	player = Paddle(window, 40, 190)
	opponent = Paddle(window, 900, 190)
	ball = Ball(window)

	opinion = messagebox.askquestion("Instructions", "Welcome to Python Ping Pong.\n\nYou control the left paddle, and face off against a smart AI.\nUse you arrow keys to move up or down. The first to score 10 points wins!\n\nDo you want to play?", icon='info')
	run = True if opinion == "yes" else False

	while run:
		window.fill((0, 0, 0))
		draw_center_line(window)
		pygame.time.delay(50)

		playertxt = font.render("Player", 1, (255, 255, 255))
		opponenttxt = font.render("AI", 1, (255, 255, 255))
		admintext = adminfont.render("Aditya VN Kadiyala", 1, (0, 255, 255))
		window.blit(playertxt, (230, 0))
		window.blit(opponenttxt, (640, 0))
		window.blit(admintext, (10, 510))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			player.move_up()
		if keys[pygame.K_DOWN]:
			player.move_down()

		ball.update()
		ball.move()
		ball.collision(player)
		ball.collision(opponent)

		if ball.x > 550:
			if ball.y < opponent.y + 15:
				opponent.move_up()
			elif ball.y > opponent.y + 15:
				opponent.move_down()

		if ball.x - ball.radius <= 0:
			opponent_score += 1
			ball.reset()

		if ball.x + ball.radius >= 970:
			player_score += 1
			ball.reset()

		if player_score == 10:
			neo_opinion = messagebox.askquestion("Message", "Congratualations! You won against the smart AI!\n\nDo you want to play again?", icon='info')
			if neo_opinion == "yes":
				player_score, opponent_score = 0, 0
				player = Paddle(window, 40, 190)
				opponent = Paddle(window, 900, 190)
				ball.reset()
			else:
   				pygame.quit()
   				return

		if opponent_score == 10:
			neo_opinion = messagebox.askquestion("Message", "Tough Luck! The Smart AI has won!\n\nDo you want to play again?", icon='info')
			if neo_opinion == "yes":
				player_score = opponent_score = 0
				player = Paddle(window, 40, 190)
				opponent = Paddle(window, 900, 190)
				ball.reset()
			else:
   				pygame.quit()
   				return

		player_text = font.render(str(player_score), 1, (255, 255, 0))
		opponent_text = font.render(str(opponent_score), 1, (255, 255, 0))
		window.blit(player_text, (290, 80))
		window.blit(opponent_text, (660, 80))

		player.update()
		opponent.update()

		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
	main()
