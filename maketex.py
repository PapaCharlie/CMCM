#!/usr/bin/python

import sys
import os
import argparse
from subprocess import Popen

DEVNULL = open(os.devnull, 'wb')

gitignore = """\
%s.*
!%s
.build/"""

classes = {'3': 'MATH 3610',  '4': 'CS 4320',  'A': 'ASTRO 3310',  'C': 'CS 4700',  'E': 'ECON 1110',  'P': 'PRAC CS 4700'}

extras = {
    '3': r"""\usepackage{float}
\usepackage{listings, color, times, textcomp, float}
\definecolor{mygreen}{RGB}{28,172,0} % color values Red, Green, Blue
\definecolor{mylilas}{RGB}{170,55,241}
\lstset{language=Matlab, basicstyle=\scriptsize\ttfamily,breaklines=true,
frame=single,morekeywords={matlab2tikz},keywordstyle=\color{blue},
morekeywords=[2]{1},keywordstyle=[2]{\color{black}},
identifierstyle=\color{black},stringstyle=\color{mylilas},
commentstyle=\color{mygreen},showstringspaces=false, numbers=left,
numberstyle={\tiny \color{black}},numbersep=9pt,emph=[1]{for,end,break},
emphstyle=[1]\color{red},literate={~} {\texttildelow}{1}}""",
    '4': r"""\usepackage{listings, times}
\usepackage[usenames,dvipsnames]{xcolor}
\lstset{language=SQL,basicstyle=\ttfamily\small,numbers=left,
numberstyle=\footnotesize,stepnumber=0,numbersep=5pt,
backgroundcolor=\color{white},commentstyle=\color{Aquamarine},
keywordstyle=\color{OrangeRed},showspaces=false,showstringspaces=false,
showtabs=false,frame=single,tabsize=2,captionpos=b,
breaklines=true,breakatwhitespace=false,moredelim=**[is][\color{black}]{@}{@}}""",
    'A': r'\usepackage[binary-units=true]{siunitx}',
    'E': '',
    'C': r"""\usepackage{tikz, caption,subcaption, float}
\usetikzlibrary{arrows}
\usetikzlibrary{positioning}""",
    'P': ''
}

makefile_extras = {
    '3': '',
    '4': '',
    'A': '',
    'E': '',
    'C': '',
    'P': ''
}

default_author = "Paul Chesnais (pmc85)"

authors = {
    '3': default_author,
    '4': 'Paul Chesnais (pmc85), Justin Hendrick (jjh267) and Benjamin Shulman (bgs53)',
    'A': default_author,
    'E': default_author,
    'C': default_author,
    'P': default_author
}

tex = r"""\documentclass{{article}}
% \usepackage[margin=2.5cm]{{geometry}}
\usepackage[margin=2cm, headheight=0pt, headsep=1cm]{{geometry}}
\usepackage{{enumerate, fancyhdr, graphicx, amsmath}}

\title{{{class_name} - HW\#{hw}}}
\author{{{author}}}
\date{{\today}}

\pagestyle{{fancy}}
\fancyhead{{}}
\lhead{{{short_author}}}
\chead{{{class_name} - HW\#{hw}}}
\rhead{{\today}}
\fancyfoot{{}}
\rfoot{{\thepage}}
\lfoot{{\includegraphics[height=20pt]{{Logo}}}}
\renewcommand{{\headrulewidth}}{{0.5pt}}
\renewcommand{{\footrulewidth}}{{0.5pt}}

{extra_packages}

\newcommand{{\exo}}[1]{{\section*{{Exercise #1}}}}
\newcommand{{\prob}}[1]{{\section*{{Problem #1}}}}
\newcommand{{\quest}}[1]{{\section*{{Question #1}}}}
\newcommand{{\e}}{{&=&}}
\newcommand{{\p}}[1]{{\times 10^{{#1}}}}

\begin{{document}}
\maketitle
\thispagestyle{{empty}}



\end{{document}}"""

make = """SHELL := /bin/sh

SRC := $(wildcard *.tex)
PDF := $(SRC:.tex=.pdf)
FIGURES := $(filter-out $(wildcard figures/*-crop.pdf), $(wildcard figures/*.pdf))

all:
\t-mkdir .build
\t-rm $(PDF)
\tfor t in $(SRC) ; do \\
\t\tpdflatex -shell-escape -output-directory=.build $$t ; \\
\tdone
\tmake links

crop:
\tfor fig in $(FIGURES) ; do \\
\t\tpdfcrop $$fig ; \\
\tdone

clean:
\t-rm $(PDF)
\t-rm -rf .build/*

links:
\t-rm $(PDF)
\tln -s .build/*.pdf .



%s"""

def make_makefile_extras(c, n):
    return makefile_extras[c].format(c=c,n=n)

def main(name, hw, path):
    if os.path.isdir(path):
        print '"' + path + "\" already exists. Please choose another hw#."
        exit()
    else:
        maintex = "HW" + str(hw) + ".tex"
        mainpdf = "HW" + str(hw) + ".pdf"
        try:
            os.mkdir(path)
            f = open(os.path.join(path,maintex),'w')
            f.write(tex.format(
                extra_packages = extras[name[:1]],
                class_name = classes[name[:1]],
                hw = hw,
                author = authors[name[:1]],
                short_author = authors[name[:1]] if len(authors[name[:1]]) < 50 else ''
            ))
            f.close()
            os.system('ln Logo.png "' + path + '"')
            os.mkdir(os.path.join(path,'.build'))
            f = open(os.path.join(path,'Makefile'),"w")
            f.write(make%(make_makefile_extras(name[:1],hw)))
            f.close()
            f = open(os.path.join(path,'.gitignore'),"w")
            f.write(gitignore%("HW" + str(hw), maintex))
            f.close()
        except Exception as e:
            os.system("rm -Rf \"" + path + '"')
            raise e
        else:
            os.chdir(path)
            Popen(["make"], stdout=DEVNULL, stderr=DEVNULL)


def begins_with_number(s): return s[0].isdigit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create LaTeX template for class')
    parser.add_argument('name', metavar='class', type=str, help='Class name in current directory')
    parser.add_argument('hw', nargs='?', type=int, help='Port on which to listen for incoming guesses')
    args = parser.parse_args()

    directory = None

    host = os.popen('hostname').read().strip()
    if host == 'wondergirl':
        directory = '/cygdrive/c/Users/Paul/Dropbox/Cornell/Fall_2015'
    elif host == 'grapes':
        directory = '/home/papacharlie/Dropbox/Cornell/Fall_2015'

    os.chdir(directory)

    # ls = filter(lambda x: os.path.isdir(x), os.listdir('.'))

    for c in filter(lambda x: os.path.isdir(x), os.listdir('.')):
        if args.name[0] is c[0]:
            if args.hw is None:
                correct_dirs = list(filter(lambda x: begins_with_number(x) and os.path.isdir(os.path.join(c,x)), os.listdir(c))) + ['0hw']
                hw = int(max(correct_dirs, key=lambda x: 0 if not x[0].isdigit() else int(x[0]))[0]) + 1
            else:
                hw = args.hw
            path = os.path.join(c,str(hw)+"hw")
            main(c,hw,path)
            print os.path.join(directory,path)
            exit()
    print "Could not find the class you're looking for"