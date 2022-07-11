import os
import io
import streamlit as st
from math import ceil

PIL_GRAYSCALE = 'L'
PIL_WIDTH_INDEX = 0
PIL_HEIGHT_INDEX = 1

def lines_to_image(lines):
    font = ImageFont.load_default()

    # make a sufficiently sized background image based on the combination of font and lines
    font_points_to_pixels = lambda pt: round(pt * 96.0 / 72)
    margin_pixels = 20

    # height of the background image
    tallest_line = max(lines, key=lambda line: font.getsize(line)[PIL_HEIGHT_INDEX])
    max_line_height = font_points_to_pixels(font.getsize(tallest_line)[PIL_HEIGHT_INDEX])
    realistic_line_height = max_line_height * 0.8  # apparently it measures a lot of space above visible content
    image_height = int(ceil(realistic_line_height * len(lines) + 2 * margin_pixels))

    # width of the background image
    max_line_width = font.getsize(lines[0])[PIL_WIDTH_INDEX]
    image_width = int(ceil(max_line_width + (2 * margin_pixels)))

    # draw the background
    background_color = 0  # white
    image = Image.new(PIL_GRAYSCALE, (image_width, image_height), color=background_color)
    draw = ImageDraw.Draw(image)

    # draw each line of text
    font_color = 255  # black
    horizontal_position = margin_pixels
    for i, line in enumerate(lines):
        vertical_position = int(round(margin_pixels + (i * realistic_line_height)))
        draw.text((horizontal_position, vertical_position), line, fill=font_color, font=font)

    return image


def lines_to_color_image(lines):
    font = ImageFont.load_default()

    # make a sufficiently sized background image based on the combination of font and lines
    font_points_to_pixels = lambda pt: round(pt * 96.0 / 72)
    margin_pixels = 20

    # height of the background image
    tallest_line = max(lines, key=lambda line: font.getsize(line)[PIL_HEIGHT_INDEX])
    max_line_height = font_points_to_pixels(font.getsize(tallest_line)[PIL_HEIGHT_INDEX])
    realistic_line_height = max_line_height * 0.8  # apparently it measures a lot of space above visible content
    image_height = int(ceil(realistic_line_height * len(lines) + 2 * margin_pixels))

    # width of the background image
    strings = [i[0] for i in lines[0]]
    string = ''.join(strings)

    max_line_width = font.getsize(string)[PIL_WIDTH_INDEX]
    image_width = int(ceil(max_line_width + (2 * margin_pixels)))


    # draw the background
    image = Image.new("RGBA", (image_width, image_height), color=(0, 0, 0, 255))
    draw = ImageDraw.Draw(image)

    horizontal_position = margin_pixels

    total_lines = len(lines)
    for i, line in enumerate(lines):
        for q, txt_col in enumerate(line):
            vertical_position = int(round(margin_pixels + (i * realistic_line_height)))
            draw.text((horizontal_position + (6 * q), vertical_position), txt_col[0], fill=txt_col[1], font=font)

        my_bar.progress(((i * 100) // total_lines))

    return image

from PIL import (
    Image,
    ImageOps,
    ImageFont,
    ImageDraw,
)

st.write("""
# Image to Ascii converter!
Convert any image to Ascii art. Larger images take significantly longer to convert. Scroll down to see the progress bar,
and converted images.
""")

# get the image
image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg", "gif"])

#example button
example = st.button("See an Example")
if example:
    image = "img.png"

if image is not None:
    st.image(image, use_column_width=True)

    with st.spinner('Converting image...'):
        my_bar = st.progress(0)
        file = ""
        lines = []
        colored_lines = []

        im = Image.open(image)

        pix = im.load()

        pixel_ascii_map = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

        countx = 0
        for x in range(0, im.size[1]):
            printsting = ""
            county = 0
            colored_lines.append([])
            for i in range(0, im.size[0]):
                pixel = pix[county, countx]
                brightness = (pixel[0] + pixel[1] + pixel[2]) // 3
                ascii_val = pixel_ascii_map[brightness * (len(pixel_ascii_map) - 1) // 255]
                colored_lines[-1].append((ascii_val, pixel))
                printsting += ascii_val

                county += 1

            file += (printsting + "\n")
            lines.append(printsting)
            countx += 1

        image = lines_to_color_image(colored_lines)
        image2 = lines_to_image(lines)


        output = io.BytesIO()
        image.save(output, format='PNG')

        output2 = io.BytesIO()
        image2.save(output2, format='PNG')

        my_bar.progress(100)

    st.success('Done! Scroll down to see the result.')
    colum1, colum2 = st.columns([1, 1])
    with colum1:
        st.image(output, use_column_width=True)
    with colum2:
        st.image(output2, use_column_width=True)

    st.balloons()

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.download_button(
            label="Download color image",
            data=output.getvalue(),
            file_name="output.png",
            mime="image/png"
        )

    with col2:
        st.download_button(
            label="Download plain text image",
            data=output2.getvalue(),
            file_name="output.png",
            mime="image/png"
        )

    with col3:
        st.download_button(
            label="Download as text",
            data=file,
            file_name="output.txt",
            mime="text/plain"
        )

st.markdown("Made by [Noah Virjee](https://blucardin.github.io/) © 2022. You can use the code, but please credit me.", unsafe_allow_html=True)