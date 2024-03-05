import pandas as pd

from metastock.modules.core.util.dict_deep_merge import dict_deep_merge
from metastock.modules.core.util.environment import is_development
from metastock.modules.mbinance.um.trade.strategy.config.sell_strategy_v1_config import (
    SellStrategyV1Config,
)
from metastock.modules.mbinance.um.trade.strategy.hull import (
    get_hull_from_kline,
    get_hull_status,
)
from metastock.modules.mbinance.um.trade.strategy.strategy_base import StrategyBase
from metastock.modules.mbinance.um.trade.strategy.wt import get_wt_status_from_kline
from metastock.modules.mbinance.um.value.trade_strategy_type import DecideInfo
from metastock.modules.mbinance.um.value.trade_strategy_value import TradeStrategyValue
from metastock.modules.mbinance.value.common import CommonValue


class MSellV1Strategy(StrategyBase):
    __STRATEGY_NAME__ = "msell_v1"

    def get_strategy_config(self) -> SellStrategyV1Config:
        """
        Typing cho strategy config
        :return: SellStrategyV1Config
        """
        return self._strategy_config

    # def _cal_price_zero_diff_wt_for_current_candle(self):
    #     """
    #     Hàm này đã phải pass điều kiện cây nến trước đó đang âm
    #     Tính toán cây nến hiện tại làm cho diff wt = 0
    #     :return:
    #     """
    #     if not self._is_last_kline_diff_wt_positive():
    #         raise AppError(
    #             "Hàm này chỉ tính toán cho trường hợp DIFF_WT chưa chuyển sang ÂM mà muốn tiệm cận đến 0"
    #         )
    #
    #     wt_data = self._get_wt_data()
    #     diff_wt: pd.Series = wt_data[2]
    #     near_zero = 0
    #
    #     if diff_wt.iat[1] > UMSellStrategyValue.POSITIVE_NEAR_ZERO[0]:
    #         # Đây là điều kiện specific, nếu đang âm quá cao mà cây nến tiếp theo có thể về ~ -1 coi như pass
    #         near_zero = UMSellStrategyValue.POSITIVE_NEAR_ZERO[1]
    #
    #     def __cal_diff_wt_for_current_candle(kline_df: pd.DataFrame):
    #         est_wt_data = get_wt_status_from_kline(kline_df)
    #         est_diff_wt: pd.Series = est_wt_data[2]
    #         est_diff = est_diff_wt.iat[0]
    #         return est_diff <= near_zero
    #
    #     # tính nhanh cho giá max trước, nếu đến giá max còn không thỏa mãn thì sẽ bỏ qua luôn tiết kiệm thời gian
    #     actual_min_max_price = self._get_actual_min_max_price_by_wt(uptrend=False)
    #     actual_max_price = actual_min_max_price[1]
    #     df = self.get_kline()
    #     df.at[df.index[0], "close"] = actual_max_price
    #     is_max_price_pass = __cal_diff_wt_for_current_candle(df)
    #     if not is_max_price_pass:
    #         return None
    #
    #     # Process để tìm ra price làm cho diff_wt thỏa mãn
    #     est_zero_price = None
    #     i = 1
    #     while est_zero_price is None:
    #         df = self.get_kline()
    #         df.at[df.index[0], "close"] = round(
    #             df.at[df.index[0], "open"] * (100 - 0.001 * i) / 100, 4
    #         )
    #         if __cal_diff_wt_for_current_candle(df):
    #             est_zero_price = df.at[df.index[0], "close"]
    #         i = i + 1
    #
    #     return est_zero_price

    def _cal_price_pass_diff_wt_slope(self):
        """
        Làm cho độ dốc của wt_diff đủ lớn, tức là hiệu của 2 wt_diff liền kề vượt qua 1 số N
        :return:
        """

        def __cal_diff_wt_slope(kline_df: pd.DataFrame):
            est_wt_data = get_wt_status_from_kline(kline_df)
            est_wt_diff: pd.Series = est_wt_data[2]
            est_diff_wt = est_wt_diff.iat[1] - est_wt_diff.iat[0]
            return (
                est_diff_wt >= self.get_strategy_config().get_wt_diff_min()
                and est_wt_diff.iat[0]
                < self.get_strategy_config().get_current_wt_diff_max()
            )

        # Tính nhanh giá max để có thể thoát điều kiện sớm
        actual_min_max_price = self._get_actual_min_max_price_by_wt(uptrend=False)
        actual_max_price = actual_min_max_price[1]
        df = self.__change_current_candlestick_price(actual_max_price)
        if not __cal_diff_wt_slope(df):
            return None

        est_wt_diff_price = None
        i = 1
        while est_wt_diff_price is None:
            ref_price = self._get_ref_price_by_wt(uptrend=False)
            df = self.__change_current_candlestick_price(
                round(
                    ref_price * (100 - 0.001 * i) / 100,
                    CommonValue.ROUND_DECIMAL,
                )
            )

            if i > TradeStrategyValue.MAX_LOOP:
                self._logger.error(
                    f"Loop exceeded {TradeStrategyValue.MAX_LOOP} while calculating '_cal_price_pass_diff_wt_slope' at {df.iloc[0]}"
                )
                break

            if __cal_diff_wt_slope(df):
                est_wt_diff_price = df.at[df.index[0], "close"]
            i = i + 1

        return est_wt_diff_price

    def __change_current_candlestick_price(self, price):
        df = self.get_kline()
        df.at[df.index[0], "close"] = price

        # TODO: có nên change các giá khác hay không? Nếu có thì sẽ nhất quán, nhưng lại bị cứng
        df.at[df.index[0], "high"] = price
        df.at[df.index[0], "low"] = price
        df.at[df.index[0], "open"] = price

        return df

    def _cal_price_pass_wt1_slope(self):
        """
        Tính toán để làm cho wt1 vượt cây nến trước N đơn vị
        :return:
        """

        def _cal_price_pass_wt1_slope(kline_df: pd.DataFrame):
            est_wt_data = get_wt_status_from_kline(kline_df)
            est_wt1: pd.Series = est_wt_data[0]
            est_diff_wt1 = est_wt1.iat[0] - est_wt1.iat[1]
            return est_diff_wt1 <= self.get_strategy_config().get_wt1_diff_min()

        # tính nhanh cho giá max trước, nếu đến giá max còn không thỏa mãn thì sẽ bỏ qua luôn tiết kiệm thời gian
        actual_min_max_price = self._get_actual_min_max_price_by_wt(uptrend=False)
        actual_max_price = actual_min_max_price[1]
        df = self.__change_current_candlestick_price(actual_max_price)
        if not _cal_price_pass_wt1_slope(df):
            return None

        est_wt1_price = None
        i = 1
        while est_wt1_price is None:
            ref_price = self._get_ref_price_by_wt(uptrend=False)
            df = self.__change_current_candlestick_price(
                round(ref_price * (100 - 0.001 * i) / 100, CommonValue.ROUND_DECIMAL)
            )

            if i > TradeStrategyValue.MAX_LOOP:
                self._logger.error(
                    f"Loop exceeded {TradeStrategyValue.MAX_LOOP} while calculating '_cal_price_pass_wt1_slope' at {df.iloc[0]}"
                )
                break

            if _cal_price_pass_wt1_slope(df):
                est_wt1_price = df.at[df.index[0], "close"]
            i = i + 1

        return est_wt1_price

    def _check_wt(self) -> DecideInfo:
        # Check trend đầu tiên để có thể fast return
        check_trend = self._check_trend_by_wt(is_up_trend=False)
        if isinstance(check_trend, DecideInfo):
            return check_trend

        if self._is_last_kline_diff_wt_positive():
            # _______________________ HAPPY CASE _______________________
            #
            # Nếu cây nến trước đó chưa chuyển sang ÂM(chưa chính thức vào DOWN-TREND). Mình cần tính xem cây nến
            # hiện tại với giá nào thì thỏa mãn các điều kiện của WT, tức là nếu giá có thể GIẢM đến đó thì có thể mở
            # vị thế BÁN
            #

            # _______________________ Điều kiện I của WT _______________________
            # Mở vị thế BÁN chỉ khi DIFF_WT chuyển dần đến 0
            # Bắt buộc chênh lệch giữa 2 wt_diff phải lớn hơn phần tử đầu tiên, và giá trị hiện tại của nó phải
            # nhỏ hơn phần tử thứ 2 tức là tiến về ÂM(DOWNTREND)
            self._logger.info("Checking wt condition I")
            price_pass_wt_diff = self._cal_price_pass_diff_wt_slope()
            if price_pass_wt_diff is None:
                return DecideInfo(
                    open_pos=False,
                    message="Không có giá nào trong phạm vi min/max price cho phép làm slope diff_wt thỏa mãn",
                )

            # price_make_diff_wt_negative = (
            #     self._cal_price_zero_diff_wt_for_current_candle()
            # )
            # if price_make_diff_wt_negative is None:
            #     return DecideInfo(
            #         open_pos=False,
            #         message="Không có giá nào trong phạm vi min/max price cho phép làm diff_wt chuyển sang giá trị ÂM "
            #         "(downtrend)",
            #     )

            # _______________________ ################### _______________________
            # diff_wt_area = self._cal_diff_wt_area()
            # if diff_wt_area < 16.1:
            #     return DecideInfo(
            #         open_pos=False,
            #         message="diff_wt_area < 16.1",
            #     )

            # _______________________ Điều kiện II của WT _______________________
            #
            # _AND, mức giá tại cây nến này làm cho wt1 vượt được N đơn vị so với cây nến trước đó(~xét hệ số góc)
            self._logger.info("Checking wt condition II")
            price_pass_wt1_slope = self._cal_price_pass_wt1_slope()
            if price_pass_wt1_slope is None:
                return DecideInfo(
                    open_pos=False,
                    message="Không có giá nào trong phạm vi min/max price cho phép làm slope wt1 thỏa mãn",
                )

            # Combine để tìm ra min price
            combine_min_price = min(price_pass_wt_diff, price_pass_wt1_slope)
            # _______________________ ################### _______________________

            # _______________________
            actual_min_max_price = self._get_actual_min_max_price_by_wt(uptrend=False)
            if actual_min_max_price[1] > combine_min_price:
                return DecideInfo(
                    open_pos=False,
                    message="Giá làm cho WT thỏa mãn các điều kiện DOWNTREND lại nhỏ hơn cả MAX_PRICE cho phép",
                )

            return DecideInfo(
                open_pos=True,
                message="Có thể mở mua theo WT",
                min_open_pos=combine_min_price,
                max_open_pos=actual_min_max_price[1],
            )
        else:
            return DecideInfo(open_pos=False, message="WT NOT IMPLEMENTED")

    def _hull_cal_price_for_near_zero(self):
        """
        Tính giá có thể thỏa mãn điều kiện I của hull tại cây nến hiện tại
        :return:
        """

        def __cal_price_pass_hull_ca(kline_df: pd.DataFrame):
            hull = get_hull_from_kline(kline_df)
            trend, slope, period_range, peak_val, cur_val = get_hull_status(hull)

            return abs(
                cur_val
            ) < self.get_strategy_config().get_current_hull_max_value() or (
                cur_val / (peak_val + 0.0001)
            ) < (
                self.get_strategy_config().get_hull_max_weight() / 100
            )

        actual_min_max_price = self._get_actual_min_max_price_by_wt(uptrend=False)
        actual_max_price = actual_min_max_price[1]
        df = self.__change_current_candlestick_price(actual_max_price)
        if not __cal_price_pass_hull_ca(df):
            return None

            # Process để tìm ra price làm cho diff_wt thỏa mãn
        est_zero_price = None
        i = 1
        while est_zero_price is None:
            ref_price = self._get_ref_price_by_wt(uptrend=False)
            df = self.__change_current_candlestick_price(
                round(ref_price * (100 - 0.001 * i) / 100, CommonValue.ROUND_DECIMAL)
            )

            if i > TradeStrategyValue.MAX_LOOP:
                self._logger.error(
                    f"Loop exceeded {TradeStrategyValue.MAX_LOOP} while calculating '_hull_cal_price_for_near_zero' at {df.iloc[0]}"
                )
                break

            if __cal_price_pass_hull_ca(df):
                est_zero_price = df.at[df.index[0], "close"]
            i = i + 1

        return est_zero_price

    def _hull_cal_price_deep_fail(self):
        """
        Tính giá tối đa theo Hull, tức là tại mức giá đó hull cũng chưa đi xuống quá sâu
        :return:
        """

        def __cal_price_pass_max_hull_ca(price: float):
            (
                trend,
                slope,
                period_range,
                peak_val,
                cur_val,
            ) = self.simulate_hull_status_data_at_price(price)

            return cur_val > self.get_strategy_config().get_hull_max_deep() or (
                cur_val > 0
                or (
                    cur_val < 0
                    and abs(cur_val / peak_val)
                    < (self.get_strategy_config().get_hull_deep_max_weight() / 100)
                )
            )

        # Nếu Max Price có thể thỏa mãn thì trả về luôn max price
        actual_min_max_price = self._get_actual_min_max_price_by_wt(uptrend=False)
        actual_max_price = actual_min_max_price[1]
        if __cal_price_pass_max_hull_ca(actual_max_price):
            return actual_max_price

        # Nếu không thì phải tìm giá max
        est_max_price = None
        i = 1
        while est_max_price is None:
            # actual_max_price là giá đã giảm sâu nhất cho phép rồi
            check_price = round(
                actual_max_price * (100 + 0.001 * i) / 100, CommonValue.ROUND_DECIMAL
            )
            if check_price >= actual_min_max_price[0]:
                break

            if __cal_price_pass_max_hull_ca(check_price):
                est_max_price = check_price
            i = i + 1

        return est_max_price

    def simulate_hull_status_data_at_price(self, price: float):
        """
        Get giá trị của hull tại một giá nào đó

        :param price:
        :return:
        """
        df = self.__change_current_candlestick_price(price)

        hull = get_hull_from_kline(df)
        return get_hull_status(hull)

    def _check_hull(self) -> DecideInfo:
        trend, slope, period_range, peak_val, cur_val = self.get_hull_data()

        if not self.get_strategy_config().is_check_hull():
            return DecideInfo(
                open_pos=True,
                message="Bypass Hull",
                meta={
                    "hull": {
                        "trend": trend,
                        "slope": slope,
                        "period_range": period_range,
                        "peak_val": peak_val,
                        "cur_val": cur_val,
                    }
                },
            )
        # Check trend theo hull để thoát nhanh
        if trend != -1:
            return DecideInfo(
                open_pos=False, message="Không phải là DOWNTREND theo Hull", priority=5
            )

        # chỉ vào lệnh nếu trước đó đỉnh hullma lớn hơn 11
        # if peak_val < 11:
        #     return DecideInfo(
        #         open_pos=False,
        #         message="Chỉ vào lệnh nếu trước đó đỉnh hullma lớn hơn 11",
        #         priority=5,
        #     )

        # _______________________ Điều kiện I của Hull _______________________
        # Giá MIN
        # Phải tiệm cận 0, hoặc vẫn chấp nhận chưa tiệm cận nếu hiện tại chỉ bằng bao nhiêu % so với đỉnh
        self._logger.info("Checking hull condition I")
        price_make_hull_ca_negative = self._hull_cal_price_for_near_zero()
        if price_make_hull_ca_negative is None:
            return DecideInfo(
                open_pos=False,
                message="Không có giá nào trong phạm vi min/max price cho phép làm Hull tiệm cận Zero "
                "(downtrend)",
            )

        # _______________________ Điều kiện 2 của Hull _______________________
        self._logger.info("Checking hull condition II")
        actual_min_max_price = self._get_actual_min_max_price_by_wt(uptrend=False)
        if not self.get_strategy_config().is_check_hull_condition_2():
            actual_max_price = actual_min_max_price[1]
        else:
            # Tính giá MAX theo max hull DEEP
            hull_cal_price_deep_fail = self._hull_cal_price_deep_fail()
            if hull_cal_price_deep_fail is None:
                return DecideInfo(
                    open_pos=False,
                    message="Giá đã giảm quá sâu theo Hull, để an toàn sẽ không vào nữa",
                    code="FAIL_CHECK_DEEP_HULL",
                )
            actual_max_price = max(hull_cal_price_deep_fail, actual_min_max_price[1])

        return DecideInfo(
            open_pos=True,
            message="Pass Hull",
            min_open_pos=price_make_hull_ca_negative,
            max_open_pos=actual_max_price,
        )

    def run(self) -> DecideInfo:
        """
        Tính toán giá có thể mở vị thế tại cây nến hiện tại sử dụng dữ liệu của các cây nến trước đó
        :return:
        """

        # Hull
        decided_by_hull = self._check_hull()
        if not decided_by_hull.open_pos:
            return decided_by_hull

        # WT
        decided_by_wt = self._check_wt()

        # process additional meta for only development:
        if is_development():
            self._logger.info("Build meta sell strategy")
            meta = {}
            if decided_by_wt.open_pos:
                (
                    trend,
                    slope,
                    period_range,
                    peak_val,
                    cur_val,
                ) = self.simulate_hull_status_data_at_price(decided_by_wt.min_open_pos)
                meta["hull"] = {
                    "trend": trend,
                    "slope": slope,
                    "period_range": period_range,
                    "peak_val": peak_val,
                    "cur_val": cur_val,
                }

            # merge meta
            decided_by_wt.meta = dict_deep_merge(decided_by_wt.meta, meta)

        return decided_by_wt
