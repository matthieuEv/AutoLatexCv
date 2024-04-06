from jinja2 import Environment, FileSystemLoader
import json
from pdflatex import PDFLaTeX

import urllib.request
import os
import json

import os
import urllib.request

def download_images(data, img_count=0, img_dir='images'):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'image':
                print("image found")
                img_count += 1
                img_path = os.path.abspath(os.path.join(img_dir, f'img{img_count}.png')).replace("\\", "/")
                urllib.request.urlretrieve(value, img_path)
                print("data[key]: ",data[key])
                data[key] = img_path
                print("data[key]: ",data[key])
                print("--")
            else:
                data[key], img_count = download_images(value, img_count, img_dir)
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i], img_count = download_images(data[i], img_count, img_dir)
    return data, img_count


def generatePDF(data,lang):
    if not os.path.exists('images'):
        os.makedirs('images')
    # Download images and update the data
    data, _ = download_images(data)

    print("data: ",data)

    custom_commands = "\\newcommand{\\resumeItem}[1]{  \\item\\small{    {#1 \\vspace{-1pt}}  }}\\newcommand{\\classesList}[4]{    \\item\\small{        {#1 #2 #3 #4 \\vspace{-2pt}}  }}\\newcommand{\\resumeSubheading}[4]{  \\vspace{-2pt}\\item    \\begin{tabular*}{1.0\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}      \\textbf{\\large#1} & \\textbf{\\small #2} \\\\      \\textit{\\large#3} & \\textit{\\small #4} \\\\          \\end{tabular*}\\vspace{-7pt}}\\newcommand{\\resumeSingleSubheading}[4]{  \\vspace{-2pt}\\item    \\begin{tabular*}{1.0\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}      \\textbf{\\large#1} & \\textbf{\\small #2} \\\\          \\end{tabular*}\\vspace{-7pt}}\\newcommand{\\resumeSubSubheading}[2]{    \\item    \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}      \\textit{\\small#1} & \\textit{\\small #2} \\\\    \\end{tabular*}\\vspace{-7pt}}\\newcommand{\\resumeProjectHeading}[2]{    \\item    \\begin{tabular*}{1.001\\textwidth}{l@{\\extracolsep{\\fill}}r}      \\small#1 & \\textbf{\\small #2}\\\\    \\end{tabular*}\\vspace{-7pt}}\\newcommand{\\resumeSubItem}[1]{\\resumeItem{#1}\\vspace{-4pt}}\\renewcommand\\labelitemi{$\\vcenter{\\hbox{\\tiny$\\bullet$}}$}\\renewcommand\\labelitemii{$\\vcenter{\\hbox{\\tiny$\\bullet$}}$}\\newcommand{\\resumeSubHeadingListStart}{\\begin{itemize}[leftmargin=0.0in, label={}]}\\newcommand{\\resumeSubHeadingListEnd}{\\end{itemize}}\\newcommand{\\resumeItemListStart}{\\begin{itemize}[leftmargin=0.1in]}\\newcommand{\\resumeItemListEnd}{\\end{itemize}\\vspace{-5pt}}\\newcommand\\sbullet[1][.5]{\\mathbin{\\vcenter{\\hbox{\\scalebox{#1}{$\\bullet$}}}}}"
    data["custom_commands"] = custom_commands

    # Create a Jinja2 environment and load the templates directory
    env = Environment(loader=FileSystemLoader('./'))

    # Load the LaTeX template
    if lang == "fr":
        template = env.get_template('./template/texFileFr.tex')
    else:
        template = env.get_template('./template/texFileEn.tex')

    # Render the template with the data
    output = template.render(**data)

    # Write the output to a new LaTeX file
    try:
        with open('output.tex', 'w',encoding='utf-8') as f:
            f.write(output)

        print("Le fichier LaTeX a été généré avec succès.")
        pdfl = PDFLaTeX.from_texfile("output.tex")
        print("PDFLaTeX object created successfully.")
        pdfl.set_output_directory("build")
        print("Output directory set successfully.")
        pdfl.set_pdf_filename("output"+lang)
        print("PDF filename set successfully.")
        pdfl.create_pdf(keep_pdf_file=True)
        print("PDF file created successfully.")
    except Exception as e:
        print(f"Error: {e}")

    print("Le fichier LaTeX a été généré avec succès.")

if __name__ == "__main__":
    # Load the JSON data
    with open('template.json', 'r',encoding='utf-8') as f:
        data = json.load(f)

    generatePDF(data,"fr")