
def draw_panel(x1,y1,x2,y2,step):
    #Draws a straight line between two points
    m=(y2-y1)/(x2-x1)
    b=y1-m*x1
    xcoord=np.arange(x1,x2,step)
    ycoord=m*xcoord+b
    plt.plot(xcoord,ycoord,'-b')
    return(xcoord,ycoord)

def split_into_panels(x,y,step,numPoints,smallPanel,largePanel):
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

