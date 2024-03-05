import pandas as pd

from metastock.modules.mbinance.um.trade.strategy.strategy_base import StrategyBase
from metastock.modules.mbinance.um.trade.strategy.wt import get_wt_status_from_kline
from metastock.modules.mbinance.um.value.trade_strategy_type import DecideInfo
from metastock.modules.mbinance.um.value.um_buy_strategy_value import UMBuyStrategyValue


class MBuyV1Strategy(StrategyBase):
    def __init__(self, kline: pd.DataFrame):
        super().__init__(kline)
        self._kline = kline

    def _cal_price_zero_diff_wt_for_current_candle(self):
        """
        Hàm này đã phải pass điều kiện cây nến trước đó đang âm
        Tính toán cây nến hiện tại làm cho diff wt = 0
        :return:
        """
        wt_data = self._get_wt_data()
        diff_wt: pd.Series = wt_data[2]
        near_zero = 0

        if diff_wt.iat[1] < UMBuyStrategyValue.NEGATIVE_NEAR_ZERO[0]:
            # Đây là điều kiện specific, nếu đang âm quá cao mà cây nến tiếp theo có thể về ~ -1 coi như pass
            near_zero = UMBuyStrategyValue.NEGATIVE_NEAR_ZERO[1]

        def __cal_diff_wt_for_current_candle(kline_df: pd.DataFrame):
            est_wt_data = get_wt_status_from_kline(kline_df)
            est_diff_wt: pd.Series = est_wt_data[2]
            est_diff = est_diff_wt.iat[0]
            return est_diff >= near_zero

        # tính nhanh cho giá max trước, nếu đến giá max còn không thỏa mãn thì sẽ bỏ qua luôn tiết kiệm thời gian
        actual_min_max_price = self._get_actual_min_max_price_by_wt()
        actual_max_price = actual_min_max_price[1]
        df = self.get_kline()
        df.at[df.index[0], "close"] = actual_max_price
        is_max_price_pass = __cal_diff_wt_for_current_candle(df)
        if not is_max_price_pass:
            return None

        # Process để tìm ra price làm cho diff_wt thỏa mãn
        est_zero_price = None
        i = 1
        while est_zero_price is None:
            df = self.get_kline()
            df.at[df.index[0], "close"] = round(
                df.at[df.index[0], "open"] * (100 + 0.001 * i) / 100, 4
            )
            if __cal_diff_wt_for_current_candle(df):
                est_zero_price = df.at[df.index[0], "close"]
            i = i + 1

        return est_zero_price

    def _cal_price_pass_wt1_slope(self):
        """
        Tính toán để làm cho wt1 vượt cây nến trước N đơn vị
        :return:
        """

        def _cal_price_pass_wt1_slope(kline_df: pd.DataFrame):
            est_wt_data = get_wt_status_from_kline(kline_df)
            est_wt1: pd.Series = est_wt_data[0]
            est_diff_wt1 = est_wt1.iat[0] - est_wt1.iat[1]
            return est_diff_wt1 >= UMBuyStrategyValue.BUY_WT1_DIFF

        # tính nhanh cho giá max trước, nếu đến giá max còn không thỏa mãn thì sẽ bỏ qua luôn tiết kiệm thời gian
        actual_min_max_price = self._get_actual_min_max_price_by_wt()
        actual_max_price = actual_min_max_price[1]
        df = self.get_kline()
        df.at[df.index[0], "close"] = actual_max_price
        if not _cal_price_pass_wt1_slope(df):
            return None

        est_wt1_price = None
        i = 1
        while est_wt1_price is None:
            df = self.get_kline()
            df.at[df.index[0], "close"] = round(
                df.at[df.index[0], "open"] * (100 + 0.001 * i) / 100, 4
            )
            if _cal_price_pass_wt1_slope(df):
                est_wt1_price = df.at[df.index[0], "close"]
            i = i + 1

        return est_wt1_price

    def _cal_price_pass_diff_wt_slope(self):
        """
        Làm cho độ dốc của wt_diff đủ lớn, tức là hiệu của 2 wt_diff liền kề vượt qua 1 số N
        :return:
        """

        def __cal_diff_wt_slope(kline_df: pd.DataFrame):
            est_wt_data = get_wt_status_from_kline(kline_df)
            est_wt_diff: pd.Series = est_wt_data[2]
            est_diff_wt = est_wt_diff.iat[0] - est_wt_diff.iat[1]
            return (
                est_diff_wt >= UMBuyStrategyValue.BUY_WT_DIFF[0]
                and est_wt_diff.iat[0] > UMBuyStrategyValue.BUY_WT_DIFF[1]
            )

        # Tính nhanh giá max để có thể thoát điều kiện sớm
        actual_min_max_price = self._get_actual_min_max_price_by_wt()
        actual_max_price = actual_min_max_price[1]
        df = self.get_kline()
        df.at[df.index[0], "close"] = actual_max_price
        if not __cal_diff_wt_slope(df):
            return None

        est_wt_diff_price = None
        i = 1
        while est_wt_diff_price is None:
            df = self.get_kline()
            df.at[df.index[0], "close"] = round(
                df.at[df.index[0], "open"] * (100 + 0.001 * i) / 100, 4
            )
            if __cal_diff_wt_slope(df):
                est_wt_diff_price = df.at[df.index[0], "close"]
            i = i + 1

        return est_wt_diff_price

    def _check_wt(self):
        """
        Điều kiện quan trọng nhất, đang phải là uptrend theo WT
        :return:
        """
        is_pass_check_trend = self._check_trend_by_wt()
        if isinstance(is_pass_check_trend, DecideInfo):
            return is_pass_check_trend

        if self._is_last_kline_diff_wt_negative():
            # _______________________ HAPPY CASE _______________________
            #

            # _______________________ Điều kiện I của WT _______________________
            # Nếu cây nến trước đó chưa chuyển sang dương. Mình cần tính xem cây nến hiện tại với giá nào
            # thì thỏa mãn các điều kiện của WT, tức là nếu giá có thể tăng lên đến đó thì có thể mở vị thế mua
            #
            price_make_diff_wt_positive = (
                self._cal_price_zero_diff_wt_for_current_candle()
            )
            if price_make_diff_wt_positive is None:
                return DecideInfo(
                    open_pos=False,
                    message="Không có giá nào trong phạm vi min/max price cho phép làm diff_wt chuyển sang giá trị dương",
                )
            # _______________________ ################### _______________________

            # _______________________ Điều kiện II của WT _______________________
            # COMBINE
            # _AND, mức giá tại cây nến này làm cho diff_wt vượt được N đơn vị so với cây nến trước đó(~xét hệ số góc)
            price_pass_wt_diff = self._cal_price_pass_diff_wt_slope()
            if price_pass_wt_diff is None:
                return DecideInfo(
                    open_pos=False,
                    message="Không có giá nào trong phạm vi min/max price cho phép làm slope diff_wt thỏa mãn",
                )
            #
            # _AND, mức giá tại cây nến này làm cho wt1 vượt được N đơn vị so với cây nến trước đó(~xét hệ số góc)
            price_pass_wt1_slope = self._cal_price_pass_wt1_slope()
            if price_pass_wt1_slope is None:
                return DecideInfo(
                    open_pos=False,
                    message="Không có giá nào trong phạm vi min/max price cho phép làm slope wt1 thỏa mãn",
                )
            # Combine để tìm ra min price
            combine_min_price = max(
                price_make_diff_wt_positive,
                # TODO: min hay max day??????
                max(price_pass_wt_diff, price_pass_wt1_slope),
            )
            # _______________________ ################### _______________________

            actual_min_max_price = self._get_actual_min_max_price_by_wt()
            if actual_min_max_price[1] < combine_min_price:
                return DecideInfo(
                    open_pos=False,
                    message="Giá làm cho WT thỏa mãn các điều kiện UPTREND lại lớn hơn cả MAX_PRICE cho phép",
                )

            return DecideInfo(
                open_pos=True,
                message="Có thể mở mua theo WT",
                min_open_pos=combine_min_price,
                max_open_pos=actual_min_max_price[1],
            )

        else:
            # TODO: Đây là trường hợp phức tạp hơn
            #
            # Khi diff_wt đã chuyển sang dương nhưng quá yếu, do không thể pass được 1 trong các điều kiện làm cho hệ
            # số góc của wt1 thỏa mãn hoặc làm cho khoảng cách của diff_wt đủ lớn
            #
            return DecideInfo(open_pos=False, message="NOT IMPLEMENTED")

    def run(self):
        # WT
        decided_by_wt = self._check_wt()

        # HULL
        return decided_by_wt
