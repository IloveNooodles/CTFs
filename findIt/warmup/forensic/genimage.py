import sys
import numpy as np
import pandas as pd
from imgpro import open_image
from imgpro import get_RGB
from PIL import Image

size = (1920,1112)
image = open_image('./ayaka.jpg', size)

r_channel,g_channel,b_channel = get_RGB(image)

img_grey = np.matrix((r_channel + g_channel + b_channel) / 3)
df = pd.DataFrame(data=img_grey.astype(float))

df.to_csv('peserta/chall.txt', sep=',', header=False, float_format='%.2f', index=False)

