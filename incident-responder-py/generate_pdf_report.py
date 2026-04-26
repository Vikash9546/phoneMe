import os
import json
from fpdf import FPDF
from dotenv import load_dotenv
from agents.log_analyzer import LogAnalyzer
from agents.solution_researcher import SolutionResearcher
from agents.resolution_planner import ResolutionPlanner

class IncidentReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Incident Response Report', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body)
        self.ln()

def generate_report():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    log_files = {
        "nginx_access": "logs/nginx-access.log",
        "nginx_error": "logs/nginx-error.log",
        "app_error": "logs/app-error.log"
    }

    # Run Pipeline
    analyzer = LogAnalyzer(api_key)
    diagnosis = analyzer.analyze(log_files)
    
    researcher = SolutionResearcher()
    research = researcher.research(diagnosis)
    
    planner = ResolutionPlanner(api_key)
    plan = planner.create_plan(diagnosis, research)

    # Create PDF
    pdf = IncidentReportPDF()
    pdf.add_page()

    # Section 1: Diagnosis
    pdf.chapter_title('1. Log Analysis & Diagnosis')
    pdf.chapter_body(f"Root Cause: {diagnosis['root_cause']}\nConfidence: {diagnosis['confidence_level']}%\n\nDetails:\n{diagnosis['diagnosis_details']}")
    
    # Add Image 1 (Screenshot Placeholder)
    img1_path = "/Users/vikashkumar/.gemini/antigravity/brain/06a985e6-7c92-4fab-8605-7a6b3328c3bb/log_analysis_report_1777206328876.png"
    if os.path.exists(img1_path):
        pdf.image(img1_path, x=10, w=180)
        pdf.ln(10)

    # Section 2: Research
    pdf.add_page()
    pdf.chapter_title('2. Technical Solution Research')
    solutions_text = "\n".join([f"- {s['name']}: {s['description']}" for s in research['suggested_solutions']])
    pdf.chapter_body(f"Solutions Evaluated:\n{solutions_text}")

    # Section 3: Remediation Plan
    pdf.chapter_title('3. Final Remediation Plan')
    plan_text = f"Selected Solution: {plan['selected_solution']}\n\nSteps:\n" + "\n".join([f"{i+1}. {step}" for i, step in enumerate(plan['remediation_steps'])])
    pdf.chapter_body(plan_text)

    # Add Image 2 (Remediation Screenshot)
    img2_path = "/Users/vikashkumar/.gemini/antigravity/brain/06a985e6-7c92-4fab-8605-7a6b3328c3bb/remediation_plan_screenshot_1777206355891.png"
    if os.path.exists(img2_path):
        pdf.image(img2_path, x=10, w=180)

    output_path = "Incident_Report.pdf"
    pdf.output(output_path)
    print(f"Report generated successfully: {output_path}")

if __name__ == "__main__":
    generate_report()
