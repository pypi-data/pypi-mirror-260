# logical
# AND function
def AND(*args):
    '''
    Returns TRUE if all of its arguments are TRUE

    This function takes in any number of arguments and returns True if all the arguments are True, and False otherwise.
    It utilizes the all() function, which returns True if all elements in an iterable are True.
    '''
    return all(args)


# BYCOL function
def BYCOL(data):
    '''
    Applies a LAMBDA to each column and returns an array of the results

    This code defines a function called BYCOL() that takes a 2D list or matrix as input (data).
    It then iterates over each column in the input data and creates a new list containing the elements of that column.
    Finally, it appends each column list to the result list and returns it.
    Note: This code assumes that all rows in the input data have the same number of columns.
    If the input data is not rectangular, the function may produce unexpected results!
    '''
    result = []
    for col in range(len(data[0])):
        column = [row[col] for row in data]
        result.append(column)
    return result


# BYROW function
def BYROW(data):
    '''
    Applies a LAMBDA to each row and returns an array of the results

    The function takes a 2-dimensional list data as input and returns a new 2-dimensional list result.
    The function iterates over each row in the data list and creates a new row in the result list with the same values.
    Finally, it returns the result list.
    '''
    result = []
    for row in data:
        row_result = []
        for value in row:
            row_result.append(value)
        result.append(row_result)
    return result


# FALSE function
def FALSE():
    '''
    Returns the logical value FALSE.

    This function simply returns the boolean value False.
    '''
    return False


# IF function
def IF(condition, true_value, false_value):
    '''
    Specifies a logical test to perform

    This function takes three arguments: condition, true_value, and false_value.
    If the condition is true, the function returns the true_value.
    Otherwise, it returns the false_value.
    '''
    if condition:
        return true_value
    else:
        return false_value


# IFERROR function
def IFERROR(value, default):
    '''
    Returns a value you specify if a formula evaluates to an error. Otherwise, returns the result of the formula

    This function takes two arguments: value and default.
    It tries to return the value if it is not an error, and if an error occurs, it returns the default value.
    '''
    try:
        return value
    except:
        return default


# IFNA function
def IFNA(value, default):
    '''
    Returns the value you specify if the expression resolves to #N/A, otherwise returns the result of the expression

    This function takes two arguments: value and default.
    It checks if the value is not None and returns the value itself.
    If the value is None, it returns the default value.

    It allows you to handle cases where a value may be missing or None and provide a default value in such situations.
    '''
    return value if value is not None else default


# IFS function
def IFS(condition_list, value_list):
    '''
    Checks whether one or more conditions are met and returns a value that corresponds to the first TRUE condition

    This function takes two lists as input: condition_list and value_list.
    The condition_list contains the conditions to be evaluated, and the value_list contains the corresponding values.
    The function iterates through both lists simultaneously using the zip() function.
    For each pair of condition and value, it checks if the condition is true.
    If a condition evaluates to true, the corresponding value is returned immediately.
    If none of the conditions are true, the function returns None.
    '''
    for condition, value in zip(condition_list, value_list):
        if condition:
            return value
    return None


# LAMBDA function
def LAMBDA(x):
    '''
    Create custom, reusable functions and call them by a friendly name

    The function takes a single parameter x and returns the sum of the sine and cosine of x.
    Please note that this code is a simplified example and may not accurately represent the actual LAMBDA() function in MS Excel.
    '''
    return math.sin(x) + math.cos(x)


# LET function
def LET(*args):
    '''
    Assigns names to calculation results

    The LET() function in Excel allows you to define a variable and assign a value to it within a formula.
    It is particularly useful when you have complex formulas with repeated calculations or when you want to improve the readability of your formulas.
    The LET() function takes in any number of arguments using the *args parameter.
    It then returns the last argument passed to the function using args[-1].
    This implementation allows you to define variables and assign values within the function call itself.
    '''
    return args[-1]


# MAKEARRAY function
def MAKEARRAY(*args):
    '''
    Returns a calculated array of a specified row and column size, by applying a LAMBDA

    This function takes in any number of arguments and returns them as a list.
    The *args parameter allows the function to accept a variable number of arguments.
    '''
    return list(args)


# MAP function
def MAP(function, iterable):
    '''
    Returns an array formed by mapping each value in the array(s) to a new value by applying a LAMBDA to create a new value

    This function takes two parameters: function and iterable.
    The function parameter represents the function that will be applied to each element in the iterable.
    The iterable parameter represents the collection of elements on which the function will be applied.
    The function uses a list comprehension to iterate over each element in the iterable and applies the function to each element.
    The result is a new list containing the transformed elements.
    '''
    return [function(x) for x in iterable]


# NOT function
def NOT(value):
    '''
    Reverses the logic of its argument

    The function takes a value as input and returns the complement of that value.
    '''
    return 1 - value


# OR function
def OR(*args):
    '''
    Returns TRUE if any argument is TRUE

    This function takes in multiple arguments and returns True if at least one of the arguments is True.
    Otherwise, it returns False.
    '''
    result = False
    for arg in args:
        if arg:
            result = True
            break
    return result


# REDUCE function
def REDUCE(function, iterable, initializer=None):
    '''
    Reduces an array to an accumulated value by applying a LAMBDA to each value and returning the total value in the accumulator

    The reduce() function takes three parameters: function, iterable, and initializer.
    The function parameter represents the operation to be performed on the elements of the iterable. It can be any valid Python function that takes two arguments and returns a single value.
    The iterable parameter is the sequence of elements on which the reduction operation will be performed. It can be a list, tuple, or any other iterable object.
    The initializer parameter is an optional argument that specifies the initial value for the reduction operation. If not provided, the first element of the iterable is used as the initial value.

    This function iterates over the elements of the iterable and applies the function to each element and the accumulated value.
    The result of each iteration becomes the new accumulated value for the next iteration.
    Finally, the function returns the final accumulated value.
    '''
    it = iter(iterable)
    if initializer is None:
        value = next(it)
    else:
        value = initializer
    for element in it:
        value = function(value, element)
    return value

# SCAN function
def SCAN(*args):
    '''
    Scans an array by applying a LAMBDA to each value and returns an array that has each intermediate value

    This function takes in any number of arguments and returns a single list containing all the elements from the input arguments.
    '''
    result = []
    for arg in args:
        if isinstance(arg, list):
            result.extend(arg)
        else:
            result.append(arg)
    return result


# SWITCH function
def SWITCH(condition, true_value, false_value):
    '''
    Evaluates an expression against a list of values and returns the result corresponding to the first matching value. If there is no match, an optional default value may be returned

    This function takes three arguments: condition, true_value, and false_value.
    If the condition is true, the function returns the true_value.
    Otherwise, it returns the false_value.
    '''
    if condition:
        return true_value
    else:
        return false_value


# TRUE function
def TRUE():
    '''
    Returns the logical value TRUE

    This function simply returns the boolean value True.
    '''
    return True


# XOR function
def XOR(a, b):
    '''
    Returns a logical exclusive OR of all arguments

    It takes two inputs a and b and returns the result of the XOR operation between them.
    The XOR operation returns 1 if the inputs are different, and 0 if they are the same.
    In the analog version, instead of using logical 1 and 0, we use the values 1 and 0 to represent the inputs and the result.
    The formula a + b - 2 * a * b is used to calculate the analog XOR.
    It works by adding the inputs a and b, and then subtracting twice the product of a and b.
    This results in 1 if the inputs are different, and 0 if they are the same.
    '''
    return a + b - 2 * a * b

