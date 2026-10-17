# MyOfficeAssistant
MyOfficeAssistant

Office Assistant AI Agent

A tool-using AI agent that manages tasks, meetings and notes, and drafts emails and summaries, built with the Anthropic API.

Features
-Add, list and complete tasks
-Schedule and view meetings
-Save and search notes
-Draft emails and summarize text
-Tool-calling agent loop with a step  limit

Setup
1.python -m venv venv then activate it
2.pip install -r requirements.txt
3.Copy .env.example to .env and add your API key
4.python main.py

Example prompts
-"Add a high priority task to send the report by tomorrow"
-"Schedule a meeting with Riya next Monday at 10:30 about the demo"
-"What's on my to-do list?"
-"Draft a polite email asking my manager for Friday off"

Project structure
-tools.py: tool functions and schemas
-agent.py: agent loop
-main.py: command-line chat