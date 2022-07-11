from PIL import Image, ImageOps
# import moviepy.editor as mp

lists = [""]

for x in range(1, 26):

    variable = "img.png"

    im = Image.open(variable)
    gray_image = ImageOps.grayscale(im)
    gray_image.show()

    print(variable)
    pix = gray_image.load()
    print(im.size)

    f = open("output" + str(x) + ".txt", "w")

    pixel_ascii_map = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

    countx = 0
    for x in range(0, im.size[1]):
        printsting = ""
        county = 0
        for i in range(0, im.size[0]):
            brightness = pix[county, countx]
            ascii_val = pixel_ascii_map[brightness * (len(pixel_ascii_map) - 1) // 255]
            printsting = printsting + ascii_val

            county += 1

        f.write(printsting + "\n")
        countx += 1

