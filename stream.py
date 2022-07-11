import os
import io
import streamlit as st
from math import ceil
import imagemaker

from PIL import (
    Image,
    ImageOps,
    ImageFont,
    ImageDraw,
)

st.write("""
# Streamlit Tutorial
This is a simple Streamlit tutorial.
""")

# get the image
image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg", "gif"])
if image is not None:
    st.image(image, use_column_width=True)

    lists = [""]

    im = Image.open(image)
    gray_image = ImageOps.grayscale(im)

    print(image)
    pix = gray_image.load()
    print(im.size)

    output = ""
    lines = []

    pixel_ascii_map = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

    countx = 0
    for x in range(0, im.size[1]):
        printsting = ""
        county = 0
        for i in range(0, im.size[0]):
            brightness = pix[county, countx]
            ascii_val = pixel_ascii_map[brightness * (len(pixel_ascii_map) - 1) // 255]
            printsting += ascii_val

            county += 1

        output += (printsting + "\n")
        lines.append(printsting)
        countx += 1

    image = imagemaker.lines_to_image(lines)

    output = io.BytesIO()
    image.save(output, format='PNG')

    btn = st.download_button(
        label="Download image",
        data=output.getvalue(),
        file_name="output.png",
        mime="image/png"
    )

    st.download_button(
        label="Download as png",
        data=output,
        file_name="output",
        mime="text/plain"
    )
