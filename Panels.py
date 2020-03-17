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
    for xcoord, ycoord in zip(x[smallPanel:firstThird][::smallPanel],y[smallPanel:firstThird][::smallPanel]):
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

# account for the last two panels
    panel_list.append(panels(draw_panel(lastx,lasty,x[-1],0,step)))
    return(panel_list)

def findJ(paneli,panelj):
    # this is straightforward math as described in the panel method
    xi = paneli.controlPoint[0]
    yi = paneli.controlPoint[1]
    xj = panelj.xcoords[0]
    yj = panelj.ycoords[0]
    sj = panelj.s
    phii = paneli.phi
    phij = panelj.phi

    A = -(xi-xj)*np.cos(phij) - (yi-yj)*np.sin(phij)
    B = (xi-xj)**2 + (yi-yj)**2
    C = -np.cos(phii-phij)
    D = (xi-xj)*np.cos(phii) + (yi-yj)*np.sin(phii)
    E = np.sqrt(B-A**2)
    J = C/2*np.log((sj**2+2*A*sj+B)/B)+(D-A*C)/E*(np.arctan2(sj+A,E)-np.arctan2(A,E))
    return(J)

def findLift (listOfPanels,freestream,alpha,lastPanelIndex):
    # initialize empty matrices so we dont have to append a matrix every iteration
    JMatrix = np.empty ([len(listOfPanels),len(listOfPanels)])
    RHSMatrix = np.empty(len(listOfPanels))
    for i,paneli in enumerate(listOfPanels):
        for j,panelj in enumerate(listOfPanels):
            if paneli == panelj:
                # the diagonal of the matrix with all the J values is equal to pi
                JMatrix[i,j]= np.pi
            else:
                JMatrix[i,j]= findJ(paneli,panelj)
        RHSMatrix[i] = -freestream*2*np.pi*np.sin(paneli.phi-alpha)

    # need to remove one row in the matrix and then impose kutta condition
    removed_row = len(listOfPanels) -4
    JMatrix = np.delete(JMatrix,removed_row,0)
    RHSMatrix = np.delete(RHSMatrix, removed_row,0)

    new_row = np.zeros(len(listOfPanels))
    new_row[lastPanelIndex] = 1
    new_row[-1] = 1
    JMatrix = np.vstack([JMatrix,new_row])
    RHSMatrix = np.append(RHSMatrix,0)

    X = np.linalg.solve(JMatrix,RHSMatrix)
    lift= 0
    for i, panel in enumerate(listOfPanels):
        lift =lift + X[i]*panel.s

    return(lift)

# Required inputs, airfoil number and chord length
airfoil = 4418
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

fig1 = plt.figure()
botPanels= split_into_panels(xl,yl,c/numPoints,numPoints)
topPanels = split_into_panels(xu,yu,c/numPoints,numPoints)
listOfPanels = topPanels + botPanels

freestream = 1
alpha_range = [-10,15]
alpha_deg = np.linspace(alpha_range[0],alpha_range[1],alpha_range[-1]-alpha_range[0])
alpha = alpha_deg*np.pi/180
cl = np.empty(len(alpha))
for i,a in enumerate(alpha):
    cl[i] = findLift(listOfPanels,freestream,a, len(topPanels)-1)


fig1
plt.plot(xu, yu, 'b-',linewidth=0.5)
plt.plot(xl, yl, 'b-',linewidth=0.5)
plt.xlim(0, c)
plt.ylim(-c, c)
plt.title('NACA ' + str(airfoil) + ' Airfoil')
plt.grid()
plt.xlabel("x/c")
plt.ylabel("t/c")

fig2 = plt.figure()
plt.grid()
plt.plot(alpha_deg,cl)
plt.title('NACA ' + str(airfoil) + ' Airfoil Cl vs Angle of Attack')
plt.xlabel('Angle of Attack (\u00b0)')
plt.ylabel('Cl')
plt.xlim(alpha_range)
plt.show()

print(listOfPanels[-1].xcoords)
