import datetime

temp=str(datetime.date.today()).split('-')
temp0=[[0, 60, 70], [0, 10, 20], [0, 30, 90], [0, 58, 40], [0, 75, 4], [0, 54, 20], [str(datetime.date.today()), 1, 0]]

for i in range(1,7):
    delta=datetime.timedelta(days=i)
    temp0[6-i][0]=str(datetime.date(int(temp[0]),int(temp[1]),int(temp[2]))-delta)
temp=temp0
with open('wordslist_test.py','w') as f:
	f.write("wordslist={'%s':{'1':'1'}}\ndaka={'L_D':'%s','CON':9,'TOT':9}\nMap=%s\nMap0=0"%(str(datetime.date.today()),str(datetime.date.today()),str(temp)))
