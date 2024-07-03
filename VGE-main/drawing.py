import cairo
import math
from point import EPS, Point

def parallel_anims(anims):
    """Combina múltiples animaciones para que se ejecuten simultáneamente"""
    def func(ctx, time):
        for anim in anims:
            anim(ctx, time)
    return func

def combine_anims(anims, timeline):
    """Combina múltiples animaciones en una sola función de animación que se ejecuta secuencialmente según un timeline especificado."""
    if len(anims) != len(timeline):
        raise ValueError("anims y timeline deben de ser iguales")
    
    timeline_length = sum(timeline)
    # prefijo sum
    start_times = [sum(timeline[:i]) for i in range(len(timeline))]
    end_times = [sum(timeline[:i+1]) for i in range(len(timeline))]
    def func(ctx, time):
        time = time * timeline_length
        index = None
        for i in range(len(start_times)):
            if time >= start_times[i] and time <= end_times[i]:
                index = i
                break
        if index is not None:
            #Ejecuta las animaciones anteriores
            for i in range(index):
                anims[i](ctx, 1.0)
            anims[index](ctx, (time - start_times[index])/timeline[index])
        else:
            # Ejecuta la animación actual con un time > 1
            for anim in anims:
                anim(ctx, 1.0)
    return func

def create_pause_anim():
    """Crea una animación que no dibuja nada para que mostrar la animacion pausada"""
    def func(ctx, time):
        pass
    return func

def draw_polygon_segments(vertices):
    """Dibuja el contorno de un polígono a partir de una lista de vértices.
    args:
        vertices - a arreglo de puntos"""
    if len(vertices) < 1:
        raise ValueError("Los vértices deben tener al menos un punto.")
    def func(ctx):
        vertex_iter = iter(vertices)
        ctx.move_to(*next(vertex_iter))
        for vertex in vertex_iter:
            ctx.line_to(*vertex)
        ctx.close_path()
    return func

def draw_polygon_segment(start, to):
    """Dibuja una línea entre dos puntos. - start(inicial) y to(final)"""
    def func(ctx):
        ctx.move_to(*start)
        ctx.line_to(*to)
    return func

def create_polygon_segment_anim(start, to):
    """ Crea una animación que dibuja un segmento de polígono en un tiempo determinado."""
    def func(ctx, time):
        ctx.set_source_rgba(*rgba_to_bgra(0.5,0.5,0.5))
        vec = Point(to.x - start.x, to.y - start.y)
        target = Point(start.x + time * vec.x, start.y + time * vec.y)
        ctx.move_to(*start)
        ctx.line_to(*target)
        ctx.stroke()
    return func


def draw_polygon_vertex(vertex, radius):
    """Dibuja un vértice de polígono como un círculo."""
    def func(ctx):
        ctx.arc(*vertex, radius, 0, 2 * math.pi)
    return func

def create_polygon_vertex_anim(vertex, radius):
    """Crea una animación que dibuja un círculo que resalta un vértice de polígono, con el radio aumentando progresivamente"""
    def func(ctx, time):
        curr_radius = radius * time
        ctx.arc(*vertex, curr_radius, 0, 2 * math.pi)
        ctx.fill()
    return func

def create_polygon_vertex_blink_anim(vertex, radius, color):
    """ Crea una animación que dibuja un círculo que resalta un vértice de polígono, con el radio disminuyendo al final."""
    def func(ctx, time):
        ctx.set_source_rgba(*rgba_to_bgra(*color))
        curr_radius = -4 * radius * (time * time - time)
        ctx.arc(*vertex, curr_radius, 0, 2 * math.pi)
        ctx.fill()
    return func

def draw_triangle(t):
    """Dibuja un triángulo a partir de tres vértices. t = (v0, v1, v2)"""
    def func(ctx):
        v0, v1, v2 = t
        ctx.move_to(v0.x, v0.y)
        ctx.line_to(v1.x, v1.y)
        ctx.line_to(v2.x, v2.y)
        ctx.close_path()
    return func

def create_alpha_color_anim(red, green, blue, static_draw_f, fill=False, max_alpha=1.0, line_width=None):
    """Crea una animación que cambia el canal alfa de un dibujo estático de manera lineal."""
    def func(ctx: cairo.Context, time):
        ctx.set_source_rgba(*rgba_to_bgra(red, green, blue, time*max_alpha))
        static_draw_f(ctx)
        if fill:
            ctx.fill()
        else:
            if line_width is not None:
                prev_line_width = ctx.get_line_width()
                ctx.set_line_width(line_width)
                ctx.stroke()
                ctx.set_line_width(prev_line_width)
            else:
                ctx.stroke()
    return func

def create_alpha_color_blink_anim(red, green, blue, static_draw_f, fill=False):
    """Crea una animación que cambia el canal alfa de un dibujo estático de manera intermitente (blink)."""
    def func(ctx, time):
        alpha = -4 * (time * time - time)
        ctx.set_source_rgba(*rgba_to_bgra(red, green, blue, alpha))
        static_draw_f(ctx)
        if fill:
            ctx.fill()
        else:
            ctx.stroke()
    return func


def rgba_to_bgra(red, green, blue, alpha=1.0):
    """Reordena los canales de color para la compatibilidad entre pycairo y pygame."""
    return (blue, green, red, alpha)