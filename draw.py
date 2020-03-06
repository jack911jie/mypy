import numpy as np
import matplotlib.pyplot as plt
import seaborn

# 中文和负号的正常显示
plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False

# 使用ggplot的绘图风格
plt.style.use('ggplot')

# 构造数据
values = [3.2,2.1,3.5,2.8,3]
feature = ['个人能力','QC知识','解决问题能力','服务质量意识','团队精神']

# N = len(values)
N=np.arange(0,2*np.pi,0.02)




# 绘图
fig=plt.figure()
# 这里一定要设置为极坐标格式
ax = fig.add_subplot(111, projection='polar', fc='#3DBCE3',alpha=0.08)
# 绘制折线图
ax.plot(N, 2*N, '-', linewidth=1)

# 填充颜色
#ax.fill(angles, values, alpha=0.25)
# 添加每个特征的标签
#ax.set_thetagrids(angles * 180/np.pi, feature)
# 设置雷达图的范围
# ax.set_ylim(0,5)
# 添加标题
plt.title('活动前后员工状态表现')
# 添加网格线
ax.grid(True,color='k',alpha=0.2)
# 显示图形
plt.show()