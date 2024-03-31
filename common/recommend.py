from goods.models import Collect
from users.models import User
from .map_reduce import hashmap


def PPR(id):
    # 获取用户信息
    user = User.objects.get(id=id)
    # 获取用户收藏(喜欢)的商品
    goods = Collect.objects.filter(user=user)
    group_list = []
    # 将其喜欢的商品的类型进行统计
    for good in goods:
        group_list.append(good.group)
    result = hashmap(group_list)
    # 按照字典的 value 进行排序
    sorted_dict = sorted(result.items(), key=lambda x: x[1], reverse=True)

    # 取出前三个 key
    top_keys = [item[0] for item in sorted_dict[:3]]

    print(top_keys)
    return top_keys


if __name__ == '__main__':
    id = 1
    PPR(id)
