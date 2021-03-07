import sys
import textwrap

def get_data(infile):
    """Lazy function to get data from file in groups of 80 characters.
    It breaks when there are no more characters to read in."""

    while True:
        data = infile.read(80)
        # data = infile.readline()
        # data = infile.readline().replace('\n', '')
        
        if not data:
            break
        yield data

def produce(gen):
    """Generates lines of words with maximum of 80 characters. Additional
    characters from new word gets split to next line."""
    # s = item
    # w = ""
    # print("item: " + item)
    
    # while s:
    #     print("s: " + s)

    #     if (len(s) > 80):
    #         w = textwrap.wrap(s, 80, break_long_words=False)
    #     #         print(w)
    #         s = ""
    #     else:
    #         s += item

    #     if not s:
    #         break
    #     yield w

    # yield textwrap.TextWrapper(width=80, subsequent_indent=indent, fix_sentence_endings=True).wrap(text=item)
    # w = textwrap.wrap(item, 40, break_long_words=False)
    # print(w)
    # yield item

    item = next(gen)
    
    while item:
        # item = yield + item
        # print("new: " + item)
        i = item.rfind(' ')
        print("index: " + str(i))
        # print("--")

        if (i > 80):
            i = item.rfind(' ', 0, 80)
            # item = item[:i]
            # leftover = item[i + 1:]
        
        if (i > 0) and (len(item) >= 80):
            yield item[:i]
            leftover = item[i + 1:]
        #     # yield leftover
        else:
            yield item

        print("--")
        item = leftover + next(gen)
        print("string: " + item)
        print("leftover: " + leftover)



def consume():
    """Not sure if this is needed if consuming in main?"""

    print(produce())


if __name__ == '__main__':

    # filegen = open(sys.argv[1]).read(20)
    # print(filegen)

    with open(sys.argv[1]) as f:
        # for line in get_data(f):
        #     # print(line)
        for item in produce(get_data(f)):
            print(item)

    # for line in open(sys.argv[1]):
    #     for item in produce(get_data(line)):
    #         print(item)


    # for item in consume():
    #     print(item)
