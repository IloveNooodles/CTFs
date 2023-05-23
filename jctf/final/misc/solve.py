from PIL import Image

# Open the three images
image1 = Image.open("flag1.png")
image2 = Image.open("flag2.png")
image3 = Image.open("flag3.png")

red, green, blue, aplha = image2.split()

# Save the combined image
red.save("im2_red.png")
blue.save("im2_blue.png")
green.save("im2_green.png")
