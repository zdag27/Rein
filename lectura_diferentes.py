import matplotlib.pyplot as plt
with open('out.txt','r', encoding='utf-8') as f:
	lines=f.readlines()
total=len(lines)-2
x=[]
y=[]
diff=0
num=0
for line in lines:
	lst=line.split(",")
	if(len(lst)==3):
		diff=diff+1
		num=num+int(lst[0])
		y.append(diff)
		x.append(num)
print (x[10000],y[10000]);
print (x[35000],y[35000]);
print(total)
plt.plot(x,y)
plt.show()
