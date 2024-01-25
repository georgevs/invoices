import re


def parse_number_ranges(number_ranges):
    number_ranges = [number_range.strip() for number_range in number_ranges.split(',')]
    number_range_pattern = re.compile('(\!)?\s*(\d+)?\s*(-)?\s*(\d+)?')
    positive_number_ranges = []
    negative_number_ranges = []
    for number_range in number_ranges:
        match = number_range_pattern.search(number_range)

        neg = (match.group(1) != None)
        start = match.group(2)
        to = (match.group(3) != None)
        end = match.group(4)

        if start and to and end:
            r = (int(start), int(end))
        elif start and to:
            r = (int(start), end)
        elif to and end:
            r = (start, int(end))
        else:
            r = (int(start), int(start))
        if neg:
            negative_number_ranges.append(r)
        else:
            positive_number_ranges.append(r)

    return (positive_number_ranges, negative_number_ranges)


def number_in_number_ranges(number_ranges, number):
    def number_in_number_range(number_range, number):
        start, end = number_range
        if start != None and end != None:
            return start <= number <= end
        elif start == None and end != None:
            return number <= end
        elif start != None and end == None:
            return start <= number
        else:
            raise Exception('bad range')

    negative_number_ranges = number_ranges[1]
    for number_range in negative_number_ranges:
        if number_in_number_range(number_range, number):
            return False
    positive_number_ranges = number_ranges[0]
    for number_range in positive_number_ranges:
        if number_in_number_range(number_range, number):
            return True
    return False
