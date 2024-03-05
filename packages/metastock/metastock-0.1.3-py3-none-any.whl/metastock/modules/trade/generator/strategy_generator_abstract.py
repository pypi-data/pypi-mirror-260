from abc import abstractmethod

import arrow


class StrategyGeneratorAbstract:
    @abstractmethod
    def generate(self):
        pass

    def _get_range_data(self, range_config: dict):
        if range_config["type"] == "relative":
            return self._get_range_data_relative(range_config)

        if range_config["type"] == "absolute":
            return range_config["from"], range_config["to"]

    def _get_range_data_relative(self, range_config: dict):
        from_date = None
        to_date = arrow.now().format("YYYY-MM-DD")  # Mặc định là ngày hiện tại

        from_config = range_config["from"]
        if (
            "modify" in from_config
            and "amount" in from_config
            and "amount_type" in from_config
        ):
            if from_config["modify"] == "shift":
                amount = int(from_config["amount"])
                amount_type = from_config["amount_type"]
                from_date = (
                    arrow.now().shift(**{amount_type: -amount}).format("YYYY-MM-DD")
                )

        to_config = range_config["to"]
        if to_config:
            # Xử lý "to_date" nếu cung cấp
            pass

        return from_date, to_date
