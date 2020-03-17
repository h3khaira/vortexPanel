import numpy as np
import matplotlib.pyplot as plt

class panels:
    # a panel object is used to keep track of parameters associated with each panel
    def __init__(self, coords):
        self.xcoords = coords[0]
        self.ycoords = coords[1]
        self.controlPoint=(np.median(self.xcoords),np.median(self.ycoords))
        self.phi = np.arctan2(self.ycoords[-1]-self.ycoords[0],self.xcoords[-1]-self.xcoords[0])
        self.s = np.sqrt((self.ycoords[-1]-self.ycoords[0])**2+(self.xcoords[-1]-self.xcoords[0])**2)

    def plot_controlPoint():
        plt.plot(self.controlPoint[0],self.controlPoint[1],'ob')

def draw_panel(x1,y1,x2,y2,step):
    #Draws a straight line between two points
    m=(y2-y1)/(x2-x1)
    b=y1-m*x1
    xcoord=np.arange(x1,x2,step)
    ycoord=m*xcoord+b
    plt.plot(xcoord,ycoord,'-b')
    return(xcoord,ycoord)

def split_into_panels(x,y,step,numPoints):
    firstThird = int(0.33*numPoints)
    secondThird = int(0.66*numPoints)
    panel_list=[]
    # splits airfoil into pairs of x and y coordinates representing each panel
    lastx=0
    lasty=0
    for xcoord, ycoord in zip(x[:firstThird][::smallPanel],y[:firstThird][::smallPanel]):
        panel_list.append(panels(draw_panel(lastx,lasty,xcoord,ycoord,step)))
        lastx=xcoord
        lasty=ycoord
    for xcoord, ycoord in zip(x[firstThird:secondThird][::largePanel],y[firstThird:secondThird][::largePanel]):
        panel_list.append(panels(draw_panel(lastx,lasty,xcoord,ycoord,step)))
        lastx=xcoord
        lasty=ycoord
    for xcoord, ycoord in zip(x[secondThird:numPoints][::smallPanel],y[secondThird:numPoints][::smallPanel]):
        panel_list.append(panels(draw_panel(lastx,lasty,xcoord,ycoord,step)))
        lastx=xcoord
        lasty=ycoord
    return(panel_list)



# Required inputs, airfoil number and chord length
airfoil = 4420
c = 1

m = (airfoil // 1000) / 100 * 1.0
p = ((airfoil // 100) % 10) / 10 * 1.0
t = airfoil % 100 / 100 * 1.0

numPoints = 1000
x = np.linspace(0, c, numPoints)

smallPanel=25
largePanel=50

yt = 5 * t * (0.2969 * np.sqrt(x / c) - 0.126 * (x / c) - 0.3516 *
              (x / c)**2 + 0.2843 * (x / c)**3 - 0.1015 * (x / c)**4)

yc = np.piecewise(x, [x <= p * c, x > p * c], [
    lambda x: m / p**2 * (2 * p * (x / c) - (x / c)**2), lambda x: m /
    (1 - p)**2 * ((1 - 2 * p) + 2 * p * (x / c) - (x / c)**2)
])

dyc = np.piecewise(x, [x <= p * c, x > p * c], [
    lambda x: 2 * m / p**2 * (p - (x / c)), lambda x: 2 * m / (1 - p)**2 *
    (p - (x / c))
])

theta = np.arctan(dyc)

xu = x - yt * np.sin(theta)
xl = x + yt * np.sin(theta)

yu = yc + yt * np.cos(theta)
yl = yc - yt * np.cos(theta)

listOfPanels = split_into_panels(xl,yl,c/numPoints,numPoints) + split_into_panels(xu,yu,c/numPoints,numPoints)
print(len(listOfPanels))

plt.plot(xu, yu, 'b-',linewidth=0.5)
plt.plot(xl, yl, 'b-',linewidth=0.5)
plt.xlim(0, c)
plt.ylim(-c, c)
plt.title('NACA ' + str(airfoil) + ' Airfoil')
plt.grid()
plt.xlabel("x/c")
plt.ylabel("t/c")
plt.show()
