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
                }
            ],
            "session leak": [
                {
                    "title": "Identifying and Fixing SQLAlchemy Session Leaks",
                    "source": "Engineering Handbook",
                    "url": "https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-frequently-asked-questions",
                    "content": "Ensure every session is closed using context managers or try/finally blocks. Common in long-running background tasks or rebalance workflows.",
                    "pros": "Solves the actual root cause, prevents memory growth",
                    "cons": "Requires code changes and thorough testing"
                },
                {
                    "title": "Python Context Manager Patterns for DB Sessions",
                    "source": "Tech Blog",
                    "url": "https://example.com/blog/python-db-sessions",
                    "content": "Use @contextmanager to wrap DB sessions. Ensure session.close() is always called.",
                    "pros": "Highly reliable pattern",
                    "cons": "Initial refactoring effort"
                }
            ],
            "default": [
                # ... existing default
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
        if "session" in query or "leak" in query:
            results = self.kb["session leak"]
        elif "connection" in query or "pool" in query:
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
