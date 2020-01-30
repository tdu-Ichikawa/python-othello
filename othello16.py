import numpy as np
import random


# 黒または白石が置かれている座標を返す
# 引数は置かれている石(list)
def stone_location(stone):
    stone_list = []
    for i in range(4):
        for j in range(4):
            if(field[(i, j)] == stone):
                stone_list.append((i, j))
    return stone_list

# 引数のoffset範囲内に対する
# 空マスの座標とoffsetの組み合わせを返す(dic)
def empty_location(stone_list):
    emp = {}
    for x, y in stone_list:
        for i in offset_x:
            for j in offset_y:
                p = (x+i, y+j)
                if((p[0] <= 3) and (p[0] >= 0) and (p[1] <= 3) and (p[1] >= 0) ):
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

# 黒石の手番
# 黒石を置く座標とoffsetを返す
def black_turn():
    #白石が置かれている場所のリスト
    white_stone = stone_location(WHITE)
    # 空マスの座標を返す
    emp = empty_location(white_stone)
    # 黒石が置ける座標を返す
    black_possible = []
    black_dic = {}
    for kx, ky in emp.keys():
        #print("({0}, {1})".format(kx, ky))
        for vx, vy in emp[kx, ky]:
            addx = vx*(-1)
            addy = vy*(-1)
            px = kx+(vx*(-1))
            py = ky+(vy*(-1))
            p = (px, py)
            while((px >=0 and px <= 3) and (py >= 0 and py <= 3)):
                #print(p, end="")
                if(field[p] == WHITE):
                    #print("WHITE")
                    pass
                elif(field[p] == BLACK):
                    if(not((kx, ky) in black_dic) and not((kx, ky) in black_possible)):
                        black_possible.append((kx, ky))
                        black_dic[(kx, ky)] = [(addx, addy)]
                    elif(((kx, ky) in black_dic) and ((kx, ky) in black_possible)):
                        black_dic[(kx, ky)].append((addx, addy))
                    #print("BLACK")
                    break
                else:
                    #print("EMPTY")
                    break
                px = px + addx
                py = py + addy
                p = (px, py)
            #print("({0}, {1})".format(kx+(vx*(-1)), ky+(vy*(-1))))
            #print("")
    # black_possibleから1つ選出する
    if(len(black_possible) == 0):
        return (-1, -1), [(0, 0)]
    r = random.randrange(len(black_possible))
    return black_possible[r], black_dic[black_possible[r]]


# 白石の手番
# 白石を置く座標とoffsetを返す
def white_turn():
    #黒石が置かれている場所のリスト
    black_stone = stone_location(BLACK)
    # 空マスの座標を返す
    emp = empty_location(black_stone)
    # 白石が置ける座標を返す
    white_possible = []
    white_dic = {}
    for kx, ky in emp.keys():
        #print("({0}, {1})".format(kx, ky))
        for vx, vy in emp[kx, ky]:
            addx = vx*(-1)
            addy = vy*(-1)
            px = kx+(vx*(-1))
            py = ky+(vy*(-1))
            p = (px, py)
            while((px >=0 and px <= 3) and (py >= 0 and py <= 3)):
                #print(p, end="")
                if(field[p] == WHITE):
                    if(not((kx, ky) in white_dic) and not((kx, ky) in white_possible)):
                        white_possible.append((kx, ky))
                        white_dic[(kx, ky)] = [(addx, addy)]
                    elif(((kx, ky) in white_dic) and ((kx, ky) in white_possible)):
                        white_dic[(kx, ky)].append((addx, addy))
                    #print("WHITE")
                    break
                elif(field[p] == BLACK):
                    #print("BLACK")
                    pass
                else:
                    #print("EMPTY")
                    break
                px = px + addx
                py = py + addy
                p = (px, py)
            #print("({0}, {1})".format(kx+(vx*(-1)), ky+(vy*(-1))))
            #print("")
    # black_possibleから1つ選出する
    if(len(white_possible) == 0):
        return (-1, -1), [(0, 0)]
    r = random.randrange(len(white_possible))
    return white_possible[r], white_dic[white_possible[r]]


# 盤面を更新する
# 更新されたfieldを返す
def update_field(TURN, point, offset_list):
    # 石を更新する座標を返す
    px = point[0]
    py = point[1]
    update_possible = []
    update_possible.append(point)
    for addx, addy in offset_list:
        vx = px
        vy = py
        value = point
        while((vx >=0 and vx <= 3) and (vy >= 0 and vy <= 3)):
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


# アドレスから座標に変換
# 座標を返す
def address2point(address):
    for i in range(0, 4):
        for j in range(0, 4):
            if(field_address[(i, j)] == address and field[(i, j)] == 0):
                return (i, j)
    return (-1, -1)

# 座標から石をひっくり返す方向を取得
# offsetを返す
# しかし、empty_locationと合わせるためひっくり返す石からみたoffset
def point2offset(point, TURN):
    #print("TURN", TURN)
    px = point[0]
    py = point[1]
    p2o_list = []
    for i in offset_x:
        for j in offset_y:
            vx = px + i
            vy = py + j
            p = (vx, vy)
            if((p[0] <= 3) and (p[0] >= 0) and (p[1] <= 3) and (p[1] >= 0) and (field[p] != TURN) and (field[p] != EMPTY)):
                vx = vx + i
                vy = vy + j
                p = (vx, vy)
                while((p[0] <= 3) and (p[0] >= 0) and (p[1] <= 3) and (p[1] >= 0)):
                    if(field[p] != TURN and field[p] != EMPTY):
                        #print(" not TURN and not EMPTY")
                        pass
                    elif(field[p] == TURN and field[p] != EMPTY):
                        #print("TURN")
                        p2o_list.append((i, j))
                        break
                    elif(field[p] != TURN and field[p] == EMPTY):
                        #print("EMPTY")
                        break
                    vx = vx + i
                    vy = vy + j
                    p = (vx, vy)
    return p2o_list


# 入力した手が有効な手であるか判断
# True or Falseを返す
def address_check(point, TURN):
    #TURNと反対の石が置かれている場所のリスト
    bw_stone = stone_location(3-TURN)
    # 空マスの座標を返す
    emp = empty_location(bw_stone)
    # TURNが置ける座標を返す
    stone_possible = []
    stone_dic = {}
    for kx, ky in emp.keys():
        for vx, vy in emp[kx, ky]:
            addx = vx*(-1)
            addy = vy*(-1)
            px = kx+(vx*(-1))
            py = ky+(vy*(-1))
            p = (px, py)
            while((px >=0 and px <= 3) and (py >= 0 and py <= 3)):
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

def othello16():

    """ define """
    # 4*4のオセロ
    # 空白＝０、　黒＝１、　白＝２
    global EMPTY
    EMPTY = 0
    global BLACK
    BLACK = 1
    global WHITE
    WHITE = 2

    global field
    field = np.array([[0,0,0,0],
                      [0,2,1,0],
                      [0,1,2,0],
                      [0,0,0,0]])

    global field_address
    #                        　  a,    b,    c,    d
    field_address = np.array([["a1", "b1", "c1", "d1"],  # 1
                              ["a2", "b2", "c2", "d2"],  # 2
                              ["a3", "b3", "c3", "d3"],  # 3
                              ["a4", "b4", "c4", "d4"]]) # 4
    
    global offset_x
    offset_x = [-1, 0, 1]
    global offset_y
    offset_y = [-1, 0, 1]

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
    print(field)
    print(field_address)
    num = 0
    before_field = field
    after_field = field
    while(num == 0):
        print("") # 改行
        # 黒の手番
        if(TURN == BLACK):
            point, offset_list = black_turn()
            if(TURN == Player):
                print("TURN : you")
                if(point == (-1, -1)):
                    print("pass")
                    print(field)
                    num = np.min(field)
                    TURN = WHITE
                    if((before_field == after_field).all()):
                        break
                    before_field = after_field
                    continue
                address = input("石を置く場所を指定してください : ")
                point = address2point(address)
                offset_list = point2offset(point, Player)
                if(not(address_check(point, TURN))):
                    print("「{0}」は無効な手です。".format(address))
                    print(field)
                    break
            else:
                print("TURN : computer")
            if((point == (-1, -1) and TURN == Player)):
                print("「{0}」は無効な手です。".format(address))
                print(field)
                break
            if((point == (-1, -1) and TURN == Computer)):
                print("pass")
                print(field)
                num = np.min(field)
                TURN = WHITE
                if((before_field == after_field).all()):
                    print("盤面上に打てるマスが無いため対局を終了します。")
                    break
                before_field = after_field
                continue
            field = update_field(TURN, point, offset_list)
            #before_field = after_field
            after_field = field
            TURN = WHITE
        # 白の手番
        elif(TURN == WHITE):
            point, offset_list = white_turn()
            if(TURN == Player):
                print("TURN : you")
                if(point == (-1, -1)):
                    print("pass")
                    print(field)
                    num = np.min(field)
                    TURN = BLACK
                    if((before_field == after_field).all()):
                        break
                    before_field = after_field
                    continue
                address = input("石を置く場所を指定してください : ")
                point = address2point(address)
                offset_list = point2offset(point, Player)
                if(not(address_check(point, TURN))):
                    print("「{0}」は無効な手です。".format(address))
                    print(field)
                    break
            else:
                print("computer")
            if((point == (-1, -1) and TURN == Player)):
                print("「{0}」は無効な手です。".format(address))
                print(field)
                break
            if((point == (-1, -1) and TURN == Computer)):
                print("pass")
                print(field)
                num = np.min(field)
                TURN = BLACK
                if((before_field == after_field).all()):
                    print("盤面上に打てるマスが無いため対局を終了します。")
                    break
                before_field = after_field
                continue
            field = update_field(TURN, point, offset_list)
            #before_field = after_field
            after_field = field
            TURN = BLACK
        else:
            print("error : TURN is not BLACK and WHITE")
            break

        print(field)
        num = np.min(field)
    return field


if __name__ == '__main__':
    field = othello16()
    black_stone = 0
    white_stone = 0
    for i in range(4):
        for j in range(4):
            stone = field[(i, j)]
            if(stone == 1):
                black_stone += 1
            elif(stone == 2):
                white_stone += 1
            else:
                pass
    winner = ""
    if(black_stone < white_stone):
        winner = "後手（白石）"
    elif(black_stone > white_stone):
        winner = "先手（黒石）"
    else:
        winner = ""

    print("")
    print("===================")
    print("結果発表")
    print("黒石：{0}石".format(black_stone))
    print("白石：{0}石".format(white_stone))
    print("")
    print("よって、勝者は「{0}」です。".format(winner))
