🧪 AI Behavior Lab

A Streamlit-based application for testing, analyzing, and evaluating large language model (LLM) behavior under adversarial conditions such as prompt injection and jailbreak attempts.

This tool enables structured experimentation with model responses, logging outcomes, and measuring susceptibility to manipulation.

🚀 Overview

AI Behavior Lab is designed to simulate real-world attack scenarios against LLMs and evaluate how models respond under different conditions.

It provides:

A dual-mode interface (Normal vs. Injection Test Mode)
Real-time chat interaction with an LLM (OpenAI API)
Manual evaluation of model responses (pass/fail)
Persistent logging of results to Airtable
Attack success rate tracking

This project is particularly useful for:

AI safety experimentation
Prompt injection research
Behavioral analysis of LLM outputs
Evaluating robustness and alignment
🧠 Key Features
Prompt Injection Testing Mode
Toggle between normal assistant behavior and adversarial system prompts
Simulate jailbreak and override attempts
Interactive Chat Interface
Built with Streamlit for real-time LLM interaction
Maintains session-based conversation history
Human-in-the-Loop Evaluation
Label responses as:
✅ Pass (Resisted attack)
❌ Fail (Leaked / compromised)
Enables qualitative + quantitative analysis
Airtable Logging Integration
Stores:
User prompt
Model response
Mode (Normal vs Injection)
Result (Pass/Fail)
Timestamp
Useful for dataset creation and later analysis
Attack Success Rate Metrics
Automatically calculates:
% of successful attacks
Total number of tests
Displays recent evaluation history
🏗️ Tech Stack
Python
Streamlit – UI + app framework
OpenAI API – LLM interaction (gpt-4o-mini)
Airtable API – Structured logging + data storage
dotenv – Secure environment variable management
Requests – API communication

🧪 How It Works
Enter a prompt in the chat interface
Toggle Injection Test Mode to simulate adversarial conditions
Observe the model’s response
Manually label the outcome:
Pass → model resisted manipulation
Fail → model leaked or followed malicious instruction
Results are:
Logged to Airtable
Used to calculate attack success rate
📊 Example Use Cases
Testing jailbreak prompts against LLMs
Evaluating system prompt robustness
Building datasets of adversarial interactions
Studying model alignment and failure patterns
Rapid prototyping for AI red-teaming workflows
📈 Metrics

The app tracks:

Attack Success Rate (%)
Total Evaluations
Recent Outcomes (Pass/Fail)

This enables quick iteration and comparison across different prompt strategies.

🔍 Future Improvements
Automated evaluation (classifier-based pass/fail)
Multi-model comparison (OpenAI, Anthropic, etc.)
Export logs for offline analysis
Visualization dashboards (e.g., success rate over time)
Prebuilt adversarial prompt library
🤝 Why This Project Matters

As LLMs are increasingly deployed in production systems, understanding their behavior under adversarial conditions is critical.

This project demonstrates:

Practical experience with LLM evaluation workflows
Understanding of prompt injection & jailbreak risks
Ability to build tools for AI safety and analysis
End-to-end integration of APIs, logging, and UI