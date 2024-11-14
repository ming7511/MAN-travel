from third_service.kimi_api import multi_turn_chat
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from datetime import datetime
from .models import TripInformation, TripPlan
import re
from third_service.kimi_api import multi_turn_chat
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TripPlan, TripInformation
import json
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from .models import TripInformation, TripPlan
from django.db import models

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def kimi_chat_view(request):
    # 提取请求中的参数
    query_url = request.data.get("url")
    trip_name = request.data.get("trip_name")
    start_date = request.data.get("start_date")
    end_date = request.data.get("end_date")

    # 检查参数是否完整
    if not all([query_url, trip_name, start_date, end_date]):
        return JsonResponse({"error": "参数 url, trip_name, start_date 和 end_date 是必需的"}, status=400)

    # 确保日期格式正确，转换日期字符串
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"error": "日期格式应为 YYYY-MM-DD"}, status=400)

    # 构造 AI 查询
    query = (f"我想去{trip_name}旅游，从{start_date}开始，到{end_date}结束，参考链接中的内容，帮我规划一下行程。"
             f"链接内容：{query_url}")

    # 调用 multi_turn_chat 函数获取 AI 响应
    response, history = multi_turn_chat(query)
    # print(response)

    # 解析 AI 返回的数据
    return parse_and_save_trip_data(response, request.user.id, trip_name, start_date, end_date)


def parse_and_save_trip_data(response, user_id, trip_name, start_date, end_date):
    """
    解析 AI 返回的旅游规划数据，并将相关数据存储到数据库
    """
    # 提取地点和日期
    # 创建 TripInformation 对象
    trip_info = TripInformation.objects.create(
        trip_name=trip_name,
        user_id=user_id,
        start_date=start_date,
        end_date=end_date
    )

    # 提取旅游规划
    itinerary = parse_itinerary(get_tag_content(response, "travel"))
    attractions = parse_attractions(get_tag_content(response, "q"))

    # 保存每日行程内容到 TripPlan
    for day, destinations in itinerary.items():
        for order, destination in enumerate(destinations, start=1):
            # 在 attractions 中查找完整的 key
            full_tag = None
            for key in attractions.keys():
                if destination in key:
                    full_tag = key
                    break

            # 如果找到了对应的标签
            if full_tag:
                description = attractions[full_tag]  # 获取描述
                tag = full_tag.split("’(")[1][:-1]  # 提取标签（例如 '景点'）
            else:
                description = ""  # 如果没有找到，默认为空
                tag = "未知"  # 没有找到标签时，设为 "未知"

            # 保存行程信息到 TripPlan
            TripPlan.objects.create(
                trip_information_id=trip_info.id,  # 使用 trip_information_id 关联到 TripInformation
                days=day,
                trip_description=destination,  # 景点或活动名称
                trip_order=order,  # 顺序
                description=description,  # 景点或活动描述
                tag=tag  # 使用完整的标签
            )

    return JsonResponse({"message": "行程已成功生成并保存"}, status=201)



def extract_tag_from_destination(destination):
    """
    提取目标字符串中的标签，例如 '(景点)', '(美食)' 等
    """
    # 正则表达式匹配类似 '(景点)', '(美食)', '(交通)' 等格式
    match = re.search(r'\((.*?)\)', destination)
    if match:
        return match.group(1)  # 返回括号中的内容作为标签
    return None  # 没有标签时返回 None


def parse_itinerary(itinerary_str):
    """
    解析 <travel> 标签中的行程数据，返回按天分配的旅游内容
    """
    itinerary = {}
    lines = itinerary_str.strip().split("\n")
    current_day = None
    day_index = 1

    for line in lines:
        if "第一天" in line or "第二天" in line or "第三天" in line:  # 标识新的旅游天
            current_day = day_index
            itinerary[current_day] = []
            day_index += 1
        elif line:
            # 解析每天的景点名称
            destination = line.split("：")[1].strip() if "：" in line else line.strip()
            itinerary[current_day].append(destination)

    return itinerary


def parse_attractions(attractions_str):
    """
    解析 <q> 标签中的景点和美食信息，返回一个字典，存储景点名称和对应的描述
    """
    attractions = {}
    lines = attractions_str.strip().split("\n")

    for line in lines:
        if "：" in line:
            place, description = line.split("：")
            place = place.strip()  # 去除前后空格
            description = description.strip() if description else ""
            attractions[place] = description

    return attractions


def get_tag_content(text, tag):
    """
    提取指定标签中的内容
    """
    start = text.find(f"<{tag}>") + len(f"<{tag}>")
    end = text.find(f"</{tag}>")
    return text[start:end].strip()



from third_service.gaodemap_api import AMapClient
from django.shortcuts import get_object_or_404
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_weather_for_trip(request):
    """
    视图函数：根据行程ID获取天气信息并保存
    请求参数:
    - trip_id: TripInformation 的唯一 ID
    """
    trip_id = request.data.get('trip_id')  # 获取行程ID

    if not trip_id:
        return JsonResponse({"error": "缺少必要的参数 trip_id"}, status=400)

    # 获取对应的 TripInformation 对象
    trip_info = get_object_or_404(TripInformation, id=trip_id)

    # 从 TripInformation 中获取 trip_name 作为城市名称
    trip_name = trip_info.trip_name

    # 创建 AMapClient 实例
    amap_client = AMapClient()

    # 获取城市的 adcode（城市编码）
    print(trip_name)
    location_info = amap_client.geocode(trip_name)  # 获取城市的经纬度和城市编码
    print(location_info)
    if not location_info:
        return JsonResponse({"error": "无法获取城市编码"}, status=500)

    longitude, latitude, city_code = location_info  # 提取出 city_code

    # 获取天气信息
    weather_info = amap_client.get_weather_info(city_code)
    if not weather_info:
        return JsonResponse({"error": "无法获取天气信息"}, status=500)

    # 更新 TripInformation 对象并保存天气信息
    trip_info.weather_info = weather_info
    trip_info.save()

    # 返回成功的响应
    return JsonResponse({
        "message": "行程和天气信息更新成功",
        "trip_info": {
            "trip_name": trip_info.trip_name,
            "start_date": trip_info.start_date,
            "end_date": trip_info.end_date,
            "weather_info": trip_info.weather_info
        }
    })





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_photo(request):
    """
    视图函数：根据行程ID和景点描述获取景点的第一张图片
    请求参数:
    - trip_id: TripPlan 的唯一 ID
    """
    trip_id = request.data.get('trip_id')  # 获取行程ID

    if not trip_id:
        return JsonResponse({"error": "缺少必要的参数 trip_id"}, status=400)

    # 获取对应的 TripPlan 对象
    trip_plan = get_object_or_404(TripPlan, id=trip_id)
    trip_description = trip_plan.trip_description

    # 获取相关联的 TripInformation 的 trip_name
    trip_info = get_object_or_404(TripInformation, id=trip_plan.trip_information_id)
    trip_name = trip_info.trip_name

    print(trip_description)
    print(trip_name)

    # 创建 AMapClient 实例
    amap_client = AMapClient()

    # 调用 POI 搜索接口
    poi_data = amap_client.poi_search(keywords=trip_description, city=trip_name)

    # 检查是否有数据返回，并确保 poi_data 是一个字典
    if not poi_data or not isinstance(poi_data, dict) or "pois" not in poi_data:
        return JsonResponse({"error": "未找到相关景点信息"}, status=404)


    # 从返回数据中获取第一个 POI 的 `name` 和第一张 `photo`
    pois = poi_data["pois"]
    if not pois:
        return JsonResponse({"error": "未找到相关景点信息"}, status=404)

    first_poi = pois[0]
    poi_name = first_poi.get("name")
    photos = first_poi.get("photos", [])
    photo_url = photos[0]["url"] if photos else None

    if not photo_url:
        return JsonResponse({"error": "该景点没有可用的图片"}, status=404)

    # 返回景点名称和图片链接
    return JsonResponse({
        "message": "获取景点图片信息成功",
        "photos": {
            "name": poi_name,
            "url": photo_url
        }
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def kimi_chat_view_style(request):
    # 提取请求中的参数
    style = request.data.get("style")
    trip_name = request.data.get("trip_name")
    start_date = request.data.get("start_date")
    end_date = request.data.get("end_date")

    # 检查参数是否完整
    if not all([style, trip_name, start_date, end_date]):
        return JsonResponse({"error": "参数 style, trip_name, start_date 和 end_date 是必需的"}, status=400)

    # 确保日期格式正确，转换日期字符串
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"error": "日期格式应为 YYYY-MM-DD"}, status=400)

    # 构造 AI 查询
    query = (f"我想去{trip_name}旅游，从{start_date}开始，到{end_date}结束，参考链接中的内容，帮我规划一下行程。"
             f"旅游风格：{style}")

    # 调用 multi_turn_chat 函数获取 AI 响应
    response, history = multi_turn_chat(query)
    print(response)

    # 解析 AI 返回的数据
    return parse_and_save_trip_data(response, request.user.id, trip_name, start_date, end_date)



# 视图：创建行程
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from .models import TripInformation

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_trip(request):
    if request.method == 'POST':
        try:
            # 解析请求体中的 JSON 数据
            data = JSONParser().parse(request)

            # 检查数据是否完整
            trip_name = data.get('trip_name')
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            if not trip_name or not start_date or not end_date:
                return JsonResponse({"error": "缺少必要的参数"}, status=400)

            # 验证日期格式（简单验证）
            if start_date > end_date:
                return JsonResponse({"error": "开始日期不能晚于结束日期"}, status=400)

            # 创建行程信息，使用认证用户的 user_id
            trip = TripInformation.objects.create(
                trip_name=trip_name,
                user_id=request.user.id,  # 获取当前用户 ID
                start_date=start_date,
                end_date=end_date
            )

            return JsonResponse({"message": "行程创建成功", "trip_id": trip.id}, status=201)

        except json.JSONDecodeError:
            # 处理 JSON 解码错误
            return JsonResponse({"error": "无效的 JSON 数据"}, status=400)
        except Exception as e:
            # 捕获其他异常
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "仅支持 POST 请求"}, status=405)



# 视图：设置行程天数
@csrf_exempt  # 禁用 CSRF 验证，适用于 POST 请求
def set_trip_days(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            trip_id = data.get('trip_id')
            days = data.get('days')

            if not trip_id or not days:
                return JsonResponse({"error": "缺少必要的参数"}, status=400)

            try:
                trip_info = TripInformation.objects.get(id=trip_id)
            except TripInformation.DoesNotExist:
                return JsonResponse({"error": "行程信息不存在"}, status=404)

            # 创建行程计划（按天数）
            for day in range(1, days + 1):
                TripPlan.objects.create(
                    trip_information=trip_info,
                    days=day,
                    trip_description="待定",
                    trip_order=1,
                    description="待定"
                )

            return JsonResponse({"message": "行程天数设置成功"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "无效的 JSON 数据"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"设置行程天数时出错: {str(e)}"}, status=500)

    return JsonResponse({"error": "仅支持 POST 请求"}, status=405)


# 视图：更新行程日期
@csrf_exempt  # 禁用 CSRF 验证，适用于 PUT 请求
def update_dates(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            trip_id = data.get('trip_id')
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            if not trip_id or not start_date or not end_date:
                return JsonResponse({"error": "缺少必要的参数"}, status=400)

            try:
                trip = TripInformation.objects.get(id=trip_id)
            except TripInformation.DoesNotExist:
                return JsonResponse({"error": "行程信息不存在"}, status=404)

            trip.start_date = start_date
            trip.end_date = end_date
            trip.save()

            return JsonResponse({"message": "行程日期更新成功"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "无效的 JSON 数据"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"更新日期时出错: {str(e)}"}, status=500)

    return JsonResponse({"error": "仅支持 PUT 请求"}, status=405)


# 视图：添加地点/活动
@csrf_exempt  # 禁用 CSRF 验证，适用于 POST 请求
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_place_activity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            trip_information_id = data.get('trip_information_id')
            days = data.get('days')
            trip_destination = data.get('trip_destination')
            description = data.get('description', "")  # 默认值为空字符串

            # 检查是否有缺少的必要参数
            if not trip_information_id or not days or not trip_destination:
                return JsonResponse({"error": "缺少必要的参数"}, status=400)

            # 获取对应的 TripInformation 对象，确保当前用户拥有此行程信息
            try:
                trip_info = TripInformation.objects.get(id=trip_information_id, user_id=request.user.id)
            except TripInformation.DoesNotExist:
                return JsonResponse({"error": "行程信息不存在，或者您无权访问该行程"}, status=403)

            # 检查行程天数是否合法
            total_days = (trip_info.end_date - trip_info.start_date).days + 1
            if days > total_days or days < 1:
                return JsonResponse({"error": "行程的第几天超出了行程的天数范围"}, status=400)

            # 获取该行程和天数下的现有活动，查找最大 trip_order
            existing_activities = TripPlan.objects.filter(trip_information=trip_info, days=days)
            if existing_activities.exists():
                max_order = existing_activities.aggregate(Max('trip_order'))['trip_order__max']
                next_order = max_order + 1
            else:
                next_order = 1

            # 创建新的活动记录
            TripPlan.objects.create(
                trip_information=trip_info,
                days=days,
                trip_destination=trip_destination,
                trip_order=next_order,
                description=description  # 保持空或使用前端传递的描述
            )

            return JsonResponse({"message": "地点/活动添加成功"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "无效的 JSON 数据"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"添加地点/活动时出错: {str(e)}"}, status=500)

    return JsonResponse({"error": "仅支持 POST 请求"}, status=405)



@csrf_exempt
def get_trip_activities(request):
    if request.method == 'GET':
        trip_information_id = request.GET.get('trip_information_id')
        days = request.GET.get('days', None)  # 可选参数

        if not trip_information_id:
            return JsonResponse({"error": "缺少必要的参数 (trip_information_id)"}, status=400)

        try:
            trip_info = TripInformation.objects.get(id=trip_information_id)
        except TripInformation.DoesNotExist:
            return JsonResponse({"error": "行程信息不存在"}, status=404)

        if days:
            activities = TripPlan.objects.filter(trip_information=trip_info, days=days).order_by('trip_order')
        else:
            activities = TripPlan.objects.filter(trip_information=trip_info).order_by('days', 'trip_order')

        activities_data = [
            {
                "id": activity.id,
                "days": activity.days,
                "trip_order": activity.trip_order,
                "trip_destination": activity.trip_destination,
                "description": activity.description
            }
            for activity in activities
        ]

        return JsonResponse({"activities": activities_data}, status=200)

    return JsonResponse({"error": "仅支持 GET 请求"}, status=405)

@csrf_exempt
def update_activity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            activity_id = data.get('activity_id')
            new_trip_order = data.get('trip_order', None)
            new_days = data.get('days', None)
            trip_destination = data.get('trip_destination', None)
            description = data.get('description', None)

            if not activity_id or new_trip_order is None:
                return JsonResponse({"error": "缺少必要的参数 (activity_id 和 trip_order)"}, status=400)

            # 获取目标活动
            try:
                activity = TripPlan.objects.get(id=activity_id)
            except TripPlan.DoesNotExist:
                return JsonResponse({"error": "活动信息不存在"}, status=404)

            old_trip_order = activity.trip_order

            # 检查新旧顺序是否一致，如果一致则无需更新
            if old_trip_order == new_trip_order:
                return JsonResponse({"message": "活动顺序未更改"}, status=200)

            # 获取同一天同一行程的所有活动
            trip_info = activity.trip_information
            day = activity.days

            if new_trip_order > old_trip_order:
                # 如果新顺序大于旧顺序，其他活动往前移动
                TripPlan.objects.filter(
                    trip_information=trip_info,
                    days=day,
                    trip_order__gt=old_trip_order,
                    trip_order__lte=new_trip_order
                ).update(trip_order=models.F('trip_order') - 1)

            elif new_trip_order < old_trip_order:
                # 如果新顺序小于旧顺序，其他活动往后移动
                TripPlan.objects.filter(
                    trip_information=trip_info,
                    days=day,
                    trip_order__gte=new_trip_order,
                    trip_order__lt=old_trip_order
                ).update(trip_order=models.F('trip_order') + 1)

            # 更新目标活动的顺序
            activity.trip_order = new_trip_order

            # 更新其他字段
            if new_days is not None:
                activity.days = new_days
            if trip_destination is not None:
                activity.trip_destination = trip_destination
            if description is not None:
                activity.description = description

            # 保存更新
            activity.save()

            return JsonResponse({"message": "活动更新成功"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "无效的 JSON 数据"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"更新活动时出错: {str(e)}"}, status=500)

    return JsonResponse({"error": "仅支持 POST 请求"}, status=405)



@csrf_exempt
def delete_activity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            activity_id = data.get('activity_id')

            if not activity_id:
                return JsonResponse({"error": "缺少必要的参数 (activity_id)"}, status=400)

            try:
                activity = TripPlan.objects.get(id=activity_id)
                activity.delete()

                # 删除后调整顺序
                remaining_activities = TripPlan.objects.filter(
                    trip_information=activity.trip_information,
                    days=activity.days
                ).order_by('trip_order')

                # 重新调整剩下的活动的顺序
                for index, remaining_activity in enumerate(remaining_activities):
                    remaining_activity.trip_order = index + 1
                    remaining_activity.save()

                return JsonResponse({"message": "活动删除成功"}, status=200)

            except TripPlan.DoesNotExist:
                return JsonResponse({"error": "活动信息不存在"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "无效的 JSON 数据"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"删除活动时出错: {str(e)}"}, status=500)

    return JsonResponse({"error": "仅支持 POST 请求"}, status=405)
