import pygame
import math
pygame.init()
WIDTH,HEIGHT =800,800
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(" 1 ")
FONT = pygame.font.SysFont("Sans Serif",32)
class Planet:
    AU = 149.6e6*1000
    G = 6.67e-11
    SCALE = 250/ AU #makes it so that the planets are scaled down
    TIMESTEP = 86400


    def __init__(self,x,y,radius,colour,mass,name):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour 
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0


        self.x_vel = 0
        self.y_vel = 0    
        
#draws the thing with offset cause the origin is in topleft
    def draw(self,win):
        x = WIDTH/2 + self.x * self.SCALE
        y = HEIGHT/2 + self.y * self.SCALE
        if len(self.orbit) >= 2:
            updated_points = []
            for point in self.orbit: 
    
                    x,y = point
                    x = x * self.SCALE + WIDTH/2
                    y = y * self.SCALE + HEIGHT/2
                    updated_points.append((x,y))
            pygame.draw.lines(win,self.colour,False,updated_points,3)

        if not self.sun:
            planet_txt = FONT.render(f"{self.name}",0,(255,255,255))
            distance_txt = FONT.render(f"{self.distance_to_sun/1000} km",0,(255,255,255))
            win.blit(distance_txt,(x,y))
            win.blit(planet_txt,(x,y+20))
        pygame.draw.circle(win,self.colour,(x,y),self.radius)

        
    def attraction(self,other):
        other_x,other_y = other.x,other.y #Distance formula 
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance
        force = other.G * (self.mass * other.mass )/ distance**2
        theta = math.atan2(distance_y,distance_x) #tan2 is used because it gives value from -pi to pi
        force_x = math.cos(theta) * force #Resolution of forces
        force_y = math.sin(theta) * force #Resolution of forces
        return force_x,force_y

    def update_pos(self,planets):
        total_fx = total_fy =0
        for planet in planets:
            if self == planet:
                continue

            fx,fy = self.attraction(planet) #gives forces resolved,in a tuple which then get stored in individual variables
            total_fx += fx
            total_fy +=fy
        self.x_vel += total_fx/self.mass * self.TIMESTEP
        self.y_vel += total_fy/self.mass * self.TIMESTEP
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x,self.y)) # calculation of displacement by simple ds = dv/dt and addition of it all

def main():
    run = True
    clock = pygame.time.Clock()
    sun = Planet(0,0,50,(255,255,0),1.98892 * 10**30,"sun")
    earth = Planet(1*Planet.AU,0,15,(100,149,237),5.9742*10**24,"earth")
    earth.y_vel = 29.783 * 1000
    mars = Planet(1.5*Planet.AU,0,10,(188,39,50),6.39*10**23,"mars")
    mars.y_vel = 24.077 * 1000
    mercury = Planet(0.5*Planet.AU,0,8,(200,25,100),0.33010*10**24,"mercury")
    mercury.y_vel = 47 * 1000
    moon = Planet(1.3*Planet.AU,0,5,(255,255,255), 7.342 * 10**22,"moon")
    sun.sun = True
    planets = [sun,earth,mars,mercury,moon]


    moon.y_vel = (29.783 + 1.0034) * 1000


    while run:
        clock.tick(60)#it's for the fps
        WIN.fill((0,0,0))#fills with colour everytime it updates

        for event in pygame.event.get(): #takes a list and iterates through all the type of event and if any is a type "pygame.QUIT"(yes it is a type of data,when a pygame window is intended to be closed),shuts down the program.
           if event.type == pygame.QUIT:
               run = False          
        for planet in planets:
                if planet == moon:
                    moon.update_pos([earth,moon])
                    moon.draw(WIN)
                else:
                    planet.update_pos(planets)
                    planet.draw(WIN)
                         
        pygame.display.update()
    pygame.quit()
main()