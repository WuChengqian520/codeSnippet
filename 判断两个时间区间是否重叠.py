from typing import Dict, Union


def _time_a_include_b(range_a: dict, range_b: dict) -> bool:
    """
    判断时间返回A是否包含时间范围B

    :param range_a: 时间范围
    :param range_b: 时间范围
    :return: 判断结果，True/False
    """
    include_flag = False
    start_in = range_a['start_time'] <= range_b['start_time'] <= range_a['end_time']
    end_in = False
    if range_b['end_time']:
        end_in = range_a['start_time'] <= range_b['end_time'] <= range_a['end_time']
    if start_in or end_in:
        include_flag = True
    return include_flag


def time_conflict_detection(time_range1: Dict[str, Union[str, None]],
                            time_range2: Dict[str, Union[str, None]],
                            auto_exchange: bool = False) -> bool:
    """
    判断两个时间范围是否有冲突，接收的时间参数仅支持字符串，请自行做格式转换

    :param time_range1: 包含起始时间和结束时间的字典 {'start_time': '10:00', 'end_time': '13:30'}
    :param time_range2: 包含起始时间和结束时间的字典 {'start_time': '10:00', 'end_time': '13:30'}
    :param auto_exchange: 如果结束时间小于起始时间，是否自动交换两个值
    :return: 冲突检测结果， True/False

    >>> time_a = {'start_time': '10:00', 'end_time': '13:30'}
    >>> time_b = {'start_time': '10:30', 'end_time': '14:00'}
    >>> time_conflict_detection(time_a, time_b)
    True
    >>> time_c = {'start_time': '10:00', 'end_time': None}
    >>> time_d = {'start_time': '10:30', 'end_time': '14:00'}
    >>> time_conflict_detection(time_c, time_d)
    False
    """
    assert isinstance(time_range1, dict), "参数类型错误，接收参数格式：{start_time: [str,time], end_time: [str,None]}"
    assert isinstance(time_range2, dict), "参数类型错误，接收参数格式：{start_time: [str,time], end_time: [str,None]}"
    if not time_range1['start_time'] or not time_range2['start_time']:
        raise ValueError('传入的字典缺少字段： start_time ')

    # 两个参数都只有一个时间的情况
    if (not time_range1['end_time']) and (not time_range2['end_time']):
        return time_range1['start_time'] == time_range2['start_time']

    # 冲突标记
    detection_flag = False

    # 判断时间2是否包含时间1
    if time_range2['end_time']:
        if time_range2['start_time'] > time_range2['end_time']:
            if auto_exchange:
                time_range2['start_time'], time_range2['end_time'] = time_range2['end_time'], time_range2['start_time']
            else:
                raise ValueError('时间范围错误, end_time 应该大于 start_time')
        if _time_a_include_b(time_range2, time_range1):
            detection_flag = True

    # 判断时间1是否包含时间2
    if time_range1['end_time']:
        if time_range1['start_time'] > time_range1['end_time']:
            if auto_exchange:
                time_range1['start_time'], time_range1['end_time'] = time_range1['end_time'], time_range1['start_time']
            else:
                raise ValueError('时间范围错误, end_time 应该大于 start_time')
        if _time_a_include_b(time_range1, time_range2):
            detection_flag = True
    return detection_flag


if __name__ == '__main__':
    print(f' 时间冲突功能校验(部分情况) '.center(100, '*'))
    time_A = {'start_time': '10:00', 'end_time': '13:30'}
    time_B = {'start_time': '12:00', 'end_time': '13:00'}
    res = time_conflict_detection(time_A, time_B)
    print(f'【A包含B】 是否冲突：{res}, '
          f'时间A：{time_A["start_time"]}--{time_A["end_time"]}, 时间B：{time_B["start_time"]}--{time_B["end_time"]}')

    time_A = {'start_time': '12:00', 'end_time': '13:30'}
    time_B = {'start_time': '10:00', 'end_time': '14:00'}
    res = time_conflict_detection(time_A, time_B)
    print(f'【B包含A】：是否冲突：{res}, '
          f'时间A：{time_A["start_time"]}--{time_A["end_time"]}, 时间B：{time_B["start_time"]}--{time_B["end_time"]}')

    time_A = {'start_time': '12:00', 'end_time': '13:30'}
    time_B = {'start_time': '15:00', 'end_time': '18:00'}
    res = time_conflict_detection(time_A, time_B)
    print(f'【AB无交集】：是否冲突：{res}, '
          f'时间A：{time_A["start_time"]}--{time_A["end_time"]}, 时间B：{time_B["start_time"]}--{time_B["end_time"]}')

    time_A = {'start_time': '12:00', 'end_time': None}
    time_B = {'start_time': '15:00', 'end_time': None}
    res = time_conflict_detection(time_A, time_B)
    print(f'【AB截止时间为空】：是否冲突：{res}, '
          f'时间A：{time_A["start_time"]}--{time_A["end_time"]}, 时间B：{time_B["start_time"]}--{time_B["end_time"]}')

    time_A = {'start_time': '12:00', 'end_time': None}
    time_B = {'start_time': '15:00', 'end_time': '18:00'}
    res = time_conflict_detection(time_A, time_B)
    print(f'【A截止时间为空】：是否冲突：{res}, '
          f'时间A：{time_A["start_time"]}--{time_A["end_time"]}, 时间B：{time_B["start_time"]}--{time_B["end_time"]}')

    time_A = {'start_time': '12:00', 'end_time': '18:00'}
    time_B = {'start_time': '15:00', 'end_time': None}
    res = time_conflict_detection(time_A, time_B)
    print(f'【B截止时间为空】：是否冲突：{res}, '
          f'时间A：{time_A["start_time"]}--{time_A["end_time"]}, 时间B：{time_B["start_time"]}--{time_B["end_time"]}')

    time_A = {'start_time': '12:00', 'end_time': '10:00'}
    time_B = {'start_time': '11:00', 'end_time': None}
    res = time_conflict_detection(time_A, time_B, auto_exchange=True)
    print(f'【自动交换起始截止时间】：是否冲突：{res}, '
          f'时间A：{time_A["start_time"]}--{time_A["end_time"]}, 时间B：{time_B["start_time"]}--{time_B["end_time"]}')
