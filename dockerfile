FROM python:3.11

WORKDIR /auto-latex-cv

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install texlive-latex-base -y
RUN apt-get update -y
RUN apt-get install texlive-fonts-recommended -y
RUN apt-get install texlive-fonts-extra -y
RUN apt autoremove -y
RUN mkdir build

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "main.py" ]

# docker buildx build . -t matthieuev/auto-latex-cv:v0.1.1 --platform linux/arm64/v8 --push