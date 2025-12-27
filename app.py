import pandas as pd
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

app=Flask(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model=genai.GenerativeModel("gemini-2.5-flash")

df=pd.read_csv("qa_data (1).csv")

context_text=" "
for index, row in df.iterrows():
    context_text += f"Q: {row['question']}\nA: {row['answer']}\n\n"

def ask_gemini(query):
    prompt=f""" you are an expert assistant that provides accurate and concise answers based on the provided context.
    Answer only using the context below. If the answer is not found in the context, respond with "I don't know" . 
    
    context:
    {context_text}
    Question: {query}
"""   
    
    response = model.generate_content(prompt)
    return response.text.strip()

#while True:
 #   user_input=input("You")

  #  if user_input.lower()=='exit':
   #     print("Good bye")
    #    break
    #answer=ask_gemini(user_input)
    #print(answer)

@app.route("/",methods=["GET","POST"])
def home():
    answer=""
    if request.method=="POST":
        query=request.form["query"]
        answer=ask_gemini(query)
    return render_template("index.html",answer=answer)

if __name__=="__main__":
    app.run()           