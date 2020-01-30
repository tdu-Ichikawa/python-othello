import numpy as np
import random
import copy

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

    """
    global offset_x
    offset_x = [-1, 0, 1]
    global offset_y
    offset_y = [-1, 0, 1]
    """
    global offset
    offset = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]

    """ program """
    print("先手：BLACK (1)")
    print("後手：WHITE (2)")
    print("空欄：EMPTY (0)")
    Player = input("先手か後手を選んでください：")
    if(Player == "BLACK"):
        Player = BLACK
        Computer = WHITE
        TURN = Player
    elif(Player == "WHITE"):
        Player = WHITE
        Computer = BLACK
        TURN = Computer
    else:
        print("error : Please write your turn.(BLACK or WHITE)")
        return field
    print("")
    print(field)
    print("")
    print(field_address)
    num = 0
    before_field = copy.copy(field)
    after_field = copy.copy(field)
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
                        TURN = 0
                        break
                    before_field = copy.copy(after_field)
                    continue
                address = input("石を置く場所を指定してください : ")
                point = address2point(address)
                offset_list = point2offset(point, Player)
                if(not(address_check(point, TURN))):  # 有効手判定
                    print("「{0}」は無効な手です。".format(address))
                    print("よって、対局を終了します。")
                    print(field)
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
                        TURN = 0
                        break
                    before_field = copy.copy(after_field)
                    continue
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
                        break
                    before_field = copy.copy(after_field)
                    continue
                address = input("石を置く場所を指定してください : ")
                point = address2point(address)
                offset_list = point2offset(point, Player)
                if(not(address_check(point, TURN))):  # 有効手判定
                    print("「{0}」は無効な手です。".format(address))
                    print(field)
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
                        TURN = 0
                        break
                    before_field = copy.copy(after_field)
                    continue
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
            TURN = 0
            break
    return field


if __name__ == '__main__':
    main()
