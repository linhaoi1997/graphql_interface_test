from Apis.SpareParts.createSparePartOutbound import CreateSparePartOutbound
from Apis.SpareParts.auditSparePartOutbound import AuditSparePartOutbound
from Apis.SpareParts.updateSparePartOutbounds import UpdateSparePartOutbound
from Apis.SpareParts.querySpareOutbound import SparePartOutbound
from Apis.SpareParts.querySpareParts import QuerySpareParts
from Apis.SpareParts.querySparePartStocks import QuerySparePartStocks
from Apis.SpareParts.createSparePartsReceipts import CreateSparePartReceipt
from Apis.Things.thingOverView import ThingOverView

from support import resource


class SparePartOutboundFlow(object):

    def __init__(self, create_stocks_number=100):
        self.report_user = resource.get_user("report_user")
        self.audit_user = resource.get_user("audit_user")
        self.feed_back_user = resource.get_user("feed_back_user")
        self.other_user = resource.get_user("other_user")
        self.create_stocks_number = create_stocks_number

        # 权限测试，三个人员的overview
        self.report_user_overview = ThingOverView(self.report_user)
        self.feed_back_user_overview = ThingOverView(self.feed_back_user)
        self.audit_user_overview = ThingOverView(self.audit_user)
        self.other_user_overview = ThingOverView(self.other_user)
        self.old_report_user_count = self.report_user_overview.sparePartOutboundToFinishedCount
        self.old_feedback_user_count = self.feed_back_user_overview.sparePartOutboundToFinishedCount
        self.old_audit_user_count = self.audit_user_overview.sparePartOutboundToFinishedCount
        self.old_other_user_count = self.other_user_overview.sparePartOutboundToFinishedCount

        # 业务层 创建出库单,及查询出库单的接口
        self.spare_part_list = QuerySpareParts(self.report_user).query_and_return_ids()
        self.create = CreateSparePartOutbound(self.report_user)
        self.create.create_outbound_by_other(self.feed_back_user.id, spare_part_list=self.spare_part_list,
                                             spare_part_num=self.create_stocks_number)
        self.query = SparePartOutbound(self.report_user, self.create.id)

        # 出库单创建后status为待审核
        self.status = self.query.query_and_return_status()
        assert self.status == "PENDING"

        # 初始化审核/反馈接口
        self.audit = AuditSparePartOutbound(self.audit_user, self.create.id)
        self.feed_back = UpdateSparePartOutbound(self.report_user, self.create.id)

        # 入库并初始化库存
        self.create_receipt = CreateSparePartReceipt(self.report_user)
        self.create_receipt.create_receipt(spare_part_list=self.spare_part_list,
                                           spare_part_num=self.create_stocks_number)

        # 记录起始库存
        self.stocks = QuerySparePartStocks(self.report_user).query_and_return_stocks(
            spare_part_list=self.spare_part_list)
