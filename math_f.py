def median(values: list[int]) -> float:
    n = len(values)

    values.sort()

    if n % 2 == 0:
        median1 = values[n // 2]
        median2 = values[n // 2 - 1]
        median = (median1 + median2) / 2
    else:
        median = values[n // 2]
    return median


def find_iqr(values: list[int]) -> tuple[float, float, float]:
    values.sort()
    med = median(values)
    q1_list = [v for v in values if v < med]
    q3_list = [v for v in values if v > med]

    if len(q1_list) > 0:
        q1 = median(q1_list)
    else:
        q1 = values[0]
    if len(q3_list) > 0:
        q3 = median(q3_list)
    else:
        q3 = values[-1]

    iqr = q3 - q1
    return q3, q1, iqr


def find_bounds(values: list[int]) -> tuple[float, float]:
    q3, q1, iqr = find_iqr(values)
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return upper_bound, lower_bound


def iqr_filter(values: list[int]) -> list[int]:
    upper_bound, lower_bound = find_bounds(values)
    res_list = [v for v in values if v < upper_bound and v > lower_bound]

    if len(res_list) > 0:
        return res_list
    return values
