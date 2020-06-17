# GradCafe Analyzer

A small foray into analyzing the user-submitted admissions data over at https://www.thegradcafe.com/survey/index.php.


## Setup

 1. Install [Python 3.2+](https://www.python.org/downloads/).
 2. Clone or download the repository.
 3. Open up a command line interface.
 4. Type `python3 gradcafe-analyzer.py` followed by one or more options (see below).

##  Usage

The script takes four arguments:

 - `-h` or `--help` prints these bullet points
 - `--school SCHOOL`  where `SCHOOL` is a school name, in quotation marks
 - `--subject SUBJECT` where `SUBJECT` is a subject name, in quotation marks
 - `--year [YEAR]` where `[YEAR]` is an integer year to search for

You must enter either a school and/or a subject in order for the script to return results. If no year is provided, the current year is used.

## Roadmap

Features I'd like to incorporate at some point include:

 - [ ] Calculate median and average GPAs and GRE scores
 - [ ] Incorporate the excellent scraping work done over at [deedy/gradcafe_data](https://github.com/deedy/gradcafe_data)
