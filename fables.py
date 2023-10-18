"""This script parses a web file and presents the data to the user

This script separates each line of the file into a list item using comprehension, using the
index method, gets the start of the contents section, the start of the fables and the end of the fables.
Then it stores all the fable titles. It gets the start index of each fable by checking for the location
of the name within the fables. Then it sorts all the fable titles in the correct order then gets the
last index of each fable, which is the start index of the next fable. Then it displays the fable titles,
asks the user which number fable to present and prints out the desired selection.
"""
import urllib.request
import ssl  # library to handle security in IP


def rearrange_titles(unordered_start_index, unordered_titles):
    """Original order of titles in contents does not match order of
    fables in file. This function reorders the titles to match the order
    of the fables
    :param unordered_start_index: unordered list of start index of each fable
    :param unordered_titles: titles in original, unordered list
    :return: titles in correct order as fables are in file
    """
    ordered_tuples = sorted(zip(unordered_start_index, unordered_titles), key=lambda x: x[0])
    return [title for start_index, title in ordered_tuples]


def show_contents(titles):
    """displays contents list
    :param titles: list of titles of fables
    :return: numbered list of titles
    """
    print('Choose among the following fables: ')
    for i, title in enumerate(titles, start=1):
        print(f'{i}) {title}')


def show_fable(indexes_tuples, fable_index):
    """stores start and end of fable by getting index of fable
    from user input, then prints each line in the slice from start to end
    :param indexes_tuples: list of tuples of start and end index of each fable
    :param fable_index: index of fable to returned
    :return: fable
    """
    start, end = indexes_tuples[fable_index - 1]
    print()
    for line in lines_in_file[start:end]:
        print(line)
    print('=' * 20 + ' + ' + '=' * 20 + '\n' * 2)


url = "http://www.gutenberg.org/cache/epub/28/pg28.txt"
print("Connecting...\r", end="")
# Modifying some settings urllib.request will use.
ctx = ssl.create_default_context()
ctx.check_hostname = False  # Disables hostname checks.
ctx.verify_mode = ssl.CERT_NONE  # Disables certificate checks.
file = urllib.request.urlopen(url, context=ctx)
input_file = file.read().decode('utf-8-sig')

# stripping twice to get rid of invisible characters
lines_in_file = [line.strip() for line in input_file.strip().split('\n')]


# stores beginning of contents, start of fables, end of fables
contents_index = lines_in_file.index('Contents')
fables_start = lines_in_file.index('Aesop’s Fables')
fables_end = lines_in_file.index('And this is the end of Æsop’s Fables. HURRAH!')

titles = []
current_index = contents_index
preface_count = 0
while True:
    if lines_in_file[current_index]:  # check if line is empty
        if lines_in_file[current_index] == 'PREFACE':
            preface_count += 1
            if preface_count > 1:  # stops at second instance of preface, full contents read at that point
                break
            current_index += 1
            continue
        else:
            try:
                # checks if index of line exists within fable start and end, if not, moves on
                # otherwise, adds line to list of contents
                lines_in_file.index(lines_in_file[current_index], fables_start, fables_end)
            except ValueError:
                pass
            else:
                titles.append(lines_in_file[current_index])
    current_index += 1

# list of all start indexes of fables
unordered_start_index = [lines_in_file.index(title, fables_start, fables_end) for title in titles]
titles = rearrange_titles(unordered_start_index, titles)  # titles rearranged in correct order

# sorted list of start indexes of all fables
ordered_start_index = sorted(unordered_start_index)

# list of all end indexes of fables (start index of next fable), last end index is end of all fables
titles_end_index = ordered_start_index[1:] + [fables_end]
fable_indexes = list(zip(ordered_start_index, titles_end_index))

show_contents(titles)  # called outside while loop to avoid reprinting contents if there is index input error
firstIteration = True

while True:
    if firstIteration:
        choice = input('Which fable would you like to read? (1 - 82) ')
        firstIteration = False
    else:
        choice = input('Which fable would you like to read next? (1 - 82) ')
    if not choice:
        break
    try:  # checks for any error in user input, whether not an int or out of range of indexes
        show_fable(fable_indexes, int(choice))
    except ValueError:
        print('Invalid index, try again. ')
        continue
    except IndexError:
        print('Invalid index, try again. ')
        continue
    move_on = input('Press enter when done. ')
    print()
    show_contents(titles)
