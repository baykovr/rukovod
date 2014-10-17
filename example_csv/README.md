CSV 

    1. EMAIL	SECTION	ASSIGNMENT	SCORE	FEEDBACK / COMMENT
    2. john-doe@some.edu	999	MP-X	100/100	
    3. john-doe@some.edu	999	MP-X	100/100	
    4. john-doe@some.edu	999	MP-X	100/100	
    5. john-doe@some.edu	999	MP-X	100/100	
    6. john-doe@some.edu	999	MP-X	100/100	
    7. john-doe@some.edu	999	MP-X	100/100	
    
    # Run Result

    python rukovod.py -g example_csv/example_sheet.csv
    [...] FILE   : example_csv/example_sheet.csv
    [ ! ] WARNING: always double check email / roster records against this csv before mailing.
    [ ? ] continue (y/N):[...] total entries extracted: 6
    [...] estimated time to send : 6 (seconds)
    [ ? ] preview first message (y/N)
    
    DESTINATION: john-doe@some.edu
    BEGIN-MESSAGE****************************************
    EMAIL        john-doe@some.edu
    SECTION      999
    ASSIGNMENT   MP-X
    SORE        100/100
    FEEDBACK / COMMENT 
    END-MESSAGE******************************************
