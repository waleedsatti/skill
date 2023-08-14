import openai
from docx import Document
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    cv_file = request.files['cv']
    job_desc_file = request.files['jobDescription']

    # Load and process the CV text
    cv_text = cv_file.read().decode('utf-8')

    # Load and process the job description text from docx file
    doc = Document(job_desc_file)
    job_description = "\n".join([para.text for para in doc.paragraphs])

    # Extract skills using ChatGPT from CV
    openai.api_key = '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'

    # Combine job description analysis and resume analysis
    combined_prompt = f"Analyze the job description to identify the required skills, experience, and qualifications, and analyze the applicant's resume to identify their soft skills, hard skills, transferable skills, the relevance of their experience to the job, and other qualifications.\n\nJob description:\n{job_description}\n\nResume:\n{cv_text}\n\nMatching skills and report:"

    response_combined_analysis = openai.Completion.create(
        engine="text-davinci-003",
        prompt=combined_prompt,
        max_tokens=200  # You can adjust this based on your requirements
    )

    # Extracted required qualifications and matching skills report from combined analysis response
    response_text = response_combined_analysis.choices[0].text.strip()
    required_qualifications = response_text.split('\n\n')[0]
    matching_skills_report = "\n\n".join(response_text.split('\n\n')[1:])

    # Prompt for analyzing skills in CV in the context of job description
    analyze_prompt = f"Analyze the context of each skill mentioned in the CV to understand how it is relevant to the job description. Provide a bullet-point list of skills gap and their relevance.\n\nJob description:\n{job_description}\n\nCV skills:\n{cv_text}\n\n skills gap and relevance:\n"

    response_analyze = openai.Completion.create(
        engine="text-davinci-003",
        prompt=analyze_prompt,
        max_tokens=200  # You can adjust this based on your requirements
    )

    # Extracted matching skills and relevance from response
    matching_skills_and_relevance = response_analyze.choices[0].text.strip()

 

    # Render results template with extracted data
    return render_template('results.html', matching_skills_report=matching_skills_report, matching_skills_and_relevance=matching_skills_and_relevance)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


