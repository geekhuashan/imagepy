from sciapp.action import Free
from skimage import data
import numpy as np
# 替换scipy.misc.face，现在从其他地方获取

class Data(Free):
    def __init__(self, title):
        self.title = title
        # 修复face和ascent不在misc中的问题
        if title == 'face':
            # 使用skimage.data.astronaut替代face
            self.data = data.astronaut
        elif title == 'ascent':
            # 使用其他图像替代ascent
            self.data = data.camera
        elif hasattr(data, title):
            self.data = getattr(data, title)
        else:
            # 防止错误
            self.data = data.camera

    def run(self, para = None):
        img = self.data()
        if isinstance(img, tuple):
            return self.app.show_img(list(img), self.title)
        if img.dtype == 'bool': 
            img.dtype = np.uint8
            img *= 255
        self.app.show_img([img], self.title)

    def __call__(self): return self

# 移除不存在的数据集，只保留skimage.data中有的
datas = ['-', 'binary_blobs', 'astronaut', 'camera', 'cell', 
    'checkerboard', 'chelsea', 'clock', 'coffee', 'coins',
    'horse', 'page', 'text', 'rocket']

plgs = [i if i=='-' else Data(i) for i in datas]