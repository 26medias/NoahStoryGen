from GPT import *
from Image import *
from tqdm import tqdm
import os
import json

class Story:
    def __init__(self):
        self.gpt = GPT()
        self.image = StoryImage()

    def write(self, filename, data):
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            if isinstance(data, str):
                f = open(filename, "w")
                f.write(data)
                f.close()
            else:
                with open(filename, 'w') as file:
                    json.dump(data, file, indent=4)
            return True
        except Exception as e:
            print(f"Error writing to file {filename}: {e}")
            return False
    
    def generateStory(self, idea, pages=10):
        sys_prompt = self.gpt.getPrompt('prompts/story.txt', {"pages": pages})
        response = self.gpt.ask(sys_prompt, idea, model="gpt-4o-mini")
        pages = response["pages"]
        return pages
    
    def generateCharacters(self, idea, storyPages):
        sys_prompt = self.gpt.getPrompt('prompts/characters.txt')
        response = self.gpt.ask(sys_prompt, f"Story description: {idea}."+("\n\n".join(storyPages)), model="gpt-4o-mini")
        characters = response["characters"]
        return characters
    
    def generateImagesPrompts(self, pages=[], characters=[]):
        sys_prompt = self.gpt.getPrompt('prompts/image-prompts.txt', {"characters": json.dumps(characters, indent=4)})
        response = self.gpt.ask(sys_prompt, json.dumps(pages, indent=4), model="gpt-4o-mini")
        prompts = response["illustrations"]
        return prompts
    
    def generateIllustrations(self, prompts=[], cwd="./"):
        output = []
        for n, prompt in enumerate(tqdm(prompts, desc="Processing prompts")):
            filename = f"{cwd}/{n}"
            img = self.gpt.generateBFLImage(prompt, filename=filename)
            output.append(f"{n}.jpeg")
        return output
    
    def generateIllustrations_sticker(self, prompts=[], cwd="./"):
        output = []
        for n, prompt in enumerate(tqdm(prompts, desc="Processing prompts")):
            filename = f"{cwd}/{n}.png"
            self.image.generate(prompt, filename=filename)
            output.append(f"{n}.png")
        return output
    
    def generatePages(self, project, cwd="./"):
        output = []
        for n, page in enumerate(project["pages"]):
            sentences = page.split("\n")
            img = project["illustrations"][n]
            self.image.create_page(f"{cwd}/{img}", sentences[0], sentences[1], f"{cwd}/page_{n}.png")
            output.append(f"page_{n}.png")
        return output
    
    def generatePages_html(self, project, cwd="./"):
        output = []
        for n, page in enumerate(project["pages"]):
            text = "<p>" + "</p><p>".join(page.split("\n")) + "</p>"
            img = project["illustrations"][n]
            html = self.gpt.getPrompt('templates/page.html', {
                "img": img,
                "text": text
            })
            self.write(f"{cwd}/{n}.html", html)
            output.append(f"{n}.html")
        return output