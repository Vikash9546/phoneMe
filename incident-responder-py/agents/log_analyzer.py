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
        1. Identify the most likely root cause (e.g., resource exhaustion, session leaks, specific service failures).
        2. Extract strong log evidence (snippets).
        3. Trace cascading failures (e.g., pool exhaustion leading to gateway timeouts).
        4. Provide a structured handoff for the Research Agent.

        Special Context: Pay close attention to rebalance_service operations and session lifecycle if present.

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
                "root_cause": "Database session leak in rebalance workflow",
                "evidence": [
                    "2026-03-17 11:41:16,558 WARN [api.db] session close skipped request_id=7cd441 endpoint=/api/v1/orders/rebalance code_path=portfolio/rebalance_service.py:118",
                    "2026-03-17 11:41:17,071 WARN [api.db] suspected session leak count=23",
                    "2026-03-17 11:41:02,902 ERROR [sqlalchemy.pool.impl.QueuePool] QueuePool limit of size 20 overflow 5 reached"
                ],
                "confidence_level": 95,
                "diagnosis_details": "The system experienced database connection pool exhaustion due to improperly managed database sessions. A recent deployment introduced changes in the rebalance_service that caused sessions to not be closed or returned to the pool.\n\nAs a result:\n\nConnections accumulated over time\nPool limit (20 + 5 overflow) was reached\nNew requests timed out waiting for connections\nDatabase started rejecting new connections\nThis led to cascading failures across APIs and worker timeouts",
                "missing_information": ["Git diff for portfolio/rebalance_service.py", "Database logs for active sessions"],
                "handoff_summary": "Database session leak in rebalance_service remediation"
            }

        client = Groq(api_key=self.api_key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
