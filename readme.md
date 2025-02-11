# Autonomous AI Agent

This project is an autonomous AI agent capable of generating images and performing web searches based on user input. It uses OpenAI, Replicate, and Perplexity APIs to handle tasks such as image generation, decision-making, and web browsing.

---

## Features

- **Image Generation**: Create high-quality images using Stable Diffusion 3 via Replicate.
- **Decision Agent**: Automatically decide whether to generate an image or perform a web search based on user input.
- **Web Browsing**: Search the web for information using Perplexity's API.
- **Environment Setup**: Securely manage API keys and environment variables.

---

## Environment Setup

### Prerequisites

1. **Python 3.8+**: Ensure Python is installed on your system.
2. **API Keys**:
   - OpenAI API Key
   - Replicate API Token
   - Perplexity API Key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/autonomous-ai-agent.git
   cd autonomous-ai-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - For local development, create a `.env` file in the root directory:
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key
     REPLICATE_API_TOKEN=your_replicate_api_token
     PERPLEXITY_API_KEY=your_perplexity_api_key
     ```
   - For Google Colab, use the `get_secret` function to securely retrieve API keys.

---

## Usage

### Running the Agent

1. Start the agent:
   ```bash
   python main.py
   ```

2. Enter your query when prompted:
   ```plaintext
   What would you like to create or research? 
   ```

3. The agent will decide whether to generate an image or perform a web search based on your input.

---

## Code Overview

### Environment Setup

```python
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
```

### Image Generation

```python
def generate_image(prompt: str, negative_prompt: str = "blur, non-realistic, low quality") -> str:
    output = replicate.run(
        "stability-ai/stable-diffusion-3",
        input={
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "cfg": 5.0,
            "steps": 28,
            "aspect_ratio": "3:2",
            "output_format": "png",
            "output_quality": 90,
            "prompt_strength": 1.0
        }
    )
    return output[0]  # Return first image URL
```

### Decision Agent

```python
def decision_agent(user_input):
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a decision-making agent..."},
            {"role": "user", "content": f"Decide the best tool for this task: {user_input}..."}
        ]
    )
    return json.loads(response.choices[0].message.content)
```

### Web Browsing

```python
def web_browsing(query):
    response = perplexity_client.chat.completions.create(
        model="sonar-reasoning",
        messages=[
            {"role": "system", "content": "Provide a concise answer based on web search."},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content
```

---

## Example Workflow

1. **Image Generation**:
   ```plaintext
   What would you like to create or research? A futuristic cityscape
   Decision: GENERATE_IMAGE
   Reason: The input describes a visual concept suitable for image generation.
   Generated image URL: https://example.com/image.png
   ```

2. **Web Browsing**:
   ```plaintext
   What would you like to create or research? Latest trends in AI
   Decision: WEB_BROWSING
   Reason: The input is a research query best answered by web search.
   Search results: The latest trends in AI include...
   ```

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [OpenAI](https://openai.com) for GPT-4 and API support.
- [Replicate](https://replicate.com) for Stable Diffusion 3 integration.
- [Perplexity](https://perplexity.ai) for web browsing capabilities.
```

---

### Key Sections:
1. **Features**: Highlights the main functionalities of the project.
2. **Environment Setup**: Provides instructions for setting up the project locally or in Google Colab.
3. **Usage**: Explains how to run the agent and interact with it.
4. **Code Overview**: Breaks down the key components of the code.
5. **Example Workflow**: Demonstrates how the agent works with sample inputs.
6. **Contributing**: Encourages contributions from the community.
7. **License**: Specifies the project's license.
8. **Acknowledgments**: Credits the tools and services used.

---

This `README.md` file is comprehensive and user-friendly, making it easy for others to understand and use your project. Let me know if you need further adjustments!