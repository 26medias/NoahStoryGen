import replicate

class Image:
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