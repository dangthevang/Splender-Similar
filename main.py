from numpy.core.fromnumeric import take
from base.player import Player
from base import board
from players import player5_Phong as p1
from players import player6_HungThom as p2
from players import player7_MA as p3
from players import player2_Trang as p4
import pandas as pd
import random
from CodeDuDoan import DuDoan

def Victory(arr):
    global pVictory
    arr_point = [i.score for i in arr]
    max_point = max(arr_point)
    if max_point >= 15:
      arr_point = [1 if i == max_point else 0 for i in arr_point]
      arr_amount_card = [len(i.card_open) for i in arr]
      min = 100
      for i in range(len(arr_point)):
        if arr_point[i] == 1 and arr_amount_card[i] < min:
          min = arr_amount_card[i]
          pVictory = arr[i]
    return pVictory

def save_excel(b ,arr,turn):
  result = {}
  result[b.name + " Stocks"] = b.stocks.copy()
  for i in b.dict_Card_Stocks_Show.keys():
    result[b.name +" "+ i] = [j.id for j in b.dict_Card_Stocks_Show[i]]
  for i in b.dict_Card_Stocks_UpsiteDown.keys():
    result[b.name +"UpsiteDown"+ i] = [j.id for j in b.dict_Card_Stocks_UpsiteDown[i]]
  for i in arr:
    result[i.name + " Score"] = i.score
    result[i.name + " Stocks"] = i.stocks.copy()
    result[i.name + " Stocks Const"] = i.stocks_const.copy()
    result[i.name + " Open"] = [j.id for j in i.card_open]
    result[i.name + " Noble"] = [j.id for j in i.card_noble]
    result[i.name + " Upsite Down"] = [j.id for j in i.card_upside_down]
  result["Turn"] = turn
  return result

# df_message = pd.DataFrame({"Action":[]})
# arr_message = []
# def saveAction(t):
#   arr_message.append(t)

# def checkNone(b,player,turn):
#   saveAction("Lượt: " + str(turn) +" "+player.message)
#   if b == None:
#     print("Lỗi của :",player.name)

def RunGame():
    b = board.Board()
    b.LoadBase()
    b.setupCard()
    turn = 0
    result_turn = []
    arr_stt = [1,2,3,4]
    random.shuffle(arr_stt) 
    # for i in range(len(arr_stt)):
    #     if arr_stt[i] == 1:
    #       p1.player_01.setName = p1.player_01.name +" "+ str(i+1)
    #     elif arr_stt[i] == 2:
    #       p2.player_02.setName = p2.player_02.name +" "+ str(i+1)
    #     elif arr_stt[i] == 3:
    #       p3.player_03.setName = p3.player_03.name +" "+ str(i+1)
    #     elif arr_stt[i] == 4:
    #       p4.player_04.setName = p4.player_04.name +" "+ str(i+1)
    # result_turn.append(save_excel(b ,[p1.player_01, p2.player_02, p3.player_03, p4.player_04]))
    p = Victory([p1.player_01, p2.player_02, p3.player_03, p4.player_04])
    while p.name == "0":
        turn+=1
        # print("Luot: ", turn)
        for i in arr_stt:
          if i == 1:
            b = p1.action(b, [p2.player_02, p3.player_03, p4.player_04])
          elif i == 2:
            b = p2.action(b, [p1.player_01, p3.player_03, p4.player_04])
          elif i == 3:
            b = p3.action(b, [p1.player_01, p2.player_02, p4.player_04],turn)
          else:
            b = p4.action(b, [p1.player_01, p2.player_02, p3.player_03])
        if turn > 0 and turn <=30:
          a = save_excel(b ,[p1.player_01, p2.player_02, p3.player_03, p4.player_04],turn)
          result_turn.append(a)
        if turn == 17:
          w = DuDoan.DuDoan(pd.json_normalize([a],max_level=0))
        p = Victory([p1.player_01, p2.player_02, p3.player_03, p4.player_04])
    data = pd.json_normalize(result_turn,max_level=0)
    print("So vong choi: ",turn)
    # data["win"] = [p.name for i in range(6)]
    return data,w

pVictory = Player("0", 0)
arr_scale = [0,0,0,0]
def check():
  for i in arr_scale:
    if i < 100:
      return True
  return False
data_last = pd.DataFrame({})
lan = 0
dudoan = 0
while True:
    data_last = pd.DataFrame({})
    lan +=1
    print(lan)
    if lan == 100:
      break
    pVictory = Player("0", 0)
    p1.player_01 = p1.player.Player("1", 0)
    p2.player_02 = p2.player.Player("2", 0)
    p3.player_03 = p3.player.Player("3", 0)
    p4.player_04 = p4.player.Player("4", 0)
    try:
      t,winWill = RunGame()
      print("Win That: ",pVictory.name, "WinDoan: ", winWill)
      if pVictory.name == winWill:
        dudoan+=1
      if arr_scale[int(pVictory.name)-1] < 100:
        data_last = data_last.append(t)
        arr_scale[int(pVictory.name)-1]+=1
        data_last.to_csv("DataTrain/"+str(lan) + ".csv",index=False)
        print(arr_scale)
    except:
      lan-=1
print("So tran doan dung: ",dudoan)





