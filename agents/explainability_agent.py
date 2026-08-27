from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0
)


def explain_incident(incident, threat, mitre):

    prompt = f"""
You are an explainable cybersecurity AI agent.

Explain why the security incident was classified the way it was.

You have the following information:

SECURITY INCIDENT:
{incident}

THREAT ANALYSIS:
{threat}

MITRE ATT&CK MAPPING:
{mitre}

Provide a clear explanation covering:

1. Why the activity is considered suspicious
2. What evidence supports the classification
3. Why the MITRE ATT&CK technique is appropriate
4. Why the assigned severity is reasonable

Do not invent evidence.
Only use information provided above.

Write the explanation in clear language that a SOC analyst can understand.
"""

    response = llm.invoke(prompt)

    return response.content