import re
import os
import datetime
from difflib import get_close_matches
from groq import Groq

# Automatically Initiating required envoirnmental variable
os.environ["GROQ_API_KEY"] = "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"

# Configure the Groq API with your API key
client = Groq(
    api_key=os.environ.get("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"),
)

# Separate commands into general and argumented commands
argumented_commands = [
    "open application", "close application", "web search", "youtube search", "open website",
    "click on"
]

general_commands = [
    "battery status", "cpu usage", "internet status",
    "check email", "check internet", "get weather", "increase volume",
    "decrease volume", "mute sound", "unmute sound", "sleep mode",
    "shutdown", "restart", "current date", "current time",
    "close window", "minimize window", "maximize window", "switch window",
    "snap window left", "snap window right", "close all windows", "open new window",
    "minimize all windows", "restore window", "toggle taskbar visibility", "open task manager",
    "open file explorer", "open command prompt", "open browser", "open notepad",
    "open calculator", "open snipping tool", "open paint", "open wordpad",
    "open registry editor", "open disk management", "open device manager", "open event viewer",
    "take screenshot", "toggle full screen", "lock computer", "minimize all windows",
    "create virtual desktop", "switch virtual desktop", "open settings", "open update settings",
    "open sound settings", "open bluetooth settings", "open wifi settings", "open keyboard settings",
    "open mouse settings", "open display settings", "open language settings", "open time and date settings",
    "open taskbar settings", "open privacy settings", "open storage settings", "open apps settings",
    "open power and sleep settings", "open default apps settings", "open personalization settings", "open fonts settings",
    "open region settings", "open accounts settings", "open backup settings", "open security and maintenance",
    "open feedback hub", "open system properties", "open network connections", "open action center",
    "open device encryption settings", "open control panel", "open services"
]

# Function to extract command and arguments
def extract_command_and_arguments(user_input):
    """
    Extract the command and argument from user input.
    """
    user_input = user_input.strip().lower()

    # Check if the command is one of the argumented commands
    for command in argumented_commands:
        if user_input.startswith(command):
            argument = user_input.replace(command, "").strip()
            return command, argument

    # Match the input to a general command
    closest_match = get_close_matches(user_input, general_commands, n=1, cutoff=0.6)
    if closest_match:
        command = closest_match[0]
        return command, ""

    # Fallback: Use Groq API for ambiguous input
    return get_command_from_groq(user_input)

# Function to get command from Groq API
def get_command_from_groq(user_input):
    """
    Use the Groq API to extract command and argument for ambiguous inputs.
    """
    prompt = (
        f"User input: {user_input}\n"
        f"Map the user input to one of the predefined commands: {', '.join(argumented_commands + general_commands)}.\n"
        f"Also extract the argument if present. Return the result in the format:\n"
        f"Command: <command>\nArgument: <argument>\n"
    )

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    generated_text = response.choices[0].message.content.strip()
    match = re.search(r"Command: (.+)\nArgument: (.*)", generated_text)
    if match:
        command = match.group(1).strip()
        argument = match.group(2).strip()
        
        # Remove "None" if it appears in command or argument
        if command.lower() == "none":
            command = ""
        if argument.lower() == "none":
            argument = ""
            
            
        print(command, argument)
        return command, argument
    else:
        return "Invalid command", ""



a = "I want to see sound settings"
get_command_from_groq(a)