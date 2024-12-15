from Project import *
from Story import *
from PdfBuilder import *

class Generator(Project):
    def __init__(self, cwd='./projects'):
        self.cwd = cwd
        self.story = Story()
        self.pdf = PdfBuilder()
        super().__init__(cwd)

    def open(self, id):
        self.openProject(f"{self.cwd}/{id}")
    
    def generate(self, idea, pages=10):
        if "pages" not in self.project:
            pages = self.story.generateStory(idea, pages)
            print(json.dumps(pages, indent=4))
            self.project["idea"] = idea
            self.project["pages"] = pages
            self.saveProject()

        if "characters" not in self.project:
            characters = self.story.generateCharacters(self.project["idea"], self.project["pages"])
            print(json.dumps(characters, indent=4))
            self.project["characters"] = characters
            self.saveProject()

        if "prompts" not in self.project:
            prompts, raw = self.story.generateImagesPrompts(pages=self.project["pages"], characters=self.project["characters"])
            print(json.dumps(prompts, indent=4))
            self.project["prompts"] = prompts
            self.project["prompts_raw"] = raw
            self.saveProject()

        if "illustrations" not in self.project:
            illustrations = self.story.generateIllustrations(prompts=self.project["prompts"], cwd=self.projectPath)
            print(json.dumps(illustrations, indent=4))
            self.project["illustrations"] = illustrations
            self.saveProject()
        
        if "html" not in self.project:
            html = self.story.generatePages(project=self.project, cwd=self.projectPath)
            print(json.dumps(html, indent=4))
            self.project["html"] = html
            self.saveProject()
        
        if "pdf" not in self.project:
            pdf = self.pdf.assemble_pdf(self.project["html"], f"{self.projectPath}/book.pdf", cwd=self.projectPath)
            self.project["pdf"] = "book.pdf"
            self.saveProject()
        return


        # if "pdf" not in self.project:
        #     pdf = self.pdf.generate(self.project["html"], f"{self.projectPath}/book.pdf", cwd=self.projectPath)
        #     self.project["pdf"] = "book.pdf"
        #     self.saveProject()
        
        

gen = Generator()
gen.open("beach-treasure-4")

#gen.generate('A story about "Ms DSouza", a kind teacher at "AMS" (40s, indian, dark hair), and "Noah" (6 years old, *blond hair*, caucasian kid). Noah learns to read with his teacher. Happy ending.', pages=10)

# gen.generate('A story about "Ms DSouza", a kind teacher at "AMS" (40s, indian, dark hair), and "Noah" (6 years old, *blond hair*, caucasian kid). Noah learns to read with his teacher. Happy ending.', pages=10)

# gen.generate('A story about "Cop Cat", a cat who is a cop. A Transformer makes a mess in the towN; Cop cat needs to stop him and together they clean the mess. No fighting. Happy ending.', pages=10)

#gen.generate('A story about "Cop Cat", a cat who is a cop in a far west town. He needs to catch Billy The Kid (a human). Conflict resolution. Happy ending.', pages=10)

#gen.generate('A squirrel and a chipmunk work together to open a mystery box in the forest.', pages=10)

gen.generate('Noah is digging in the sand and finds an old compass with an arrow that spins. The arrow points him to a big log on the beach. Under the log, he finds a metal box, but it\'s locked. The compass points again, and Noah finds a key hidden inside a cluster of shells nearby. Noah is a blond 6-year-old boy.', pages=16)

#gen.generate('A story about Optimus Prime learning to transform. Happy ending.', pages=10)