from ..core.datastructures import ImmutableList
from ..core.datastructures import ImmutableDict
from ..core.constants import UserRole

__all__ = [
    'AftersaleStatus', 'AfterSaleType', 'AftersaleSource', 'AftersaleCancelSource', 'AfsReturnStatus',
    'AftersaleActions', 'AftersaleFinanceStatus', 'AftersaleFinanceType', 'AftersaleRefundStatus',
    'AfterSaleReasons', 'AFTERSALE_USER_REASON_DICT', 'AFTERSALE_USER_REASON_HG_ECARD_DICT', 'AfsSubTicketStatus',
    'OutstorageInterruptedLocation', 'WechatDeliveryReturnOrderStatus', 'WechatDeliveryReturnStatus',
    'Aftersale_Number_Refund_Status', 'AfsLineGenerateFrom', 'AfsVersionConst', 'AftersaleEventConst',
    'AftersaleCanbeRefundedReason', 'AFTERSALE_USER_REASON_DICT_V2', 'AFTERSALE_ENTIRE_REASON_DICT',
    'AFTERSALE_USER_REASON_HG_ECARD_DICT_V2', 'AftersaleRefundRule',
]


class Aftersale_Number_Refund_Status(object):
    # 退单子退款状态(init初始/doing进行中/done已完成)
    INIT = "init"
    DOING = "doing"
    DONE = "done"
    FAILED = "failed"
    AFTERSALE_NUMBER_REFUND_STATUS_CHOICES = (
        (INIT, '初始'),
        (DOING, '进行中'),
        (DONE, "已完成"),
        (FAILED, "失败"),

    )
    AFTERSALE_NUMBER_REFUND_STATUS_DICT = dict(AFTERSALE_NUMBER_REFUND_STATUS_CHOICES)


## WechatDeliveryReturnStatus、WechatDeliveryReturnOrderStatus 对接微信退单功能 ##
class WechatDeliveryReturnStatus:
    """ 用户寄回时的方式 """
    INIT = 0  # 用户未填写退货信息
    APPLY = 1  # 在线预约
    SELF = 2  # 自主填写


class WechatDeliveryReturnOrderStatus:
    """ 退单状态 """
    INIT = 0  # 已下单, 待揽收
    PACKAGED = 1  # 已揽件
    TRANSIT = 2  # 运输中
    DELIVERING = 3  # 派件中
    SELF_SIGNED = 4  # 已签收
    ABNORMAL = 5  # 异常
    PRE_SIGNED = 6  # 代签收
    FAIL_PACKAGED = 7  # 揽件失败
    FAIL_SIGNED = 8  # 签收失败(拒签、超区)
    CANCEL = 11  # 已取消
    RETURNING = 13  # 退件中
    RETURNED = 14  # 已退件
    UNHEARD = 99  # 未知

    # 非终态退单状态
    UNTERMINATE_ORDER_TYPE_LIST = ImmutableList(
        [INIT, PACKAGED, TRANSIT, DELIVERING, RETURNING, UNHEARD]
    )


class AfsLineGenerateFrom:
    SELECT = 'select'  # 创建售后时选中的
    VIRTUAL = 'virtual'  # 虚拟订单数据
    ORIGIN = 'origin'  # 创建售后前的订单(或虚拟订单)数据

    CHOICES = (
        (SELECT, "创建售后时选择的商品"),
        (VIRTUAL, "虚拟订单数据"),
        (ORIGIN, "创建售后前的订单(或虚拟订单)数据"),
    )

    # 非售后要退的行
    NON_AFSLINE = [VIRTUAL, ORIGIN]


class AfsVersionConst:
    V2 = "V2"
    V3 = "V3"

    CHOICES = (
        (V2, 'V2'),
        (V3, 'V3')
    )


class AftersaleActions(object):
    # 创建售后单
    CREATE = "create"
    # 修改售后单
    UPDATE = "update"
    # 关闭售后单
    REMOVE = "remove"
    # 完成售后单
    COMPLETE = "complete"
    # 客服审核通过
    OPERATOR_APPROVE = "operator_approve"
    # 客服审核拒绝- 消费抖店拒绝售后消息
    OPERATOR_REFUSED = "operator_refused"
    # 财务审核通过
    FINANCE_APPROVE_1ST = "finance_approve_1st"
    # 财务审核通过
    FINANCE_APPROVE = "finance_approve"
    # 财务驳回
    FINANCE_REJECT = "finance_reject"
    # 店内系统驳回
    INSTORE_REJECT = "instore_reject"
    # 店内通过
    ALL_APPROVE = "all_approve"
    # 退款失败
    REFUND_FAIL = "refund_fail"
    # 开始退款
    START_REFUND = "start_refund"
    # 退款成功
    REFUND_SUCCEED = "refund_succeed"
    # 待退货
    PENDING_RETURN = "pending_return"
    # 待退款
    PENDING_REFUND = "pending_refund"
    # 直接退款
    REFUND_DIRECTLY = "pending_directly"
    # 自动
    AUTO = "auto"
    # 确认已经退货
    CONFIRM_RETURNED = "confirm_returned"
    # 客户回填运单信息
    CUSTOMER_WRITEBACK_EXPRESS = "customer_writeback_express"
    # 拦截失败
    BLOCK_FAILED = "block_failed"
    # 客服修改运单信息
    CUSSERVICE_MODIFY_EXPRESS = "cusservice_modify_express"
    # 强制确收退货
    FORCE_CONFIRM_RETURNED = "force_confirm_returned"
    # 同步线下-总退单
    SYNC_OFFLINE = "sync_offline"
    # 同步线下-退款
    SYNC_OFFLINE_AFS = "sync_offline_afs"
    # 同步线下-营业外收入
    SYNC_OFFLINE_HGINCOME = "sync_offline_hgincome"
    # 打印退款单
    PRINT_AFTERSALE_SUB = "print"
    # 自动
    AUTO_REFUND = "auto_refund"


class AfterSaleType(object):
    # 正常售后单
    NORMAL = "normal"
    # 换货
    EXCHANGE = "exchange"
    # 投诉
    COMPLAINT = "complaint"
    # 催货
    REMINDER = "reminder"
    # 仅退运费
    ONLY_REFUND_POSTAGE = "only_refund_postage"
    # 其他
    OTHER = "other"
    # 退定金
    REFUND_DEPOIST = "refund_deposit"
    # 退海淘
    REFUND_HAITAO = "refund_haitao"
    # 仅退差价
    ONLY_REFUND = "onlyrefund"

    # 特殊售后单快递转自提退运费
    AFSPLUS_REFUND_POSTAGE = "afsplus_refund_postage"
    # 抖音生活退券售后
    TIKAL = "tikal"

    CHOICES = (
        (NORMAL, "退货退款"),
        (EXCHANGE, "换货"),
        (COMPLAINT, "投诉"),
        (REMINDER, "提醒发货"),
        (ONLY_REFUND_POSTAGE, "仅退运费"),
        (REFUND_DEPOIST, "退定金"),
        (REFUND_HAITAO, "退海淘"),
        (OTHER, "其他"),
        (ONLY_REFUND, "仅退差价"),
        (AFSPLUS_REFUND_POSTAGE, "退运费"),
        (TIKAL, "抖音生活退券"),
    )


class AfterSaleReasons(object):
    """
    用户售后原因

    说明: 本次修改售后原因发现很多不再需要，先注释掉，后续删除 见https://sparrow614.feishu.cn/docx/NWlOdxg0MoXLwJxXKXucu232nWc
    """

    class _issueParty:
        ''' 问题责任方 '''
        BUYER = 'buyer'
        SELLER = 'seller'

        CHOICES = {
            BUYER: '买方',
            SELLER: '卖方',
        }

    class _ifNeedDetail:
        ''' 是否需要手填明细原因 '''
        OPTIONAL = 'optional'  # 选填
        ESSENTIAL = 'essential'  # 必填
        INHIBITORY = 'inhibitory'  # 必须不填的

    class _ifNeedPics:
        ''' 是否需要上传图片 '''
        OPTIONAL = 'optional'  # 选填
        ESSENTIAL = 'essential'  # 必填
        INHIBITORY = 'inhibitory'  # 必须不填的

    class _ifNeedApproveInHg:
        ''' 汉光未发货是否需要人工审核 (该售后单内任一商品) '''
        Y = True
        N = False

    class _ifNeedApproveOutHg:
        ''' 汉光已发货是否需要人工审核 (该售后单内任一商品) '''
        Y = True
        N = False

    # 催单
    REMINDER = "reminder"  # 目前用户售后原因中已经删除了催单相关的原因, 此处暂时保留
    # 退运费
    RETURN_POST = "return_post"
    # 不喜欢/不想要了
    NOT_LIKE_OR_NOT_WANT = "not_like_or_not_want"
    # 快递太慢了不想等了
    SHIPPING_TOO_SLOW_AND_NO_WAIT = "shipping_too_slow_and_no_wait"
    # # 快递太慢，帮我催一下
    # SHIPPING_TOO_SLOW_AND_REMINDER = "shipping_too_slow_reminder"
    # # 换货：质量问题
    # EXCHANGE_PRODUCT_QUALITY_ISSUE = "exchange_product_quality_issue"
    # 退货：质量问题
    RETURN_PRODUCT_QUALITY_ISSUE = "return_product_quality_issue"
    # # 退货：不喜欢，不想要了
    # RETURN_PRODUCT_NOT_LIKE_OR_NOT_WANT = "return_product_not_like_or_not_want"
    # # 退货：穿着不合适需退货
    # RETURN_PRODUCT_INAPPROPRIATE = "return_product_inappropriate"
    # # 换货：大小/款式不合适
    # EXCHANGE_PRODUCT_INAPPROPRIATE = "exchange_inappropriate"
    # 退货：商品与描述不符
    RETURN_PRODUCT_DESCRIPTION_MISMATCH = "return_product_description_mismatch"
    # 其他
    OTHER = "other"
    ##其他前缀，用来做过滤查询
    OTHER_PREFIX = "其他-"
    # ###############
    # # 客人不想要了
    # CUSTOMER_NOT_WANT = "customer_not_want"
    # 商品缺货，不想等了
    PRODUCT_LACK_NO_WAIT = "product_lack_no_wait"
    # # 订单不能按预计时间送达
    # ORDER_CANNOT_SHIPPING_ONTIME = "order_cannot_shipping_ontime"
    # # 操作有误（商品、地址等选错）
    # OPERATE_ERROR = "operate_error"
    # # 重复下单/误下单
    # ORDER_DUPLICATE = "order_duplicate"
    # 其他渠道价格更低
    CHIPPER_ON_OTHER_CHANNEL = "chipper_on_other_channel"
    # # 该商品降价了
    # CHIPPER_NOW = "chipper_now"
    # # 重新下单买（商品/数量拍错了）
    # ORDER_DUPLICATE2 = "order_duplicate2"
    # # 不想买了
    # NOT_WANT_ANYMORE = "not_want_anymore"
    # 用户整单退
    USER_ENTIRE_RETURN = "user_entire_return"
    # 整单退
    ENTIRE_RETURN = "entire_return"
    # 商品发错/少件/破损
    ITEMS_ISSUE = 'items_issue'
    # 尺码不合适  2024.01 新增售后原因
    PRODUCT_INAPPROPRIATE = 'product_inappropriate'

    # E卡原因
    # 买多了/买错了
    BOUGHT_TOO_MUCH = "bought_too_much"
    # 计划有变，暂时不需要了
    PLAN_CHANGED = "plan_changed"
    # 信息填错
    INFORMATION_ERROR = "information_error"
    # 无法绑卡
    CAN_NOT_BIND_CARD = "can_not_bind_card"
    # 发票问题
    INVOICE_ISSUE = "invoice_issue"

    # 取消订单整单退原因
    ENTIRE_CUSTOMER_NOT_WANT = 'entire_not_want'  # 不想买了
    ENTIRE_REORDER = 'entire_reorder'  # 重新下单买（商品/数量拍错了）
    ENTIRE_ADDRESS_ERROR = 'entire_address_error'  # 收货信息选错了（改地址/改收货人/改电话）
    ENTIRE_SHIPPING_TOO_SLOW = 'entire_shipping_too_slow'  # 发货太慢了不想等
    ENTIRE_PRODUCT_LACK = 'entire_product_lack'  # 商品缺货/断货等不起
    ENTIRE_CHIPPER_ON_OTHER = 'entire_chip_on_other' # 别的地方更便宜
    ENTIRE_CHIPPER_PROMOTION = 'entire_chip_promotion'  # 商品有活动降价了
    ENTIRE_OTHER = 'entire_other'  # 其他

    # 用户原因-旧  等C端全部升级后可删除-  本次改了文案
    NOT_LIKE_OR_NOT_WANT_OLD = "not_like_or_not_want_old"
    SHIPPING_TOO_SLOW_AND_NO_WAIT_OLD = 'shipping_too_slow_and_no_wait_old'
    RETURN_PRODUCT_INAPPROPRIATE_OLD = "return_product_inappropriate_old"
    RETURN_PRODUCT_DESCRIPTION_MISMATCH_OLD = "return_product_description_mismatch_old"

    # 说明: 本次修改售后原因发现很多不再需要，先注释掉，后续删除
    CHOICES = {
        # 用户原因-旧  等C端全部升级后可删除-  本次改了文案
        NOT_LIKE_OR_NOT_WANT_OLD: "不喜欢了/不想要了",
        SHIPPING_TOO_SLOW_AND_NO_WAIT_OLD: "快递太慢了不想等了",
        RETURN_PRODUCT_INAPPROPRIATE_OLD: "退货：穿着不合适需退货",
        RETURN_PRODUCT_DESCRIPTION_MISMATCH_OLD: "退货：商品与描述不符",

        REMINDER: "提醒发货",
        RETURN_POST: "退运费",    # 用户第二版原因
        NOT_LIKE_OR_NOT_WANT: "多拍/错拍/不喜欢",  # 用户第二版原因
        SHIPPING_TOO_SLOW_AND_NO_WAIT: "发货太慢不想等了",  # 用户第二版原因
        # SHIPPING_TOO_SLOW_AND_REMINDER: '快递太慢，帮我催一下',
        # EXCHANGE_PRODUCT_INAPPROPRIATE: '换货：大小/款式不合适',
        # EXCHANGE_PRODUCT_QUALITY_ISSUE: '换货：质量问题',
        RETURN_PRODUCT_QUALITY_ISSUE: '退货：质量问题',  # 用户第二版原因
        # RETURN_PRODUCT_INAPPROPRIATE: '退货：穿着不合适需退货',  # 用户第二版原因中删除
        # RETURN_PRODUCT_NOT_LIKE_OR_NOT_WANT: '商品缺货',
        RETURN_PRODUCT_DESCRIPTION_MISMATCH: '规格/效期/效果等描述不符',  # 用户第二版原因
        # CUSTOMER_NOT_WANT: "客人不想要了",
        PRODUCT_LACK_NO_WAIT: "商品缺货",  # 用户第二版原因
        # ORDER_CANNOT_SHIPPING_ONTIME: "订单不能按预计时间送达",
        # OPERATE_ERROR: "操作有误（商品、地址等选错）",
        # ORDER_DUPLICATE: "重复下单/误下单",
        CHIPPER_ON_OTHER_CHANNEL: "商品降价/其他平台更便宜",  # 用户第二版原因
        # CHIPPER_NOW: "该商品降价了",
        # ORDER_DUPLICATE2: "重新下单买（商品/数量拍错了）",
        # NOT_WANT_ANYMORE: "不想买了",
        USER_ENTIRE_RETURN: "用户整单退",  # 当用户取消订单或符合整单退时使用
        ENTIRE_RETURN: "整单退",  # 当B端整单退或者符合整单退时使用
        OTHER: "其他",  # 用户第二版原因
        ITEMS_ISSUE: "商品发错/少件/破损",  # 用户第二版原因  (新增)
        PRODUCT_INAPPROPRIATE: "尺码不合适",

        BOUGHT_TOO_MUCH: "买多了/买错了",  # E卡原因
        PLAN_CHANGED: "计划有变，暂时不需要了",  # E卡原因
        INFORMATION_ERROR: "信息填错",  # E卡原因
        CAN_NOT_BIND_CARD: "无法绑卡",  # E卡原因
        INVOICE_ISSUE: "发票问题",  # E卡原因

        # 整单退原因
        ENTIRE_CUSTOMER_NOT_WANT: "不想买了",
        ENTIRE_REORDER: "重新下单买（商品/数量拍错了）",
        ENTIRE_ADDRESS_ERROR: "收货信息选错了（改地址/改收货人/改电话）",
        ENTIRE_SHIPPING_TOO_SLOW: "发货太慢了不想等",
        ENTIRE_PRODUCT_LACK: "商品缺货/断货等不起",
        ENTIRE_CHIPPER_ON_OTHER: "别的地方更便宜",
        ENTIRE_CHIPPER_PROMOTION: "商品有活动降价了",
        ENTIRE_OTHER: "其他",
    }
    REASON_2_CODE = {
        v: k for k, v in CHOICES.items()
    }

    _IssuePartyMap = {  # 问题方
        NOT_LIKE_OR_NOT_WANT: _issueParty.BUYER,
        SHIPPING_TOO_SLOW_AND_NO_WAIT: _issueParty.BUYER,
        RETURN_PRODUCT_QUALITY_ISSUE: _issueParty.SELLER,
        RETURN_PRODUCT_DESCRIPTION_MISMATCH: _issueParty.SELLER,
        PRODUCT_LACK_NO_WAIT: _issueParty.SELLER,
        CHIPPER_ON_OTHER_CHANNEL: _issueParty.BUYER,
        ITEMS_ISSUE: _issueParty.SELLER,
        PRODUCT_INAPPROPRIATE: _issueParty.BUYER,
    }

    IfNeedDetailMap = {  # 是否需要填写补充原因
        NOT_LIKE_OR_NOT_WANT: _ifNeedDetail.OPTIONAL,
        SHIPPING_TOO_SLOW_AND_NO_WAIT: _ifNeedDetail.OPTIONAL,
        RETURN_PRODUCT_QUALITY_ISSUE: _ifNeedDetail.ESSENTIAL,
        RETURN_PRODUCT_DESCRIPTION_MISMATCH: _ifNeedDetail.ESSENTIAL,
        PRODUCT_LACK_NO_WAIT: _ifNeedDetail.OPTIONAL,
        CHIPPER_ON_OTHER_CHANNEL: _ifNeedDetail.OPTIONAL,
        ITEMS_ISSUE: _ifNeedDetail.ESSENTIAL,
        OTHER: _ifNeedDetail.ESSENTIAL,
        RETURN_POST: _ifNeedDetail.INHIBITORY,
        PRODUCT_INAPPROPRIATE: _ifNeedDetail.OPTIONAL,
    }

    IfNeedPicsMap = {  # 是否需要上传图片
        NOT_LIKE_OR_NOT_WANT: _ifNeedPics.OPTIONAL,
        SHIPPING_TOO_SLOW_AND_NO_WAIT: _ifNeedPics.OPTIONAL,
        RETURN_PRODUCT_QUALITY_ISSUE: _ifNeedPics.ESSENTIAL,
        RETURN_PRODUCT_DESCRIPTION_MISMATCH: _ifNeedPics.ESSENTIAL,
        PRODUCT_LACK_NO_WAIT: _ifNeedPics.OPTIONAL,
        CHIPPER_ON_OTHER_CHANNEL: _ifNeedPics.OPTIONAL,
        ITEMS_ISSUE: _ifNeedPics.ESSENTIAL,
        OTHER: _ifNeedPics.ESSENTIAL,
        RETURN_POST: _ifNeedPics.INHIBITORY,
        PRODUCT_INAPPROPRIATE: _ifNeedPics.OPTIONAL,
    }

    IF_NEED_APPROVE_IN_HG_MAP = {  # 汉光未发货是否需要人工审核 (该售后单内任一商品)
        NOT_LIKE_OR_NOT_WANT: _ifNeedApproveInHg.N,
        SHIPPING_TOO_SLOW_AND_NO_WAIT: _ifNeedApproveInHg.N,
        RETURN_PRODUCT_QUALITY_ISSUE: _ifNeedApproveInHg.N,
        RETURN_PRODUCT_DESCRIPTION_MISMATCH: _ifNeedApproveInHg.N,
        PRODUCT_LACK_NO_WAIT: _ifNeedApproveInHg.N,
        CHIPPER_ON_OTHER_CHANNEL: _ifNeedApproveInHg.N,
        ITEMS_ISSUE: _ifNeedApproveInHg.N,
        OTHER: _ifNeedApproveInHg.Y,
        RETURN_POST: _ifNeedApproveInHg.Y,
        PRODUCT_INAPPROPRIATE: _ifNeedApproveInHg.N,
    }

    IF_NEED_APPROVE_OUT_HG_MAP = {  # 汉光已发货是否需要人工审核 (该售后单内任一商品)
        NOT_LIKE_OR_NOT_WANT: _ifNeedApproveOutHg.N,
        SHIPPING_TOO_SLOW_AND_NO_WAIT: _ifNeedApproveOutHg.N,
        RETURN_PRODUCT_QUALITY_ISSUE: _ifNeedApproveOutHg.N,
        RETURN_PRODUCT_DESCRIPTION_MISMATCH: _ifNeedApproveOutHg.Y,
        PRODUCT_LACK_NO_WAIT: _ifNeedApproveOutHg.N,
        CHIPPER_ON_OTHER_CHANNEL: _ifNeedApproveOutHg.N,
        ITEMS_ISSUE: _ifNeedApproveOutHg.Y,
        OTHER: _ifNeedApproveOutHg.Y,
        RETURN_POST: _ifNeedApproveOutHg.Y,
        PRODUCT_INAPPROPRIATE: _ifNeedApproveOutHg.N,
    }

    _userReasonList = [  # 为了控制顺序
        NOT_LIKE_OR_NOT_WANT,
        SHIPPING_TOO_SLOW_AND_NO_WAIT,
        CHIPPER_ON_OTHER_CHANNEL,
        PRODUCT_INAPPROPRIATE,
        PRODUCT_LACK_NO_WAIT,
        RETURN_PRODUCT_QUALITY_ISSUE,
        RETURN_PRODUCT_DESCRIPTION_MISMATCH,
        ITEMS_ISSUE,
        RETURN_POST,
        OTHER,
    ]

    _ecardReasonList = [
        BOUGHT_TOO_MUCH,
        PLAN_CHANGED,
        INFORMATION_ERROR,
        CAN_NOT_BIND_CARD,
        INVOICE_ISSUE,
    ]

    _entireReasonList = [
        ENTIRE_CUSTOMER_NOT_WANT,
        ENTIRE_REORDER,
        ENTIRE_ADDRESS_ERROR,
        ENTIRE_SHIPPING_TOO_SLOW,
        ENTIRE_PRODUCT_LACK,
        ENTIRE_CHIPPER_ON_OTHER,
        ENTIRE_CHIPPER_PROMOTION,
        ENTIRE_OTHER,
    ]


# 用户售后原因dict
AFTERSALE_USER_REASON_DICT = {item: AfterSaleReasons.CHOICES[item] for item in AfterSaleReasons._userReasonList}
AFTERSALE_USER_REASON_DICT_V2 = [
    {
        'code': code,
        'name': AfterSaleReasons.CHOICES.get(code),
        'if_need_desc': AfterSaleReasons.IfNeedDetailMap.get(code, False),
        'if_need_pic': AfterSaleReasons.IfNeedPicsMap.get(code, False),
    }
    for code in AfterSaleReasons._userReasonList
]
AFTERSALE_ENTIRE_REASON_DICT = [
    {
        'code': code,
        'name': AfterSaleReasons.CHOICES.get(code),
        'if_need_desc': AfterSaleReasons._ifNeedDetail.INHIBITORY,  # 符合整单退时不需要填写原因
        'if_need_pic': AfterSaleReasons._ifNeedPics.INHIBITORY,
    }
    for code in AfterSaleReasons._entireReasonList
]

# E卡售后原因dict
AFTERSALE_USER_REASON_HG_ECARD_DICT = {item: AfterSaleReasons.CHOICES[item] for item in AfterSaleReasons._ecardReasonList}
AFTERSALE_USER_REASON_HG_ECARD_DICT_V2 = [
    {
        'code': code,
        'name': AfterSaleReasons.CHOICES.get(code),
        'if_need_desc': AfterSaleReasons._ifNeedDetail.INHIBITORY,  # E卡不需要填写原因
        'if_need_pic': AfterSaleReasons._ifNeedPics.INHIBITORY,
    }
    for code in AfterSaleReasons._ecardReasonList
]


# 退款单状态
class AftersaleStatus(object):
    # 财务待审
    IN_FINANCE = "in_finance"
    # 财务一审通过，待二审
    IN_FINANCE_2ND = "in_finance_2nd"
    # 财务驳回, 目前这个状态仅在抖店售后在抖店平台拒绝时使用
    REJECTED = "rejected"
    # 店内通过的售后单状态们
    # AFTER_APPROVES = [ALL_APPROVED, REFUND_FAILED, COMPLETED]
    # IN_OPENS = [OPEN, IN_FINANCE, IN_FINANCE_2ND, REJECTED, INSTORE_REJECTED]
    ###### 以上为需求v190611之前的状态，现在不用了,但必须保留做兼容 #########

    # 待审核/审核中
    OPEN = "open"
    # 待退货
    PENDING_RETURN = "pending_return"
    PENDING_RETURN_0 = "pending_return_0"  # For C端， 待客服退货，此状态，在数据库中并不存在
    PENDING_RETURN_1 = "pending_return_1"  # For C端， 待客人退货，此状态，在数据库中并不存在
    PENDING_RETURN_2 = "pending_return_2"  # For C端， 待外仓退货，此状态，在数据库中并不存在
    # 待退款
    PENDING_REFUND = "pending_refund"
    # 店内系统通过
    INSTORE_APPROVED = "instore_approved"
    # 店内系统驳回
    INSTORE_REJECTED = "instore_rejected"
    # 已完成主流程，不涉及退款 —— 这是一个中间状态，退款的时候用来校验
    # 这里店内系统也已经记录了，绝对不能改了。如果退款失败了只能单独和用户沟通或者店内系统也得改
    # 只有是这个状态才能发起退款
    ALL_APPROVED = "all_approved"

    # 退款失败
    REFUND_FAILED = "refund_failed"
    # 已完成
    COMPLETED = "completed"
    # 已取消，已关闭
    CLOSED = "closed"

    # 2022.07 售后单和发货单解耦新增中间状态
    OPENING = 'opening'  # 申请中
    CLOSING = 'closing'  # 关闭中
    COMPLETING = 'completing'  # 完成中
    OPEN_FAILED = 'open_failed'  # 申请售后失败
    CLOSE_FAILED = 'close_failed'  # 关闭售后失败
    COMPLETE_FAILED = 'complete_failed'  # 完成售后失败

    ## 2023.05 货款分离退
    # 未退货已退款
    UNCONFIRM_REFUNDED = 'unconfirm_refunded'

    AFTERSALE_STATUS_CHOICES = (
        (OPEN, "待审核"),
        # (IN_FINANCE, "财务待审"),
        # (IN_FINANCE_2ND, "财务一审通过"),
        (REJECTED, "客服驳回"),
        (PENDING_RETURN, "待退货"),
        (PENDING_REFUND, "待退款"),
        (INSTORE_APPROVED, "店内系统通过"),
        (INSTORE_REJECTED, "店内系统驳回"),
        (ALL_APPROVED, "店内系统通过"),
        (REFUND_FAILED, "退款失败"),
        (COMPLETED, "已完成"),
        (CLOSED, "已取消"),
        (UNCONFIRM_REFUNDED, '未退货已退款'),
    )
    AFTERSALE_STATUS_CHOICES_FOR_C = (
        (OPEN, "待审核"),
        (PENDING_RETURN_0, "待审核"),  # 待客服退货
        (PENDING_RETURN_1, "待退货"),  # 待客人退货
        (PENDING_RETURN_2, "待退货"),  # 发货拦截中
        (PENDING_REFUND, "待退款"),
        (INSTORE_APPROVED, "待退款"),
        (INSTORE_REJECTED, "待退款"),
        (ALL_APPROVED, "待退款"),
        (REFUND_FAILED, "待退款"),
        (COMPLETED, "已完成"),
        (CLOSED, "已关闭"),
        (UNCONFIRM_REFUNDED, "已退款"),
    )
    AFTERSALE_MESSAGE_DICT_FOR_C = {
        # OPEN: ["您的退换货申请已提交，等待客服审核，请保持电话畅通。"],
        OPEN: ["您的售后已申请成功，待售后审核中"],
        # PENDING_RETURN_0: ["您的售后正在审核中，请耐心等待。"],
        PENDING_RETURN_0: ["您的售后审核已通过，待售后中心收退货"],
        # PENDING_RETURN_1: ["您的售后已审核通过，请将售后商品邮寄到指定地址并填写物流单号，查看退货地址"],
        PENDING_RETURN_1: ["您的售后审核已通过，待售后中心收退货"],
        # PENDING_RETURN_2: ["正在为您尝试拦截中，请耐心等待。"],
        PENDING_RETURN_2: ["您的售后审核已通过，待售后中心收退货"],
        # PENDING_REFUND: ["客服正在为您处理退款。"],
        PENDING_REFUND: ["您的售后待客服处理退款"],
        # INSTORE_APPROVED: ["客服正在为您处理退款。"],
        INSTORE_APPROVED: ["您的售后待客服处理退款"],
        # INSTORE_REJECTED: ["客服正在为您处理退款。"],
        INSTORE_REJECTED: ["您的售后待客服处理退款"],
        # ALL_APPROVED: ["客服正在为您处理退款。"],
        ALL_APPROVED: ["您的售后待客服处理退款"],
        # REFUND_FAILED: ["客服正在为您处理退款。"],
        REFUND_FAILED: ["您的售后待客服处理退款"],
        # COMPLETED: ["售后已完成，退款金额将原路返回到您的账户，预计最晚到账1-7个工作日，请您注意查收。"],
        COMPLETED: ["售后服务已完成，感谢您对汉光的支持"],
        CLOSED: ["售后已关闭。"],
        UNCONFIRM_REFUNDED: ["售后服务已完成退款，感谢您对汉光的支持"],
    }


class AftersaleFinanceStatus(object):
    # 未审核
    INIT = "init"
    # 一审通过
    APPROVED_1ST = "approved_1st"
    # 二审通过
    APPROVED = "approved"
    # 财务驳回
    REJECTED = "rejected"


class AftersaleFinanceType(object):
    '''一期有一些需要财务手动调账的'''
    # 普普通通的售后单
    AUTO = "auto"
    # 需要财务手动调账的售后单，微信不能自动退款
    MANUAL = "manual"


# 申请售后来源：客人、客服
class AftersaleSource(object):
    """
    售后来源
    """
    # 客人发起
    GUEST_INITIATED = "guest_initiated"
    # 客服发起
    SERVICE_INITIATED = "service_initiated"


class AftersaleCancelSource(object):
    """
    售后取消来源
    """
    # 客人取消
    GUEST_CANCEL = "guest_cancel"
    # 客服取消
    SERVICE_CANCEL = "service_cancel"
    # 高级客服取消
    SUPER_SERVICE_CANCEL = "super_service_cancel"
    # 超时自动取消
    TIMEOUT_CANCEL = "timeout_cancel"


class AftersaleRefundStatus(object):
    # 未退款，初始状态
    INIT = "init"
    # 退款成功
    SUCCEEDED = "succeeded"
    # 退款失败
    FAILED = "failed"


class AfsSubTicketStatus(object):
    """ 发货单小票状态 """
    VALID = 'valid'
    """ 有效 """
    INVALID = 'invalid'
    """ 无效 """

    CHOICES = (
        (VALID, '有效'),
        (INVALID, '无效'),
    )


class OutstorageInterruptedLocation:
    ''' 外仓售后申请售后时发货单位置 '''

    PACKAGED = "packaged"
    UNPACKAGED = "unpackaged"

    CHOICES = {
        PACKAGED: "已发货",
        UNPACKAGED: "未发货",
    }


## 退款单 Event 相关: EventMapKey、AftersaleEventConst ##
class EventMapKey(object):
    TO_STATUS_KEY = "to_status"
    USER_ROLES_KEY = "user_roles"


class AftersaleEventConst:
    # 重新退款
    REFUND = 'refund'
    # 提交售后
    COMMIT = 'commit'
    # 强制提交售后
    FORCELY_COMMIT = 'forcelyCommit'
    # 保存
    SAVE = 'save'
    # 关闭售后
    CLOSE = 'close'
    # 关闭售后并重置退货
    CLOSE_FORCELY = 'closeForcely'
    # 确认退款
    CONFIRM_REFUND = 'confirmRefund'
    # 强制导购已确收，发起退款
    CONFIRM_AND_START_REFUND_FORCELY = 'confirmAndStartRefundForcely'
    # 强制确认退款
    CONFIRM_REFUND_FORCELY = 'confirmRefundForcely'
    # 抖店售后确认退款
    TIKTOK_CONFIRM_REFUND = 'tiktok_confirm_refund'
    # 抖店售后提交售后, 当抖店平台拒绝售后导致两边不匹配时, 麻雀系统可以使用该按钮执行下一步
    TIKTOK_COMMIT_AGAIN = 'tiktok_commit_again'
    # 抖店换货类型的售后关闭
    TIKTOK_EXCHANGE_CLOSE = 'tiktok_exchange_close'
    # 小红书保存备注
    XHSHU_SAVE = 'xhshu_save'

    ## 2023.05 货款分离退一期：退款单状态机
    # 创建换货单
    NEW_ADD = "new_add"
    # 退款单可退款
    AFTERSALE_CAN_REFUND = 'aftersale_can_refund'
    # 同步线下成功
    SYNC_OFFLINE_SUCCESS = 'sync_offline_success'
    # 同步线下失败
    SYNC_OFFLINE_FAILED = 'sync_offline_failed'
    # 退款失败
    REFUND_FAILED = 'refund_failed'
    # 完成退款单
    AFTERSALE_COMPLETE = 'aftersale_complete'
    # 未退货已退款
    UNCONFIRM_REFUNDED = 'unconfirm_refunded'
    # 审核通过
    APPROVE = 'approve'
    # 关闭售后再新建
    CLOSE_AND_READD = 'close_and_readd'
    # 强制先退款再退货
    FORCELY_REFUND_FIRST = 'forcely_refund_first'

    EVENT_TO_BUTTONNAME_MAP = {
        REFUND: "重新退款",
        COMMIT: "提交售后",
        FORCELY_COMMIT: "强制提交售后",
        SAVE: "保存",
        CLOSE: "关闭售后",
        CLOSE_FORCELY: "关闭售后并重置退货",
        CONFIRM_AND_START_REFUND_FORCELY: "强制导购已确收，发起退款",
        CONFIRM_REFUND: "确认退款",
        CONFIRM_REFUND_FORCELY: "强制确认退款",
        TIKTOK_CONFIRM_REFUND: "抖店售后确认退款",
        TIKTOK_COMMIT_AGAIN: "抖店重新提交售后",
        TIKTOK_EXCHANGE_CLOSE: "关闭抖店换货",
        XHSHU_SAVE: "小红书保存备注",

        ## 2023.05 货款分离退一期
        NEW_ADD: "创建退款单",
        SYNC_OFFLINE_SUCCESS: "同步线下成功",
        SYNC_OFFLINE_FAILED: "同步线下失败",
        AFTERSALE_CAN_REFUND: "退款单可退款",
        REFUND_FAILED: "退款失败",
        AFTERSALE_COMPLETE: "完成退款单",
        UNCONFIRM_REFUNDED: "未退货已退款",
        APPROVE: "审核通过",
        CLOSE_AND_READD: "关闭售后再新建",
        FORCELY_REFUND_FIRST: "强制先退款再退货",

    }
    # 这些按钮，在E卡售后单中不显示
    ECARD_NOT_DISPLAY_LIST = [CONFIRM_REFUND_FORCELY, CONFIRM_AND_START_REFUND_FORCELY, CLOSE_FORCELY, COMMIT,
                              FORCELY_COMMIT, TIKTOK_CONFIRM_REFUND]
    # 这些按钮, 可以在抖店售后中展示
    TIKTOK_DISPLAY_LIST = [TIKTOK_CONFIRM_REFUND, TIKTOK_COMMIT_AGAIN]

    EVENT_TO_OPERATION_VO_MAP = {
        REFUND: {'name': "重新退款", 'code': REFUND, 'doubleConfirm': True, 'type': 'danger'},
        COMMIT: {'name': "提交售后", 'code': COMMIT, 'doubleConfirm': True, 'type': 'danger'},
        FORCELY_COMMIT: {'name': "强制提交售后", 'code': FORCELY_COMMIT, 'doubleConfirm': True, 'type': 'danger'},
        SAVE: {'name': "保存", 'code': SAVE, 'doubleConfirm': False, 'type': None},
        CLOSE: {'name': "关闭售后", 'code': CLOSE, 'doubleConfirm': True, 'type': 'danger'},
        CLOSE_FORCELY: {'name': "关闭售后并重置退货", 'code': CLOSE_FORCELY, 'doubleConfirm': True, 'type': 'danger'},
        CONFIRM_AND_START_REFUND_FORCELY: {'name': "强制导购已确收，发起退款", 'code': CONFIRM_AND_START_REFUND_FORCELY, 'doubleConfirm': True, 'type': 'danger'},
        CONFIRM_REFUND: {'name': "确认退款", 'code': CONFIRM_REFUND, 'doubleConfirm': True, 'type': 'danger'},
        CONFIRM_REFUND_FORCELY: {'name': "强制确认退款", 'code': CONFIRM_REFUND_FORCELY, 'doubleConfirm': True, 'type': 'danger'},
        FORCELY_REFUND_FIRST: {'name': "强制先退款再退货", 'code': FORCELY_REFUND_FIRST, 'doubleConfirm': True, 'type': 'danger'},
        TIKTOK_CONFIRM_REFUND: {'name': "抖店售后确认退款", 'code': TIKTOK_CONFIRM_REFUND, 'doubleConfirm': True, 'type': 'danger'},
        TIKTOK_COMMIT_AGAIN: {'name': "抖店重新提交售后", 'code': TIKTOK_COMMIT_AGAIN, 'doubleConfirm': True, 'type': 'danger'},
        TIKTOK_EXCHANGE_CLOSE: {'name': "关闭抖店换货", 'code': TIKTOK_EXCHANGE_CLOSE, 'doubleConfirm': True, 'type': 'danger'},
        CLOSE_AND_READD: {'name': "关闭售后再新建", 'code': CLOSE_AND_READD, 'doubleConfirm': False, 'type': 'danger'},
        XHSHU_SAVE: {'name': "小红书保存备注", 'code': XHSHU_SAVE, 'doubleConfirm': False, 'type': 'danger'},
    }

    AftersaleStatus_2_Event_map = {
        AftersaleStatus.REFUND_FAILED: [REFUND],
        AftersaleStatus.OPEN: [COMMIT, SAVE, CLOSE, FORCELY_COMMIT, CLOSE_FORCELY],
        AftersaleStatus.PENDING_RETURN: [SAVE, CLOSE, CONFIRM_AND_START_REFUND_FORCELY, CLOSE_FORCELY, FORCELY_REFUND_FIRST],
        AftersaleStatus.PENDING_REFUND: [CONFIRM_REFUND, SAVE, CLOSE, CONFIRM_REFUND_FORCELY, CLOSE_FORCELY],
        AftersaleStatus.INSTORE_REJECTED: [COMMIT, SAVE, CLOSE, FORCELY_COMMIT, CLOSE_FORCELY],
        # 已同步线下，不能关闭
        AftersaleStatus.ALL_APPROVED: [],
        # 店内系统通过，不能关闭
        AftersaleStatus.INSTORE_APPROVED: [],
        AftersaleStatus.COMPLETED: [],
        AftersaleStatus.REJECTED: [TIKTOK_COMMIT_AGAIN],
    }

    FROM_TO_MAP = {
        NEW_ADD: {  # 创建换货单
            AftersaleStatus.OPEN: {
                EventMapKey.TO_STATUS_KEY: None,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSTOMER, UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE, UserRole.AUTO, UserRole.GUIDE]
            }
        },
        APPROVE: {
            AftersaleStatus.OPEN: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.PENDING_RETURN,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE, UserRole.AUTO, UserRole.SUPER_CUSSERVICE]
            },
            AftersaleStatus.REJECTED: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.PENDING_RETURN,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE]
            },
        },
        CLOSE: {  # 关闭售后
            AftersaleStatus.OPEN: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSTOMER, UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE, UserRole.AUTO]
            },
            AftersaleStatus.PENDING_RETURN: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSTOMER, UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE, UserRole.AUTO]
            },
            AftersaleStatus.CLOSING: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE, UserRole.AUTO]
            },
            AftersaleStatus.INSTORE_REJECTED: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE, UserRole.AUTO]
            },
            AftersaleStatus.PENDING_REFUND: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE, UserRole.AUTO]
            },
            AftersaleStatus.REJECTED: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE, UserRole.AUTO]
            },
        },
        CLOSE_FORCELY: {  # 强制关闭售后
            AftersaleStatus.OPEN: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [UserRole.SUPER_CUSSERVICE]
            },
            AftersaleStatus.PENDING_RETURN: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [UserRole.SUPER_CUSSERVICE]
            },
            AftersaleStatus.PENDING_REFUND: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [UserRole.SUPER_CUSSERVICE]
            },
            AftersaleStatus.CLOSING: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [UserRole.SUPER_CUSSERVICE, UserRole.AUTO]
            },
            AftersaleStatus.INSTORE_REJECTED: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.CLOSED,
                EventMapKey.USER_ROLES_KEY: [UserRole.SUPER_CUSSERVICE]
            },
        },
        AFTERSALE_CAN_REFUND: {
            AftersaleStatus.OPEN: {  # 直接到待退款(包含可整单退、可极速退、仅退差价、退运费
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.PENDING_REFUND,
                EventMapKey.USER_ROLES_KEY: [UserRole.AUTO, UserRole.CUSSERVICE, UserRole.CUSTOMER,
                                             UserRole.SUPER_CUSSERVICE, UserRole.GUIDE],
            },
            AftersaleStatus.PENDING_RETURN: {  # 导购确退所有商品或客服确收所有商品且可极速退款
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.PENDING_REFUND,
                EventMapKey.USER_ROLES_KEY: [UserRole.AUTO, UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE],
            }
        },
        SYNC_OFFLINE_SUCCESS: {  # 同步线下成功
            AftersaleStatus.PENDING_REFUND: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.INSTORE_APPROVED,
                EventMapKey.USER_ROLES_KEY: [UserRole.AUTO, UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE],
            },
            AftersaleStatus.INSTORE_REJECTED: {  # 同步失败后再次尝试同步线下
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.INSTORE_APPROVED,
                EventMapKey.USER_ROLES_KEY: [UserRole.AUTO, UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE],
            },
        },
        SYNC_OFFLINE_FAILED: {  # 同步线下成功
            AftersaleStatus.PENDING_REFUND: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.INSTORE_REJECTED,
                EventMapKey.USER_ROLES_KEY: [UserRole.AUTO, UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE],
            },
            AftersaleStatus.INSTORE_REJECTED: {  # 同步失败后再次尝试同步线下
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.INSTORE_REJECTED,
                EventMapKey.USER_ROLES_KEY: [UserRole.AUTO, UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE],
            }
        },
        REFUND_FAILED: {
            # 退款失败
            AftersaleStatus.INSTORE_APPROVED: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.REFUND_FAILED,
                EventMapKey.USER_ROLES_KEY: [UserRole.AUTO, UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE],
            }
        },
        AFTERSALE_COMPLETE: {
            AftersaleStatus.INSTORE_APPROVED: {  # 退款成功且不需退货或已退货
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.COMPLETED,
                EventMapKey.USER_ROLES_KEY: [UserRole.AUTO, UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE],
            },
            AftersaleStatus.UNCONFIRM_REFUNDED: {
                # 未确退已退款的情况
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.COMPLETED,
                EventMapKey.USER_ROLES_KEY: [UserRole.AUTO, UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE],
            },
            AftersaleStatus.REFUND_FAILED: {  # 退款失败重新退款的情况
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.COMPLETED,
                EventMapKey.USER_ROLES_KEY: [UserRole.AUTO, UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE],
            },
        },
        UNCONFIRM_REFUNDED: {
            AftersaleStatus.INSTORE_APPROVED: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.UNCONFIRM_REFUNDED,
                EventMapKey.USER_ROLES_KEY: [UserRole.AUTO, UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE]
            },
            AftersaleStatus.REFUND_FAILED: {  # 退款失败重新退款的情况
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.UNCONFIRM_REFUNDED,
                EventMapKey.USER_ROLES_KEY: [UserRole.AUTO, UserRole.CUSSERVICE, UserRole.SUPER_CUSSERVICE],
            }
        },
        FORCELY_REFUND_FIRST: {
            AftersaleStatus.PENDING_RETURN: {
                EventMapKey.TO_STATUS_KEY: AftersaleStatus.UNCONFIRM_REFUNDED,
                EventMapKey.USER_ROLES_KEY: {UserRole.SUPER_CUSSERVICE},
            }
        },
    }


class AfsNoteEventSource:
    ''' 是哪个数据的 日志 '''
    Afs = "afs"
    Afsline = "afsline"


## 执行实际退款的事件 ##
class AfsNumberRefundEventConst(object):
    ### 子退单事件 ###
    # 子退单开始申请退
    START = "start"
    # 子退单完成
    SUCCESS = "success"
    # 子退单失败
    FAIL = "fail"

    EVENT_2_BUTTONNAME_MAP = {
        START: "子退单开始申请退",
        SUCCESS: "子退单完成",
        FAIL: "子退单失败"
    }

    FROM_TO_MAP = {
        START: {  # 子退单开始申请退
            Aftersale_Number_Refund_Status.INIT: {
                EventMapKey.TO_STATUS_KEY: Aftersale_Number_Refund_Status.DOING,
                EventMapKey.USER_ROLES_KEY: None
            }
        },
        SUCCESS: {  # 子退单完成
            Aftersale_Number_Refund_Status.DOING: {
                EventMapKey.TO_STATUS_KEY: Aftersale_Number_Refund_Status.DONE,
                EventMapKey.USER_ROLES_KEY: None
            },
            Aftersale_Number_Refund_Status.FAILED: {
                EventMapKey.TO_STATUS_KEY: Aftersale_Number_Refund_Status.DONE,
                EventMapKey.USER_ROLES_KEY: None
            },
        },
        FAIL: {  # 子退单失败
            Aftersale_Number_Refund_Status.DOING: {
                EventMapKey.TO_STATUS_KEY: Aftersale_Number_Refund_Status.FAILED,
                EventMapKey.USER_ROLES_KEY: None
            },
            Aftersale_Number_Refund_Status.FAILED: {
                EventMapKey.TO_STATUS_KEY: Aftersale_Number_Refund_Status.FAILED,
                EventMapKey.USER_ROLES_KEY: None
            }
        }
    }


class AfsReturnStatus:
    ''' 退款单货物寄回状态 '''
    NONE = 'none'
    DOING = 'doing'
    DONE = 'done'

    CHOICES = (
        ('none', '无需退货'),
        ('done', '已经完成'),
        ('doing', '正在退货'),
    )


class AftersaleCanbeRefundedReason:
    ''' 退款单可退款的原因 '''
    ENTIRE_ORDER = "整单退"
    ONLY_REFUND = "仅退差价"
    ONLY_REFUND_POSTAGE = "退运费"
    AFSPLUS_REFUND_POSTAGE = "特需售后退运费"
    CONFIRM_ALL_ITEMS = "已确退所有商品"
    NO_ASSIGN = "全部未配货, 可退款"
    CAN_REFUND_IMMEDIATELY = "可极速退款"


class AftersaleRefundRule:
    ''' 退款单执行退款的规则 '''
    NORMAL = 'normal'  # 常规的, 包括 未出专柜退款完成; 出专柜后导购确收退货退款完成
    AUTO = 'auto'  # 客服已提时, 执行了极速退款
    MANNAL = 'mannal'  # 已出汉光的, 客服手动执行退款

    CHOICES = ImmutableDict(
        (
            (NORMAL, "常规的"),
            (AUTO, "未出汉光极速退款"),
            (MANNAL, "客服强制极速退款"),
        )
    )

