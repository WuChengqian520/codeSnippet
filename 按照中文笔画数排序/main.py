# ------------------------
#
# 按照中文笔画数量对字符串进行排序
# 使用场景：按照人名笔画数量排序（香港人的习惯）
# 最后编辑：2021-11-02
# 作者：wuchengqian
#
# ------------------------

from typing import Iterable, Callable, Union

# 加载汉字笔画对照文件，参考同级目录下的 chinese_unicode_table.txt 文件格式
chinese_char_map = {}
with open('./chinese_unicode_table.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    for line in lines[6:]:  # 前6行是表头，去掉
        line_info = line.strip().split()
        # 处理后的数组第一个是文字，第7个是笔画数量
        chinese_char_map[line_info[0]] = line_info[6]


def __sort_by_strokes_core(words: Iterable) -> int:
    """
    统计字符串中所有文字的笔画总数

    :param words: 需要统计的字符串
    :return: 笔画总数
    """
    strokes = 0
    for word in words:
        if 0 <= ord(word) <= 126:  # 数字，英文符号范围
            strokes += 1
        elif 0x4E00 <= ord(word) <= 0x9FA5:  # 常用汉字Unicode编码范围4E00-9FA5，20902个字
            strokes += int(chinese_char_map.get(word, 1))
        else:  # 特殊符号字符一律排在最后
            strokes += 1
    return strokes


def __sort_by_sequence_core(words: Iterable) -> Iterable[int]:
    """
    计算字符串中各个字符的优先级，组成数组返回，用于后面排序，
    优先排数字，再拍英文字母，最后排汉字， 为了确保汉字排在后面，所有汉字在笔画数量基础上再 +1000

    :param words: 需要统计的字符串
    :return: 字符串中字符笔画数列表
    """
    weight = []
    for word in words:
        if 0 <= ord(word) <= 126:  # 数字，英文符号范围
            weight.append(ord(word))
        elif 0x4E00 <= ord(word) <= 0x9FA5:  # 常用汉字Unicode编码范围4E00-9FA5，20902个字
            weight.append(1000 + int(chinese_char_map.get(word, 0)))
        else:  # 特殊符号字符一律排在最后
            weight.append(99999)
    return weight


def sort_by_strokes(object_list: Iterable,
                    model: str = 'sequence',
                    key: Union[Callable, None] = None,
                    reverse=False
                    ) -> Iterable:
    """
    根据笔画数量对中文字符串进行排序

    :param object_list: 文字字符串列表
    :param model: 排序模式，sequence--按照文字笔画依次排序， total--按照笔画总数排序，默认：sequence
    :param key: 文字字符串列表
    :param reverse: 倒序排序
    :return: 排序后的字符串列表

    >>> name_list = ['张三', '李四', '王五', '赵六', '尼古拉丁', '周吴郑王']
    >>> print(sort_by_strokes(name_list))
    ['王五', '尼古拉丁', '张三', '李四', '周吴郑王', '赵六']
    """
    assert model in ['sequence', 'total'], '仅支持【sequence】和【total】两种模式'
    if model == 'sequence':
        _core_function = __sort_by_sequence_core
    else:
        _core_function = __sort_by_strokes_core

    __order_key = '__sort_weight'
    sorted_obj = []
    for obj in object_list:
        words = key(obj) if key else obj
        assert isinstance(words, Iterable), '用于排序的对象必须是一个可迭代对象, 其他类型请自行实现！'
        strokes = _core_function(words)
        # 构建一个新的字典，用于存放排序对象和排序权重，后面根据权重进行排序后再取出对象
        sorted_obj.append({'obj': obj, __order_key: strokes})

    sorted_words = sorted(sorted_obj, key=lambda x: x[__order_key], reverse=reverse)
    # 取出排序后的对象
    sorted_words = [item['obj'] for item in sorted_words]
    return sorted_words


if __name__ == '__main__':
    peoples = ['张三', '李四', '王五', '赵六', '尼古拉丁', '周吴郑王']
    print('普通排序：', sort_by_strokes(peoples))
    print('倒序排序：', sort_by_strokes(peoples, reverse=True))
    print('按照笔画总数排序：', sort_by_strokes(peoples, model='total'))
    students = [
        {'name': '王梓涵', 'sex': '男', 'age': 12, 'grade': 60},
        {'name': '周小静', 'sex': '女', 'age': 13, 'grade': 99},
        {'name': '张靓颖', 'sex': '女', 'age': 11, 'grade': 80},
        {'name': '欧阳晓晓', 'sex': '女', 'age': 14, 'grade': 67},
        {'name': '东方不败', 'sex': '男', 'age': 13, 'grade': 72},
        {'name': '周一天', 'sex': '男', 'age': 15, 'grade': 72},
        {'name': '♂卐', 'sex': '男', 'age': 13, 'grade': 72},
    ]
    print('字典排序：', sort_by_strokes(students, key=lambda x: x['name']))
