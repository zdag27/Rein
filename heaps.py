import matplotlib.pyplot as plt
x=[]
y=[]
K=598.563
b=0.29872
n=15000
while n<18000:
	y.append(K*(n**b))
	x.append(n)
	n=n+1
	print(n)
plt.plot(x,y)
plt.show()
