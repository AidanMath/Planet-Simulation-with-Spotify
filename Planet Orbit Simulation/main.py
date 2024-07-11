import pygame
import math

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('Orbit Simulation of Solar System')
clock = pygame.time.Clock()

# Set up font for rendering text
font = pygame.font.SysFont('Arial', 18)

screen.fill("black")

class Planet:
    # Distance in meters from the sun
    AU = (149.6e6 * 1000)
    G = 6.67428e-11
    SCALE = 250 / AU  # 1 AU = 100 px
    TIMESTEP = 3600 * 24  # One day
    MAX_TRAIL_LENGTH = 100  # Maximum length of the trail

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.distance_to_sun = 0
        self.sun = False

        self.x_vel = 0
        self.y_vel = 0
        
    def draw(self, screen):
        x = self.x * self.SCALE + 1920 / 2
        y = self.y * self.SCALE + 1080 / 2
        pygame.draw.circle(screen, self.color, (int(x), int(y)), self.radius)
        
        # Draw the orbit trail
        if len(self.orbit) > 1:
            updated_orbit = [(pos[0] * self.SCALE + 1920 / 2, pos[1] * self.SCALE + 1080 / 2) for pos in self.orbit]
            pygame.draw.lines(screen, self.color, False, updated_orbit, 1)
        
        # Render the distance from the sun above the planet
        if not self.sun:
            distance_text = font.render(f'{self.distance_to_sun / 1000:.2f} km', True, (255, 255, 255))
            screen.blit(distance_text, (int(x) - distance_text.get_width() // 2, int(y) - self.radius - 20))
    
    def attraction(self, other):
        other_x = other.x
        other_y = other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y

        # Pythagorean Theorem 
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if distance == 0:
            return 0, 0  # Avoid division by zero

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2

        # Calculate the angle which the planets are from each other 
        theta = math.atan2(distance_y, distance_x)
        
        # Calculate the force in x and y directions, magnitude of each direction 
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y
    
    def update_position(self, planets):
        total_force_x = 0
        total_force_y = 0

        for planet in planets:
            if self == planet:
                continue

            force_x, force_y = self.attraction(planet)
            total_force_x += force_x
            total_force_y += force_y

        # Calculate velocity 
        self.x_vel += total_force_x / self.mass * self.TIMESTEP
        self.y_vel += total_force_y / self.mass * self.TIMESTEP

        # Update the x and y coordinates 
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP 

        self.orbit.append((self.x, self.y))

        # Limit the length of the orbit trail
        if len(self.orbit) > self.MAX_TRAIL_LENGTH:
            self.orbit.pop(0)
        # F = m * a
        # a = F / m

def main():
    running = True

    # Initialization of the planets 
    sun = Planet(0, 0, 30, (255, 255, 0), 1.98892e30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, (0, 0, 255), 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000  # Earth's orbital velocity

    mercury = Planet(0.387 * Planet.AU, 0, 12, (169, 169, 169), 3.3 * 10**23)
    mercury.y_vel = 47.4 * 1000  # Mercury's orbital velocity

    venus = Planet(0.723 * Planet.AU, 0, 14, (255, 255, 255), 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000  # Venus's orbital velocity

    mars = Planet(-1.524 * Planet.AU, 0, 12, (255, 0, 0), 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000  # Mars's orbital velocity
  
    planets = [sun, earth, mercury, venus, mars]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")  
        
        for planet in planets:
            planet.update_position(planets)
            # Continuously redraw the planets each frame 
            planet.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()
