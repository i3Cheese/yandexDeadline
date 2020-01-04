import pygame
import os


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
size = (500, 500)
screen = pygame.display.set_mode(size)
screen.fill((100, 100, 100))

running = True
MOVEEVENT = 30
GOEVENT = 30

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
pygame.time.set_timer(GOEVENT, 15)
pygame.time.set_timer(MOVEEVENT, 100)


class Character(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.x = x
        self.y = y
        self.frames = 11
        self.vx = 0
        self.vy = 0

        self.direction = 1
        self.cur_frame = 0
        self.status = 'standing'
        self.images_standing = [[], [], [], []]
        self.images_walking = [[], [], [], []]
        print(self.images_standing)
        self.image = None
        # forward - 0, left - 1, back - 2, right - 3

        for direction in range(4):
            for number_file in range(11):
                name = ['data', 'character', 'standing', str(direction), f'{number_file + 1}.png']
                self.images_standing[direction].append(load_image('\\'.join(name), (0, 0, 0)))
        for direction in range(4):
            for number_file in range(11):
                name = ['data', 'character', 'walking', str(direction), f'{number_file + 1}.png']
                self.images_walking[direction].append(load_image('\\'.join(name), (0, 0, 0)))

        self.image = self.images_standing[0][self.cur_frame]
        self.rect = self.image.get_rect()

    def update(self):
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_LEFT] ^ keys[pygame.K_RIGHT]:
            self.status = 'walking'
            self.direction = 1 if keys[pygame.K_LEFT] else 3
            self.vx = -10 if keys[pygame.K_LEFT] else 10
            self.x += self.vx
            moving = True
        elif keys[pygame.K_UP] ^ keys[pygame.K_DOWN]:
            self.status = 'walking'
            self.direction = 2 if keys[pygame.K_UP] else 0
            self.vy = 10 if keys[pygame.K_DOWN] else -10
            self.y += self.vy
            moving = True
        else:
            self.vx = 0
            self.vy = 0
            self.status = 'standing'

        self.image = self.images_standing[self.direction][self.cur_frame % self.frames] \
            if not moving else self.images_walking[self.direction][self.cur_frame % self.frames]
        self.cur_frame += 1
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

class Tasks(pygame.sprite.Sprite):
    image = load_image(f"data\\tasks\\ + {choice(['task_1.png', 'task_2.png', 'task_3.png'])}",
                       (0, 0, 0))

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Tasks.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.save_y = self.rect.y
        self.upd = 0

    def update(self):
        self.upd += 1
        if self.upd % 4 == 1:
            self.rect.y += 1
        elif self.upd % 4 == 2:
            self.rect.y += 1
        elif self.upd % 4 == 3:
            self.rect.y += 1
        else:
            self.rect.y = self.save_y


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class CompilationError(pygame.sprite.Sprite):
    image = load_image("data\\mobs\\mob_1.png", (0, 0, 0))

    def __init__(self, group, width, height):
        super().__init__(group)
        self.image = CompilationError.image
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = height
        self.vx = 3

    def update(self):
        self.rect = self.rect.move(self.vx, 0)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class RuntimeError(pygame.sprite.Sprite):
    image = load_image("data\\mobs\\mob_3.png", (0, 0, 0))

    def __init__(self, group, width, height):
        super().__init__(group)
        self.image = RuntimeError.image
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = height
        self.vy = 3

    def update(self):
        self.rect = self.rect.move(0, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy


class WrongAnswer(pygame.sprite.Sprite):
    image = load_image("data\\mobs\\mob_2.png", (0, 0, 0))

    def __init__(self, group, width, height):
        super().__init__(group)
        self.image = WrongAnswer.image
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = height
        self.vx = 2
        self.vy = 2

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx

Border(5, 5, 300 - 5, 5)
Border(5, 300 - 5, 300 - 5, 300 - 5)
Border(5, 5, 5, 300 - 5)
Border(300 - 5, 5, 300 - 5, 300 - 5)
CompilationError(all_sprites, 200, 200)
RuntimeError(all_sprites, 200, 200)
WrongAnswer(all_sprites, 200, 200)

Character(all_sprites, 250, 200)


# create all possible coord
tasks_places = [(50, 40)]
for _ in range(1):
    Tasks(all_sprites, *choice(tasks_places)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == GOEVENT:
            all_sprites.update()

        screen.fill((100, 100, 100))
        all_sprites.draw(screen)
        vertical_borders.draw(screen)
        horizontal_borders.draw(screen)

    pygame.display.flip()