from PIL import Image, ImageChops
import numpy as np

first_image = Image.open("flag.png")
second_image = Image.open("lemur.png")


n1 = np.array(first_image)
n2 = np.array(second_image)

# print(n1)
n3 = np.bitwise_xor(n1, n2).astype(np.uint8)
Image.fromarray(n3).save("flag_real.png")
# im3 = ImageChops.add(ImageChops.subtract())


# img = Image.frombytes("RGB", (320, 240), pwn.xor(first_image, second_image))
# img.save("test.png")
