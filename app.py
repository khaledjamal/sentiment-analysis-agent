# app.py

# Import the necessary classes and functions from smolagents
from smolagents import CodeAgent, HfApiModel, load_tool, tool

# Standard library imports
import yaml

# External imports
import torch
from transformers import pipeline

# Import custom final answer tool and Gradio UI
from tools.final_answer import FinalAnswerTool
from Gradio_UI import GradioUI

# Initialize the Transformer-based sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

@tool
def my_custom_tool(arg1: str, arg2: int) -> str:
    """A tool that does nothing yet 
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build?"

@tool
def advanced_sentiment_tool(text: str) -> str:
    """A tool that uses a pre-trained transformer model to do sentiment analysis.
    Args:
        text: The text to analyze for sentiment.
    """

    analysis = sentiment_pipeline(text)
    label = analysis[0]['label']
    score = analysis[0]['score']
    
    #sample values that could be assigned to the above two variables:
    #label = "positive"
    #score = "0.99"
    
    return f"Sentiment: {label} (confidence: {score:.4f})"

@tool
def simple_sentiment_tool(text: str) -> str:
    """A tool that uses a pre-trained transformer model to do sentiment analysis.
    Args:
        text: The text to analyze for sentiment.
    """
    text = text.lower()
    
    if "happy" in text:
        return "Sentiment: Joyful (confidence: 1.00)"
    elif "sad" in text:
        return "Sentiment: Sorrowful (confidence: 1.00)"
    
    label = "positive"
    score = "0.99"
    
    return f"Sentiment: {label} (confidence: {score:.4f})"


# Final answer tool
final_answer = FinalAnswerTool()

# Initialize the model
model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
    custom_role_conversions=None,
)

# Load prompt templates
with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)

# Initialize the agent, including the sentiment analysis tool
agent = CodeAgent(
    model=model,
    tools=[final_answer, advanced_sentiment_tool],
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)

# Launch the Gradio UI
GradioUI(agent).launch()
