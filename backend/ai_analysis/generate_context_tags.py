import os
from dotenv import load_dotenv
from config import client

load_dotenv()

gpt_user_content = os.getenv("GPT_USER_CONTENT")
gpt_system_content = os.getenv("GPT_SYSTEM_CONTENT")

def generate_tags(tags: set):
    
    prompt = gpt_user_content.replace("[Insert list of words here]", ", ".join(map(str, tags)))

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": gpt_system_content}, 
                {"role": "user", "content": prompt}],
            max_tokens=1000,
        )
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error: {e}")
