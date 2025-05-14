from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

import os
import dotenv

dotenv.load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")
chat_model_name=os.getenv("GROQ_MODEL_NAME")

chat_model = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name=chat_model_name)

async def chunk(text: str):
    prod_comp_chain = create_prod_comp_chain()
    return prod_comp_chain.invoke({"content":text})

def create_prod_comp_chain():
  parser = JsonOutputParser()
  prompt_template = PromptTemplate(
    template="""
      
     Format the provided website text into structured divisions based on the website type. 
     Ensure each division has the same features, using null for missing ones. 
     Return a JSON dictionary with no alterations to the data. 
     Do not modify, correct, or interpret any content—only format it.
      {format_instructions}
      website: {content}
      """,
    input_variables=['content'],
    partial_variables={'format_instructions': parser.get_format_instructions()},
  )
  prod_comp_chain = prompt_template | chat_model | parser
  return prod_comp_chain

