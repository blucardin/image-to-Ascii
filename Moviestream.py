import os
import io
import time

import streamlit as st
from math import ceil
from PIL import (
    Image,
    ImageOps,
    ImageFont,
    ImageDraw,
)
import moviepy.editor as mp

PIL_GRAYSCALE = 'L'
PIL_WIDTH_INDEX = 0
PIL_HEIGHT_INDEX = 1


def image_to_ascii(image):
    lines = []

    im = image
    pix = im.load()

    pixel_ascii_map = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

    for x in range(0, im.size[1]):
        printsting = ""
        lines.append([])
        for y in range(0, im.size[0]):
            pixel = pix[y, x]
            brightness = (pixel[0] + pixel[1] + pixel[2]) // 3
            ascii_val = pixel_ascii_map[brightness * (len(pixel_ascii_map) - 1) // 255]
            lines[-1].append((ascii_val, pixel))
            printsting += ascii_val

    font = ImageFont.load_default()
    margin_pixels = 20
    realistic_line_height = 10
    image_height = realistic_line_height * len(lines) + 2 * margin_pixels

    # width of the background image
    strings = [i[0] for i in lines[0]]
    string = ''.join(strings)

    max_line_width = font.getsize(string)[PIL_WIDTH_INDEX]
    image_width = int(ceil(max_line_width + (2 * margin_pixels)))

    # draw the background
    canvas = Image.new("RGBA", (image_width, image_height), color=(0, 0, 0, 255))
    draw = ImageDraw.Draw(canvas)

    canvas2 = Image.new("RGB", (image_width, image_height), color=(0, 0, 0))
    draw2 = ImageDraw.Draw(canvas2)

    horizontal_position = margin_pixels

    for i, line in enumerate(lines):
        for q, txt_col in enumerate(line):
            vertical_position = margin_pixels + (i * realistic_line_height)
            draw.text((horizontal_position + (6 * q), vertical_position), txt_col[0], fill=txt_col[1], font=font)
            draw2.text((horizontal_position + (6 * q), vertical_position), txt_col[0], fill=(255, 255, 255), font=font)

    return canvas, canvas2


st.write("""
# Movie to Ascii converter!
Convert any image to Ascii art. Larger images take significantly longer to convert. Scroll down to see the progress bar,
and converted images.
""")

# get the image
movie = st.file_uploader("Upload an image", type=["mp4", "mpg"])

path = os.path.join(os.getcwd(), "temp.mp4")
if movie is not None:
    with open(path, "wb") as f:
        f.write(movie.getbuffer())

# example button
example = st.button("See an Example")
if example:
    movie = True
    path = "Rick Roll.mp4"

if movie is not None:
    st.video(path)

    with st.spinner('Converting movie...'):
        with st.info("Loading files and creating temp folders..."):
            main_progress = st.progress(0)
            clip = mp.VideoFileClip(path)
            if movie is not True:
                os.remove(path)
            clip = clip.subclip(0, clip.duration)
            clip = clip.resize(width=150)
            num_frames = int(clip.duration * clip.fps)
            frames = clip.iter_frames()
            color = []
            mono = []

            # create temp folder
            color_folder = "temp_color"
            if not os.path.exists(color_folder):
                os.makedirs(color_folder)

            mono_folder = "temp_mono"
            if not os.path.exists(mono_folder):
                os.makedirs(mono_folder)

        progress = st.empty()
        with st.info("Parsing Each Frame"):
            for i, frame in enumerate(frames):
                image1, image2 = image_to_ascii(Image.fromarray(frame))

                name = "/frame" + str(i) + ".png"
                image1.save(color_folder + name, format="PNG")
                color.append(color_folder + name)

                image2.save(mono_folder + name, format="PNG")
                mono.append(mono_folder + name)

                main_progress.progress(((i * 100) // num_frames))
                progress.text("Converting frame " + str(i) + " of " + str(num_frames))

        progress.empty()
        main_progress.empty()

        with st.info("Assembling and writing to files"):
            output1 = mp.ImageSequenceClip(color, fps=clip.fps)
            output2 = mp.ImageSequenceClip(mono, fps=clip.fps)
            output1.audio = clip.audio
            output2.audio = clip.audio
            file1 = "color.mp4"
            file2 = "mono.mp4"
            # create files
            output1.write_videofile(file1, fps=clip.fps, audio_codec="aac")
            time.sleep(3)
            # output2.write_videofile(file2, fps=clip.fps, audio_codec="aac")
            for file in os.listdir(color_folder):
                os.remove(os.path.join(color_folder, file))
                os.remove(os.path.join(mono_folder, file))
            os.rmdir(color_folder)
            os.rmdir(mono_folder)

    st.success('Done! Scroll down to see the result.')
    st.video(file1, format="mp4")
    st.balloons()

    col1, col2 = st.columns([1, 1])

    with col1:
        with open(file1, "rb") as f:
            st.download_button(
                label="Download color movie",
                data=f,
                file_name="color.mp4",
                mime="video/mp4",
            )

    # with col2:
    #     with open(file2, "rb") as f:
    #         st.download_button(
    #             label="Download plain text movie",
    #             data=f,
    #             file_name="mono.mp4",
    #             mime="video/mp4",
    #         )

st.markdown("Made by [Noah Virjee](https://blucardin.github.io/) © 2022. You can use the code, but please credit me. "
            "Version 1.3.0", unsafe_allow_html=True)
