def same_frequency(num1, num2):
    """Do these nums have same frequencies of digits?

        >>> same_frequency(551122, 221515)
        True

        >>> same_frequency(321142, 3212215)
        False

        >>> same_frequency(1212, 2211)
        True
    """
    num1_dict = {}
    num2_dict = {}
    num1_list = [int(x) for x in str(num1)]
    num2_list = [int(x) for x in str(num2)]

    for num in set(num1_list):
        num1_dict[num] = num1_list.count(num)

    for num in set(num2_list):
        num2_dict[num] = num2_list.count(num)

    if num1_dict == num2_dict:
        return True
    else:
        return False
