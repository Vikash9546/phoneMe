import os
import json
from dotenv import load_dotenv
from agents.log_analyzer import LogAnalyzer
from agents.solution_researcher import SolutionResearcher
from agents.resolution_planner import ResolutionPlanner

def main():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

    print("\n" + "="*60)
    print("INCIDENT RESPONSE SYSTEM - MULTI-AGENT EXECUTION")
    print("="*60)
    
    log_files = {
        "nginx_access": "logs/nginx-access.log",
        "nginx_error": "logs/nginx-error.log",
        "app_error": "logs/app-error.log"
    }

    try:
        # --- AGENT 1: LOG ANALYSIS ---
        print("\n[AGENT 1] LOG ANALYSIS RESULTS")
        print("-" * 30)
        analyzer = LogAnalyzer(api_key)
        diagnosis = analyzer.analyze(log_files)
        
        print(f"OVERALL ROOT CAUSE: {diagnosis['root_cause']}")
        print(f"CONFIDENCE LEVEL: {diagnosis['confidence_level']}%")
        
        print("\nINDIVIDUAL LOG FILE ANALYSIS:")
        for log_name, analysis in diagnosis.get('per_log_analysis', {}).items():
            print(f"  > {log_name.upper()}: {analysis}")

        print("\nLOG EVIDENCE SNIPPETS:")
        for snippet in diagnosis['evidence']:
            print(f"  - {snippet}")

        # --- AGENT 2: SOLUTION RESEARCH ---
        print("\n[AGENT 2] SOLUTION RESEARCH RESULTS")
        print("-" * 30)
        researcher = SolutionResearcher()
        research = researcher.research(diagnosis)
        
        print(f"RESEARCH SUMMARY: {len(research['suggested_solutions'])} sources retrieved.")
        for i, sol in enumerate(research['suggested_solutions'], 1):
            print(f"\nSOLUTION {i}: {sol['name']}")
            print(f"  Description: {sol['description']}")
            print(f"  Source: {sol['source_url']}")
            print(f"  Pros: {sol['pros']}")
            print(f"  Cons: {sol['cons']}")

        # --- AGENT 3: RESOLUTION PLANNING ---
        print("\n[AGENT 3] RESOLUTION PLANNING RESULTS")
        print("-" * 30)
        planner = ResolutionPlanner(api_key)
        plan = planner.create_plan(diagnosis, research)

        print(f"SELECTED STRATEGY: {plan['selected_solution']}")
        print(f"RATIONALE: {plan['rationale']}")

        print("\nOPERATOR REMEDIATION STEPS:")
        for i, step in enumerate(plan['remediation_steps'], 1):
            print(f"  {i}. {step}")

        print("\nVALIDATION CHECKS:")
        for check in plan['validation_checks']:
            print(f"  [ ] {check}")

        print("\nSAFETY & ROLLBACK PLAN:")
        print(f"  {plan['rollback_plan']}")
        
        print("\n" + "="*60)
        print("EXECUTION COMPLETE")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error in Incident Pipeline: {str(e)}")

if __name__ == "__main__":
    main()
