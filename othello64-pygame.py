""" othello16-pygame.py  Copyright 2019 niwakoma """
import numpy as np
import random
import copy
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import sys
from math import floor


pygame.init() # pygameを初期化
global SURFACE
SURFACE = pygame.display.set_mode((1000, 600)) # windowのサイズを設定
global FPSCLOCK
FPSCLOCK = pygame.time.Clock()


def stone_location(stone):
    stone_list =[]
    tuple_list = np.where(field == stone)
    for i in range(len(tuple_list[0])):
        stone_list.append((tuple_list[0][i], tuple_list[1][i]))
    return stone_list

def empty_location(stone_list):
    emp = {}
    for x, y in stone_list:
        for i, j in offset:
            p = (x+i, y+j)
            if((p[0] <= 7) and (p[0] >= 0) and (p[1] <= 7) and (p[1] >= 0) ):
                if((field[p] == EMPTY) and not(p in emp)):
                    emp[p] = []
                    emp[p].append((i, j))
                elif((field[p] == EMPTY) and (p in emp)):
                    emp[p].append((i, j))
                else:
                    pass
            else:
                pass
    return emp

def bw_turn(TURN):
    stone_list = stone_location(3 - TURN)
    emp = empty_location(stone_list)
    stone_possible = []
    stone_dic = {}
    for kx, ky in emp.keys():
        for vx, vy in emp[kx, ky]:
            addx = vx*(-1)
            addy = vy*(-1)
            px = kx+(vx*(-1))
            py = ky+(vy*(-1))
            p = (px, py)
            while((px >=0 and px <= 7) and (py >= 0 and py <= 7)):
                if(field[p] == (3 - TURN)):
                    pass
                elif(field[p] == TURN):
                    if(not((kx, ky) in stone_dic) and not((kx, ky) in stone_possible)):
                        stone_possible.append((kx, ky))
                        stone_dic[(kx, ky)] = [(addx, addy)]
                    elif(((kx, ky) in stone_dic) and ((kx, ky) in stone_possible)):
                        stone_dic[(kx, ky)].append((addx, addy))
                    break
                else:
                    break
                px = px + addx
                py = py + addy
                p = (px, py)
    # black_possibleから1つ選出する
    print(stone_possible)
    if(len(stone_possible) == 0):
        return (-1, -1), [(0, 0)]
    r = random.randrange(len(stone_possible))
    return stone_possible[r], stone_dic[stone_possible[r]]

def update_field(TURN, point, offset_list):
    px = point[0]
    py = point[1]
    update_possible = []
    update_possible.append(point)
    for addx, addy in offset_list:
        vx = px
        vy = py
        value = point
        while((vx >=0 and vx <= 8) and (vy >= 0 and vy <= 8)):
            p = field[value]
            if((p == TURN) or (p == EMPTY) and not(value in update_possible)):
                break
            elif((p != TURN) and (p != EMPTY) and not(value in update_possible)):
                update_possible.append(value)
            else:
                pass
            vx = vx + addx
            vy = vy + addy
            value = (vx, vy)
    for i in update_possible:
        field[i] = TURN
    return field

def address2point(address):
    for i in range(8):
        for j in range(8):
            if(field_address[(i, j)] == address and field[(i, j)] == 0):
                return (i, j)
    return (-1, -1)

def point2offset(point, TURN):
    px = point[0]
    py = point[1]
    p2o_list = []
    for i, j in offset:
        vx = px + i
        vy = py + j
        p = (vx, vy)
        if((p[0] <= 7) and (p[0] >= 0) and (p[1] <= 7) and (p[1] >= 0) and (field[p] != TURN) and (field[p] != EMPTY)):
            vx = vx + i
            vy = vy + j
            p = (vx, vy)
            while((p[0] <= 7) and (p[0] >= 0) and (p[1] <= 7) and (p[1] >= 0)):
                if(field[p] != TURN and field[p] != EMPTY):
                    pass
                elif(field[p] == TURN and field[p] != EMPTY):
                    p2o_list.append((i, j))
                    break
                elif(field[p] != TURN and field[p] == EMPTY):
                    break
                vx = vx + i
                vy = vy + j
                p = (vx, vy)
    return p2o_list

def address_check(point, TURN):
    bw_stone = stone_location(3-TURN)
    emp = empty_location(bw_stone)
    stone_possible = []
    stone_dic = {}
    for kx, ky in emp.keys():
        for vx, vy in emp[kx, ky]:
            addx = vx*(-1)
            addy = vy*(-1)
            px = kx+(vx*(-1))
            py = ky+(vy*(-1))
            p = (px, py)
            while((px >=0 and px <= 7) and (py >= 0 and py <= 7)):
                if(field[p] != TURN):
                    pass
                elif(field[p] == TURN):
                    if(not((kx, ky) in stone_dic) and not((kx, ky) in stone_possible)):
                        stone_possible.append((kx, ky))
                        stone_dic[(kx, ky)] = [(addx, addy)]
                    elif(((kx, ky) in stone_dic) and ((kx, ky) in stone_possible)):
                        stone_dic[(kx, ky)].append((addx, addy))
                    break
                else:
                    break
                px = px + addx
                py = py + addy
                p = (px, py)
    if(point in stone_possible):
        return True
    return False

def point2address(point):
    if(field_address[point] and field[point] == 0):
        return field_address[point]
    return z0

def show_result():
    black_stone = 0
    white_stone = 0
    for i in range(8):
        for j in range(8):
            stone = field[(i, j)]
            if(stone == 1):
                black_stone += 1
            elif(stone == 2):
                white_stone += 1
            else:
                pass
    s = ""
    winner = ""
    if(black_stone < white_stone):
        winner = "後手（白石）"
        s = "勝者は{0}".format(winner)
    elif(black_stone > white_stone):
        winner = "先手（黒石）"
        s = "勝者は{0}".format(winner)
    elif(black_stone == white_stone):
        s = "引き分け"
    else:
        winner = ""

    print("")
    print("===================")
    print("結果発表")
    print("黒石：{0}石".format(black_stone))
    print("白石：{0}石".format(white_stone))
    print("")
    print("よって、{0}です。".format(s))


def draw_stone(SURFACE, field):
    for i in range(8):
        for j in range(8):
            stone = field[(i, j)]
            ypos = 37.5 + (75 * i) - 30
            xpos = 137.5 + (75 * j) - 30
            if(stone == BLACK):
                pygame.draw.ellipse(SURFACE, 0x000000, ((xpos, ypos), (60, 60)))
            elif(stone == WHITE):
                pygame.draw.ellipse(SURFACE, 0x000000, ((xpos, ypos), (60, 60)), 5)
            elif(stone == EMPTY):
                pass
            else:
                print("error")
                sys.exti()

def draw_info(string_one, string_two, string_three, string_four):
    leftpos = 750
    sysfont_one = pygame.font.SysFont(None, 24)
    one = sysfont_one.render(string_one, True, (0, 0, 0))
    one_rect = one.get_rect()
    one_rect.left = leftpos
    one_rect.bottom = 100
    sysfont_two = pygame.font.SysFont(None, 24)
    two = sysfont_two.render(string_two, True, (0, 0, 0))
    two_rect = two.get_rect()
    two_rect.left = leftpos
    two_rect.bottom = 150
    sysfont_three = pygame.font.SysFont(None, 24)
    three = sysfont_three.render(string_three, True, (0, 0, 0))
    three_rect = three.get_rect()
    three_rect.left = leftpos
    three_rect.bottom = 200
    sysfont_four = pygame.font.SysFont(None, 24)
    four = sysfont_four.render(string_four, True, (0, 0, 0))
    four_rect = four.get_rect()
    four_rect.left = leftpos
    four_rect.bottom = 250
    x, y = -1, -1
    while(True):
        for event in pygame.event.get():
            if(event.type == QUIT):
                pygame.quit()
                sys.exit()
            if(event.type == MOUSEBUTTONDOWN and event.button == 1):
                x, y = event.pos[0], event.pos[1]
                break
        SURFACE.fill((255, 255, 255))
        weight = 5
        for xpos in range(100, 701, 75):
            pygame.draw.line(SURFACE, 0x000000, (xpos, 0), (xpos, 601), weight)
        for ypos in range(0, 601, 75):
            pygame.draw.line(SURFACE, 0x000000, (100, ypos), (701, ypos), weight)
        draw_stone(SURFACE, field)
        SURFACE.blit(one, one_rect)
        SURFACE.blit(two, two_rect)
        SURFACE.blit(three, three_rect)
        SURFACE.blit(four, four_rect)
        pygame.display.update()
        FPSCLOCK.tick(3)
        if(x >= 0 and y >= 0):
            break

def player_turn():
    fontsize = 36
    leftpos = 750
    sysfont_turn = pygame.font.SysFont(None, fontsize)
    turn = sysfont_turn.render("TURN", True, (0, 0, 0))
    turn_rect = turn.get_rect()
    turn_rect.left = leftpos
    turn_rect.bottom = 100
    s = ""
    if(Player == BLACK):
        s = "BLACK"
    elif(Player == WHITE):
        s = "WHITE"
    sysfont_pt = pygame.font.SysFont(None, fontsize)
    pt = sysfont_pt.render(": Player   ({0})".format(s), True, (0, 0, 0))
    pt_rect = pt.get_rect()
    pt_rect.left = leftpos
    pt_rect.bottom = 150
    while(True):
        address = ""
        for event in pygame.event.get():
            if(event.type == QUIT):
                pygame.quit()
                sys.exit()
            if(event.type == MOUSEBUTTONDOWN and event.button == 1 and (event.pos[0] >= 100 and event.pos[0] < 700)):
                xpos, ypos = floor((event.pos[0]-100)/75), floor(event.pos[1]/75)
                address = field_address[(ypos, xpos)]
                break
        if(address in field_address):
            break
        # drawing line
        SURFACE.fill((255, 255, 255))
        weight = 5
        for xpos in range(100, 701, 75):
            pygame.draw.line(SURFACE, 0x000000, (xpos, 0), (xpos, 601), weight)
        for ypos in range(0, 601, 75):
            pygame.draw.line(SURFACE, 0x000000, (100, ypos), (701, ypos), weight)
        # drawing stone
        draw_stone(SURFACE, field)
        SURFACE.blit(turn, turn_rect)
        SURFACE.blit(pt, pt_rect)
        pygame.display.update()
        FPSCLOCK.tick(3)
    return address

def computer_turn():
    fontsize = 36
    leftpos = 750
    sysfont_turn = pygame.font.SysFont(None, fontsize)
    turn = sysfont_turn.render("TURN", True, (0, 0, 0))
    turn_rect = turn.get_rect()
    turn_rect.left = leftpos
    turn_rect.bottom = 100
    s = ""
    if(Computer == BLACK):
        s = "BLACK"
    elif(Computer == WHITE):
        s = "WHITE"
    sysfont_ct = pygame.font.SysFont(None, fontsize)
    ct = sysfont_ct.render(": Computer ({0})".format(s), True, (0, 0, 0))
    ct_rect = ct.get_rect()
    ct_rect.left = leftpos
    ct_rect.bottom = 150
    sysfont_click = pygame.font.SysFont(None, fontsize)
    click = sysfont_click.render("Click somewhere.", True, (0, 0, 0))
    click_rect = click.get_rect()
    click_rect.left = leftpos
    click_rect.bottom = 200
    x, y = -1, -1
    while(True):
        for event in pygame.event.get():
            if(event.type == QUIT):
                pygame.quit()
                sys.exit()
            if(event.type == MOUSEBUTTONDOWN and event.button == 1):
                x, y = event.pos[0], event.pos[1]
                break
        # drawing line
        SURFACE.fill((255, 255, 255))
        weight = 5
        for xpos in range(100, 701, 75):
            pygame.draw.line(SURFACE, 0x000000, (xpos, 0), (xpos, 601), weight)
        for ypos in range(0, 601, 75):
            pygame.draw.line(SURFACE, 0x000000, (100, ypos), (701, ypos), weight)
        # drawing stone
        draw_stone(SURFACE, field)
        SURFACE.blit(turn, turn_rect)
        SURFACE.blit(ct, ct_rect)
        SURFACE.blit(click, click_rect)
        pygame.display.update()
        FPSCLOCK.tick(3)
        if(x >= 0 and y >= 0): # クリック判定
            break

def draw_result():
    black_stone = 0
    white_stone = 0
    for i in range(8):
        for j in range(8):
            stone = field[(i, j)]
            if(stone == 1):
                black_stone += 1
            elif(stone == 2):
                white_stone += 1
            else:
                pass
    s = ""
    winner = ""
    if(black_stone < white_stone):
        winner = "Last hand (WHITE)."
        s = "Winner is {0}.".format(winner)
    elif(black_stone > white_stone):
        winner = "First hand (BLACK)."
        s = "Winner is {0}.".format(winner)
    elif(black_stone == white_stone):
        s = "Draw."
    else:
        winner = ""

    result_title = "Result."
    # 石の数え方
    bstring = "BLACK stone : {0}.".format(black_stone)
    wstring = "WHITE stone : {0}.".format(white_stone)
    string_winner = "{0}".format(s)
    draw_info(result_title, bstring, wstring, string_winner)

def draw_pass():
    black_stone = 0
    white_stone = 0
    for i in range(8):
        for j in range(8):
            stone = field[(i, j)]
            if(stone == 1):
                black_stone += 1
            elif(stone == 2):
                white_stone += 1
            else:
                pass
    result_title = "Result"
    pass_string = "There is nothing square\n"\
                  "that possible putting."
    bstring = "BLACK stone : {0}.".format(black_stone)
    wstring = "WHITE stone : {0}.".format(white_stone)
    draw_info(result_title, pass_string, bstring, wstring)

def draw_foul():
    if(TURN == Player):
        s  = "You"
    elif(TUNR == Computer):
        s = "Computer"
    else:
        s = ""
    result_title = "Result"
    foul_string = "{0} commited a foul.".format(s)
    draw_info(result_title, foul_string, "", "")

def main():
    # define
    global EMPTY
    EMPTY = 0
    global BLACK
    BLACK = 1
    global WHITE
    WHITE = 2
    global Player
    global Computer
    global TURN

    global field
    field = np.array([[0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,2,1,0,0,0],
                      [0,0,0,1,2,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0]])

    global field_address
    field_address = np.array([["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"],
                              ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"],
                              ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"],
                              ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"],
                              ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"],
                              ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"],
                              ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"],
                              ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]]) # 4

    global offset
    offset = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]


    """ drawing title """
    sysfont_title = pygame.font.SysFont(None, 80)
    title = sysfont_title.render("othello(8×8).", True, (0, 0, 0))
    title_rect = title.get_rect()
    title_rect.center = (500, 200)
    sysfont_start = pygame.font.SysFont(None, 60)
    start = sysfont_start.render("start.", True, (255, 255, 255))
    start_rect = start.get_rect()
    start_rect.center = (500, 400)
    while(True):
        xpos = 0
        ypos = 0
        for event in pygame.event.get():
            if(event.type == QUIT):
                pygame.quit()
                sys.exit()
            if(event.type == MOUSEBUTTONDOWN and event.button == 1):
                xpos, ypos = event.pos[0], event.pos[1]
        if((xpos >= 425) and (xpos <= 575) and (ypos >= 375) and (ypos <= 425)):
            break
        SURFACE.fill((255, 255, 255))
        SURFACE.blit(title, title_rect)
        x = 150
        y = 50
        pygame.draw.rect(SURFACE, (0, 0, 0), ((500-(x/2), 400-(y/2)), (x, y)))
        SURFACE.blit(start, start_rect)
        pygame.display.update()
        FPSCLOCK.tick(3)


    """ drawing select first hand or late hand """
    bxpos, bypos = 300, 350
    wxpos, wypos = 700, 350
    radius = 100
    d = radius * 2 # diameter
    sysfont = pygame.font.SysFont(None, 60)
    select_black = sysfont.render("First hand.", True, (0, 0, 0))
    select_black_rect = select_black.get_rect()
    select_black_rect.center = (bxpos, 200)
    select_white = sysfont.render("Late hand.", True, (0, 0, 0))
    select_white_rect = select_white.get_rect()
    select_white_rect.center = (wxpos, 200)
    select_message = sysfont.render("Select First hand or Late hand.", True, (0, 0, 0))
    select_message_rect = select_message.get_rect()
    select_message_rect.center = (500, 100)
    while(True):
        xpos = 0
        ypos = 0
        for event in pygame.event.get():
            if(event.type == QUIT):
                pygame.quit()
                sys.exit()
            if(event.type == MOUSEBUTTONDOWN and event.button == 1):
                xpos, ypos = event.pos[0], event.pos[1]
        # calculate radius
        br = np.sqrt((xpos - bxpos)**2 + (ypos - bypos)**2)
        wr = np.sqrt((xpos - wxpos)**2 + (ypos - wypos)**2)
        if(br <= radius):
            Player = BLACK
            Computer = WHITE
            TURN = Player
            break
        elif(wr <= radius):
            Player = WHITE
            Computer = BLACK
            TURN = Computer
            break
        # drawing background
        SURFACE.fill((255, 255, 255))
        # Rect
        pygame.draw.ellipse(SURFACE, (0, 0, 0), ((bxpos-100, bypos-100), (d, d)))
        pygame.draw.ellipse(SURFACE, (0, 0, 0), ((wxpos-100, wypos-100), (d, d)), 10)
        # Font
        SURFACE.blit(select_black, select_black_rect)
        SURFACE.blit(select_white, select_white_rect)
        SURFACE.blit(select_message, select_message_rect)
        pygame.display.update()
        FPSCLOCK.tick(3)

    """ othello (8x8) """
    before_field = copy.copy(field)
    after_field = copy.copy(field)
    while(True):
        """ pygame """
        for event in pygame.event.get():
            if(event.type == QUIT):
                pygame.quit()
                sys.exit()

        """ othello """
        while(TURN != 0):
            if(TURN == BLACK):
                point, offset_list = bw_turn(BLACK)
                if(TURN == Player):
                    print("TURN : You")
                    if(point == (-1, -1)):  # pass判定
                        print("pass")
                        print(field)
                        TURN = WHITE
                        if((before_field == after_field).all()):  # 両者pass判定
                            print("両者passのため対局を終了")
                            draw_pass()
                            TURN = 0
                            break
                        before_field = copy.copy(after_field)
                        continue
                    address = player_turn()
                    print("石を置く場所 : {0} ".format(address))
                    point = address2point(address)
                    offset_list = point2offset(point, Player)
                    if(not(address_check(point, TURN))):  # 有効手判定
                        print("「{0}」は無効な手です。".format(address))
                        print("よって、対局を終了します。")
                        print(field)
                        draw_foul()
                        TURN = 0
                        break
                elif(TURN == Computer):
                    print("TURN : Computer")
                    if(point == (-1, -1)):  # pass判定
                        print("pass")
                        print(field)
                        TURN = WHITE
                        if((before_field == after_field).all()):  # 両者pass判定
                            print("両者passのため対局を終了")
                            draw_pass()
                            TURN = 0
                            break
                        before_field = copy.copy(after_field)
                        continue
                    computer_turn()
                    print("石を置く場所 : {0} ".format(point2address(point)))
                else:
                    print("error")
                    TURN = 0
                    break
                field = update_field(TURN, point, offset_list)
                print(field)
                print("")
                before_field = copy.copy(after_field)
                after_field = copy.copy(field)
                TURN = WHITE
            elif(TURN == WHITE):
                point, offset_list = bw_turn(WHITE)
                if(TURN == Player):
                    print("TURN : You")
                    if(point == (-1, -1)):  # pass判定
                        print("pass")
                        print(field)
                        TURN = BLACK
                        if((before_field == after_field).all()):  # 両者pass判定
                            print("両者passのため対局を終了")
                            TURN = 0
                            draw_pass()
                            break
                        before_field = copy.copy(after_field)
                        continue
                    address = player_turn()
                    print("石を置く場所 : {0} ".format(address))
                    point = address2point(address)
                    offset_list = point2offset(point, Player)
                    if(not(address_check(point, TURN))):  # 有効手判定
                        print("「{0}」は無効な手です。".format(address))
                        print(field)
                        draw_foul()
                        TURN = 0
                        break
                elif(TURN == Computer):
                    print("TURN : Computer")
                    if(point == (-1, -1)):  # pass判定
                        print("pass")
                        print(field)
                        TURN = BLACK
                        if((before_field == after_field).all()):  # 両者pass判定
                            print("両者passのため対局を終了")
                            draw_pass()
                            TURN = 0
                            break
                        before_field = copy.copy(after_field)
                        continue
                    computer_turn()
                    print("石を置く場所 : {0} ".format(point2address(point)))
                else:
                    print("error")
                    TURN = 0
                    break
                field = update_field(TURN, point, offset_list)
                print(field)
                print("")
                before_field = copy.copy(after_field)
                after_field = copy.copy(field)
                TURN = BLACK
            else:
                print("error")
                TURN = 0
                break
            if(len(np.where(field == 0)[0]) == 0):
                print("")
                print(field)
                print("")
                print("対局を終了します。")
                print("")
                show_result()
                draw_result()
                TURN = 0
                break

        """ drawing field """
        SURFACE.fill((255, 255, 255))
        weight = 5
        for xpos in range(100, 701, 75):
            pygame.draw.line(SURFACE, 0x000000, (xpos, 0), (xpos, 601), weight)
        for ypos in range(0, 601, 75):
            pygame.draw.line(SURFACE, 0x000000, (100, ypos), (701, ypos), weight)
        # drawing stone
        draw_stone(SURFACE, field)
        pygame.display.update()
        FPSCLOCK.tick(3)
    return field


if __name__ == '__main__':
    main()
