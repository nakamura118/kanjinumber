from fastapi import FastAPI,status,Response
from starlette.middleware.cors import CORSMiddleware # 追加
import re #文字列分割用標準ライブラリ

app = FastAPI()

# CORSを回避するために追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

@app.get("/v1/number2kanji/{number}",status_code=status.HTTP_200_OK)
def number2kanji(number,response: Response):
    judge=str(number)#変換出来るかどうか判定のため文字列に位変換
    #取り扱い可能ではない場合
    if(("." in judge) or ("-" in judge) or (len(judge)>16)):
        return Response(status_code = status.HTTP_204_NO_CONTENT)   
         
    number=int(number)#どんな形でもint型に変換
    decimalList=["零","壱","弐","参","四","五","六","七","八","九"]#0～9の値
    digitsList=["","拾","百","千"]#一，十，百，千の位
    tenthousandList=["万","億","兆"]#万，億，兆の位
    kanji:str=""#返り値
    girderDivision:int=10000#4桁句切り用
    tenDivision:int=10#千百拾一の位用
    #0の時
    if(number==0):return {"result":decimalList[0]}
    #x兆x億x万xの4回
    for i in range(4):
        numberThousand=number%girderDivision#桁区切り
        number=number//girderDivision#下4桁を切り捨てる
        for j in range(4):#x千x百x拾xの4回
            tmpNumber=numberThousand%tenDivision#一番右側の数の値を取得
            numberThousand=numberThousand//tenDivision#桁数減らす
            #0の時，後の処理をスキップする
            if(decimalList[tmpNumber]=="零"):continue
            else:
                kanji=digitsList[j]+kanji#拾，百，千を挿入
                kanji=decimalList[tmpNumber]+kanji#壱～九を挿入                  
            if(numberThousand==0):break#numberThousandが0になると終わり             
        if(number==0):break#numberが0になると終わり
        kanji=tenthousandList[i]+kanji#万，億，兆の位を挿入
    #兆憶万が連続してはいけないため
    if("兆億"in kanji):kanji=kanji.replace("億","")
    if(("億万"in kanji)or("兆万"in kanji)):kanji=kanji.replace("万","")  
    
    return {"result":kanji}


@app.get("/v1/kanji2number/{kanjiNumber}",status_code=status.HTTP_200_OK)
def kanji2number(kanjiNumber: str):
    tenthousandKanji=["兆","億","万"]#兆,億,万の位(漢数字)
    tenthousandNumber=[(10**12),(10**8),(10**4)]#兆,億,万の位(数字)
    number:int=0#返り値
    
    if(len(kanjiNumber)==0):
        return Response(status_code = status.HTTP_204_NO_CONTENT) 
    
    if(kanjiNumber=="零"):return 0 
    try:
        for i in range(3):#兆,億,万の位用
            if(tenthousandKanji[i] in kanjiNumber):#"兆","億","万"を含むとき
                #"兆"or"億"or"万"で分割
                kanjiNumber=kanjiNumber.split(tenthousandKanji[i])
                #対応するdigitsNumberと兆,億,万の前の漢数字を掛ける
                number+=tenthousandNumber[i]*thousandChange(kanjiThousand=kanjiNumber[0])
                kanjiNumber=kanjiNumber[1]#kanjiNumberを更新
        if(len(kanjiNumber)!=0):#万より下の桁用
            number+=thousandChange(kanjiThousand=kanjiNumber)
    except(TypeError):
        return Response(status_code = status.HTTP_204_NO_CONTENT)    

    return {"result":number}

def thousandChange(kanjiThousand:str):
    thousandNumber:int=0#返り値
    digitsKanji=["千","百","拾"]#千,百,十の位(漢数字)
    digitsNumber=[1000,100,10]#千,百,十の位(数字)
    decimal={""  : 0,#漢数字のとき途中の零は書かないため
             "壱": 1,
             "弐": 2,
             "参": 3,
             "四": 4,
             "五": 5,
             "六": 6,
             "七": 7,
             "八": 8,
             "九": 9}#0～9の値
    try:
        for i in range(3):#千,百,十,一の位の4回繰り返す
            if(kanjiThousand==""):break
            elif(digitsKanji[i] in kanjiThousand):#千,百,十の位用
                #千,百,十で分割
                kanjiThousand=kanjiThousand.split(digitsKanji[i])
                if(len(kanjiThousand)!=2):#千,百,十で同じものが含まれている場合
                    return "error" #kanji2numberでエラー起こす用
                #対応するdigitsNumberと千，百，拾の前の漢数字を掛ける
                thousandNumber+=digitsNumber[i]*decimal[kanjiThousand[0]]
                kanjiThousand=kanjiThousand[1]#値の更新
        if(len(kanjiThousand)!=0):#一の位用
            #対応するdigitsNumberと分割後の一番右側の漢数字を掛ける
            thousandNumber+=decimal[kanjiThousand]
    except(KeyError,IndexError):
        return "error" #kanji2numberでエラー起こす用
    return int(thousandNumber)

