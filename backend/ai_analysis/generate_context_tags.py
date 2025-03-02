import os
from dotenv import load_dotenv

from openai import OpenAIError
from exceptions.tags_generation_failed_exception import TagsGenerationFailedException

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
    
    except (KeyError, IndexError, AttributeError) as e:
        raise TagsGenerationFailedException("Invalid response received", errors=str(e))
    except (OpenAIError, ConnectionError, TimeoutError, ValueError) as e:
        raise TagsGenerationFailedException("Failed to generate tags", errors=str(e))
    except Exception as e:
        raise TagsGenerationFailedException("An unexpected error occurred", errors=str(e))
