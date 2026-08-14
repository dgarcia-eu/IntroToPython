# Introduction to Programming with Python
[David Garcia](http://dgarcia.eu)

Welcome to the online materials for the Python Crash Course at SEDS.

This introductory course is exclusively designed for first-semester MA SEDS students, aiming to provide a solid foundation in Python programming. 
It consists of hands-on sessions that cover theoretical and technical aspects of programming with Python and practical sessions where participants directly apply their acquired knowledge.
Students will learn fundamental programming concepts such as variables, control flow, basic data structures, and functions, and will also learn how to use Python to load, manipulate, and visualize data. 
Successfully completing this course will enable students to apply these skills to basic data analysis and programming in other courses and will help them develop more advanced, domain-specific Python skills.
The course does not follow a specific textbook but useful references are "Learn Python the Hard Way" by Zed Shaw and "Introduction to Python" by Eric Matthes.

**Time and place in WS 2025/26: K503, October 13-17, 2025, 9:00 - 17:00**

## Course contents

### Day 0

Before starting the block course:

1. Install the Jupyter environment or another IDE that allows you to follow the course.  
[Instructions how to install Jupyter can be found here.](https://dgarcia-eu.github.io/IntroToPython/setup/Anaconda.html)  
If your installation is not working on the first morning, don't lose the session to it:
open the course in your browser instead and sort the installation out in the afternoon.  
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/dgarcia-eu/IntroToPython/refresh-2026)  
⚠️ **Binder is a fallback for following the lecture, not a place to work.** It can take a
few minutes to start, and **anything you write there is lost when the tab closes** — it
saves nothing. If you do use it, download your notebook before you leave (*File → Download*).
Write your assignments locally.
2. Familiarize yourself with the Jupyter environment.  
You can start trying to do the steps in the [Jupyter walkthrough.](Day1/10_jupyter_walkthrough.txt)
3. **Run the [Day 0 self-check notebook](Day1/00_day0_selfcheck.ipynb).** Ten minutes, not graded.
It confirms your installation works and shows you where you are starting from, so nobody loses
Monday morning to a broken setup.
4. Make sure that you have a university account and can access course Ilias. If you have problems with this, talk to support at the university.
5. Check out Ilias to get the link to our private DataCamp Classroom. DataCamp is for you to do extra exercises besides the course. 
6. Take a look at the [Github forum to ask questions](https://github.com/dgarcia-eu/IntroToPython/discussions/)

### Day 1

- Welcome and course logistics: [Slides](https://dgarcia-eu.github.io/IntroToPython/Day1/Slides/Day1.html)
- Interactive lecture: Jupyter Notebook walkthrough
    - [10_jupyter_walkthrough.txt](Day1/10_jupyter_walkthrough.txt)
- Interactive lecture: Variables, strings, and numbers
    - [11_var_string_num.ipynb](Day1/11_var_string_num.ipynb)
- Interactive lecture: Introduction to lists and basic loops
    - [12_lists_tuples-1.ipynb](Day1/12_lists_tuples-1.ipynb)
- Assignment 1: Variables, Strings, Numbers, Lists, and Loops
  - [assignment_1.ipynb](Day1/assignment_1/assignment_1.ipynb) -- **Deadline: October 13th, 23:59**
  - [Extra exercises 1 (ungraded)](Day1/assignment_1/assignment_1-extra.ipynb)

### Day 2

- Quiz about Day 1: [Slides](https://dgarcia-eu.github.io/IntroToPython/Day2/Slides/Day2.html)
- Interactive lecture: Advanced lists, slicing, mutability, and nesting
    - [21_lists_advanced.ipynb](Day2/21_lists_advanced.ipynb)
- Interactive lecture: Conditional statements
    - [22_if_statements.ipynb](Day2/22_if_statements.ipynb)
- Interactive lecture: List comprehensions
    - [23_comprehensions.ipynb](Day2/23_comprehensions.ipynb)
- Assignment 2: Lists, Tuples, Sets, Comprehensions, and if-statements
  - [assignment_2.ipynb](Day2/assignment_2/assignment_2.ipynb) -- **Deadline: October 14th, 23:59**
  - [Extra exercises 2 (ungraded)](Day2/assignment_2/assignment_2-extra.ipynb)

### Day 3

- Quiz about Day 2: [Slides](https://dgarcia-eu.github.io/IntroToPython/Day3/Slides/Day3.html)
- Interactive lecture: Dictionaries
  - [31_dictionaries.ipynb](Day3/31_dictionaries.ipynb)
- Interactive lecture: Functions, lambda, and scope
  - [32_functions.ipynb](Day3/32_functions.ipynb)
- Assignment 3: Dictionaries and Functions
  - [assignment_3.ipynb](Day3/assignment_3/assignment_3.ipynb) -- **Deadline: October 15th, 23:59**
  - [Extra exercises 3 (ungraded)](Day3/assignment_3/assignment_3-extra.ipynb)

### Day 4

- Quiz about Day 3: [Slides](https://dgarcia-eu.github.io/IntroToPython/Day4/Slides/Day4.html)
- Interactive lecture: Flexible function arguments (*args and **kwargs)
  - [40_arguments.ipynb](Day4/40_arguments.ipynb)
- Interactive lecture: Python modules and exceptions
  - [41_modules_exceptions.ipynb](Day4/41_modules_exceptions.ipynb)
- Interactive lecture: Write and read files
  - [42_files.ipynb](Day4/42_files.ipynb)
- Interactive lecture: Data Exploration with Pandas
  - [43_data_exploration_Pandas.ipynb](Day4/43_data_exploration_Pandas.ipynb)
- Assignment 4: Data exploration
  - [assignment_4.ipynb](Day4/assignment_4/assignment_4.ipynb) - **Deadline: October 16th, 23:59**
  - [Extra exercises 4 (ungraded)](Day4/assignment_4/assignment_4-extra.ipynb)

### Day 5

- Quiz about Day 4: [Slides](https://dgarcia-eu.github.io/IntroToPython/Day5/Slides/Day5.html)
- **Written exam (90 min)** -- first thing, so you are not sitting through a lecture worrying about it
- Interactive lecture: Data visualisation in Python
  - [51_visualization.ipynb](Day5/51_visualization.ipynb)
- Interactive lecture: Beyond the notebook -- scripts, packages, and environments
  - [52_beyond_the_notebook.ipynb](Day5/52_beyond_the_notebook.ipynb)
- Assignment 5: Data visualization
  - [assignment_5.ipynb](Day5/assignment_5/assignment_5.ipynb) -- **Deadline: October 17th, 23:59**

--------------------------------------------------


## Course grading

- The course is graded as pass/fail. To pass the course, you need the following:
  - **Pass each of the five daily assignments (at least 50% points in each)**
  - **Pass the final written exam (at least 50% points)**

- **[Read the exam blueprint](EXAM_BLUEPRINT.md)** on Day 1: what the exam covers, the three kinds of question, and five worked examples.
- **[Two-page Python reference](python_reference.md)**: everything the course uses, on one page, for revision. Not permitted in the exam.
- During the daily sessions, we will do small ungraded quizzes as practice for the final written exam.
- Attendance is not mandatory but highly recommended to pass the assignments and to practice for the final exam.
- **From Monday to Friday, there is an assignment due each day by 23:59.**
- Assignment submissions are done through ILIAS

## Who am I?

I am the Professor for Social and Behavioral Data Science at the University of Konstanz. My background is Computer Science but I worked my whole career with psychologists, sociologists and physicists 
to learn new ways to understand human behavior. I got my PhD from ETH Zurich in 2012 and a habilitation in 2018, starting to work as 
full professor TU Graz in 2020 and then at the University of Konstanz in 2022. To learn more about my work, check my 
[website](https://dgarcia.eu).
