# ------------
# ENVIRONMENT SETUP
# ------------
#from google.colab import userdata  # For Colab secrets
from openai import OpenAI
import replicate
import os
import json
from tenacity import retry, stop_after_attempt, wait_exponential
from IPython import get_ipython

def get_secret(key):
    ipython = get_ipython()
    if 'google.colab' in str(ipython):
        from google.colab import userdata
        return userdata.get(key)
    else:
        import os
        return os.environ.get(key)

# Initialize API keys securely
openai_api_key = get_secret('OPENAI_API_KEY')
replicate_api_token = get_secret('REPLICATE_API_TOKEN')
perplexity_api_key = get_secret('PERPLEXITY_API_KEY')

# Handle missing keys
if not openai_api_key:
    openai_api_key = input("Please enter your OpenAI API Key: ")
if not replicate_api_token:
    replicate_api_token = input("Please enter your Replicate API Token: ")
if not perplexity_api_key:
    perplexity_api_key = input("Please enter your Perplexity API Key: ")

os.environ.update({
    "OPENAI_API_KEY": openai_api_key,
    "REPLICATE_API_TOKEN": replicate_api_token,
    "PERPLEXITY_API_KEY": perplexity_api_key
})

# Initialize clients
openai_client = OpenAI()
perplexity_client = OpenAI(
    api_key=os.environ["PERPLEXITY_API_KEY"],
    base_url="https://api.perplexity.ai"
)
replicate_client = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])

# ------------
# IMAGE PROMPT AGENT
# ------------
def image_prompt_agent(user_input):  # Fixed typo in function name
    print("\nWriting prompt for image generation...")
    response = openai_client.chat.completions.create(
        model="gpt-4o",  # Updated model name
        messages=[
            {"role": "system", "content": "You are an expert prompt writer. You specialize in writing descriptive prompts for the AI image tool Stable Diffusion."},
            {"role": "user", "content": f"Write a concise prompt for this {user_input}. Always include: 'text saying Afarsemon AI Agency'. Only output the prompt itself, no extra text."}
        ]
    )
    prompt = response.choices[0].message.content
    print("Generated prompt:", prompt)
    return prompt

# ------------
# IMAGE GENERATION
# ------------
def generate_image(prompt: str,
                     negative_prompt: str = "blur, non-realistic, low quality") -> str:
    if len(prompt.strip()) < 30:  # Reduced minimum length
        raise ValueError("Prompt must be at least 20 characters")

    try:
        output = replicate.run(
            "stability-ai/stable-diffusion-3",
            input={
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "cfg": 5.0,  # Valid range: 1-5
                "steps": 28,  # Max 28 steps
                "aspect_ratio": "3:2",
                "output_format": "png",
                "output_quality": 90,
                "prompt_strength": 1.0
            }
        )
        return output[0]  # Return first image URL
    except Exception as e:
        raise RuntimeError(f"Image generation failed: {str(e)}")
    
# ------------
# DECISION AGENT
# ------------
def decision_agent(user_input):
    response = openai_client.chat.completions.create(
        model="gpt-4o",  # Updated model name
        messages=[
            {"role": "system", "content": """You are a decision-making agent. Analyze the user's input and decide whether to use the "generate_image" tool or the "web_browsing" tool.
                                          Output your decision in JSON format with 'reasoning' and 'tool' fields.
                                          The JSON should start and end with curly brackets, with no additional text.
                                          Example format:
                                          {
                                            "reasoning": "Thorough explanation for the decision...",
                                            "tool": "generate_image" or "web_browsing"."
                                          }
                                          Do NOT output any text other than the JSON."""},
            {"role": "user", "content": f"Decide the best tool for this task: {user_input}. Output ONLY the JSON with 'reasoning' and 'tool' fields, nothing else."}
        ]
    )

    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        return {"tool": "web_browsing", "reasoning": "Default to search"}
    
# ------------
# WEB BROWSING
# ------------
def web_browsing(query):
    print("\nSearching the web...")
    response = perplexity_client.chat.completions.create(
        model="sonar-reasoning",  # Updated model name
        messages=[
            {"role": "system", "content": "Provide a concise answer based on web search."},
            {"role": "user", "content": query}
        ]
    )
    print("\nSearch results:")
    print(response.choices[0].message.content)


# ------------
# MAIN FLOW
# ------------
def get_user_input():
    return input("\nWhat would you like to create or research? ")

def execute_decision(decision, user_input):
    print(f"\nDecision: {decision['tool'].upper()}")
    print(f"Reason: {decision['reasoning']}")

    if decision["tool"] == "generate_image":
        prompt = image_prompt_agent(user_input)
        image_url = generate_image(prompt)
        print(f"\nGenerated image URL: {image_url}")
    elif decision["tool"] == "web_browsing":
        web_browsing(user_input)
    else:
        print("Invalid tool selected")

# Run the full workflow
user_input = get_user_input()
decision = decision_agent(user_input)
execute_decision(decision, user_input)