class BrokerAdapter:
    """Interface placeholder. No credentials or live order methods are implemented."""
    def connect(self):
        raise NotImplementedError("Select and configure an officially supported broker integration.")

    def submit_order(self, order):
        raise RuntimeError("Live broker execution is disabled. Use the paper-order endpoint.")
