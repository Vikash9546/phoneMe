import os
import json
from dotenv import load_dotenv
from agents.log_analyzer import LogAnalyzer
from agents.solution_researcher import SolutionResearcher
from agents.resolution_planner import ResolutionPlanner

def main():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

    print("\n--- 🐍 Python Incident Response System (Powered by Groq) ---")
    
    log_files = {
        "nginx_access": "logs/nginx-access.log",
        "nginx_error": "logs/nginx-error.log",
        "app_error": "logs/app-error.log"
    }

    try:
        # Agent 1: Analysis
        print("\n[Agent 1] Analyzing Logs...")
        analyzer = LogAnalyzer(api_key)
        diagnosis = analyzer.analyze(log_files)
        print(f"Detected Root Cause: {diagnosis['root_cause']} (Confidence: {diagnosis['confidence_level']}%)")

        # Agent 2: Research
        print("\n[Agent 2] Researching Solutions...")
        researcher = SolutionResearcher()
        research = researcher.research(diagnosis)
        print(f"Found {len(research['suggested_solutions'])} technical references.")

        # Agent 3: Planning
        print("\n[Agent 3] Generating Remediation Plan...")
        planner = ResolutionPlanner(api_key)
        plan = planner.create_plan(diagnosis, research)

        # Final Report
        print("\n" + "="*60)
        print("FINAL INCIDENT RESPONSE REPORT")
        print("="*60)
        print(f"\nROOT CAUSE:\n{diagnosis['diagnosis_details']}")
        
        print(f"\nSELECTED SOLUTION:\n{plan['selected_solution']}")
        print(f"Rationale: {plan['rationale']}")

        print("\nREMEDIATION STEPS:")
        for i, step in enumerate(plan['remediation_steps'], 1):
            print(f"{i}. {step}")

        print("\nVALIDATION CHECKS:")
        for check in plan['validation_checks']:
            print(f"[ ] {check}")

        print("\nSAFETY & ROLLBACK:")
        print(plan['rollback_plan'])
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error in Incident Pipeline: {str(e)}")

if __name__ == "__main__":
    main()
