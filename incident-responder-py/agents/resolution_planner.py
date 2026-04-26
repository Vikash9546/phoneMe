import json
from groq import Groq

class ResolutionPlanner:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def create_plan(self, diagnosis, research):
        prompt = f"""
        You are the Incident Commander (Resolution Planner Agent).
        Based on the following inputs, create a step-by-step remediation plan.

        --- DIAGNOSIS ---
        {json.dumps(diagnosis, indent=2)}

        --- RESEARCH ---
        {json.dumps(research, indent=2)}

        Objectives:
        1. Select the safest and most practical solution.
        2. Provide ordered operator instructions.
        3. Include validation steps (pre, during, post).
        4. Include safety/rollback notes.

        Return ONLY a valid JSON object with this structure:
        {{
            "selected_solution": "name",
            "rationale": "reasoning",
            "remediation_steps": ["step 1", "step 2"],
            "pre_checks": ["check 1"],
            "validation_checks": ["check 1"],
            "rollback_plan": "steps",
            "safety_notes": "warnings"
        }}
        """

        if not self.api_key or "placeholder" in self.api_key or "gsk_" not in self.api_key:
            print("[Agent 3] Note: Using Demo Mode (Placeholder Key)")
            return {
                "selected_solution": "Hotfix: Reduce Pool Size + Plan PgBouncer",
                "rationale": "Immediate relief is needed to stop the timeouts. Reducing the pool size per instance will free up DB capacity while we prepare PgBouncer.",
                "remediation_steps": [
                    "Lower DB_POOL_MAX to 10 in config.",
                    "Rolling restart of app instances.",
                    "Monitor for decrease in 504 errors.",
                    "Schedule PgBouncer deployment for next maintenance window."
                ],
                "pre_checks": ["Confirm active connections via 'SELECT count(*) FROM pg_stat_activity'"],
                "validation_checks": ["Check /api/health returns 200 within 100ms", "Check Nginx error logs"],
                "rollback_plan": "Revert DB_POOL_MAX to 20 and restart.",
                "safety_notes": "Ensure you don't reduce the pool below what's needed for peak load handling."
            }

        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
