from jinja2 import Environment, FileSystemLoader
import json
from pdflatex import PDFLaTeX

def generatePDF(data,lang):
    custom_commands = "\\newcommand{\\resumeItem}[1]{  \\item\\small{    {#1 \\vspace{-1pt}}  }}\\newcommand{\\classesList}[4]{    \\item\\small{        {#1 #2 #3 #4 \\vspace{-2pt}}  }}\\newcommand{\\resumeSubheading}[4]{  \\vspace{-2pt}\\item    \\begin{tabular*}{1.0\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}      \\textbf{\\large#1} & \\textbf{\\small #2} \\\\      \\textit{\\large#3} & \\textit{\\small #4} \\\\          \\end{tabular*}\\vspace{-7pt}}\\newcommand{\\resumeSingleSubheading}[4]{  \\vspace{-2pt}\\item    \\begin{tabular*}{1.0\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}      \\textbf{\\large#1} & \\textbf{\\small #2} \\\\          \\end{tabular*}\\vspace{-7pt}}\\newcommand{\\resumeSubSubheading}[2]{    \\item    \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}      \\textit{\\small#1} & \\textit{\\small #2} \\\\    \\end{tabular*}\\vspace{-7pt}}\\newcommand{\\resumeProjectHeading}[2]{    \\item    \\begin{tabular*}{1.001\\textwidth}{l@{\\extracolsep{\\fill}}r}      \\small#1 & \\textbf{\\small #2}\\\\    \\end{tabular*}\\vspace{-7pt}}\\newcommand{\\resumeSubItem}[1]{\\resumeItem{#1}\\vspace{-4pt}}\\renewcommand\\labelitemi{$\\vcenter{\\hbox{\\tiny$\\bullet$}}$}\\renewcommand\\labelitemii{$\\vcenter{\\hbox{\\tiny$\\bullet$}}$}\\newcommand{\\resumeSubHeadingListStart}{\\begin{itemize}[leftmargin=0.0in, label={}]}\\newcommand{\\resumeSubHeadingListEnd}{\\end{itemize}}\\newcommand{\\resumeItemListStart}{\\begin{itemize}[leftmargin=0.1in]}\\newcommand{\\resumeItemListEnd}{\\end{itemize}\\vspace{-5pt}}\\newcommand\\sbullet[1][.5]{\\mathbin{\\vcenter{\\hbox{\\scalebox{#1}{$\\bullet$}}}}}"
    data["custom_commands"] = custom_commands

    # Create a Jinja2 environment and load the templates directory
    env = Environment(loader=FileSystemLoader('./'))

    # Load the LaTeX template
    if lang == "fr":
        template = env.get_template('texFileFr.tex')
    else:
        template = env.get_template('texFileEn.tex')

    # Render the template with the data
    output = template.render(**data)

    # Write the output to a new LaTeX file
    try:
        with open('output.tex', 'w',encoding='utf-8') as f:
            f.write(output)

        pdfl = PDFLaTeX.from_texfile("output.tex")
        pdfl.set_output_directory("output")
        pdfl.set_pdf_filename("output"+lang)
        pdfl.create_pdf(keep_pdf_file=True)
    except Exception as e:
        print(f"Error: {e}")

    print("Le fichier LaTeX a été généré avec succès.")

if __name__ == "__main__":
    # Load the JSON data
    with open('data.json', 'r',encoding='utf-8') as f:
        data = json.load(f)

    generatePDF(data,"fr")