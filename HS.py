from bs4 import BeautifulSoup
import xlwt,os,time,requests
from sheen import Str

page = 1 #起始管卡
total_pages = 20 #总游戏关卡，爬10关请设定为11
count = 1 #每抓到一次游戏名称增加一次，用来排序
pool=[] #每次抓到的游戏名称都会放进pool列表里，用来去重
document = 'hs' #设定爬取的数据存的excel的档案名称
wb = xlwt.Workbook() #创建excel
ws = wb.add_sheet("TopSellers") #在excel新增一个sheet页
ws.write(0,0,'hs')#参数
ws.write(0,1,'分数') #在excel第一行第二列先行写入'Game Title'
ws.write(0,2,'姓名') #在excel第一行第三列先行写入'Released Date'
f = open("hs.txt",'w')#用于写入成绩，然后一键上传成绩
root = os.getcwd() #获取当前工作路径
date = '' #获取当前日期 格式为yyyymmdd
list45 =[3827574,3827575,3827576,3827578,3827579,3827580,3827581,3827582,3827586,3827587,3827588,3827589,3951857,3951858,3951859,3951860,3951862,3951863,4007344]
listbo =[3827557,3827560,3827561,3827562,3827563,3827564,3827565,3827566,3827567,3827568,3827569,3827570,3951841,3951842,3951843,3951844,3951845,3951846,4007340]
lisths =[3595540,3595543,3595547,3595549,3595550,3595551,3595552,3595553,3595554,3595556,3595557,3595558,3951832,3951833,3951835,3951836,3951837,3951839,4007339]
listsr =[3595541,3635754,3595562,3595563,3595564,3595565,3595566,3595567,3595568,3595569,3595570,3595571,3951847,3951848,3951853,3951854,3951855,3951856,4007341]
#获取页面关卡

while page<total_pages:


    url = 'https://steamcommunity.com/stats/1114430/leaderboards/%s' %str(lisths[page-1]) #设定url，变量控制页数
    r = requests.session()
    res = r.get(url).text
    soup = BeautifulSoup(res,"html.parser")
    game_scores = soup.find('div',attrs={'class':'score'}) # 遍历第一名div的标签，且class属性值为'score' 即分数
    game_names = soup.find('a',attrs={'class':'playerName'}) #第一名的名字
    if game_scores is None:
        game_scores = soup.find('h1')
    if game_names is None:
        game_names=soup.find('h1')
    for game_score, game_name in zip(game_scores,game_names): #同时遍历连个列表的方法 for x,y in zip(xs,ys):

            fenshu=int(game_score.string.replace(',',''))
            print('第%s关 .分数：%s 姓名：%s' % (page,fenshu,game_name.string)) #打印给自己看的
            pool.append(game_score.string) #把爬到的数据增加到pool列表里
            ws.write(count,0,'第%s关'%page) #往excel写入编号
            
            ws.write(count,1,fenshu) #往excel写入游戏分数
            ws.write(count,2,game_name.string) #往excel写入第一名
            name=game_name.string
            if game_name.string!='xxxx':
                print(Str.red.BLACK.Bold('第%s关 .分数：%s 需要更新' % (page,fenshu))) #突出非自己名字显示红色

            count += 1 #每遍历一次 count 变量 +1 ，用来排序写入excel里的顺序
    rate = page / (total_pages - 1)
    print('--------------------------第%s关爬取完成--------------------已完成: %.2f%%' % (str(page),(rate * 100)))
    page += 1
    wb.save('%s%s.xls' % (document,date)) #保存excel
    f.write("%s\n" % fenshu) #保存txt,在游戏种一键读取并上传成绩
print('--------------------------爬取完成--------------------------')
print('所有数据已存至：%s\%s%s.xls' % (root,document,date))
