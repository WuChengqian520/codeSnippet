from typing import Dict, List
from math import radians, cos, sin, asin, sqrt

# 地球平均半径，单位为千米，数据来源百度百科
EARTH_RADIUS = 6371.393


def get_distance(location1: Dict[str, float], location2: Dict[str, float]) -> float:
    """
    计算两个坐标点之间的直线距离

    :param location1: 坐标点1 {lng: x, lat: x}
    :param location2: 坐标点2 {lng: x, lat: x}
    :return : 两个点的距离，浮点型，单位为：米
    """
    try:
        lng1 = location1['lng']
        lat1 = location1['lat']
        lng2 = location2['lng']
        lat2 = location2['lat']
    except KeyError:
        raise KeyError("用于转换的参数必须是包含 'lng' 和 'lat' 为键的字典！")

    # 将十进制度数转化为弧度
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])

    # haversine公式
    lng_distance = lng2 - lng1
    lat_distance = lat2 - lat1
    f = sin(lat_distance / 2) ** 2 + cos(lat1) * cos(lat2) * sin(lng_distance / 2) ** 2
    c = 2 * asin(sqrt(f))
    return c * EARTH_RADIUS * 1000


def is_point_in_polygon(point: Dict[str, float], polygon: List[Dict[str, float]]) -> bool:
    """
    判断點是否在矩形內，采用射线法求解。
    射线法原理讲解：https://www.jianshu.com/p/ba03c600a557
    原处理方法：http://www.manongjc.com/detail/7-fvhxxmyhoruohss.html

    :param point: 定位坐标，包含lat和lng属性的字典
    :param polygon: 多边形的所有点组成的列表
    :return: Bool
    """
    lng_list = []
    lat_list = []
    for i in range(len(polygon) - 1):
        lng_list.append(polygon[i]['lng'])
        lat_list.append(polygon[i]['lat'])
    max_lng = max(lng_list)
    min_lng = min(lng_list)
    max_lat = max(lat_list)
    min_lat = min(lat_list)

    # 点的坐标小于区域最小，大于区域最大的点的坐标
    if point['lng'] > max_lng or point['lng'] < min_lng or point['lat'] > max_lat or point['lat'] < min_lat:
        return False
    count = 0
    point1 = polygon[0]
    for i in range(1, len(polygon)):
        point2 = polygon[i]
        # 点与多边形顶点重合
        same1 = point['lng'] == point1['lng'] and point['lat'] == point1['lat']
        same2 = point['lng'] == point2['lng'] and point['lat'] == point2['lat']
        if same1 or same2:
            return False
        # 判断线段两端点是否在射线两侧 不在肯定不相交 射线（-∞，lat）（lng,lat）
        if (point1['lat'] < point['lat'] <= point2['lat']) or (point1['lat'] >= point['lat'] > point2['lat']):
            # 求线段与射线交点 再和lat比较
            point12lng = point2['lng'] - (point2['lat'] - point['lat']) * (point2['lng'] - point1['lng']) / (
                        point2['lat'] - point1['lat'])
            # 点在多边形边上
            if point12lng == point['lng']:
                return False
            if point12lng < point['lng']:
                count += 1
        point1 = point2
    return count % 2 != 0


if __name__ == '__main__':
    # 计算两个坐标的距离
    point_1 = {'lat': 22.30514503955198, 'lng': 114.18568361243977}
    point_2 = {'lat': 22.306901940726775, 'lng': 114.18910477003827}
    distance = get_distance(point_1, point_2)
    print(f'坐标点1与坐标点2的距离为：{distance} m')

    # 判断点是否在区域内
    point = {"lat": 22.2677121556423, "lng": 114.21096912531813}
    region_points = [
        {"lat": 22.27598222764702, "lng": 114.20825066516139},
        {"lat": 22.274552569751968, "lng": 114.19915261218287},
        {"lat": 22.263829669824094, "lng": 114.20035424182154},
        {"lat": 22.26100980783833, "lng": 114.2164474959109},
        {"lat": 22.266133176888804, "lng": 114.20322956988551},
        {"lat": 22.272844903671423, "lng": 114.20275750109889},
        {"lat": 22.27415543996565, "lng": 114.2124134535525},
        {"lat": 22.270700363252548, "lng": 114.21335759112574},
        {"lat": 22.265537445938044, "lng": 114.21189846942164},
        {"lat": 22.265458014953, "lng": 114.21915116259791},
        {"lat": 22.270779791261706, "lng": 114.21897950122096},
        {"lat": 22.276816188004133, "lng": 114.21292843768336}
    ]
    result = is_point_in_polygon(point, region_points)
    print(f'坐标点是否在区域内： {result}')
