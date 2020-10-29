from janome.tokenizer import Tokenizer
import csv
def negaposi_check(words):
    t = Tokenizer()
    #ネガポジ辞書作成
    np_dic = {}
    fp = open("../dictonary/pn.csv","rt",encoding="utf-8")
    reader = csv.reader(fp,delimiter='\t')
    for i, row in enumerate(reader):
        name = row[0]
        result = row[1]
        np_dic[name] = result

#入力文字をネガティブがポジティブがチェックする
    token = t.tokenize(words,wakati=True)

    #ネガポジカウンター
    pn = {'p':0,'n':0,'e':0}


    for i,word in enumerate(token):
        #まず最初に辞書にあるか否かチェック
        try:
            checker = np_dic[word]
        except KeyError:
            continue

        if checker=='p':
            pn["p"]+=1
        elif checker=="n":
            pn["n"]+=1
        elif checker=="e":
            pn["e"]+=1
        #print("{}文字目 : {}".format(i,word))

    max_key,max_value = max(pn.items(),key=lambda x:x[1])

    if max_value >= 5 and max_key == 'p':
        return("めっちゃポジティブだねぇ!!")
    elif max_value >= 5 and max_key == 'n':
        return("めっちゃネガティブだねぇ!!")
    elif max_value >= 5 and max_key == 'e':
        return("感情が普通らしいぞ もっと感情揺さぶられる体験をしろ!!")
    else:
        return("とにかく言うことはない。そのままの君でいてくれ")
