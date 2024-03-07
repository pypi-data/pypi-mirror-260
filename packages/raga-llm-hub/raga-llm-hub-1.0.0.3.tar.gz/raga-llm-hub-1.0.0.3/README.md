<p align="center">
    <img src="https://raw.githubusercontent.com/raga-ai-hub/raga-llm-hub/main/docs/assets/logo-lg_black.png" alt="RagaAI - Logo" width="100%">
</p>

<h1 align="center">
    Raga LLM Hub
</h1>

<h3 align="center">
    <a href="https://raga.ai">Raga AI</a> |
    <a href="https://docs.raga.ai/raga-llm-hub">Documentation</a> |
    <a href="https://docs.raga.ai/raga-llm-hub/quickstart">Getting Started</a>

</h3>


<div align="center">


[![PyPI - Version](https://img.shields.io/pypi/v/raga-llm-hub?label=PyPI%20Package)](https://badge.fury.io/py/raga-llm-hub) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1PQGqDGdcSUxhSvpSQYX8ZdHf5r90WSYf?usp=sharing)
</a> [![Python Compatibility](https://img.shields.io/pypi/pyversions/raga-llm-hub)](https://pypi.org/project/raga-llm-hub/) []()

</div>


Welcome to Raga LLM Eval, a comprehensive evaluation toolkit for Language and Learning Models (LLMs). With over 100 meticulously designed metrics, it is the most comprehensive platform that allows developers and organizations to evaluate and compare LLMs effectively and establish essential guardrails for LLMs and Retrieval Augmented Generation(RAG)  applications. These tests assess various aspects including Relevance & Understanding, Content Quality, Hallucination, Safety & Bias, Context Relevance, Guardrails, and Vulnerability scanning, along with a suite of Metric-Based Tests for quantitative analysis.

The RagaAI LLM Hub is uniquely designed to help teams identify issues and fix them throughout the LLM lifecycle, by identifying issues across the entire RAG pipeline. This is pivotal for understanding the root cause of failures within an LLM application and addressing them at their source, revolutionizing the approach to ensuring reliability and trustworthiness.

## Installation

### Via pip

```bash
# Create and activate a new Python environment
python -m venv venv
source venv/bin/activate
# Install Raga LLM Hub
pip install raga-llm-hub
```


### Via conda
```py
# Create and activate a new Conda environment
conda create --name myenv python=3.11
conda activate myenv
# Install Raga LLM Hub
python -m pip install raga-llm-hub

```

## Quick Tour
### Initialization

```py
from raga_llm_hub import RagaLLMEval, get_data

# Initialize the evaluator with your API key
evaluator = RagaLLMEval(api_key="your_api_key")
```



4. Re-using Previous Results
Leverage previous results for comparative analysis or to track your LLM's performance over time.

```py
PREV_EVAL_ID = "PREVIOUS_RUN_ID"

evaluator.load_eval(
    eval_name=PREV_EVAL_ID
)

evaluator.print_results()
evaluator.save_results("filename.json")
```

### Discover and Run Tests

```py
# List all available tests
evaluator.list_available_tests()

# Add and run a custom test
evaluator.add_test(
    test_name="relevancy_test",
    data={
        "prompt": "How are you?",
        "context": "Responding as a student to a teacher.",
        "response": "I am well, thank you.",
    },
    arguments={"model": "gpt-4", "threshold": 0.5},
).run()

# Review the results
evaluator.print_results()

```

## Managing Results
- **Instant Overview**: Quickly view your test results directly.
- **Save for Detailed Analysis**: Export your results for comprehensive examination or sharing with your team.
- **In-depth Access**: Utilize the app for advanced result processing and visualization.
- **Historical Comparisons**: Leverage past evaluations for ongoing performance tracking.

```py
# Printing Results: View your test results immediately for a quick analysis
evaluator.print_results()

# Saving Results: Export your results to a JSON file for in-depth analysis 
evaluator.save_results("my_test_results.json")

# Accessing Results: Utilize the fetched detailed results and metrics for further processing or visualization
detailed_results = evaluator.get_results()

# Re-using Previous Results: If you have an evaluation ID from a previous run, you can load and compare those results
previous_eval_id = "your_previous_eval_id_here"
evaluator.load_eval(previous_eval_id)

# After loading, you can print, save, or further analyze these results
evaluator.print_results()
```

## Enterprise
Enterprise Version
Introducing raga-llm-platform,(enterprise version of raga-llm-hub)  for Large Language Model (LLM) evaluation and guardrails, designed to empower organizations to harness the full potential of LLMs securely and efficiently. Here’s what sets raga-llm-platform apart:
1. **Production Scale Analysis**
2. **State-of-the-Art Evaluation Methods and Metrics**
3. **Issue Diagnosis and Remediation**
4. **On-Prem/Private Cloud Deployment with Real-Time Streaming Support**
5. **Real-Time Evaluation and Guardrails**

To learn more and see how raga-llm-platform can benefit your organization, [book a call with our team today](https://calendly.com/vijay-srinivas/ragaai-product-offering?month=2024-03). Discover the value of enterprise-grade LLM management tailored to your needs.

## Learn More
For those who wish to dive deeper, we encourage exploring [our extensive documentation](https://docs.raga.ai)

For more details and the latest news from RagaAI, visit [our official website](https://raga.ai).
