def dates_overlap(first_start_dt, first_end_dt, second_start_dt, second_end_dt):
    """

    :param first_start_dt:
    :param first_end_dt:
    :param second_start_dt:
    :param second_end_dt:
    :return:
    """
    overlaps = first_start_dt <= second_start_dt <= first_end_dt or first_start_dt <= second_end_dt <= first_end_dt
    envelops = second_start_dt <= first_start_dt and second_end_dt >= first_end_dt

    return overlaps or envelops
