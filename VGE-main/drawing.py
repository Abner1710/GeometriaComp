"""Definitions of animation building blocks"""

import cairo
import math
from point import EPS, Point

def parallel_anims(anims):
    """Combines animations in anims to a single animation,
    where the animations run simultaneously"""
    def func(ctx, time):
        for anim in anims:
            anim(ctx, time)
    return func

def combine_anims(anims, timeline):
    """Combines animations in anims to a single animation function,
    anims and timeline should be the same lenght,
    timeline should be a list of float numbers 
    that define the ratios of time of animations"""
    if len(anims) != len(timeline):
        raise ValueError("anims and timeline should be the same length")
    
    timeline_length = sum(timeline)
    # prefix sum
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
            # finish previous anims
            for i in range(index):
                anims[i](ctx, 1.0)
            anims[index](ctx, (time - start_times[index])/timeline[index])
        else:
            # just finish all anims as time > 1
            for anim in anims:
                anim(ctx, 1.0)
    return func

def create_pause_anim():
    """Returs a function that draw nothing"""
    def func(ctx, time):
        pass
    return func

def draw_polygon_segments(vertices):
    """Draws a polygon outline = its segments as lines
    args:
        vertices - a array of points"""
    if len(vertices) < 1:
        raise ValueError("vertices should have at least one point")
    def func(ctx):
        vertex_iter = iter(vertices)
        ctx.move_to(*next(vertex_iter))
        for vertex in vertex_iter:
            ctx.line_to(*vertex)
        ctx.close_path()
    return func

def draw_polygon_segment(start, to):
    """Draws a line between to points - start and to"""
    def func(ctx):
        ctx.move_to(*start)
        ctx.line_to(*to)
    return func

def create_polygon_segment_anim(start, to):
    """Returns a function
    that draws a polygon segment animation frame in the specified time"""
    def func(ctx, time):
        ctx.set_source_rgba(*rgba_to_bgra(0.5,0.5,0.5))
        vec = Point(to.x - start.x, to.y - start.y)
        target = Point(start.x + time * vec.x, start.y + time * vec.y)
        ctx.move_to(*start)
        ctx.line_to(*target)
        ctx.stroke()
    return func


def draw_polygon_vertex(vertex, radius):
    """Draws a circle that highlights a specified vertex"""
    def func(ctx):
        ctx.arc(*vertex, radius, 0, 2 * math.pi)
    return func

def create_polygon_vertex_anim(vertex, radius):
    """Returns a function
    that draws a circle that highlights a specified vertex,
    at the end of the animation the radius is as specified"""
    def func(ctx, time):
        curr_radius = radius * time
        ctx.arc(*vertex, curr_radius, 0, 2 * math.pi)
        ctx.fill()
    return func

def create_polygon_vertex_blink_anim(vertex, radius, color):
    """Returns a function
    that draws a circle that highlights a specified vertex,
    at the end of the animation radius is 0"""
    def func(ctx, time):
        ctx.set_source_rgba(*rgba_to_bgra(*color))
        curr_radius = -4 * radius * (time * time - time)
        ctx.arc(*vertex, curr_radius, 0, 2 * math.pi)
        ctx.fill()
    return func

def draw_triangle(t):
    """Draws a triangle t = (v0, v1, v2)"""
    def func(ctx):
        v0, v1, v2 = t
        ctx.move_to(v0.x, v0.y)
        ctx.line_to(v1.x, v1.y)
        ctx.line_to(v2.x, v2.y)
        ctx.close_path()
    return func

def create_alpha_color_anim(red, green, blue, static_draw_f, fill=False, max_alpha=1.0, line_width=None):
    """Returns a function
    that animates a static drawing changing the alpha channel lineary"""
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
    """Returns a function
    that animates a static drawing changing the alpha channel lineary"""
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
    """Reorders channels, it is necessary for pycairo-pygame compatibility"""
    return (blue, green, red, alpha)