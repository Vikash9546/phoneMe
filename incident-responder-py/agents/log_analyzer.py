import json
import os
from groq import Groq

class LogAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def analyze(self, log_files):
        logs_content = {}
        for name, file_path in log_files.items():
            with open(file_path, 'r') as f:
                logs_content[name] = f.read()

        prompt = f"""
        You are an expert SRE (Site Reliability Engineer). 
        Analyze the following log files from a production API incident:

        {json.dumps(logs_content, indent=2)}

        Objectives:
        1. Identify the most likely root cause.
        2. Extract strong log evidence (snippets).
        3. Highlight uncertainty or missing evidence.
        4. Provide a structured handoff for the Research Agent.

        Return ONLY a valid JSON object with this structure:
        {{
            "root_cause": "brief description",
            "evidence": ["snippet 1", "snippet 2"],
            "confidence_level": 0-100,
            "diagnosis_details": "detailed explanation",
            "missing_information": ["item 1"],
            "handoff_summary": "structured string for search query"
        }}
        """

        if not self.api_key or "placeholder" in self.api_key or "gsk_" not in self.api_key:
            print("[Agent 1] Note: Using Demo Mode (Placeholder Key)")
            return {
                "root_cause": "Database Connection Pool Exhaustion",
                "evidence": [
                    "ERROR: ConnectionAcquisitionTimeout: Pool is full.",
                    "upstream timed out (110: Connection timed out)"
                ],
                "confidence_level": 98,
                "diagnosis_details": "The application is unable to acquire connections from the pool (max_size=20), leading to 504 Gateway Timeouts on critical endpoints.",
                "missing_information": ["DB server CPU usage", "Network latency between app and DB"],
                "handoff_summary": "PostgreSQL connection pool exhaustion remediation and PgBouncer setup"
            }

        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
