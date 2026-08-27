from langchain_ollama import ChatOllama
from models.schemas import ThreatAnalysis


llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0
)

structured_llm = llm.with_structured_output(ThreatAnalysis)


def threat_hunter(incident):

    prompt = f"""
You are a cybersecurity threat-hunting agent.

Analyze the following security incident.

Determine:
1. Attack type
2. Severity
3. Confidence between 0 and 1
4. Evidence supporting your conclusion
5. A short explanation

Only use evidence contained in the incident.
Do not invent events or information.

Security Incident:

{incident}
"""

    result = structured_llm.invoke(prompt)

    return result