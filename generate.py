import re
import subprocess
import os
from dotenv import load_dotenv
from pdflatex import PDFLaTeX

load_dotenv()

def generatePDF(jsonObject,lang):
    def getComplexValue(key, jsonData):
        remplacement = ''
        match key:
            case "links":
                print("---Generating Link---")
                for link in jsonData[key]:
                    remplacement += r'\\small{-}'+"\n"
                    remplacement += r'\\href{'+jsonData[key][link]+r'}{\\color{blue}{'+link+r'}} ~ '+"\n"
            case "education":
                print("---Generating Education---")
                for education in jsonData[key]:
                    remplacement += r'\\resumeSubheading'+"\n"
                    remplacement += r'{'+education["Name"]+'}{'+education["Location"]+'}'+"\n"
                    remplacement += r'{'+education["Degree"]+'}{'+education["Start"]+' - '+education["End"]+'}'+"\n"
            case "skills":
                print("---Generating Skills---")
                for skill in jsonData[key]:
                    remplacement += r'\\resumeItem{\\normalsize{\\textbf{'+skill["Name"]+r':} '+', '.join(skill["list"])+r'}}'+"\n"
                    remplacement += r'\\vspace{-5pt}'+"\n"
            case "experience":
                print("---Generating Experience---")
                for experience in jsonData[key]:
                    remplacement += r'\\resumeSubheading'+"\n"
                    remplacement += r'{'+experience["Title"]+'}{'+experience["Company"]+'}{'+experience["Location"]+'}{'+experience["Start"]+' - '+experience["End"]+'}'+"\n"
                    remplacement += r'\\resumeItemListStart'+"\n"
                    for description in experience["Description"]:
                        remplacement += r'\\resumeItem{\\normalsize{'+description+'}}'+"\n"
                    remplacement += r'\\resumeItemListEnd'+"\n"
            case "projects":
                print("---Generating Projects---")
                for project in jsonData[key]:
                    remplacement += r'\\resumeItem{\\normalsize{\\textbf{'+project["Name"]+r'}, '+project["Description"]+r'} \\href{'+project["Link"]+r'}{\\color{blue}\\underline{GitHub}}}'+"\n"
                    remplacement += r'\\vspace{-5pt}'+"\n"
            case "certification":
                print("---Generating Certification---")
                for certification in jsonData[key]:
                    if certification["Link"] == "":
                        remplacement += r'\\resumeItem{\\normalsize{\\textbf{'+certification["Name"]+r' ('+certification["Date"]+r')}}}'+"\n"
                        remplacement += r'\\vspace{-5pt}'+"\n"
                    else:
                        remplacement += r'\\resumeItem{\\normalsize{\\textbf{'+certification["Name"]+r' ('+certification["Date"]+r')}} \\href{'+certification["Link"]+r'}{\\color{blue}\\underline{Link}}}'+"\n"
                        remplacement += r'\\vspace{-5pt}'+"\n"
            case "languages":
                print("---Generating Languages---")
                for language in jsonData[key]:
                    remplacement += r'\\resumeItem{\\normalsize{'+language+' - '+jsonData[key][language]+r'}}'+"\n"
                    remplacement += r'\\vspace{-5pt}'+"\n"
            case "extracurricular":
                print("---Generating Extracurricular---")
                for extra in jsonData[key]:
                    remplacement += r'\\resumeItem{\\normalsize{\\textbf{'+extra["Name"]+r':} '+extra["Description"]+r'}}'+"\n"
                    remplacement += r'\\vspace{-5pt}'+"\n"
            case _:
                print("---Generating Default---")
                remplacement = jsonData[key]
        return remplacement

    # Ouvrir le fichier .tex en mode lecture
    print("Lang: ",lang)
    if lang == "fr":
        print("---Opening French File---")
        with open('texFileFr.tex', 'r', encoding='utf-8') as file:
            print("---File Opened---")
            filedata = file.read()
    else:
        print("---Opening English File---")
        with open('texFileEn.tex', 'r', encoding='utf-8') as file:
            print("---File Opened---")
            filedata = file.read()

    # Remplacer chaque {{key}} par la valeur correspondante dans le fichier JSON
    for key, value in jsonObject.items():
        if isinstance(value, str):
            filedata = re.sub(r'{{'+key+'}}', value, filedata)
        else:
            filedata = re.sub(r'{{complex.'+key+'}}', getComplexValue(key,jsonObject), filedata)

    # Créer un nouveau fichier .tex temporaire dans le répertoire /build
    tempTex = os.path.join(os.getenv('OUTPUT_DIRECTORY'), "temp.tex")
    print("---Creating Temp File---")
    print(tempTex)
    with open(tempTex, 'w', encoding='utf-8') as file:
        print("---Temp File Created---")
        file.write(filedata)

    print("\n\nOutput Directory: ",os.getenv('OUTPUT_DIRECTORY'))
    # Convertir le fichier .tex temporaire en PDF en utilisant pdflatex
    print("\n\nConverting Latex to PDF")
    pdfl = PDFLaTeX.from_texfile(tempTex)
    print("\n\nPDFLatex Object Created")
    pdfl.set_output_directory(os.getenv('OUTPUT_DIRECTORY'))
    print("\n\nOutput Directory Set")
    pdfl.set_pdf_filename("output"+lang)
    print("\n\nPDF Filename Set")
    pdfl.create_pdf(keep_pdf_file=True)
    print("\n\nLatex to PDF Converted Successfully")

if __name__ == "__main__":

    json={
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
    generatePDF(json,"en")