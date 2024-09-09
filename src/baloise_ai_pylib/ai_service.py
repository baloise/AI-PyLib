import importlib.resources as pkg_resources
from baloise_ai_pylib import resources


class AIService:
    def banner(self)-> str:
        with pkg_resources.open_text(resources, "banner.txt") as banner_file:
            return banner_file.read()

if __name__ == "__main__":
    print(AIService().banner())
