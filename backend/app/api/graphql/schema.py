import graphene
from ...services import kpi_service

class SalesDaily(graphene.ObjectType):
    date = graphene.String()
    amount = graphene.Int()

class QuoteFunnel(graphene.ObjectType):
    new = graphene.Int()
    sent = graphene.Int()
    won = graphene.Int()

class RepairQueue(graphene.ObjectType):
    pending = graphene.Int()

class Query(graphene.ObjectType):
    sales_daily = graphene.List(SalesDaily, days=graphene.Int())
    quotes_funnel = graphene.Field(QuoteFunnel)
    repairs_queue = graphene.Field(RepairQueue)

    def resolve_sales_daily(self, info, days=7):
        data = kpi_service.get_sales_daily(days)
        return [SalesDaily(**d) for d in data]

    def resolve_quotes_funnel(self, info):
        return QuoteFunnel(**kpi_service.get_quotes_funnel())

    def resolve_repairs_queue(self, info):
        return RepairQueue(**kpi_service.get_repairs_queue())

schema = graphene.Schema(query=Query)
