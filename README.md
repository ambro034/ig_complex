# ig_complex
## Python functions for evaluating the complexity within policy statements.

One Paragraph of the project description

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
  
