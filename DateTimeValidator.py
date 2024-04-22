import datetime
import sys
import re
import logging

# Usage:
#  python3 DateTimeValidator.py <input_filename> <output_filename>

datetime_set = {}
INPUT_DIR = "input/"
OUTPUT_DIR = "output/"
LOG_FILENAME = "log/default"

# pieces of regex for matching
YEAR = "[0-9]{4}$"  # Four-digit year with a valid range from 0000 to 9999
MONTH = "([0][1-9]|[1][0-2])$"  # Two-digit month with valid range 01-12
DAY = "([0][1-9]|[1-2][0-9]|[3][0-1])$"  # Two-digit day with valid range 01-31
DELIMITER = "T"
HOURS = "([0-1][0-9]|[2][0-3])$"  # Two-digit hour with valid range 00-23
MINUTES = "[0-5][0-9]$"  # Two-digit minute with valid range 00-59
SECONDS = "[0-5][0-9]$"  # Two-digit second with valid range 00-59
TZD = r"((\+|-)([0][0-9]|[1][0-4]):[0-5][0-9])$"  # Timezone designator that's not 'Z', must be at end of string

# initialize logger
logger = logging.getLogger(__name__)
timeStamp = datetime.datetime.now().strftime("%Y-%b-%d_%H-%M-%S")
logging.basicConfig(filename=LOG_FILENAME+"_%s.log" % timeStamp, level=logging.INFO)
logger.addHandler(logging.StreamHandler())


def validate_datetime(line):
    invalid_values = []
    time = ""
    date = ""
    time_no_tzd = ""

    # split value into two parts: date and time
    if DELIMITER in line:
        split = line.split(DELIMITER)
        date = split[0]
        time = split[1]
    else:
        return False

    # validate the date component
    date_values = date.split("-")
    if len(date_values) < 3 or len(date_values) > 3:
        return False
    else:
        # validate year
        if not re.fullmatch(YEAR, date_values[0]):
            return False
        # validate month
        if not re.fullmatch(MONTH, date_values[1]):
            return False
        # validate day
        if not re.fullmatch(DAY, date_values[2]):
            return False

    # validate TZD next and remove it from the 'time' string if valid
    if 'Z' in time:
        time_split = time.split('Z')
        if len(time_split) > 2:
            return False
        else:
            if time_split[1]:
                return False
            time_no_tzd = time_split[0]
    else:
        tzd_match = re.search(TZD, time)
        if not tzd_match:
            return False
        else:
            timezone = tzd_match.group(1)
            time_no_tzd = time.replace(timezone, "")

    time_values = time_no_tzd.split(":")
    if len(time_values) < 3 or len(time_values) > 3:
        return False
    else:
        # validate hour
        if not re.fullmatch(HOURS, time_values[0]):
            return False
        # validate minute
        if not re.fullmatch(MINUTES, time_values[1]):
            return False
        # validate second
        if not re.fullmatch(SECONDS, time_values[2]):
            return False

    return True


def load_values():
    # read in file
    filename = sys.argv[1]
    input_file = None
    try:
        input_file = open(INPUT_DIR + filename, "r")
        logger.info("File successfully loaded.")
    except Exception as err:
        logger.error("Error reading in file: ", err)

    while True:
        line = input_file.readline().replace("\n", "")

        # break out of loop at EOF
        if not line:
            break

        # ignore line if it's a comment
        if line[0] == "#":
            continue
        else:
            if line not in datetime_set:
                if validate_datetime(line):
                    # store datetime as a key in the dictionary, no value needed
                    datetime_set[line] = None
                    logger.info(" %s: Datetime value is VALID." % line)
                else:
                    logger.error(" %s: Datetime value is INVALID." % line)
            else:
                logger.info(" %s: Datetime value is a REPEAT." % line)

    input_file.close()


def write_output():
    filename = sys.argv[2]
    output_file = open(OUTPUT_DIR + filename + "_" + timeStamp, "w+")

    for key in datetime_set.keys():
        output_file.write("%s\n" % key)

    output_file.close()


if __name__ == "__main__":
    # Check arguments are present
    if len(sys.argv) < 3:
        print("Missing arguments.\nUsage:\n"
              "\tpython DateTimeValidator.py <input_filename> <output_filename>")
        exit(1)

    load_values()
    write_output()
