rukovod
=======

Mass email from CSV files.

Setup:
    
    # In rukovod.py modify the following starting @15
    
    # number of seconds to wait in between sending emails
    TIME_DELAY = 1 

    # email from field, ie something@something.edu
    EMAIL_FROM = 'REDACTED'

    # email authentications, ie password for something@something.edu
    EMAIL_AUTH = 'REDACTED'

    # email subject
    EMAIL_SUBJ = 'REDACTED'

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
