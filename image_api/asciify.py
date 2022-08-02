from PIL import Image

# This implmentation of asciifying an image is taken from:
# https://www.journaldev.com/60400/image-to-ascii-art-using-python
def asciify_image(img_path):

    try:
        img = Image.open(img_path)
    except:
        print(img_path, "Unable to find image ")

    width, height = img.size
    aspect_ratio = height / width
    new_width = 120
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))

    img = img.convert("L")

    chars = ["@", "J", "D", "%", "*", "P", "+", "Y", "$", ",", "."]

    pixels = img.getdata()
    new_pixels = [chars[pixel // 25] for pixel in pixels]
    new_pixels = "".join(new_pixels)
    new_pixels_count = len(new_pixels)
    ascii_image = [
        new_pixels[index : index + new_width]
        for index in range(0, new_pixels_count, new_width)
    ]
    ascii_image = "\n".join(ascii_image)
    return ascii_image
