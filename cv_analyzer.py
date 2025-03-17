import pandas as pd
import re
import io
import base64
from datetime import datetime
import PyPDF2
import docx
import random

class CVAnalyzer:
    def __init__(self):
        """Initialize the CV Analyzer with default settings."""
        self.skills_database = {
            "python": ["python", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "django", "flask"],
            "javascript": ["javascript", "react", "vue", "angular", "node.js", "express", "jquery"],
            "data_science": ["machine learning", "data analysis", "statistical analysis", "big data", "data mining"],
            "databases": ["sql", "mysql", "postgresql", "mongodb", "oracle", "database management"],
            "project_management": ["agile", "scrum", "kanban", "project planning", "team leadership"],
            "communication": ["presentation", "teamwork", "verbal communication", "written communication"],
            "languages": ["english", "german", "french", "spanish", "chinese", "russian", "arabic"],
            "design": ["ui design", "ux design", "graphic design", "adobe", "photoshop", "illustrator"]
        }
        
        self.professions = [
            "Software Engineer", "Data Scientist", "Project Manager", "UI/UX Designer",
            "Product Manager", "Marketing Specialist", "Financial Analyst", "HR Manager"
        ]
        
        self.experience_levels = ["Junior", "Mid-Level", "Senior", "Lead", "Manager", "Director", "VP", "C-Level"]
    
    def extract_text(self, file_path):
        """Extract text from PDF or DOCX file."""
        if file_path.lower().endswith('.pdf'):
            return self._extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            return self._extract_text_from_docx(file_path)
        elif file_path.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            raise ValueError("Unsupported file format. Please use PDF, DOCX, or TXT.")
    
    def _extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file."""
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        return text
    
    def _extract_text_from_docx(self, docx_path):
        """Extract text from DOCX file."""
        doc = docx.Document(docx_path)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text)
    
    def analyze_cv_file(self, file_path, job_description=None):
        """Analyze a CV file and return results."""
        # Extract text from the file
        cv_text = self.extract_text(file_path)
        
        # Perform analysis
        results = self._analyze_cv_text(cv_text)
        
        # If job description is provided, match CV against it
        if job_description:
            results.update(self._match_with_job_description(results, job_description))
        
        return results
    
    def _analyze_cv_text(self, cv_text):
        """Analyze CV text and extract key information."""
        # In a real implementation, this would use more sophisticated NLP
        # For demo purposes, we'll use simple pattern matching and randomization
        
        # Extract skills
        skills = self._extract_skills(cv_text)
        
        # Extract experience
        experience = self._extract_experience(cv_text)
        
        # Determine profession (simplified)
        profession = self._determine_profession(cv_text)
        
        # Determine experience level (simplified)
        experience_level = self._determine_experience_level(experience)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(skills, experience)
        
        return {
            "skills": skills,
            "experience": experience,
            "profession": profession,
            "experience_level": experience_level,
            "relevance_score": random.uniform(60, 95),  # Random score for demo
            "recommendations": recommendations
        }
    
    def _extract_skills(self, text):
        """Extract skills from CV text."""
        text = text.lower()
        skills = {}
        
        # For each skill category, check presence in text
        for category, keywords in self.skills_database.items():
            for keyword in keywords:
                if keyword in text:
                    # Assign a score (in a real implementation, this would be more sophisticated)
                    skills[keyword] = random.uniform(50, 100)
        
        return skills
    
    def _extract_experience(self, text):
        """Extract work experience from CV text (simplified)."""
        # In a real implementation, this would use NER and pattern recognition
        # For demo, we'll generate some plausible experience entries
        experience = []
        
        # Try to find company names (simplified)
        company_pattern = r"(?:at|for|with)\s+([A-Z][A-Za-z\s]+(?:Inc|LLC|Ltd|GmbH|AG|SE|Company|Corp)?)"
        companies = re.findall(company_pattern, text)
        
        # Generate random experience entries
        for i, company in enumerate(companies[:5]):  # Limit to 5 entries
            # Generate random dates
            end_year = 2024 - i
            start_year = end_year - random.randint(1, 4)
            
            experience.append({
                "title": random.choice(["Software Developer", "Senior Engineer", "Project Manager", "Data Analyst", "Team Lead"]),
                "company": company.strip(),
                "description": f"Worked on various projects at {company.strip()}",
                "start_date": f"{start_year}-01-01",
                "end_date": f"{end_year}-12-31",
                "duration": end_year - start_year
            })
        
        return experience
    
    def _determine_profession(self, text):
        """Determine profession from CV text."""
        # In a real implementation, this would use classification or keyword extraction
        # For demo, choose a profession that seems most relevant based on keyword count
        text = text.lower()
        profession_scores = {}
        
        profession_keywords = {
            "Software Engineer": ["software", "developer", "programming", "code", "engineer"],
            "Data Scientist": ["data", "analytics", "machine learning", "statistics", "analysis"],
            "Project Manager": ["project", "management", "agile", "scrum", "planning"],
            "UI/UX Designer": ["design", "user interface", "user experience", "ui", "ux"],
            "Product Manager": ["product", "roadmap", "features", "requirements", "stakeholders"],
            "Marketing Specialist": ["marketing", "campaign", "social media", "advertising", "brand"],
            "Financial Analyst": ["finance", "financial", "accounting", "analysis", "budget"],
            "HR Manager": ["hr", "human resources", "recruiting", "talent", "onboarding"]
        }
        
        for profession, keywords in profession_keywords.items():
            score = 0
            for keyword in keywords:
                score += text.count(keyword)
            profession_scores[profession] = score
        
        # Return profession with highest score
        if profession_scores:
            return max(profession_scores, key=profession_scores.get)
        else:
            return "Not determined"
    
    def _determine_experience_level(self, experience):
        """Determine experience level based on work history."""
        # Calculate total years of experience
        total_years = sum(exp.get("duration", 0) for exp in experience)
        
        # Determine level based on years
        if total_years < 2:
            return "Junior"
        elif total_years < 5:
            return "Mid-Level"
        elif total_years < 8:
            return "Senior"
        elif total_years < 12:
            return "Lead"
        else:
            return "Manager"
    
    def _generate_recommendations(self, skills, experience):
        """Generate recommendations based on CV analysis."""
        recommendations = []
        
        # Add recommendations based on skills
        if len(skills) < 5:
            recommendations.append("Consider adding more skills to your CV to showcase your expertise.")
        
        # Add recommendation for experience
        if len(experience) < 3:
            recommendations.append("Add more details about your work experience, including achievements and responsibilities.")
        
        # Add general recommendations
        recommendations.append("Quantify your achievements with metrics and results where possible.")
        recommendations.append("Tailor your CV for each specific job application.")
        
        return recommendations
    
    def _match_with_job_description(self, cv_results, job_description):
        """Match CV results with job description."""
        # Convert job description to lowercase for matching
        job_text = job_description.lower()
        
        # Extract required skills from job description (simplified)
        required_skills = {}
        for category, keywords in self.skills_database.items():
            for keyword in keywords:
                if keyword in job_text:
                    # Assign importance to the skill
                    required_skills[keyword] = random.uniform(60, 100)
        
        # Determine which skills are missing or need improvement
        cv_skills = cv_results.get("skills", {})
        missing_skills = {}
        
        for skill, importance in required_skills.items():
            if skill not in cv_skills:
                missing_skills[skill] = importance
            elif cv_skills[skill] < importance:
                # Skill needs improvement
                missing_skills[skill] = importance
        
        # Calculate match score
        matches = 0
        for skill in required_skills:
            if skill in cv_skills:
                matches += 1
        
        match_score = (matches / max(1, len(required_skills))) * 100 if required_skills else 70
        
        # Generate job-specific recommendations
        job_recommendations = []
        
        if missing_skills:
            skills_to_improve = ", ".join(list(missing_skills.keys())[:3])
            job_recommendations.append(f"Highlight or develop skills in: {skills_to_improve}")
        
        job_recommendations.append("Customize your CV to better match the job requirements.")
        job_recommendations.append("Highlight relevant achievements that demonstrate required competencies.")
        
        return {
            "relevance_score": match_score,
            "missing_skills": missing_skills,
            "recommendations": cv_results.get("recommendations", []) + job_recommendations
        }
    
    def export_results(self, results, format="csv"):
        """Export analysis results to specified format."""
        if format == "csv":
            return self._export_to_csv(results)
        elif format == "excel":
            return self._export_to_excel(results)
        else:
            raise ValueError("Unsupported export format. Please use 'csv' or 'excel'.")
    
    def _export_to_csv(self, results):
        """Export results to CSV format."""
        # Create DataFrames for different sections
        dfs = {}
        
        # Skills DataFrame
        if "skills" in results and results["skills"]:
            skills_df = pd.DataFrame({
                "Skill": list(results["skills"].keys()),
                "Rating": list(results["skills"].values())
            })
            dfs["Skills"] = skills_df
        
        # Experience DataFrame
        if "experience" in results and results["experience"]:
            experience_df = pd.DataFrame(results["experience"])
            dfs["Experience"] = experience_df
        
        # Create CSV output
        output = io.StringIO()
        
        # Write overview
        output.write("CV Analysis Results\n")
        output.write(f"Profession: {results.get('profession', 'Not determined')}\n")
        output.write(f"Experience Level: {results.get('experience_level', 'Not determined')}\n")
        output.write(f"Relevance Score: {results.get('relevance_score', 0):.2f}%\n\n")
        
        # Write skills table
        if "Skills" in dfs:
            output.write("Skills:\n")
            dfs["Skills"].to_csv(output, index=False)
            output.write("\n")
        
        # Write experience table
        if "Experience" in dfs:
            output.write("Experience:\n")
            dfs["Experience"].to_csv(output, index=False)
            output.write("\n")
        
        # Write recommendations
        if "recommendations" in results and results["recommendations"]:
            output.write("Recommendations:\n")
            for i, rec in enumerate(results["recommendations"]):
                output.write(f"{i+1}. {rec}\n")
        
        return output.getvalue()
    
    def _export_to_excel(self, results):
        """Export results to Excel format."""
        # Create an Excel file in memory
        output = io.BytesIO()
        
        # Create Excel writer
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Create overview sheet
            overview_data = {
                "Field": ["Profession", "Experience Level", "Relevance Score"],
                "Value": [
                    results.get("profession", "Not determined"),
                    results.get("experience_level", "Not determined"),
                    f"{results.get('relevance_score', 0):.2f}%"
                ]
            }
            overview_df = pd.DataFrame(overview_data)
            overview_df.to_excel(writer, sheet_name="Overview", index=False)
            
            # Create skills sheet
            if "skills" in results and results["skills"]:
                skills_df = pd.DataFrame({
                    "Skill": list(results["skills"].keys()),
                    "Rating": list(results["skills"].values())
                })
                skills_df.to_excel(writer, sheet_name="Skills", index=False)
            
            # Create experience sheet
            if "experience" in results and results["experience"]:
                experience_df = pd.DataFrame(results["experience"])
                experience_df.to_excel(writer, sheet_name="Experience", index=False)
            
            # Create recommendations sheet
            if "recommendations" in results and results["recommendations"]:
                recs_df = pd.DataFrame({
                    "Recommendation": results["recommendations"]
                })
                recs_df.to_excel(writer, sheet_name="Recommendations", index=False)
            
            # Create missing skills sheet if available
            if "missing_skills" in results and results["missing_skills"]:
                missing_df = pd.DataFrame({
                    "Skill": list(results["missing_skills"].keys()),
                    "Importance": list(results["missing_skills"].values())
                })
                missing_df.to_excel(writer, sheet_name="Missing Skills", index=False)
        
        # Get the Excel data
        output.seek(0)
        excel_data = output.getvalue()
        
        return excel_data
