# text
# ASC function
def ASC(text):
    '''
    Changes full-width (double-byte) English letters or katakana within a character string to half-width (single-byte) characters

    This Python code defines a function called asc that takes a single character as input and returns its ASCII value using the ord() function
    '''
    return ord(text)


# ARRAYTOTEXT function
def ARRAYTOTEXT(array):
    '''
    Returns an array of text values from any specified range
    
    It takes an array as input and returns a string where the elements of the array are concatenated with a space in between
    '''
    return ' '.join(map(str, array))


# BAHTTEXT function
def BAHTTEXT(number):
    '''
    Converts a number to text, using the ß (baht) currency format
    
    It takes a number as input and returns the Thai Baht equivalent in words
    '''
    units = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    tens = ['', 'Ten', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    teens = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    scales = ['', 'Thousand', 'Million', 'Billion', 'Trillion']

    if number == 0:
        return 'Zero'

    def convert_chunk(chunk):
        words = []
        hundreds = chunk // 100
        if hundreds > 0:
            words.append(units[hundreds] + ' Hundred')
        remainder = chunk % 100
        if remainder >= 20:
            tens_digit = remainder // 10
            words.append(tens[tens_digit])
            ones_digit = remainder % 10
            if ones_digit > 0:
                words.append(units[ones_digit])
        elif remainder >= 10:
            words.append(teens[remainder - 10])
        elif remainder > 0:
            words.append(units[remainder])
        return ' '.join(words)

    chunks = []
    while number > 0:
        chunks.append(number % 1000)
        number //= 1000

    words = []
    for i, chunk in enumerate(chunks):
        if chunk != 0:
            words.append(convert_chunk(chunk) + ' ' + scales[i])

    return ' '.join(reversed(words))


# CHAR function
def CHAR(num):
    '''
    Returns the character specified by the code number
    
    This function takes an integer as input and returns the corresponding character based on the ASCII value.
    '''
    return chr(num)


# CLEAN function
def CLEAN(text):
    '''
    Removes all nonprintable characters from text
    
    This function takes a string as input and removes any non-printable ASCII characters from the text using regular expressions.
    The function then returns the cleaned text.
    '''
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
    return cleaned_text


# CODE function
def CODE(text):
    '''
    Returns a numeric code for the first character in a text string
    
    This function takes a single argument text, which represents the character for which we want to find the Unicode value.
    The function uses the ord() built-in Python function to return the Unicode value of the given character.
    '''
    return ord(text[0])


# CONCAT function
def CONCAT(*args):
    '''
    Combines the text from multiple ranges and/or strings, but it doesn't provide the delimiter or IgnoreEmpty arguments.
    
    This function takes any number of arguments and concatenates them into a single string.
    The arguments can be of any data type, and the function converts them to strings before concatenating them.
    '''
    return ''.join(str(arg) for arg in args)


# CONCATENATE function
def CONCATENATE(*args):
    '''
    Joins several text items into one text item
    '''
    return ''.join(args)


# DBCS function
def DBCS(string):
    '''
    Changes half-width (single-byte) English letters or katakana within a character string to full-width (double-byte) characters

    The code provided above is an analog of the DBCS() function in Microsoft Excel, implemented in Python.
    The DBCS() function in Excel is used to check if a character in a string is a double-byte character or not.
    In the Python code, we define a function called DBCS() that takes a string as input.
    We initialize an empty string called "result" to store the double-byte characters found in the input string.
    We then iterate over each character in the input string using a for loop.
    Inside the loop, we use the ord() function to get the Unicode code point of the character.
    If the Unicode code point is greater than 255, it means that the character is a double-byte character.
    In that case, we append the character to the "result" string.
    Finally, we return the "result" string, which contains all the double-byte characters found in the input string.
    Note:
    This code assumes that the input string contains only Unicode characters.
    If the input string contains non-Unicode characters, the behavior of the code may vary.
    '''
    result = ""
    for char in string:
        if ord(char) > 255:
            result += char
    return result


# DOLLAR function
def DOLLAR(number, decimals=2):
    '''
    Converts a number to text, using the $ (dollar) currency format
    
    The DOLLAR() function takes two parameters: number and decimals.
    The number parameter represents the numerical value that needs to be converted to a dollar format,
    and the decimals parameter specifies the number of decimal places to include in the formatted output.
    
    The function uses the format() method to format the number parameter as a dollar value.
    The '{:.{}f}'.format(number, decimals) syntax formats the number with the specified number of decimal places.
    The '$' symbol is added at the beginning to represent the dollar currency.
    '''
    return '${:.{}f}'.format(number, decimals)


# EXACT function
def EXACT(string1, string2):
    '''
    Checks to see if two text values are identical
    '''
    if string1 == string2:
        return True
    else:
        return False


# FIND, FINDB functions
def FIND(data, value):
    '''
    Finds one text value within another (case-sensitive)
    '''
    for i in range(len(data)):
        if data[i] == value:
            return i
    return -1


def FINDB(string, substring, start=1):
    '''
    Finds one text value within another (case-sensitive)
    
    The FINDB() function takes three parameters: string, substring, and start.
    It returns the position of the first occurrence of the substring within the string, starting from the specified start position.

    Note:
    The FINDB() function returns the position of the substring as per the Excel convention, where the position starts from 1 instead of 0.
    '''
    return string.find(substring, start-1) + 1


# FIXED function
def FIXED(number, decimals):
    '''
    Formats a number as text with a fixed number of decimals
    
    The FIXED() function takes two parameters: number and decimals.
    It formats the number to a fixed number of decimal places specified by decimals and returns the formatted string.
    '''
    return "{:.{}f}".format(number, decimals)


# LEFT, LEFTB functions
def LEFT(string, num):
    '''
    Returns the leftmost characters from a text value
    
    The LEFT() function takes two parameters:
    string (the input string) 
    and num (the number of characters to extract from the left side of the string).
    '''
    return string[:num]


def LEFTB(string, num):
    '''
    Returns the leftmost characters from a text value
    '''
    return string[:num]


# LEN, LENB functions
def LEN(data):
    '''
    Returns the number of characters in a text string
    
    The LEN() function takes a parameter data and returns the length of the data provided.
    The function first checks the type of the data parameter using the isinstance() function.
    If the data is a string, list, or dictionary, the function returns the length of the data using the len() function.
    If the data is not of any of these types, the function returns 0.
    You can use this len_excel() function in your Python code to calculate the length of different types of data,
    just like the LEN() function in Microsoft Excel.
    '''
    if isinstance(data, str):
        return len(data)
    elif isinstance(data, list):
        return len(data)
    elif isinstance(data, dict):
        return len(data)
    else:
        return 0


def LENB(text):
    '''
    Returns the number of characters in a text string
    
    The LENB() function in Excel is used to count the number of bytes in a given text string.
    The Python code defines a function called lenb() that takes a text parameter.
    Inside the function, the text string is encoded using the UTF-8 encoding,
    and the length of the encoded string is returned using the len() function.
    '''
    return len(text.encode('utf-8'))


# LOWER function
def LOWER(string):
    '''
    Converts text to lowercase
    
    It returns the lowercase version of the string using the lower() method.
    '''
    return string.lower()


# MID, MIDB functions
def MID(string, start, length):
    '''
    Returns a specific number of characters from a text string starting at the position you specify
    
    The mid function takes three parameters: string, start, and length.
    The string parameter represents the input string from which we want to extract a substring.
    The start parameter specifies the starting position of the substring within the input string.
    The length parameter determines the number of characters to be extracted from the input string, starting from the start position.
    The function returns the extracted substring as the output.
    '''
    return string[start-1:start-1+length]


def MIDB(text, start_num, num_chars):
    '''
    Returns a specific number of characters from a text string starting at the position you specify
    
    The above code snippet demonstrates a Python function that serves as an equivalent to the MIDB() function in Microsoft Excel. The MIDB() function in Excel is used to extract a specific number of characters from a given text string, starting from a specified position.
    In the Python code provided, the midb() function takes three parameters:
    - text: This parameter represents the input text string from which characters need to be extracted;
    - start_num: This parameter indicates the starting position from where the extraction should begin;
    - num_chars: This parameter specifies the number of characters to be extracted from the text string.
    The function returns a substring of the input text string, starting from the start_num position and containing num_chars characters.
    '''
    return text[start_num-1:start_num-1+num_chars]


# NUMBERVALUE function
def NUMBERVALUE(value):
    '''
    Converts text to number in a locale-independent manner
    
    It takes a value as input and attempts to convert it into a floating-point number.
    If the conversion is successful, it returns the number. Otherwise, it returns None.
    '''
    try:
        return float(value)
    except ValueError:
        return None


# PHONETIC function
def PHONETIC(word):
    '''Extracts the phonetic (furigana) characters from a text string'''
    phonetic_dict = {
        'A': 'Alpha',
        'B': 'Bravo',
        'C': 'Charlie',
        'D': 'Delta',
        'E': 'Echo',
        'F': 'Foxtrot',
        'G': 'Golf',
        'H': 'Hotel',
        'I': 'India',
        'J': 'Juliet',
        'K': 'Kilo',
        'L': 'Lima',
        'M': 'Mike',
        'N': 'November',
        'O': 'Oscar',
        'P': 'Papa',
        'Q': 'Quebec',
        'R': 'Romeo',
        'S': 'Sierra',
        'T': 'Tango',
        'U': 'Uniform',
        'V': 'Victor',
        'W': 'Whiskey',
        'X': 'X-ray',
        'Y': 'Yankee',
        'Z': 'Zulu'
    }
    
    phonetic_word = ''
    for char in word.upper():
        if char.isalpha():
            phonetic_word += phonetic_dict[char] + ' '
    
    return phonetic_word.strip()


# PROPER function
def PROPER(string):
    '''
    Capitalizes the first letter in each word of a text value
    
    This code defines a Python function called proper() that takes a string as input and returns the same string with each word capitalized.
    The function uses the split() method to split the string into a list of words,
    and then uses a generator expression and the capitalize() method to capitalize the first letter of each word.
    Finally, the join() method is used to join the capitalized words back into a single string.
    '''
    return ' '.join(word.capitalize() for word in string.split())


# REPLACE, REPLACEB functions
def REPLACE(string, old, new):
    '''Replaces characters within text'''
    return string.replace(old, new)


def REPLACEB(text, start, num_chars, new_text):
    '''
    Replaces characters within text
    
    Note:
    The above code is an analog of the REPLACEB() function in Microsoft Excel.
    It replaces a specified number of characters in a string with new text, starting from a given position.
    '''
    return text[:start] + new_text + text[start + num_chars:]


# REPT function
def REPT(text, count):
    '''
    Repeats text a given number of times
    
    The rept() function takes two parameters: text and count.
    It returns a string that repeats the text a specified number of times, based on the count parameter.
    '''
    return text * count


# RIGHT, RIGHTB functions
def RIGHT(string, num):
    '''
    Returns the rightmost characters from a text value
    
    It takes two parameters: string (the input string) and num_chars (the number of characters to extract from the right side of the string).
    The function returns the specified number of characters from the right side of the input string.
    '''
    return string[-num:]


def RIGHTB(string, num):
    '''Returns the rightmost characters from a text value'''
    return string[-num:]


# SEARCH, SEARCHB functions
def SEARCH(data, value):
    '''
    Finds one text value within another (not case-sensitive)
    '''
    result = []
    for item in data:
        if value in item:
            result.append(item)
    return result


def SEARCHB(string, substring, start=0, end=None):
    '''
    Finds one text value within another (not case-sensitive)
    
    The searchb() function takes in four parameters: string, substring, start, and end.
    The string parameter represents the text in which we want to search for the substring.
    The substring parameter represents the text we are searching for within the string.
    The start parameter represents the starting index from which the search should begin (default is 0).
    The end parameter represents the ending index at which the search should stop (default is the length of the string).
    The function uses a for loop to iterate through the string from the specified start index to the end index.
    It checks if the substring matches the portion of the string at each iteration.
    If a match is found, the function returns the index of the first character of the match plus 1
    (to match the behavior of the SEARCHB() function in Excel).
    If no match is found, the function returns -1.
    '''
    if end is None:
        end = len(string)
    for i in range(start, end):
        if string[i:i+len(substring)] == substring:
            return i+1
    return -1


# SUBSTITUTE function
def SUBSTITUTE(text, old, new, occurrence=None):
    '''
    Substitutes new text for old text in a text string
    
    The function takes four parameters: text, old, new, and occurrence.
    The text parameter represents the original text or string in which the substitution will occur.
    The old parameter represents the substring that needs to be replaced, while the new parameter represents the replacement substring.
    The occurrence parameter is optional and allows you to specify the number of occurrences of the old substring that should be replaced.
    If the occurrence parameter is not provided, the function will replace all occurrences of the old substring with the new substring.
    '''
    if occurrence is None:
        return text.replace(old, new)
    else:
        return text.replace(old, new, occurrence)


# T function
def T(*args):
    '''
    Converts its arguments to text
    
    The T() function takes any number of arguments and returns a tuple containing all the arguments.
    This allows us to pass in multiple values and have them transposed into a tuple.
    The *args parameter in the function definition allows us to accept a variable number of arguments.
    '''
    return tuple(args)


# TEXT function
def TEXT(value, format):
    '''
    Formats a number and converts it to text
    
    It takes two parameters: value and format.
    The value parameter represents the value that you want to format,
    and the format parameter specifies the desired format for the value.
    To use the text() function, simply pass the value and format as arguments.
    The function will return the formatted value according to the specified format.
    '''
 format.format(value)


# TEXTAFTER function
def TEXTAFTER():
    '''Returns text that occurs after given character or string'''
    pass
    return


# TEXTBEFORE function
def TEXTBEFORE():
    '''Returns text that occurs before a given character or string'''
    pass
    return


# TEXTJOIN function
def TEXTJOIN():
    '''Text:    Combines the text from multiple ranges and/or strings'''
    pass
    return


# TEXTSPLIT function
def TEXTSPLIT():
    '''Splits text strings by using column and row delimiters'''
    pass
    return


# TRIM function
def TRIM():
    '''Removes spaces from text'''
    pass
    return


# UNICHAR function
def UNICHAR():
    '''Returns the Unicode character that is references by the given numeric value'''
    pass
    return


# UNICODE function
def UNICODE():
    '''Returns the number (code point) that corresponds to the first character of the text'''
    pass
    return


# UPPER function
def UPPER():
    '''Converts text to uppercase'''
    pass
    return


# VALUE function
def VALUE():
    '''Converts a text argument to a number'''
    pass
    return


# VALUETOTEXT function
def VALUETOTEXT():
    '''Returns text from any specified value'''
    pass
    return


