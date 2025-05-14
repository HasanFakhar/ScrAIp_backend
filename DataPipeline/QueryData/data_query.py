from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

import os
import dotenv

dotenv.load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")
chat_model_name=os.getenv("GROQ_MODEL_NAME")

chat_model = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name=chat_model_name)


async def run_query(query: str, data: dict):
    prod_comp_chain = create_prod_comp_chain(query)
    return prod_comp_chain.invoke({"content": data})


def create_prod_comp_chain(query: str):
  parser = JsonOutputParser()
  prompt_template = PromptTemplate(
    template="""
      You will be given a dictionary containing divisions of a website's text and you have to return all the data 
      required by the following query: \"
      """
            +
      query
            +
      """
      \"
      If the query is irrelevant and the data asked for in the query is not available, return none. Use json format and
       return a dictionary. Do not give code, give the output directly.  Do not modify, correct, or interpret any content—only format it.

      {format_instructions}
      website: {content}
      """,
    input_variables=['content'],
    partial_variables={'format_instructions': parser.get_format_instructions()},
  )
  prod_comp_chain = prompt_template | chat_model | parser
  return prod_comp_chain

