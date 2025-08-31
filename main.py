from flask import Flask, jsonify,request,render_template
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__,template_folder= "templates")      

messages = [     
        ]

@app.route('/' , methods=['GET','POST'])    
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password') 

        return render_template('templates/chatbot.html', username=username , password=password) 
    return render_template('index.html')

@app.route('/chatbot', methods=['POST', 'GET']) 
def chatbot():
    
    answer = None
    if request.method == 'POST':
        data = request.get_json()  
        user_message = data.get('message')  
        conversationinfo = ""
        if messages == []:
            conversationinfo = user_message+"make sure that if and only if the user does /walkthrough then you should not give the answer to the question but help guide them toward the answeralso if latex is needed Always return LaTeX math as $$...$$ for display math.When formating the latex do not produce any inline"
        else:
            conversationinfo = f"{user_message} refer to the past conversation for context {str(messages)} also if the user specifies /walkthrough then just explain the problem with steps, not directly providing an answer. Always return LaTeX math as $$...$$ for display math. "
        print(conversationinfo)
        response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "user", "content": conversationinfo}
        ]
             )
        
        
        answer = response.choices[0].message.content
        messages.extend([{"role": "user", "content": user_message}, {"role":"assistant","content":answer}])
        return jsonify({"answer":answer})
    

if __name__ == '__main__':
    app.run(debug=True, port=8080)
