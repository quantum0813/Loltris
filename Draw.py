
import Log
import pygame as Pygame

def fillJob(screen, color, job):
    if hasattr(job, "fillArea"):
        job.fillArea(color)
    else:
        padding = 0
        if hasattr(job, "border_width"):
            ## Workaround
            padding = job.border_width
        Pygame.draw.rect(
                screen,
                color,
                (job.x-padding, job.y-padding, job.width+padding*2, job.height+padding*2),
                0)

def draw3DBorder(screen, colors, rect, deepness, background=None):
    x, y, width, height = rect

    if background:
        Pygame.draw.rect(
                screen,
                background,
                (x + deepness + 1, y + deepness + 1, width - deepness - 1, height - deepness - 1)
                )

    ## Top
    Pygame.draw.polygon(
            screen,
            colors[0],
            ((x, y), (x + width, y),
             (x + width - deepness, y + deepness), (x + deepness, y + deepness), ),
            )
    ## Bottom
    Pygame.draw.polygon(
            screen,
            colors[2],
            ((x, y + height), (x + width, y + height),
             (x + width - deepness, y + height - deepness), (x + deepness, y + height - deepness), ),
            )
    ## Left
    Pygame.draw.polygon(
            screen,
            colors[3],
            ((x, y), (x + deepness, y + deepness),
             (x + deepness, y + height - deepness), (x, y + height),),
            )
    ## Right
    Pygame.draw.polygon(
            screen,
            colors[1],
            ((x + width, y), (x + width - deepness, y + deepness),
             (x + width - deepness, y + height - deepness), (x + width, y + height)),
            )
