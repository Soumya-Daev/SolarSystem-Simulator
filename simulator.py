import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulator")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (188, 39, 50)
# GREEN = (0, 255, 0)
BLUE = (100, 149, 237)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)

# FONT = pygame.font.SysFont()

class Planet:
    ASTRONOMICAL_UNIT = 149.6e6 * 1000
    GRAVITATIONAL_CONSTANT = 6.67428e-11
    SCALE = 140 / ASTRONOMICAL_UNIT # 1AU = 100px
    TIME_STEP = 3600*24 # 1 day

    def __init__(self, x, y, image, color, mass):
        self.x = x
        self.y = y
        self.image = image
        self.color = color
        self.mass = mass # Use the mass to generate the actual circular orbit.

        self.orbit = [] # keeps track of all the points this planet has travelled, so that we can draw an orbit path.
        self.sun = False # It shall tell us whetgher the planet is a sun or not, as we do not wanna draw the orbit for sun.
        self.distance_to_sun = 0 # The distance to the sun.

        self.x_velocity = 0
        self.y_velocity = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(win, self.color, False, updated_points, 1)

        rect_loc = self.image.get_rect()
        rect_loc.center = (x, y)
        WIN.blit(self.image, rect_loc)
    
    def attraction_Force(self, other) :
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun :
            self.distance_to_sun = distance
        
        force = self.GRAVITATIONAL_CONSTANT * self.mass * other.mass / (distance ** 2)
        theta = math.atan2(distance_y, distance_x)
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)

        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction_Force(planet)
            total_fx += fx
            total_fy += fy
        
        self.x_velocity += total_fx / self.mass * self.TIME_STEP # Increasing the velocity by the acceleration.
        self.y_velocity += total_fy / self.mass * self.TIME_STEP

        self.x += self.x_velocity * self.TIME_STEP # Increasing the position by the velocity.
        self.y += self.y_velocity * self.TIME_STEP
        self.orbit.append((self.x, self.y))

def main() :
    run = True
    clock = pygame.time.Clock()

    Sun = pygame.image.load('Planets\\Sun.png')
    sun = Planet(0, 0, Sun, YELLOW, 1.98892 * (10 ** 30))
    sun.sun = True

    Mercury = pygame.image.load('Planets\\Mercury.png')
    Venus = pygame.image.load('Planets\\Venus.png')
    Earth = pygame.image.load('Planets\\Earth.png')
    Mars = pygame.image.load('Planets\\Mars.png')
    Jupiter = pygame.image.load('Planets\\Jupiter.png')

    mercury = Planet(0.39 * Planet.ASTRONOMICAL_UNIT, 0, Mercury, GRAY, 3.3011 * (10 ** 23))
    mercury.y_velocity = -47.89 * (10 ** 3)
    venus = Planet(0.723 * Planet.ASTRONOMICAL_UNIT, 0, Venus, ORANGE, 4.87 * (10 ** 24))
    venus.y_velocity = -35.02 * (10 ** 3)
    earth = Planet(-1 * Planet.ASTRONOMICAL_UNIT, 0, Earth, BLUE, 5.98 * (10 ** 24))
    earth.y_velocity = 29.783 * (10 ** 3)
    mars = Planet(-1.524 * Planet.ASTRONOMICAL_UNIT, 0, Mars, RED, 6.42 * (10 ** 23))
    mars.y_velocity = 24.07 * (10 ** 3)
    jupiter = Planet(5.203 * Planet.ASTRONOMICAL_UNIT, 0, Jupiter, YELLOW, 1.9 * (10 ** 27))
    jupiter.y_velocity = -13.07 * (10 ** 3)
    # saturn = Planet(3.794 * Planet.ASTRONOMICAL_UNIT, 0, 20, GREEN, 5.6836 * (10 ** 26))
    # saturn.y_velocity = 9.64 * (10 ** 3)
    # uranus = Planet(5.793 * Planet.ASTRONOMICAL_UNIT, 0, 18, GRAY, 8.6810 * (10 ** 25))
    # uranus.y_velocity = 6.81 * (10 ** 3)
    # neptune = Planet(6.895 * Planet.ASTRONOMICAL_UNIT, 0, 16, BLUE, 1.0243 * (10 ** 26))
    # neptune.y_velocity = 5.43 * (10 ** 3)
    # pluto = Planet(9.539 * Planet.ASTRONOMICAL_UNIT, 0, 8, GRAY, 1.3e-6 * (10 ** 22))
    # pluto.y_velocity = 4.74 * (10 ** 3)

    planets = [sun, earth, mars, venus, mercury, jupiter]
    pause = False
    while run :
        clock.tick(100)
        WIN.fill(BLACK)

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    for planet in planets :
                        planet.orbit = []
                if event.key == pygame.K_p :
                    pause = True
                if event.key == pygame.K_r :
                    pause = False

        for planet in planets :
            if not pause :
                planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__" :
    main()