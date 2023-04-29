import openai
import os
from configparser import ConfigParser
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_model():
    config = ConfigParser()
    config.read('config.ini')
    gpt4_bool = config.getboolean('main', 'gpt4')
    return 'gpt-4' if gpt4_bool else 'gpt-3.5-turbo'

# API request function
def analysis(prompt):
    output = openai.ChatCompletion.create(
    model=get_model(),
    messages=[
      {"role": "system", "content": """When text is entered your job is to reply in bullet point format to the following criteria on a scale of 0-100 (0 being the worst, 100 being perfect. An average text would score 50). 

[1. Readability: Assess the text based on how easy it is to read and understand. The harder it is to understand, the lower the value.

2. Organization: Evaluate the overall structure and organization of the text. Is the information presented in a logical order? Are there clear headings and subheadings that help guide the reader through the content? The less organized the text, the lower the value.

3. Grammar: Check for proper grammar throughout the text. Errors in grammar will significantly lower this value.

4. Punctuation: Check for punctuation and proper capitalization in the text, if there is punctuation or capitalization missing, lower the value.

5. Spelling: Check for corrent spelling throughout the text. Errors in spelling will significantly lower this value.]

REMEMBER! DON'T RATE TOO HIGHLY, "100" MEANS THAT IT IS ABSOLUTE PERFECTION, AVERAGE TEXT IS ONLY 50!!!!! BE CRITICAL. RATE 25% LOWER THAN YOU THINK THEY SHOULD BE.
you must also output the setting/format/genre of the text - how is the text perceived to the reader?
your response MUST be in the following format: 

setting

1. Readability: readability/100
2. Organization: organization/100
3. Grammar: grammar/100
4. Punctuation: punctuation/100
5. Spelling: spelling/100"""},
      {"role": "user", "content": prompt}
    ]
  )
    return output.choices[0].message.content

def critique(prompt):
    output = openai.ChatCompletion.create(
    model=get_model(),
    messages=[
      {"role": "system", "content": """When text is entered your job is to find the biggest problems in the text and write a !SHORT! and !BRIEF! critique on them. ONLY OUTPUT THE CRITIQUE. DO NOT WRITE ANYTHING OTHER THAN THE CRITIQUE. Output this in numerical format (1. 2. 3.), and make sure theres a line gap between each."""},
      {"role": "user", "content": prompt}
    ]
  )
    return output.choices[0].message.content

def rewrite(prompt, rewrite_option):
    prompt_type = rewrite_prompts(rewrite_option)
    print("prompt type: ", prompt_type)
    print(rewrite_option)
    output = openai.ChatCompletion.create(
    model=get_model(),
    messages=[
      {"role": "system", "content": f"""When text is entered your job is to rewrite the text in the style/format of [{prompt_type}]. Heavily weigh in [{prompt_type}] when creating the rewritten text."""},
      {"role": "user", "content": prompt}
    ]
  )
    return output.choices[0].message.content


def rewrite_prompts(rewrite_option):
    # Generate GPT-4 prompts for each rewrite selection
    if rewrite_option == "From feedback":
        rewrite_prompt = f"Rewrite the text based on this feedback: {critique_field.cget('text')}"
    if rewrite_option == "Fix grammar":
        rewrite_prompt = "Rewrite the text to fix the grammar and ONLY the grammar."
    if rewrite_option == "Fix punctuation":
        rewrite_prompt = "Rewrite the text to fix the punctuation and ONLY the punctuation."
    if rewrite_option == "Fix spelling":
        rewrite_prompt = "Rewrite the text to fix the spelling and ONLY the spelling."
    if rewrite_option == "Formal":
        rewrite_prompt = "Rewrite the text to make it formal, try and keep a style of writing."
    if rewrite_option == "Informal":
        rewrite_prompt = "Rewrite the text to make it informal, try and keep a style of writing."
    if rewrite_option == "Casual":
        rewrite_prompt = "Rewrite the text to make it highly casual, try and keep a style of writing."
    if rewrite_option == "Condense text":
        rewrite_prompt = "Rewrite the text to make it more concise, and condense it."
    if rewrite_option == "Simplify language":
        rewrite_prompt = "Rewrite the text using simpler language and easier-to-understand terms."
    if rewrite_option == "Expand text":
        rewrite_prompt = "Rewrite the text by expanding on the ideas and providing more details."    
    if rewrite_option == "Make it persuasive":
        rewrite_prompt = "Rewrite the text to make it more persuasive and convincing."
    if rewrite_option == "Add humor":
        rewrite_prompt = "Rewrite the text by adding humor and making it more lighthearted."
    if rewrite_option == "Remove jargon":
        rewrite_prompt = "Rewrite the text by removing any jargon or technical terms and replacing them with simpler language."
    if rewrite_option == "Rephrase as a list":
        rewrite_prompt = "Rewrite the text by rephrasing it as a list, organizing the information in a clear and concise manner."
    if rewrite_option == "Rewrite for social media":
        rewrite_prompt = "Rewrite the text for a social media post, making it concise and engaging."
        
    return rewrite_prompt