# Datetime Parser

### General Notes on the Program

- Written in Python 3.

### Implementation Notes

- Dictionary used to store timedate values. Easy way to achieve uniqueness with entries.
- Pattern matching with regular expressions to validate the format of each datetime value.
- Logging implemented to provide details on validity of each datetime value or whether the value is a repeat. 

### Assumptions Made

- The year `0000` is valid.
- `00:00` can be subbed in for `Z` as a valid timezone designator (TZD).
- In the case of the TZD having format `[+|-]hh:ss`:

    - `hh` can be a value ranging from `00` to `14`.
    - `ss` can be a value ranging from `00` to `59`.
- Input files are purely lists of valid and invalid datetime values (with comment support).
No other content is expected.
