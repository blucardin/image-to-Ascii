from PIL import Image, ImageOps

lists = [""]
variable = "img.png"

im = Image.open(variable)
im.show()

print(variable)
pix = im.load()
print(im.size)

f = open("output2.txt", "w")

pixel_ascii_map = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

countx = 0
for x in range(0, im.size[1]):
    printsting = ""
    county = 0
    for i in range(0, im.size[0]):
        pixel = pix[county, countx]
        print(pixel)
        brightness = (pixel[0] + pixel[1] + pixel[2]) // 3
        ascii_val = pixel_ascii_map[brightness * (len(pixel_ascii_map) - 1) // 255]
        printsting += ascii_val

        county += 1

    f.write(printsting + "\n")
    countx += 1

