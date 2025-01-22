import requests
from bs4 import BeautifulSoup as bs


class TranslationMaker:

   def __init__(self, url="https://anationary.github.io/en/anatomy-dictionary/", english="english", polish="polish",
                latin="latin"):
      self.url = url
      self.english = english
      self.polish = polish
      self.latin = latin
      self.languages = [english, polish, latin]

   def from_to(self, word, base, translation):
      return self.url + base + "-" + translation + "/" + "_".join(word.split(" "))

   def translate(self, word, base_language, to_language):


      try:
         response = requests.get(self.from_to(word, base_language, to_language))
         response.raise_for_status()  # Raises an error if the HTTP request fails
         soup = bs(response.content, "html.parser")
         blockquote = soup.find("blockquote")
         if blockquote:
            definition = blockquote.find("h2")
            if definition:
               return definition.text.strip()
      except requests.exceptions.HTTPError as err:
         pass

   def identify_language(self, word):
      words_to_return = []
      for base_language in self.languages:
         for to_language in self.languages:
            if to_language != self.latin:

              word2 = (self.translate(word, base_language, to_language))
              if word2:
                 words_to_return.append(word2)
      return words_to_return