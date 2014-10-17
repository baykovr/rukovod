rukovod
=======

Mass email from CSV files.


Basic usage:

    python rukovod.py -g some_file.csv

CSV file structure:

    The csv file must contain at least one column (and header) titled 'email'
    this field dicates the destination address, 
    the other columns will be placed in the email body.
    
    Example (test.csv)
    
    NAME | EMAIL   | COMMENT
    ________________________
    john | j@j.net | hello!
    
    
    resulting email:
    
    NAME   : john
    EMAIL  : j@j.net
    COMMENT: hello!
    
    and so forth row by row.
