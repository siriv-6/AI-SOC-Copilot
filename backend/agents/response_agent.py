from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0
)


def generate_response(incident, threat, mitre):

    prompt = f"""
You are a cybersecurity incident response planning agent.

Analyze the following security incident and recommend appropriate
actions for a SOC analyst.

SECURITY INCIDENT:
{incident}

THREAT ANALYSIS:
{threat}

MITRE ATT&CK MAPPING:
{mitre}

Provide:

1. Immediate actions
2. Investigation actions
3. Containment recommendations
4. Prevention recommendations

Important:
- Recommendations only.
- Do not claim that any action has actually been executed.
- Do not invent evidence.
- Keep the recommendations practical and relevant to the incident.
"""

    response = llm.invoke(prompt)

    return response.content