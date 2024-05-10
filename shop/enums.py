import enum


class OrderStatus(enum.Enum):
    PENDING = '待处理'
    PROCESSING = '处理中'
    SHIPPED = '已发货'
    DELIVERED = '已送达'
    CANCELLED = '已取消'


if __name__ == '__main__':
    for status in OrderStatus:
        print(status)
