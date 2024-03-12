# AutoLatexCv

AutoLatexCv is a project that allows you to automatically generate a resume in LaTeX from a json file hosted in pocketbase.

## Installation

> [!IMPORTANT]
> Currently, the json can't really be modified, and the CV must have the same structure as the template json.

First, you need an environment where you can let the code run, like a docker environement. You can install it by following the instructions on the [official website](https://docs.docker.com/get-docker/).

You can also just run the code on your local machine, but you need to have `python3.11` installed.

Then, after cloning the repository, you need to copy the .env.template file to .env and fill the variables with your pocketbase credentials.

When done, you can run the following commands:

```bash
# install the requirements
pip install -r requirements.txt

# run the code
python main.py
```

You need also to have a pocketbase server running. You can install it by following the instructions on the [official website](https://github.com/pocketbase/pocketbase).

Pocketbase should look like:

![alt text](image.png)
![alt text](image-1.png)

For the docker environement, you can run the docker-compose file with the following command:

```bash
# will automatically build the image and run the container

# you need to modify the compose.yml file to add all the environment variables
docker-compose up -d
```

## Template json

```json
{
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
```
