import matplotlib.pyplot as plt
x=[]
y=[]
K=38804.76429
a=0.49
r=500
while r<1000:
	y.append(K/(r**a))
	x.append(r)
	r=r+1
	print(r)
plt.plot(x,y)
plt.show()
