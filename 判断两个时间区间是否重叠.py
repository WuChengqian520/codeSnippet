from typing import Dict, Union
from datetime import datetime


def datetime_conflict_detection(dt_dict1: Dict[str, Union[str, datetime]],
                                dt_dict2: Dict[str, Union[str, datetime, None]]
                                ) -> bool:
    """
    判断两个时间范围是有冲突

    :param dt_dict1: 包含起始时间和结束时间的字典：{'start_time': '', 'end_time': ''}
    :param dt_dict2: 包含起始时间和结束时间的字典：{'start_time': '', 'end_time': ''}
    :return: 判断结果，True / False

    >>> datetime_format = "%Y-%m-%d %H:%M"
    >>> dt1 = datetime.strptime("2021-11-21 12:00", datetime_format)
    >>> dt2 = datetime.strptime("2021-11-21 13:00", datetime_format)
    >>> dt3 = datetime.strptime("2021-11-22 15:00", datetime_format)
    >>> dt4 = datetime.strptime("2021-11-22 16:00", datetime_format)
    >>> dt_range1 = {'start_time': dt1, 'end_time': dt2}
    >>> dt_range2 = {'start_time': dt3, 'end_time': dt4}
    >>> datetime_conflict_detection(dt_range1, dt_range2)
    False
    >>> dt_range1 = {'start_time': dt1, 'end_time': dt3}
    >>> dt_range2 = {'start_time': dt2, 'end_time': dt4}
    >>> datetime_conflict_detection(dt_range1, dt_range2)
    True
    """
    assert isinstance(dt_dict1, dict), "参数类型错误，接收参数格式：{'start_time': datetime, 'end_time': datetime}"
    assert isinstance(dt_dict2, dict), "参数类型错误，接收参数格式：{'start_time': datetime, 'end_time': datetime}"
    if not dt_dict1.get('start_time') or not dt_dict2.get('start_time'):
        raise ValueError('传入的字典缺少字段： start_time ')

    # 两个对象都没有截止时间
    if not dt_dict1['end_time'] and not dt_dict2['end_time']:
        return dt_dict1['start_time'] == dt_dict2['start_time']

    # 第一个时间对象没有截止时间
    if dt_dict1['end_time'] is None:
        return dt_dict2['start_time'] <= dt_dict1['start_time'] <= dt_dict2['end_time']

    # 第二个时间对象没有截止时间
    if dt_dict2['end_time'] is None:
        return dt_dict1['start_time'] <= dt_dict2['start_time'] <= dt_dict1['end_time']

    # 两个对象都有截止时间
    return max(dt_dict1['start_time'], dt_dict2['start_time']) < min(dt_dict1['end_time'], dt_dict2['end_time'])


if __name__ == '__main__':
    print(f' 时间冲突功能校验(部分情况) '.center(100, '*'))
    dt_format = "%Y-%m-%d %H:%M"
    datetime1 = datetime.strptime("2021-11-21 12:00", dt_format)
    datetime2 = datetime.strptime("2021-11-21 13:00", dt_format)
    datetime3 = datetime.strptime("2021-11-22 15:00", dt_format)
    datetime4 = datetime.strptime("2021-11-22 16:00", dt_format)
    dt_range_1 = {'start_time': datetime1, 'end_time': datetime2}
    dt_range_2 = {'start_time': datetime3, 'end_time': datetime4}
    res = datetime_conflict_detection(dt_range_1, dt_range_2)
    print(f'【时间无交集】 冲突检测结果：{res}')

    dt_range_1 = {'start_time': datetime1, 'end_time': datetime3}
    dt_range_2 = {'start_time': datetime2, 'end_time': datetime4}
    res = datetime_conflict_detection(dt_range_1, dt_range_2)
    print(f'【时间有交集】 冲突检测结果：{res}')

    dt_range_1 = {'start_time': datetime2, 'end_time': None}
    dt_range_2 = {'start_time': datetime1, 'end_time': datetime4}
    res = datetime_conflict_detection(dt_range_1, dt_range_2)
    print(f'【结束时间为空且包含】 冲突检测结果：{res}')

    dt_range_1 = {'start_time': "2021-11-21 12:00", 'end_time': "2021-11-22 15:00"}
    dt_range_2 = {'start_time': "2021-11-21 13:00", 'end_time': "2021-11-22 16:00"}
    res = datetime_conflict_detection(dt_range_1, dt_range_2)
    print(f'【使用日期时间字符串】 冲突检测结果：{res}')

    dt_range_1 = {'start_time': "12:00", 'end_time': "15:00"}
    dt_range_2 = {'start_time': "13:00", 'end_time': "16:00"}
    res = datetime_conflict_detection(dt_range_1, dt_range_2)
    print(f'【不包含日期】 冲突检测结果：{res}')
