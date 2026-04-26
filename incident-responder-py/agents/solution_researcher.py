class SolutionResearcher:
    def __init__(self):
        # Simulated technical knowledge base for research
        self.kb = {
            "connection pool": [
                {
                    "title": "Scaling PostgreSQL Connections",
                    "source": "Postgres Official",
                    "url": "https://www.postgresql.org/docs/current/external-plumbing.html",
                    "content": "Implement connection pooling using tools like PgBouncer. Avoid connecting directly from many app instances.",
                    "pros": "Drastically reduces DB overhead",
                    "cons": "Requires managing an extra service"
                },
                {
                    "title": "Application Pool Tuning",
                    "source": "Engineering Blog",
                    "url": "https://example.com/blog/pool-tuning",
                    "content": "Set pool size to (Total Max Connections / Replicas) - 5 to leave headroom.",
                    "pros": "Immediate fix without new infra",
                    "cons": "May limit peak throughput"
                }
            ],
            "default": [
                {
                    "title": "Standard SRE Response",
                    "source": "SRE Handbook",
                    "url": "https://sre.google/",
                    "content": "Check CPU, memory, and disk space. Restart services if healthy but stuck.",
                    "pros": "Wide coverage",
                    "cons": "Vague for specific issues"
                }
            ]
        }

    def research(self, diagnosis):
        query = diagnosis.get("handoff_summary", "").lower()
        
        results = []
        if "connection" in query or "pool" in query:
            results = self.kb["connection pool"]
        else:
            results = self.kb["default"]

        return {
            "suggested_solutions": [
                {
                    "name": r["title"],
                    "description": r["content"],
                    "pros": r["pros"],
                    "cons": r["cons"],
                    "source_url": r["url"]
                } for r in results
            ],
            "risky_actions": ["Increasing max_connections blindly", "Restarting DB without a failover plan"]
        }
