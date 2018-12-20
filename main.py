#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Modules
import sys
import pygame
from pygame.locals import *
import numpy as np
import pygameMenu
from pygameMenu.locals import *

# Colors
# ---------------------------------------------------------------------
alive = (251,224,10)
dead = (53,83,87)
menu_color = (170, 170, 170)
menu_color_title = (170,65,50)
color_selected = (170,65,50)
font_color = (0, 0, 0)
text_color = (0, 0, 0)

# Global variables
# ---------------------------------------------------------------------
wWidth = 590
wHeight = 590
nrows = 30
ncols = 30
spacing = 1
frame_rate = 10
rects = []
universe = []
screen = pygame.display.set_mode((wWidth, wHeight))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()
paused = False
# ---------------------------------------------------------------------
 
# Functions
# ---------------------------------------------------------------------
def change_status(val):
    global paused
    paused = val

def change_frame_rate(fr):
    global frame_rate
    frame_rate = fr
    
def change_ncols(n):
    global ncols
    ncols = n
    
def change_nrows(n):
    global nrows
    nrows = n

def get_rects(nrows, ncols, x0, y0, x1, y1, spacing):
    rects = []
    rWidth = (x1 - x0 - spacing * (1 + ncols)) / ncols
    rHeight = (y1 - y0 - spacing * (1 + nrows)) / nrows
    Dx = rWidth + spacing
    Dy = rHeight + spacing
    DxVec = np.array([Dx, 0])
    DyVec = np.array([0, Dy])
    D0 = np.array([x0 + spacing, y0 + spacing])
    for j in range(nrows):
        for i in range(ncols):
            rects.append(pygame.Rect(D0 + i * DxVec + j * DyVec, (rWidth, rHeight)))
    return rects

def draw_rects(rects, universe, screen):
    colors = map(lambda cell: alive if cell else dead, universe.flat)
    for rect, color in zip(rects, colors):
        pygame.draw.rect(screen, color, rect)

def rules(cell, n):
    if n == 2:
        return cell
    elif n == 3:
        return 1
    else:
        return 0

def evolve_universe():
    global universe
    mr = np.roll(universe, 1, axis = 0)
    ml = np.roll(universe, -1, axis = 0)
    mu = np.roll(universe, 1, axis = 1)
    md = np.roll(universe, -1, axis = 1)
    mru = np.roll(mr, 1, axis = 1)
    mrd = np.roll(mr, -1, axis = 1)
    mlu = np.roll(ml, 1, axis = 1)
    mld = np.roll(ml, -1, axis = 1)
    
    nn = mr + ml + mu + md + mru + mrd + mlu + mld
    
    shape = universe.shape
    universe = np.fromiter((rules(cell, n) for cell, n in zip(universe.flat, nn.flat)), dtype='int')
    universe.shape = shape
    
def main_background():
    screen.fill((0,0,0))
    draw_rects(rects, universe, screen)

def init_game_of_life():
    global rects, universe
    screen.fill((0,0,0))
    rects = get_rects(nrows, ncols, 0, 0, wWidth, wHeight, spacing)
    universe = np.random.randint(0, 2, size = (nrows, ncols))
    
def clear_universe():
    global universe
    universe.fill(0)

def game_of_life():
    main_menu.disable()
    main_menu.reset(1)
    screen.fill((0,0,0))
    while True:
        clock.tick(frame_rate)
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if (event.key == K_ESCAPE or event.key == K_RETURN) and main_menu.is_disabled():
                    main_menu.enable()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                i = int(x / wWidth * ncols)
                j = int(y / wHeight * nrows)
                print(i,j)
                universe[j][i] = abs(1 - universe[j][i])
        main_menu.mainloop(events)
        draw_rects(rects, universe, screen)
        if not paused:
            evolve_universe()
        pygame.display.update()
# ---------------------------------------------------------------------

pygame.init()

# Menus
# ---------------------------------------------------------------------
# About menu
about_menu = pygameMenu.TextMenu(screen,
                                bgfun = main_background,
                                color_selected = color_selected,
                                font = pygameMenu.fonts.FONT_BEBAS,
                                font_title = pygameMenu.fonts.FONT_8BIT,
                                font_color = font_color,
                                menu_alpha=100,
                                menu_color_title = menu_color_title,
                                menu_color = menu_color,
                                font_size_title = wHeight // 20,
                                font_size = wHeight // 20,
                                menu_height = int(wHeight * 0.7),
                                menu_width = int(wWidth * 0.7),
                                onclose=PYGAME_MENU_DISABLE_CLOSE,
                                option_shadow=False,
                                title='About',
                                text_color = text_color,
                                text_fontsize = wHeight // 30,
                                window_height=wHeight,
                                window_width=wWidth
                                )

ABOUT = ['The game of Life',
         'Author: A. Villas',
         PYGAMEMENU_TEXT_NEWLINE,
         'Email: albertovillos@gmail.com']

for m in ABOUT:
    about_menu.add_line(m)
about_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)
about_menu.add_option('Return to menu', PYGAME_MENU_BACK)

# Settings menu
settings_menu = pygameMenu.TextMenu(screen,
                                bgfun = main_background,
                                color_selected = color_selected,
                                font = pygameMenu.fonts.FONT_BEBAS,
                                font_title = pygameMenu.fonts.FONT_8BIT,
                                font_color = font_color,
                                menu_alpha = 100,
                                menu_color = menu_color,
                                menu_color_title = menu_color_title,
                                font_size_title = wHeight // 20,
                                font_size = wHeight // 25,
                                menu_height = int(wHeight * 0.6),
                                menu_width = int(wWidth * 0.6),
                                onclose = PYGAME_MENU_DISABLE_CLOSE,
                                option_shadow = False,
                                title = 'Settings',
                                text_color = text_color,
                                text_fontsize = wHeight // 30,
                                window_height = wHeight,
                                window_width = wWidth
                                )

settings_menu.add_selector('Frame rate', 
                           list(map(lambda i: (str(i), i), range(frame_rate,51))) +\
                           list(map(lambda i: (str(i), i), range(0,frame_rate))),
                           onreturn=None,
                           onchange=change_frame_rate)
settings_menu.add_selector('Columns (*)', 
                           list(map(lambda i: (str(i), i), range(ncols,201))) +\
                           list(map(lambda i: (str(i), i), range(1,ncols))),
                           onreturn=None,
                           onchange=change_ncols)
settings_menu.add_selector('Rows (*)', 
                           list(map(lambda i: (str(i), i), range(nrows,201))) +\
                           list(map(lambda i: (str(i), i), range(1,nrows))),
                           onreturn=None,
                           onchange=change_nrows)
settings_menu.add_line('(*): Requieres restart')
settings_menu.add_option('Return to menu', PYGAME_MENU_BACK)
    
# Main menu
main_menu = pygameMenu.Menu(screen,
                                bgfun = main_background,
                                color_selected = color_selected,
                                font = pygameMenu.fonts.FONT_BEBAS,
                                font_title = pygameMenu.fonts.FONT_8BIT,
                                font_color = font_color,
                                font_size_title=wHeight // 20,
                                font_size = wHeight // 20,
                                menu_alpha = 100,
                                menu_color = menu_color,
                                menu_color_title = menu_color_title,
                                menu_height = int(wHeight * 0.7),
                                menu_width = int(wWidth * 0.7),
                                onclose = PYGAME_MENU_DISABLE_CLOSE,
                                option_shadow = False,
                                title = 'Main menu',
                                window_height = wHeight,
                                window_width = wWidth
                                )
main_menu.add_option('Resume', game_of_life)
main_menu.add_selector('Status', [('Running', False), ('Paused', True)],
                           onreturn=None,
                           onchange=change_status)
main_menu.add_option('Restart', init_game_of_life)
main_menu.add_option('Clear', clear_universe)
main_menu.add_option('Settings', settings_menu)
main_menu.add_option('About', about_menu)
main_menu.add_option('Quit', PYGAME_MENU_EXIT)
# ---------------------------------------------------------------------

init_game_of_life()
main_menu.enable()

# Main loop
while True:
    print(paused)
    clock.tick(frame_rate)
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            exit()

    # Main menu
    main_menu.mainloop(events)
        
    pygame.display.update()
