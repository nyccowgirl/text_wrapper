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
        # Nested .replace() to replace line breaks and tabs with spaces. Either
        # could be removed to customize.
        data = infile.read(80).replace('\n', ' ').replace('\t', ' ')

        # The following code would be used if line breaks and tabs should be kept.
        # data = infile.read(80)
        
        # Ends the loop when there is no more data to read in.
        if not data:
            break

        yield data


def produce(gen):
    """Generates lines of words with maximum of 80 characters. Additional
    characters for new word(s) and/or remaining words get split to next line."""

    item = next(gen)
    
    while True:
        # Finds the last space in the line from the generator object,
        # denoting where to break the string to a new line. Returns -1
        # if not found.
        i = item.rfind(' ')

        # Since the data is read in groups of 80 characters, the first line
        # would not exceed 80; however, as the leftover characters/words
        # are carried over into the next batch, this looks for the last space
        # within the 80-characters limit and resets the index to splice the
        # string.
        if (i > 80):
            i = item.rfind(' ', 0, 80)        
        
        # If space is found (i.e., not -1) and string is 80 characters or
        # more, it splices the string at the last space within the band and 
        # yields the string and assigns the remaining characters/words to 
        # leftover (deleting the space (e.g., i + 1) as it starts the 
        # beginning of a new line).
        if (i > 0) and (len(item) >= 80):
            yield item[:i]
            leftover = item[i + 1:]
        # If space is not found or string is less than 80 characters, it
        # yields the string and ends the loop.
        else:
            yield item
            break

        # Next line to evaluate is leftover plus the next batch of data read
        # from the file (generator object).
        item = leftover + next(gen)


def consume():
    """Opens the file designated by user and performs lazy read of file in
    batches of 80 characters. For each batch, it is passed onto the produce(gen)
    function to properly ensure that words are not cut off within the 
    80-character limit and prints out each modified line."""

    with open(sys.argv[1]) as f:
        for line in produce(get_data(f)):
            print(line)


if __name__ == '__main__':

    consume()
