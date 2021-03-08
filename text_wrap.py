"""
Write a generator that lazily rewraps text so that it fits an 80 column window 
without breaking words, and a consumer function that demonstrates same using the 
contents of the filename passed on the command line, as follows:

$ python3 text_wrap.py <filename>
"""

import sys

def get_data(infile):
    """Lazy function to get data from file in groups of 80 characters.
    It replaces any line breaks and tabs with spaces, to conform with 
    Sri Majunmdar's example in the discussion forum of her peer review 
    file as follows:

    "u4 Nice work! Only caveat: you could lower() or upper() to avoid
    case-sensitivity for words / lines. g9 Very nice work and use of map and lambda
    functions."

    It breaks when there are no more characters to read in."""

    while True:
        """Nested .replace() to replace line breaks and tabs with spaces. Either
        could be removed to customize."""
        data = infile.read(80).replace('\n', ' ').replace('\t', ' ')
        # data = infile.read(80).replace('\n', ' ')

        # The following code would be used if line breaks and tabs should be kept.
        # data = infile.read(80)
        
        # Ends the loop when there is no more data to read in.
        if not data:
            break

        yield data


def produce(gen):
    """Generates lines of text wrapped with words with maximum of 80 characters. 
    Additional characters for new word(s) and/or remaining words get split to next line."""

    item = next(gen)
    
    while item:
        """Finds the last space (i.e., deliminating character) in the line from 
        the generator object, denoting where to break the string to a new line. 
        Returns -1 if not found."""
        i = item.rfind(' ')

        """Customize depending on whether get_data(infile), included or excluded,
        page breaks and/or tabs. First version is if get_data(infile) replaced
        page breaks and second version is where .read(80) was used."""
        # i = max(item.rfind(i) for i in '\ \t')
        # i = max(item.rfind(i) for i in '\ \n\t')

        """Since the data is read in groups of 80 characters, the first line
        would not exceed 80; however, as the leftover characters/words
        are carried over into the next batch, this looks for the last space/
        deliminating character within the 80-characters limit and resets the 
        index to splice the string."""
        if (i > 80):
            i = item.rfind(' ', 0, 80)

            """Customize depending on whether get_data(infile), included or excluded,
            page breaks and/or tabs. First version is if get_data(infile) replaced
            page breaks and second version is where .read(80) was used."""
            # i = max(item.rfind(i, 0, 80) for i in '\ \t')
            # i = max(item.rfind(i, 0, 80) for i in '\ \n\t')  
        
        """If the deliminating character(s) is found (i.e., not -1) and string is 
        80 characters or more, it splices the string at the last space within the 
        band and yields the string and assigns the remaining characters/words to 
        leftover (deleting the space (e.g., i + 1) as it starts the 
        beginning of a new line)."""
        if (i > 0) and (len(item) >= 80):
            yield item[:i]
            leftover = item[i + 1:]
        else:
            yield item
            break
            """If the deliminating character(s) is not found or string is less than 
            80 characters, it yields the last string and ends the loop."""

        """Next line to evaluate is leftover plus the next batch of data read
        from the file (generator object). However, if there are no more lines to read in,
        but there is still leftover to text wrap into 80-character limits, StopIteration
        gets bypassed and process continues."""

        try:
            item = leftover + next(gen)
        except:
            item = leftover


def consume():
    """Opens the file designated by user and performs lazy read of file in
    batches of 80 characters. For each batch, it is passed onto the produce(gen)
    function to properly ensure that words are not cut off within the 
    80-character limit and prints out each modified line."""

    """Checks whether file name was provided. If not, SystemExit rather than
    IndexError is used to abort the program"""
    try:
        filename = sys.argv[1]
    except IndexError:
        raise(SystemExit)("Filename must be provided on the command line.")

    # Checks whether file exists. If not, porgram is aborted.
    try:
        with open(filename, 'r') as f:
            for line in produce(get_data(f)):
                print(line)
                
                """For visual purposes for reviewing assignment, divider separates the 
                lines printed."""
                print("-----")
    except FileNotFoundError:
        raise(SystemExit)(f"The {filename} file does not exist. Please try another file.")


if __name__ == '__main__':

    consume()
