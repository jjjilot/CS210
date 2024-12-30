"""
Enrollment analysis:  Summary report of majors enrolled in a class.
CS 210 project, Fall 2022.
Author:  Josh Jilot
Credits: Michaela Cheechov :)
"""
import doctest
import csv

def read_csv_column(path: str, field: str) -> list[str]:
    """
    Read one column from a CSV file with headers into a list of strings.

    >>> read_csv_column("data/test_roster.csv", "Major")
    ['DSCI', 'CIS', 'BADM', 'BIC', 'CIS', 'GSS']
    """
    maj_list = []

    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            maj_list.append(row[field])

    return maj_list

def counts(column: list[str]) -> dict[str, int]:
    """
    Returns a dict with counts of elements in column.

    >>> counts(["dog", "cat", "cat", "rabbit", "dog"])
    {'dog': 2, 'cat': 2, 'rabbit': 1}
    """
    maj_dict = {}
    
    for entry in column:
        if entry in maj_dict:
            maj_dict[entry] += 1
        else:
            maj_dict[entry] = 1

    return maj_dict

def read_csv_dict(path: str, key_field: str, value_field: str) -> dict[str, dict]:
    """
    Read a CSV with column headers into a dict with selected
    key and value fields.

    >>> read_csv_dict("data/test_programs.csv", key_field="Code", value_field="Program Name")
    {'ABAO': 'Applied Behavior Analysis', 'ACTG': 'Accounting', 'ADBR': 'Advertising and Brand Responsibility'}
    """
    program_dict = {}

    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row[key_field]
            val = row[value_field]
            program_dict[key] = val

    return program_dict

def items_v_k(dictionary: dict) -> list[str]:
    '''
    Returns a list of (value, key) pairs from a dictionary.

    >>> items_v_k({'cats' : 2 , 'dogs' : 4 , 'rabbits' : 3}, )
    [(2, 'cats'), (4, 'dogs'), (3, 'rabbits')]
    '''
    dict_organized = []
    for key, value in dictionary.items():
        pair = (value, key)
        dict_organized.append(pair)

    return dict_organized

def main():
    doctest.testmod()
    majors = read_csv_column("data/roster_selected.csv", "Major")
    counts_by_major = counts(majors)
    program_names = read_csv_dict("data/programs.csv", "Code", "Program Name")
    # --- Next line replaces several statements
    by_count = items_v_k(counts_by_major)
    # ---  
    by_count.sort(reverse=True)  # From largest to smallest
    for count, code in by_count:
        program = program_names[code]
        print(count, program)

if __name__ == "__main__":
    main()
