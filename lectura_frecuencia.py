import matplotlib.pyplot as plt
with open('out.txt','r', encoding='utf-8') as f:
	lines=f.readlines()
total=len(lines)-2
x=[]
y=[]
for line in lines:
	lst=line.split(",")
	if(len(lst)==3):
		y.append(int(lst[0]))
		x.append(int(lst[2].replace(" ","")))
print (x[26000],y[26000]);
print (x[18000],y[18000]);
plt.plot(x,y)
plt.show()
