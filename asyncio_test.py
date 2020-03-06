import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.axisartist as axisartist


def round_s(r,a,b,x):
    y1=b+pow(r*r-(x-a)*(x-a),0.5)
    y2=b-pow(r*r-(x-a)*(x-a),0.5)
    y=[y1,y2]
    return y

def draw():
    r=50
    a=25
    b=25
    x=np.linspace(-100,100,5000)
    y3=[]
    y4=[]
    xx=20
    try:
        for i in x:
            y=round_s(r,a,b,i)
            y3.append(y[0])
            y4.append(y[1])
            # print(x,y)
        yy=round_s(r,a,b,xx)

    except:
        ...
    try:
        fig=plt.figure(1,figsize=(6,6))
        ax=axisartist.Subplot(fig, 111)
        # 通过set_visible方法设置绘图区所有坐标轴隐藏
        ax.axis[:].set_visible(False)
        fig.add_axes(ax)

        # ax.new_floating_axis代表添加新的坐标轴
        ax.axis["x"] = ax.new_floating_axis(0, 0)
        # 给x坐标轴加上箭头
        # ax.axis["x"].set_axisline_style("-", size=1.0)
        # 添加y坐标轴，且加上箭头
        ax.axis["y"] = ax.new_floating_axis(1, 0)
        # ax.axis["y"].set_axisline_style("-.", size=1.0)
        # 设置x、y轴上刻度显示方向
        ax.axis["x"].set_axis_direction("top")
        ax.axis["y"].set_axis_direction("left")
        plt.gca().invert_xaxis()
        plt.scatter(y3,x,s=5,c='b')
        plt.scatter(y4,x,s=5,c='b')
        plt.scatter(b,a,s=8,c='g')
        plt.scatter(yy[0],xx,s=40,c='r')
        plt.scatter(yy[1], xx, s=40, c='r')

        plt.show()
    except:
        pass

draw()

