def mode(nums):
    """Return most-common number in list.

    For this function, there will always be a single-most-common value;
    you do not need to worry about handling cases where more than one item
    occurs the same number of times.

        >>> mode([1, 2, 1])
        1

        >>> mode([2, 2, 3, 3, 2])
        2
    """

    mode_counter = 0
    mode = 0

    nums_set = set(nums)

    for num in nums_set:
        counter = nums.count(num)
        if counter > mode_counter:
            mode_counter = counter
            mode = num

    return mode
