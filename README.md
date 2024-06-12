# ig_complex
## Python functions for evaluating the complexity within policy statements.

This package uses the Institutional Grammar (IG) as a tool to measure policy complexity at the micro-level. While the practical use of the IG as a tool will be discussed here, a more in-depth discussion of its development, application, and use can be found here: [Crawford and Ostrom 1995](https://www.cambridge.org/core/journals/american-political-science-review/article/grammar-of-institutions/7D37CD3BC5ED2D9FD57D2EE292958F47); [Frantz and Siddiki 2021](https://onlinelibrary.wiley.com/doi/full/10.1111/padm.12719); [Siddiki et al 2022](https://onlinelibrary.wiley.com/doi/full/10.1111/psj.12361), [Siddiki and Frantz 2023](https://onlinelibrary.wiley.com/doi/full/10.1111/rego.12546). The IG offers a rigorous and generalizable methodology for examining the information conveyed by institutional statements, or the individual statements that make up policies.  
At the institutional statement level, the IG allows the identification of the statements’ institutional type as constitutive or regulative (Siddiki and Frantz 2023). *Constitutive statements* are statements parameterizing features of systems in which actors interact, whereas *regulative statements* are statements describing expected behavior(s) of actors in the presence or absence of constraints. While *ig_complex* is built to evaluate regulative statements, it can successfully examine constitutive statements.  
The syntactic components for regulative statements, include: (i) Attribute: an actor that carries out, or is expected to/to not carry out the action of the statement; (ii) Object: the inanimate or animate part of statement that is the receiver of the action of the statement; (iii) Deontic: a prescriptive or permissive operator that defines to what extent the action of a statement is compelled, restrained, or discretionary; (iv) Aim: the action of the statement that is assigned to the statement actor; (v) Context: condition(s) instantiating settings in which the statement applies, or constraint(s) qualifying action of the statement; (vi) Or else: an incentive linked to the statement action. Objects can be further delineated as direct and indirect following defining characteristics of such according with English grammar. The different types of Contexts (i.e., of instantiating or qualifying kind) are delineated as Activation Conditions (Cac) and Execution Constraints (Cex). Finally, the classification of Attributes and Objects can account for actors and objects and properties (i.e., descriptors) of those (Crawford and Ostrom 1995; Frantz and Siddiki 2022).  
The syntactic components bridge -- more or less -- directly with the complexity outputs produced by *ig_complex*. 
  -*Main Attribute* -- is a list of attribute(s) that are perscribed to carry out the task.
  -*Attributes Count* -- a count of *Main Attribute*
  -*Attributes Conjunction* -- the conjunction used for *Main Attribute* if count is greater than one. This identifies logical AND or OR.
  -*Coordinating Actor* -- is a list of all actors engaged in the statements. This includes the Attribute(s) as well as additional coordinating actors in other portions of the statements. (*this code is still being developed*)
  -*Coordinating Actor Count* -- a count of *Coordinating Actor*. (*this code is still being developed*)
  -*Deontic* -- i as identified above.
  -*Negative* -- is used to identify the negation of the deontic
  -*Task* -- is a list of task(s) that are to be carry out the attribute. This reports the aIms within the statement.
  -*Task Count* -- a count of *Task*
  -*Task Conjunction* -- the conjunction used for *Task* if count is greater than one. This identifies logical AND or OR.
  -*Condition* -- is a list of contexts caluse(s) that condition the perscription for the actors to carry out the task. Both Activation Conditions (Cac) and Execution Constraints (Cex) are identified.
  -*Condition Count* -- a count of *Condition*. This returns both a count of the context clauses, as well as the number of conditions within the clauses. For example, consider the following statement:  
  "When notice is given, the departments may modify the regulations, if the outcomes of such change are determined to be economically or socailly beneficial."  
  *When notice is given* and *if the outcomes of such change are determined to be economically or socailly beneficial.* are two context clauses, but the latter has two conditions -- (1) *economically* or (2) *socailly*. This results in a condition count of three.
  -*Condition Conjunction* -- the conjunction used for *Condition* if the condition count within a context cluase is greater than one. This identifies logical AND or OR.

## Getting Started

These instructions will outline installation, a description of the functions, as well as identify examples.

# Table of Contents
1. [Installing](#Installing)
2. [Functions](#Functions)
   - [Practical Complexity Functions](#Practical-Complexity-Functions)
   - [Data Construction](#Data-Construction)
   - [Additional Data Cleaning Functions](#Additional-Data-Cleaning-Functions)
3. [Examples](#Examples)
4. [Other Stuff](#Built-With)

### Installing

All of the functions that are identified below can be installed and imported given the code below:

    !pip install "git+https://github.com/ambro034/ig_complex.git"
    import ig_complex as igc

## Functions

### Practical Complexity Functions

#### extract_grammer_complexity
This is a function that bridges IG outputs and the complexity elements, with an input of a single statements. 

    extract_grammer_complexity(txt)

Where:
  - *txt* is the text passed to the function

Output structure:  
A dataframe with columns:  
['ID', 'Statement',  
"Main Attribute", "Attributes Count", "Attributes Conjunction",  
"Coord. Actor", "Coord. Actor Count",  
"Deontic", "Negative",  
"Task", "Task Count", "Task Conjunction",  
"Condition", "Condition Count", "Condition Conjunction"]


#### extract_grammer_complexity_dataset
This is a function that bridges IG outputs and the complexity elements, with an input of a dataframe where each row is a statements. 

    extract_grammer_complexity_dataset(dataset, id, s)

Where:
  - *dataset* is the dataframe passed to the function
  - *id* is the column position for the statement id to be passes to the function
  - *s* is the column position for the text to be passes to the function
    
Output structure:  
A dataframe with columns:  
['ID', 'Statement',  
"Main Attribute", "Attributes Count", "Attributes Conjunction",  
"Coord. Actor", "Coord. Actor Count",  
"Deontic", "Negative",  
"Task", "Task Count", "Task Conjunction",  
"Condition", "Condition Count", "Condition Conjunction"]


### Data Construction

A function to aid with dataframe construction.

#### construct_dataset
This is a function that takes a variably framed dataframe and conforms it to the structure useful in the above functions.

    construct_dataset(data,id,txt)

Where:
  - *data* is the name of the dataframe
  - *id* is the column position for Statement IDs in the dataframe
  - *txt* is the column position for the statment text in the dataframe
    

### Additional Data Cleaning Functions

These functions are nested into the 'practical functions above, but can be used indamendently if needed.

#### clean_format
This is a function that removes listed formatting (i.e., “(1)” or “[a]”)

    clean_format(dataset, s)

Where:
  - *dataset* is the dataset passed to the function
  - *s* is the column position of the text in the dataset
    
#### clean_split_period
This is a function that splits cells in the dataset by the period (i.e., “.”)

    clean_split_period(dataset)

Where:
  - *dataset* is the dataset passed to the function
    
#### clean_split_semicolon
This is a function that splits cells in the dataset by the semicolon (i.e., “;”)

    clean_split_semicolon(dataset)

Where:
  - *dataset* is the dataset passed to the function
    
#### clean_split_X
This is a flexible function that splits cells in the dataset by the *split_term*

    clean_split_X(dataset, split_term)

Where:
  - *data* is the dataset passed to the function
  - *split_term* can be any character – but regular expression is recommended (see: [re — Regular expression operations](https://docs.python.org/3/library/re.html))
    
#### merge_statements
This is a function that merges all of the cells within a column into one allowing for more regular splitting rather than the splitting offered by the original text.

    merge_statements(dataset)

Where:
  - *data* is the dataset passed to the function

#### reset_index
After merging and splitting, it is recommended to reindex the rows of your dataframe allowing for cleaner recalls in future steps.

    reset_index(dataset)

Where:
  - *data* is the dataset passed to the function
    
#### Examples

    # Set up
    !pip install "git+https://github.com/ambro034/ig_complex.git"
    import ig_complex as igc
    import pandas as pd
    
    # Load Data
    data = pd.read_csv(Arkansas_2001_1.csv, encoding="utf8")
    data.info()

    # Converst the data into the standard structure for the package
    y = igc.construct_dataset(data,0,1)
    y

#### Remove formating related to policy structure

    igc.clean_format(y, 1)
    y

#### Options for splitting and merging text

While the dataframe *y* is preprocessed to represent policy text that does not need to be further split or merged, the following examples are offered.
First, *merge_statements* merges all of the text into one row of data. As such, the first 'Statement ID' will be maintained.
Second and third, the single statement in *df* is split on each period and semicolon observed in the text. It is important to note that the same 'Statement ID' is now split over all rows.
Fourth, a flexible split is executed when 'means' is obseved in the text -- while this is rather pointless, it is done to show the functionality of the function.
Fifth, when merging or splitting, the dataframe must be reindexed before being passed to additional functions. If it is not reindexed, multiple statements could be passed to the function where the function is expecting one statement. 

    df = igc.merge_statements(y)
    
    ysplit1 = igc.clean_split_period(df)
    ysplit2 = igc.clean_split_semicolon(df)
    ysplit3 = igc.clean_split_X(df, 'means')

    ysplit3=igc.reset_index(ysplit3)

#### Extract from single statement  

    # Extract from a dataset
    igc.extract_grammer_complexity(y['Statements'][11])

    # Extract from a string
    igc.extract_grammer_complexity('I and Juan must play and watch lacrosse, if it is nice and sunny.')

#### Extract from a dataset 

    # Extract from a dataset
    igc.extract_grammer_complexity_dataset(y,0,1)  

## Built With

  - [Contributor Covenant](https://www.contributor-covenant.org/) - Used
    for the Code of Conduct
  - [Creative Commons](https://creativecommons.org/) - Used to choose
    the license

## Authors

  - **Graham Ambrose** - 
    [ambro034](https://github.com/ambro034/)


## License

This project is licensed under the [CC0 1.0 Universal](LICENSE.md)
Creative Commons License - see the [LICENSE.md](LICENSE.md) file for
details

## Acknowledgments

  - People
  
