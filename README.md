# spacedrepetition

# Development
1. Download the start-dev.sh script. [This start-dev.sh script](https://drive.google.com/file/d/1ZS_aoSbCOC0ppD8TOhLTlf0JfNdeZXc5/view?usp=sharing) will only be downloadable for people with Google Drive access. 
2. Create a Python 3.8 virtual environment called **venv**
`python3.8 -m venv venv`
3. Run the start-dev.sh script to activate your development environment. 
`./start-dev.sh`


# 3/14/2021 Meeting
1. How do we let students practice as soon as possible? 
2. MIPS -> Machine Code 
3. Numbering Systems 
4. "Practice NUMBER tab" - indicating how many questions they are to be asked on a given day 
5. Ask questions about second exam material
   1. MIPS -> Binary
   2. MIPS functions - can we do templating with this? 
6. Create new templating system - use PolyPy but maybe enhance
   1. Template that creates random C code that contains different kinds of loops, if statements, other constructs 
7. Create function that will create a loop (type=while, iterations=N, controlVariable=0, increment=M, body=(return value for another function))
8. create_body(num_variables=N, are_they_all_changing=Boolean, )
9. C -> MIPS function (input = C string, output = MIPS string)
10. C string metadata -> MIPS string 
11. In the management of a C code segment, don't just store the C code string 
    1.  {
        1.  code_string: , 
        2.  metadata: {
                1.  construct_type, 
                2.  iterations, 
                3.  increment=M,
                4.  body : {
                    1.  body_string: 
                    2.  body_metadata: {
                    3.  
                    4.  }
                5.  }
            1.  }
    2.  }

# 3/15
What do we want the process to be for creating questions? 
Who creates them? How do they get mapped to users? Is there a form for creating question templates? 


Telehealth - Mamoun Mardini
