import requests
import settings
class AMapClient:
    """
    高德地图API
    """
    def __init__(self):
        self.api_key = settings.GAODE_MAP_KEY
        self.base_url = "https://restapi.amap.com/v3"

    def geocode(self, address, city=None, output="JSON"):
        """
        调用地理编码 API，根据结构化地址信息获取经纬度。
        :param address: 结构化地址信息（如：北京市朝阳区阜通东大街6号）。
        :param city: 指定查询的城市（可选）。最好填写，更为准确。
        :param output: 返回数据格式类型，默认 JSON。
        :return: 经纬度坐标（经度, 纬度）或 None（查询失败）。
        """
        url = f"{self.base_url}/geocode/geo"
        params = {
            "key": self.api_key,
            "address": address,
            "output": output
        }
        if city:
            params["city"] = city

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data.get("status") == "1" and data.get("geocodes"):
                location = data["geocodes"][0]["location"]
                longitude, latitude = map(float, location.split(","))
                return longitude, latitude
            else:
                print(f"地理编码查询失败: {data.get('info')}")
                return None
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None

    def reverse_geocode(self, location, output="JSON"):
        """
        调用逆地理编码 API，根据经纬度获取结构化地址信息。
        :param location: 经纬度坐标，格式为 "经度,纬度"（如："116.481488,39.990464"）。
        :param output: 返回数据格式类型，默认 JSON。
        :return: 地址信息或 None（查询失败）。
        """
        url = f"{self.base_url}/geocode/regeo"
        params = {
            "key": self.api_key,
            "location": location,
            "output": output
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data.get("status") == "1" and "regeocode" in data:
                address = data["regeocode"].get("formatted_address")
                return address
            else:
                print(f"逆地理编码查询失败: {data.get('info')}")
                return None
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None

    def ip_location(self, ip=None, output="JSON"):
        """
        调用 IP 定位 API，根据 IP 地址获取位置信息。
        :param ip: 需要查询的 IP 地址（仅支持国内 IP）。如果为空，则使用请求 IP。
        :param output: 返回数据格式类型，默认 JSON。
        :return: 位置信息（省、市、城市编码）或 None（查询失败）。
        """
        url = f"{self.base_url}/ip"
        params = {
            "key": self.api_key,
            "output": output
        }
        if ip:
            params["ip"] = ip

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data.get("status") == "1":
                location_info = {
                    "province": data.get("province"),
                    "city": data.get("city"),
                    "adcode": data.get("adcode")
                }
                return location_info
            else:
                print(f"IP 定位查询失败: {data.get('info')}")
                return None
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None

    # 生成静态地图的URL
    def get_static_map(self, location=None, zoom=10, size="400*400", scale=1,
                       markers=None, labels=None, paths=None, traffic=0):
        """
        获取静态地图的URL。

        :param location: 地图中心点，格式为 "经度,纬度"。
        :param zoom: 地图缩放级别，范围 [1,17]。
        :param size: 地图大小，格式 "宽*高"，最大为 1024*1024。
        :param scale: 图片比例，1 为普通图，2 为高清图。
        :param markers: 标注信息，格式参考 markers 规则。
                        - 基本格式: markers=markersStyle1:location1;location2..|markersStyle2:location3;location4..
                        - 示例：markers=mid,0xFF0000,A:116.37359,39.92437;116.47359,39.92437
                        - 参数详解：
                          - `size`: 标注大小，可选 small, mid, large。默认 small。
                          - `color`: 标注颜色，取值范围 [0x000000, 0xFFFFFF]。如 0xFF0000 表示红色。
                          - `label`: 标注标签，内容为 [0-9], [A-Z] 或单个汉字（仅在 size 不为 small 时显示）。
                          - 多个标注位置用 “;” 分隔，多个样式用 “|” 分隔。
                        - 自定义图片标注：使用 -1 表示自定义图标，格式为 markers=-1,url,0:经度,纬度；例如:
                          markers=-1,https://example.com/marker.png,0:116.37359,39.92437

        :param labels: 标签信息，格式参考 labels 规则。
                       - 基本格式: labels=labelsStyle1:location1;location2..|labelsStyle2:location3;location4..
                       - 示例：labels=朝阳公园,2,0,16,0xFFFFFF,0x008000:116.48482,39.94858
                       - 参数详解：
                         - `content`: 标签内容，最多15字符。
                         - `font`: 字体，0=微软雅黑, 1=宋体, 2=Times New Roman, 3=Helvetica。默认 0。
                         - `bold`: 是否加粗，0=否，1=是。默认 0。
                         - `fontSize`: 字体大小，范围 [1,72]。默认 10。
                         - `fontColor`: 字体颜色，范围 [0x000000, 0xFFFFFF]。默认 0xFFFFFF。
                         - `background`: 背景色，范围 [0x000000, 0xFFFFFF]。默认 0x5288d8。

        :param paths: 折线信息，格式参考 paths 规则。
                      - 基本格式: paths=pathsStyle1:location1;location2..|pathsStyle2:location3;location4..
                      - 示例：paths=10,0x0000ff,1,,:116.31604,39.96491;116.320816,39.966606;116.321785,39.966827
                      - 参数详解：
                        - `weight`: 线条宽度，范围 [2,15]。默认 5。
                        - `color`: 线条颜色，范围 [0x000000, 0xFFFFFF]。默认 0x0000FF（蓝色）。
                        - `transparency`: 线条透明度，范围 [0,1]。小数点后最多两位。默认 1（不透明）。
                        - `fillcolor`: 多边形填充颜色，取值范围同 color。
                        - `fillTransparency`: 填充透明度，范围 [0,1]。小数点后最多两位。默认 0.5。

        :param traffic: 是否展示实时路况，0 表示不展示，1 表示展示。
        :return: 返回拼接好的静态地图 URL。
        """
        url = f"{self.base_url}/staticmap"
        params = {
            "key": self.api_key,
            "zoom": zoom,
            "size": size,
            "scale": scale,
            "traffic": traffic,
            "output": "JSON"
        }

        # 如果有指定 location，加入请求参数
        if location:
            params["location"] = location

        # markers 参数处理
        if markers:
            params["markers"] = markers

        # labels 参数处理
        if labels:
            params["labels"] = labels

        # paths 参数处理
        if paths:
            params["paths"] = paths

        # 拼接 URL
        response_url = requests.Request('GET', url, params=params).prepare().url
        return response_url

    def get_weather_info(self, city_code, extensions="base", output="JSON"):
        """
        调用天气查询 API，根据城市编码获取实时或预报天气信息。

        :param city_code: 城市编码，需输入城市的 adcode（如：北京市为110000）。
        :param extensions: 气象类型。可选值：
                           - `base`：返回实时天气。
                           - `all`：返回预报天气。
        :param output: 返回格式，默认为 JSON。
        :return: 天气信息字典，或 None（查询失败）。
        """
        url = f"{self.base_url}/weather/weatherInfo"
        params = {
            "key": self.api_key,
            "city": city_code,
            "extensions": extensions,
            "output": output
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data.get("status") == "1":
                return data.get("lives") if extensions == "base" else data.get("forecasts")
            else:
                print(f"天气查询失败: {data.get('info')}")
                return None
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None


    def driving_route(self, origin, destination, strategy=0, output="JSON"):
        """
        驾车路径规划 API，根据起点和终点的经纬度规划驾车路线。

        :param origin: 出发点经纬度，格式为 "经度,纬度"（如："116.481028,39.989643"）。
        :param destination: 目的地经纬度，格式为 "经度,纬度"（如："116.465302,40.004717"）。
        :param strategy: 路线计算策略：
                         - 0：推荐
                         - 1：费用优先（不考虑时间距离因素）
                         - 2：最短距离
                         - 3：最快捷
                         - 4：躲避拥堵
                         - 5：不走高速
                         - 6：不走高速且躲避拥堵
                         - 7：躲避收费和拥堵
                         - 8：多策略综合（推荐）
        :param output: 返回数据格式类型，默认 JSON。
        :return: 路径信息字典，或 None（查询失败）。
        """
        url = f"{self.base_url}/direction/driving"
        params = {
            "key": self.api_key,
            "origin": origin,
            "destination": destination,
            "strategy": strategy,
            "output": output
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data.get("status") == "1":
                return data.get("route")
            else:
                print(f"驾车路径规划查询失败: {data.get('info')}")
                return None
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None

    def walking_route(self, origin, destination, output="JSON"):
        """
        步行路径规划 API，根据起点和终点的经纬度规划步行路线。

        :param origin: 出发点经纬度，格式为 "经度,纬度"。
        :param destination: 目的地经纬度，格式为 "经度,纬度"。
        :param output: 返回数据格式类型，默认 JSON。
        :return: 路径信息字典，或 None（查询失败）。
        """
        url = f"{self.base_url}/direction/walking"
        params = {
            "key": self.api_key,
            "origin": origin,
            "destination": destination,
            "output": output
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data.get("status") == "1":
                return data.get("route")
            else:
                print(f"步行路径规划查询失败: {data.get('info')}")
                return None
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None

    def bicycling_route(self, origin, destination, output="JSON"):
        """
        骑行路径规划 API，根据起点和终点的经纬度规划骑行路线。

        :param origin: 出发点经纬度，格式为 "经度,纬度"。
        :param destination: 目的地经纬度，格式为 "经度,纬度"。
        :param output: 返回数据格式类型，默认 JSON。
        :return: 路径信息字典，或 None（查询失败）。
        """
        url = f"{self.base_url}/direction/bicycling"
        params = {
            "key": self.api_key,
            "origin": origin,
            "destination": destination,
            "output": output
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data.get("status") == "1":
                return data.get("route")
            else:
                print(f"骑行路径规划查询失败: {data.get('info')}")
                return None
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None


    def poi_search(self, keywords, types=None, city=None, city_limit=False, page=1, offset=20, output="JSON"):
        """
        调用POI关键字搜索 API，根据关键词和分类搜索POI点。

        :param keywords: 查询的关键词，支持多个关键词，用 "|" 分隔。
        :param types: POI分类代码（可选），多个类型用 "|" 分隔，如 "餐饮|酒店"。
        :param city: 查询的城市，支持城市名、行政区划代码。
        :param city_limit: 是否限制在设定城市内搜索，True 表示限制。
        :param page: 当前页数，范围 1-100。
        :param offset: 每页记录数，最大50。
        :param output: 返回数据格式类型，默认 JSON。
        :return: POI列表或 None（查询失败）。
        """
        url = f"{self.base_url}/place/text"
        params = {
            "key": self.api_key,
            "keywords": keywords,
            "types": types,
            "city": city,
            "citylimit": "true" if city_limit else "false",
            "page": page,
            "offset": offset,
            "output": output
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data.get("status") == "1":
                return data.get("pois")
            else:
                print(f"POI关键字搜索失败: {data.get('info')}")
                return None
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None

    def poi_around_search(self, location, keywords=None, types=None, radius=1000, page=1, offset=20, output="JSON"):
        """
        调用POI周边搜索 API，根据中心点坐标搜索周边POI点。

        :param location: 中心点坐标，格式为 "经度,纬度"。
        :param keywords: 查询的关键词（可选）。
        :param types: POI分类代码（可选）。
        :param radius: 搜索半径，范围 [0,50000]，单位：米。
        :param page: 当前页数，范围 1-100。
        :param offset: 每页记录数，最大50。
        :param output: 返回数据格式类型，默认 JSON。
        :return: POI列表或 None（查询失败）。
        """
        url = f"{self.base_url}/place/around"
        params = {
            "key": self.api_key,
            "location": location,
            "keywords": keywords,
            "types": types,
            "radius": radius,
            "page": page,
            "offset": offset,
            "output": output
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data.get("status") == "1":
                return data.get("pois")
            else:
                print(f"POI周边搜索失败: {data.get('info')}")
                return None
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None

    def poi_polygon_search(self, polygon, keywords=None, types=None, page=1, offset=20, output="JSON"):
        """
        调用POI多边形搜索 API，根据指定多边形区域搜索POI点。

        :param polygon: 多边形范围，格式为 "经度1,纬度1;经度2,纬度2;经度3,纬度3"。
        :param keywords: 查询的关键词（可选）。
        :param types: POI分类代码（可选）。
        :param page: 当前页数，范围 1-100。
        :param offset: 每页记录数，最大50。
        :param output: 返回数据格式类型，默认 JSON。
        :return: POI列表或 None（查询失败）。
        """
        url = f"{self.base_url}/place/polygon"
        params = {
            "key": self.api_key,
            "polygon": polygon,
            "keywords": keywords,
            "types": types,
            "page": page,
            "offset": offset,
            "output": output
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data.get("status") == "1":
                return data.get("pois")
            else:
                print(f"POI多边形搜索失败: {data.get('info')}")
                return None
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None


