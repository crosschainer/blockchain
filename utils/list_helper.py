def merge_two_lists(list1, list2):
    """
    Merges two lists together without duplicates
    :param list1:
    :param list2:
    :return:
    """
    merged_list = list1 + list2
    merged_list = list(dict.fromkeys(merged_list))
    return merged_list