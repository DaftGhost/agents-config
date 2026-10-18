class RefundService:
    def __init__(self, repo, gateway, ledger):
        self._repo = repo
        self._gateway = gateway
        self._ledger = ledger

    def process_refund(self, order_id, amount):
        order = self._repo.get(order_id)
        result = self._gateway.refund(
            payment_id=order.payment_id,
            amount=amount,
            customer=order.customer,
        )
        self._ledger.record(order_id, amount, result["refund_id"])
        return result["refund_id"]
