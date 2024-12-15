import replicate
from PIL import Image as PILImage, ImageDraw, ImageFont
import os

class StoryImage:
    def __init__(self):
        print("")
    
    def generate(self, prompt, filename):
        output = replicate.run(
            "fofr/sticker-maker:4acb778eb059772225ec213948f0660867b2e03f277448f18cf1800b96a65a1a",
            input={
                "steps": 17,
                "width": 1152,
                "height": 1152,
                "prompt": prompt,
                "output_format": "png",
                "output_quality": 100,
                "negative_prompt": "",
                "number_of_images": 1
            }
        )
        with open(filename, 'wb') as f:
            f.write(output[0].read())
        return output

    def create_page(self, image_path, text1, text2, output_path):
        """
        Creates a single page as an image with an image, black border, and two lines of text.

        Parameters:
        - image_path (str): Path to the image file to include on the page.
        - text1 (str): The first sentence to include below the image.
        - text2 (str): The second sentence to include below the image.
        - output_path (str): Path to save the generated page image.
        """
        # Page dimensions
        page_width, page_height = 1200, 1600  # Adjust as needed
        margin = 90

        # Load the image and resize it
        image = PILImage.open(image_path)
        image.thumbnail((page_width - 2 * margin, page_height // 2 - margin))

        # Create a blank white canvas
        page = PILImage.new("RGB", (page_width, page_height), "white")
        draw = ImageDraw.Draw(page)

        # Calculate image placement
        img_x = (page_width - image.width) // 2
        img_y = margin
        page.paste(image, (img_x, img_y))

        # Draw black border around the image
        draw.rectangle(
            [img_x - 5, img_y - 5, img_x + image.width + 5, img_y + image.height + 5],
            outline="black",
            width=5,
        )

        # Load a font
        font_size = 48
        font = ImageFont.truetype("Roboto-Bold.ttf", font_size)

        # Add the first line of text
        text1_y = img_y + image.height + margin
        draw.text(
            (page_width // 2, text1_y), text1, font=font, fill="black", anchor="mm"
        )

        # Add the second line of text
        text2_y = text1_y + font_size + 20
        draw.text(
            (page_width // 2, text2_y), text2, font=font, fill="black", anchor="mm"
        )

        # Save the page
        page.save(output_path)
        print(f"Saved page to {output_path}")
