import pydicom
import matplotlib.pyplot as plt
import scipy.misc

in_path = './input.dcm'
out_path = './output.jpg'
ds = pydicom.read_file(in_path)  #读取.dcm文件
img = ds.pixel_array  # 提取图像信息
print(img.shape)
plt.imshow(img)
plt.show()
scipy.misc.imsave(out_path,img)  #