import math
import sys
from argparse import ArgumentParser

import cairo
import pygame

from helpfunctions import check_points_on_line, check_intersections
from point import Point
from earclipping_anim import EarClippingAnim
from drawing import rgba_to_bgra

from examples import examples_dict

def print_speed(speed, pause):
    sys.stdout.write("\033[K")
    if pause: 
        print(f"Velocidad actual: PAUSADA", end="\r")
    else:
        print(f"Velocidad actual: {speed}", end="\r")

def draw_points(ctx: cairo.Context, pts):
    ctx.set_line_width(2)
    ctx.set_source_rgba(*rgba_to_bgra(0.26, 0.65, 0.77,1))
    
    ctx.move_to(pts[0][0], pts[0][1])
    last = ()
    for p in pts:
        ctx.line_to(p[0], p[1])
        ctx.move_to(p[0], p[1])
        last = p
    ctx.stroke()

    ctx.set_source_rgba(*rgba_to_bgra(1,1,1,1))
    ctx.arc(last[0], last[1],3, 0, 2*math.pi)
    ctx.stroke()

    ctx.set_source_rgba(*rgba_to_bgra(0.26, 0.65, 0.77,0.3))
    ctx.move_to(last[0],last[1])
    ctx.line_to(pts[0][0], pts[0][1])
    ctx.stroke()

def draw_intesections(ctx: cairo.Context, pts):
    ctx.set_line_width(2)
    ctx.set_source_rgba(*rgba_to_bgra(1, 0, 0,1))   
    for p in pts:
        ctx.arc(p[0], p[1],5, 0, 2*math.pi)
        ctx.stroke()

def draw_info(screen, points, triangles_count):
    font = pygame.font.SysFont('Arial', 24)
    info_surface = pygame.Surface((320, 600))
    info_surface.fill((0, 0, 0))
    
    points_text = f"Puntos: {len(points)}"
    triangles_text = f"Triangulos: {triangles_count}"
    
    points_render = font.render(points_text, True, (255, 255, 255))
    triangles_render = font.render(triangles_text, True, (255, 255, 255))
    
    info_surface.blit(points_render, (10, 10))
    info_surface.blit(triangles_render, (10, 50))
    
    menu_text = [
        "f     - Iniciar Triangulacion",
        "g     - Iniciar Triangulacion con edge flipping",
        "c     - Limpiar Pantalla",
        "1-7   - Cargar Ejemplos",
        "UP    - Aumentar velocidad de animacion",
        "DOWN  - Disminuir velocidad de animacion",
        "LEFT  - Reproducir la animacion en retroceso",
        "RIGHT - Reproducir la animacion hacia adelante",
        "SPACE - Pausar la animacion"
    ]
    
    y_offset = 100
    for line in menu_text:
        menu_render = font.render(line, True, (255, 255, 255))
        info_surface.blit(menu_render, (10, y_offset))
        y_offset += 30
    
    screen.blit(info_surface, (520, 0))

def main():
    parser = ArgumentParser()
    parser.add_argument("--width", type=int, default=840, help="El ancho de la ventana de la aplicación.")
    parser.add_argument("--height", type=int, default=600, help="El alto de la ventana de la aplicación.")
    args = parser.parse_args()
    
    width, height = args.width, args.height
    pygame.init()
    window = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    time = 0.0
    total_anim_lenght = 1.0
    speed = 1.0
    speed_diff_update = 1.5
    max_speed = speed_diff_update ** 7
    min_speed = -max_speed
    time_direction = 1.0
    pause = False

    print_speed(speed, pause)

    points_ready = False
    points = []
    intersections = []
    triangles_count = 0

    while True:
        
        dt = clock.tick(60)
        
        if not pause:
            time += dt * speed * time_direction / total_anim_lenght if (total_anim_lenght != 0) else 1.0
        if time > 1.0: time = 1.0
        if time < 0: time = 0

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

        screen = pygame.display.get_surface()

        ctx = cairo.Context(surface)
        ctx.set_antialias(cairo.Antialias(cairo.Antialias.GOOD))
        
        ctx.set_source_rgba(*rgba_to_bgra(0,0,0,1))
        ctx.rectangle(0, 0, width, height)
        ctx.fill()
        
        if not points_ready and points:
            draw_points(ctx,points)
            
        if intersections:
            draw_intesections(ctx,intersections)

        ctx.set_line_width(2)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP and not points_ready and not intersections:
                pos = pygame.mouse.get_pos()
                points.append(Point(pos[0],pos[1]))

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f and not intersections and len(points)>=3:
                points,_ = check_points_on_line(points)
                intersections = check_intersections(points)
                if not intersections:
                    points_ready = True
                    anim = EarClippingAnim(points)
                    total_anim_lenght = sum((t for _, t in anim.schedule)) * 1000
                    time = 0.0
                    triangles_count = len(anim.triangles)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_g and not intersections and len(points)>=3:
                points,_ = check_points_on_line(points)
                intersections = check_intersections(points)
                if not intersections:
                    points_ready = True
                    anim = EarClippingAnim(points, edge_swapping=True)
                    total_anim_lenght = sum((t for _, t in anim.schedule)) * 1000
                    time = 0.0
                    triangles_count = len(anim.triangles)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                points_ready = False
                points = []
                intersections=[]
                triangles_count = 0
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                speed *= speed_diff_update
                if speed > max_speed: speed = max_speed
                print_speed(time_direction * speed, pause)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                speed /= speed_diff_update
                if speed < min_speed: speed = min_speed
                print_speed(time_direction * speed, pause)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                time_direction = -1.0
                print_speed(time_direction * speed, pause)
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                time_direction = 1.0
                print_speed(time_direction * speed, pause)
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = not pause
                print_speed(time_direction * speed, pause)
                
            elif event.type == pygame.KEYDOWN and (event.key >= ord('1') and event.key <=ord('7')):
                intersections = []
                example_id = event.key-ord('0')-1
                points = (list(examples_dict.values()))[example_id]
                triangles_count = 0

        if points_ready:
            anim(ctx, time)

        buf = surface.get_data()
        image = pygame.image.frombuffer(buf, (width, height), "RGBA")
        screen.blit(image, (0, 0))

        draw_info(screen, points, triangles_count)

        pygame.display.flip()

if __name__ == "__main__":
    main()
