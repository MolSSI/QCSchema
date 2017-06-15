## Roles and epics

#### QM software developer
Role: I write code that performs QM calculations and produces output for its end users
 - I want users to be able to visualize orbitals using only basis set info and MO coefficients, so that I don't have to build the infrastructure to dump gaussian cube files
 - I want to compare my package's results to other programs' without having to write complicated parsers

#### Visualization / data analysis software developer
Role: I release software that can visualize or analyze 3rd party QM data
 - I want my application to consume data in a standardized, easy-to-parse form, so that I don't have to write separate parsers for every QM package

#### End user
Role: I perform QM calculations and examine their outputs
 - I want independent output files that can be consumed by any visualization package, so that I don't have to go through an arduous process to generate Gaussian cube files
 - I want output files that allow me to understand exactly what I ran, so that I don't have to guess which input file generated which output file
 - I want output files that can be easily converted into new input files, so that I can easily iterate and refine my calculations
 - I want my QM output files that are small and efficient, so that I don't get yelled at for filling up our filesystem

#### Analyzer
Role: I consume and rationalize outputs over many different calculations
 - I need to be able to access large amounts of data across many files using automated scripts, so that I don't have to do it by hand

#### Scripter
Role: I run workflows that require passing information back and forth between several programs
 - I want standardized output from the programs, so that I don't have to write separate parsers for each one


## Personas
### The Method Developer: Renata Peña
Renata is a Phd Chemistry student entering her third year working in a QM method-development-focused lab at a midwestern state university. She's focused on producing first-author papers, raising her impact, and generally preparing for an academic career track at an R1. She's interested in explicitly correlated _ab initio_ methods that can be generally applied to bond-breaking in enzyme catalysis.

How she spends her time:
- 33% coding new methods
- 33% writing papers
- 33% running and analyzing calculations

Technical knowledge: learned Python as an undergrad and uses it for analysis and scripting. Does her low-level programming in fortran. Enthusiastic about things like GitHub and testing frameworks, but the rest of the lab doesn't get the point.

### The Software Developer: Ki-tae Lee, PhD
Ki-tae is a research scientist who works with a research group but is supported by sales of their quantum chemsitry package. He's responsible for releasing software, maintaining the code, supporting users, and generally dealing with the overhead around software sales. He's often a co-author on methods papers, and occasionally on a pure "software release" paper. Ki-tae would likely go into the software industry if he wasn't in his present job.

How he spends his time:
 - 50% dealing with users (sales, licensing, and support)
 - 40% coordinating development, fixing bugs, code maintenance
 - 10% running and analyzing calculations
 
Technical knowledge:: he's great at fortran and C++, comfortable with Python. Has a Linux / X-windows-based development and analysis stack. Self-taught enough javascript to animate the logo on their software's sales page. Understands the point of GitHub and continuous integration, but doesn't really feel it's applicable to his work.

### The Modeler: Mensah Adesida, MS
Mensah works in a small, multi-disciplinary government laboratory that focuses on atmospheric research. Mensah's background includes a masters in Chemical Engineering and some hands-on experience with Gaussian as part of an independent research project. They're often responsible for running calculations relevant to small molecule chemistry in various environments.

How they spend their time:
 - 75% running calculations and analyzing results
 - 25% writing reports and contributing to multi-author papers
 
Technical knowledge: Can do whatever's necessary to run a calculation at the command line. A lot of cutting/pasting data from output files into spreadsheets.
