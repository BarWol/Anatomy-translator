import concurrent.futures

from translation_maker import TranslationMaker

abbreviations_map = {
   "t": "tętnica",
   "ż": "żyła",
   "ż.": "żyła",
   "w.": "więzadło",
   "cz.": "część",
   "wew.": "ujście wewnętrzne",
   "w.": "więzadło",
   "cz.": "część",
   "cz": "część",
   "wew": "wewnętrzne",
   "zew": "zewnętrzne",
   "-": " "
}





class handler:
   def __init__(self,progress_callback=None, root =None):
      self.t_maker = TranslationMaker()
      self.processed_words = 0
      self.successful_words = 0
      self.total_lines = 0
      self.progress_callback = progress_callback
      self.root = root
   def process_chunk(self, lines):
      counter = 1
      word_numbers = []
      output = []
      all = 0
      for processed_lines, line in enumerate(lines, start=1):
         waiting = False
         # print(counter)
         line_words = line.split()
         exclamation = 0
         ending = 0
         found = False
         for i, line_word in enumerate(line_words):
            if (line_word == "!!!" or counter == 1) and not waiting:
               counter += 1
               waiting = True
               exclamation = i
               continue
            if waiting:
               if line_word == ";;;":
                  all += 1
                  ending = i
                  waiting = False
                  line_to_check = " ".join(line_words[exclamation + 1:ending])
                  found = True
            if found and line_to_check:
               found = False
               word = line_to_check
               ##print(word)
               table_of_translations = self.t_maker.identify_language(word)  # Language identification
               if table_of_translations:
                  word_numbers.append(all)
                  output.append(f"{word}\n")
                  for translation in table_of_translations:
                     output[-1] += f"{translation}\n"
                     #print(translation)
                  output[-1] += "\n\n"
      #print(f"len of output: {len(output)}, len of word_numbers: {len(word_numbers)}")
      self.processed_words += all
      return all, word_numbers, output

   def handle_from_data(self, csv_data):
      lines = csv_data.split("\n")
      #for line in lines:
         #print(f"line = {line} \n")
      return self.handle_all(lines)
   def handle_all(self,lines,chunk_size=5):
      output = ""
      self.total_lines = len(lines)
      #print("total lines = ", self.total_lines)
      chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
      counter = 0
      with concurrent.futures.ThreadPoolExecutor() as executor:
         results = executor.map(
            self.process_chunk,
            chunks,
         )

      for result in results:
         if result:
            all, word_numbers, chunk_output = result
            self.successful_words += len(word_numbers)
            #print(f"counter = {counter}, all = {all}, word_numbers = {word_numbers}")
            for i in range(len(chunk_output)):
               number = counter + int(word_numbers[i])
               output += str(number) +" "+ chunk_output[i]
            counter += all
         processed_lines = counter

      output += f"Success rate: {self.successful_words / self.processed_words}\n"
      return output, self.total_lines, min(processed_lines, self.total_lines)


   def handle(self, csv_file):
      with open(csv_file, "r") as f:
         lines = f.readlines()
         return self.handle_all(lines)
