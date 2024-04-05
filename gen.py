from jinja2 import Environment, FileSystemLoader
import json
from pdflatex import PDFLaTeX

# Load the JSON data
data = {
    "full_name": "John Doe",
    "phone_number": "+33600000000",
    "email": "example@example.com",
    "description": "I am a software engineer with 10 years of experience. I have worked on a variety of projects and have a strong understanding of software development. I am passionate about learning new technologies and am always looking for new challenges. I am a team player and enjoy working with others to solve complex problems. I am fluent in English and French and have a basic understanding of Spanish. I am also a musician and enjoy playing the guitar, piano, and violin in my free time. I am passionate about music and enjoy playing in my free time. I am also an avid video game player and enjoy playing a variety of games in my free time. I am always looking for new opportunities and am excited to see what the future holds.",
    "links": {
        "Portfolio": "https://example.com",
        "linkedin": "https://example.com",
        "Github": "https://example.com"
    },
    "skills":[
        {
            "Name": "Languages",
            "list": [
                "Python",
                "Java",
                "C++",
                "C"
            ]
        },
        {
            "Name":"Frameworks",
            "list": [
                "Node.js",
                "Spring",
                "React",
                "Angular"
            ]
        },
        {
            "Name":"DevOps and API Tools",
            "list": [
                "Docker",
                "Kubernetes",
                "Jenkins",
                "Postman"
            ]
        },
        {
            "Name":"Others",
            "list":[
                "Agile (Scrum)" 
            ]
        }
    ],
    "languages": {
        "French": "Native",
        "English": "Fluent",
        "Spanish": "Basic"
    },
    "education":[
        {
            "Name": "University of Example",
            "Degree": "Bachelor of Science in Computer Science",
            "Start": "2015",
            "End": "2018",
            "Location": "Paris, France"
        },
        {
            "Name": "Other University of Example",
            "Degree": "Bachelor of Science in Computer Science",
            "Start": "2012",
            "End": "2015",
            "Location": "Nantes, France"
        }
    ],
    "experience":[
        {
            "Title": "Software Engineer",
            "Company": "Example",
            "Start": "2018",
            "End": "Present",
            "Location": "Paris, France",
            "Description": [
                "Developed and maintained software for the company",
                "Worked on a team of 5 to develop a new software"
            ]
        },
        {
            "Title": "Not Software Engineer",
            "Company": "Not Example",
            "Start": "2009",
            "End": "2018",
            "Location": "Nantes, France",
            "Description": [
                "Developed and maintained software for the company",
                "Worked on a team of 5 to develop a new software"
            ]
        }
    ],
    "projects":[
        {
            "Name": "Example Project",
            "Description": "This is an example project",
            "Link": "https://example.com"
        },
        {
            "Name": "Example Project",
            "Description": "Duis et ex deserunt Lorem enim cillum officia. In labore dolor labore occaecat officia nisi. Nostrud irure velit culpa commodo ipsum ea velit aute mollit occaecat ea nulla.",
            "Link": "https://example.com"
        }
    ],
    "extracurricular":[
        {
            "Name":"Guitar",
            "Description":"I have been playing the guitar for 15 years and am passionate about music."
        },
        {
            "Name":"Piano",
            "Description":"I have been playing the piano for 10 years and enjoy playing in my free time."
        },
        {
            "Name":"Violin",
            "Description":"I have been playing the violin for 5 years and enjoy playing in my free time."
        },
        {
            "Name":"Video Games",
            "Description":"I am an avid video game player and enjoy playing a variety of games in my free time."
        }
    ],
    "certification":[
        {
            "Name": "Example Certification",
            "Date": "2018",
            "Link": "https://example.com"
        },
        {
            "Name": "Another Example Certification",
            "Date": "2005",
            "Link": ""
        }
    ]
}

custom_commands = "\\newcommand{\\resumeItem}[1]{  \\item\\small{    {#1 \\vspace{-1pt}}  }}\\newcommand{\\classesList}[4]{    \\item\\small{        {#1 #2 #3 #4 \\vspace{-2pt}}  }}\\newcommand{\\resumeSubheading}[4]{  \\vspace{-2pt}\\item    \\begin{tabular*}{1.0\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}      \\textbf{\\large#1} & \\textbf{\\small #2} \\\\      \\textit{\\large#3} & \\textit{\\small #4} \\\\          \\end{tabular*}\\vspace{-7pt}}\\newcommand{\\resumeSingleSubheading}[4]{  \\vspace{-2pt}\\item    \\begin{tabular*}{1.0\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}      \\textbf{\\large#1} & \\textbf{\\small #2} \\\\          \\end{tabular*}\\vspace{-7pt}}\\newcommand{\\resumeSubSubheading}[2]{    \\item    \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}      \\textit{\\small#1} & \\textit{\\small #2} \\\\    \\end{tabular*}\\vspace{-7pt}}\\newcommand{\\resumeProjectHeading}[2]{    \\item    \\begin{tabular*}{1.001\\textwidth}{l@{\\extracolsep{\\fill}}r}      \\small#1 & \\textbf{\\small #2}\\\\    \\end{tabular*}\\vspace{-7pt}}\\newcommand{\\resumeSubItem}[1]{\\resumeItem{#1}\\vspace{-4pt}}\\renewcommand\\labelitemi{$\\vcenter{\\hbox{\\tiny$\\bullet$}}$}\\renewcommand\\labelitemii{$\\vcenter{\\hbox{\\tiny$\\bullet$}}$}\\newcommand{\\resumeSubHeadingListStart}{\\begin{itemize}[leftmargin=0.0in, label={}]}\\newcommand{\\resumeSubHeadingListEnd}{\\end{itemize}}\\newcommand{\\resumeItemListStart}{\\begin{itemize}[leftmargin=0.1in]}\\newcommand{\\resumeItemListEnd}{\\end{itemize}\\vspace{-5pt}}\\newcommand\\sbullet[1][.5]{\\mathbin{\\vcenter{\\hbox{\\scalebox{#1}{$\\bullet$}}}}}"
data["custom_commands"] = custom_commands

# Create a Jinja2 environment and load the templates directory
env = Environment(loader=FileSystemLoader('./'))

# Load the LaTeX template
template = env.get_template('texFileFr.tex')

# Render the template with the data
output = template.render(**data)

# Write the output to a new LaTeX file
with open('output.tex', 'w',encoding='utf-8') as f:
    f.write(output)

print("Le fichier LaTeX a été généré avec succès.")
