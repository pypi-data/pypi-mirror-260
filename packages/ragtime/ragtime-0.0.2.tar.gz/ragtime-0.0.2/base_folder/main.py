import ragtime
from config import *
import keys
from typing import Optional
from expe import QA, Answer, Chunks, Expe, Prompt, Question
import expe
from generators import Prompter

class MyAnsPptr(Prompter):
    def get_prompt(self, question:Question, chunks:Optional[Chunks] = None) -> Prompt:
        result:Prompt = Prompt()
        result.user = f"{question.text}.\nRépond uniquement avec la lettre. Ne donne qu'une seule réponse."
        result.system = ""
        return result
    
    def post_process(self, qa:QA=None, cur_obj:Answer=None):
        ans:str = cur_obj.llm_answer.text.strip()[0]
        cur_obj.text = ans
        transco_table:dict = qa.question.meta.get('transco', None)
        transco:str = transco_table.get(ans, "?")
        cur_obj.meta['transco'] = transco

if __name__ == '__main__':
  logger.info('MAIN STARTS')

  # generators.gen_Answers(folder_in=FOLDER_QUESTIONS, folder_out=FOLDER_ANSWERS,
  #                        json_file="eco_fr_v2_gen_with_LeChat--47Q_0C_0F_6M_282A_0HE_0AE_2024-03-05_14,37,32.json",
  #                        prompter=MyAnsPptr(),
  #                        llm_names=["gpt-4", "gpt-3.5-turbo", "gemini-pro", "claude-2.1", "mistral/mistral-large-latest", "command-nightly"],#, "luminous-supreme-control"],
  #                        start_from=StartFrom.post_process)
  
  expe_file:str = "eco_fr_v2_gen_with_LeChat--47Q_0C_0F_6M_282A_0HE_0AE_2024-03-05_15,17,54.json"
  # expe.export_to_html(json_path=FOLDER_ANSWERS / expe_file)
  expe.export_to_spreadsheet(json_path=FOLDER_ANSWERS / expe_file, template_path=FOLDER_SST_TEMPLATES / "MCQ.xlsx")

  logger.info('MAIN ENDS')