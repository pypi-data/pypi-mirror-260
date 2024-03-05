from abc import ABC, abstractmethod

import pandas as pd

from metastock.modules.com.util.avg import avg
from metastock.modules.com.util.nearest_peak_index import nearest_peak_index
from metastock.modules.core.logging.logger import AppLogger, Logger
from metastock.modules.mbinance.um.trade.strategy.hull import (
    get_hull_from_kline,
    get_hull_status,
)
from metastock.modules.mbinance.um.trade.strategy.wt import get_wt_status_from_kline
from metastock.modules.mbinance.um.value.trade_strategy_type import DecideInfo
from metastock.modules.mbinance.value.common import CommonValue


class StrategyBase(ABC):
    def __init__(
        self, kline: pd.DataFrame, strategy_config, logger: AppLogger = Logger()
    ):
        self._kline = kline
        self._strategy_config = strategy_config
        self._logger = logger

        self.__wt_data = None
        self.__last_peak_wt_index = None
        self.__last_candlestick_status_by_wt = None
        self.__hull_data = None
        self.__hull = None
        self.__diff_wt_area = None
        self.__current_trend_by_wt = None
        self.__min_max_price_wt = None
        self.__ref_price = None

        self.__result: DecideInfo | None = None

    def get_decide(self) -> DecideInfo:
        if self.__result is None:
            self.__result = self.run()

        return self.__result

    def get_kline(self):
        return self._kline.copy(deep=True)

    def _get_wt_data(self):
        if self.__wt_data is None:
            self.__wt_data = get_wt_status_from_kline(self.get_kline())

        return self.__wt_data

    def _get_hull(self):
        if self.__hull is None:
            self.__hull = get_hull_from_kline(self.get_kline())

        return self.__hull.copy(deep=True)

    def get_hull_data(self):
        """
        Trả về thông tin trend, slope, range, đỉnh/đáy, giá trị hiện tại của Hull (đã cached)
        :return:
        """
        if self.__hull_data is None:
            hull = self._get_hull()
            self.__hull_data = get_hull_status(hull)
        return self.__hull_data

    def _get_actual_min_max_price_by_wt(self, uptrend: bool = True) -> list:
        """
        Cần phải hiểu sự khác biệt giữa vị thế mua hay bán

        Nếu là VỊ THẾ MUA

        - Min price: sẽ là giá thấp nhất tính từ thời điểm hiện tại lùi về điểm có diff_wt thấp nhất(là đáy theo WT)
        - Max price: là min price cộng thêm hằng số CL. Mình sẽ không mua quá giá này

        Nếu là VỊ THẾ BÁN

        - MIN price: sẽ là giá CAO nhất tính từ thời điểm hiện tại lùi về điểm có diff_wt CAO nhất( là Là ĐỈNH trước
        đó theo WT)
        - MAX price: Là giá thấp nhất có thể chấp nhận khi tính với hằng số CL. Đối với vị thế
        bán, giá MAX lại thấp hơn giá MIN

        :return:
        """
        if self.__min_max_price_wt is None:
            kline = self.get_kline()
            last_uptrend_prices = kline[kline.index >= self._get_last_peak_wt_index()]
            last_uptrend_prices.sort_index(ascending=False, inplace=True)

            avg_price_last_uptrend = last_uptrend_prices.apply(
                lambda row: avg(row["low"], row["close"], row["high"]),
                axis=1,
            )
            min_price = round(avg_price_last_uptrend.min(), CommonValue.ROUND_DECIMAL)
            base_price = (
                self._strategy_config.get_max_fixed_price()
                if self._strategy_config.get_max_fixed_price() is not None
                else min_price
            )
            if uptrend:
                # Giá lớn nhất có thể mua dựa vào Stop LOSS
                max_price = round(
                    base_price
                    * (100 + self._strategy_config.get_max_adj_price())
                    / 100,
                    CommonValue.ROUND_DECIMAL,
                )
            else:
                max_price = round(
                    base_price
                    * (100 - self._strategy_config.get_max_adj_price())
                    / 100,
                    CommonValue.ROUND_DECIMAL,
                )

            self._min_max_price_by_wt = [min_price, max_price]

        return self._min_max_price_by_wt

    def _get_last_peak_wt_index(self):
        """
        Tra ve dinh hoac day gan nhat theo diff_wt.
        La do thi mau blue (wt1-wt2)
        :return:
        """
        if self.__last_peak_wt_index is None:
            wt_data = self._get_wt_data()
            diff_wt = wt_data[2]

            # đỉnh/đáy gần nhất theo wt
            self.__last_peak_wt_index = nearest_peak_index(diff_wt)

        return self.__last_peak_wt_index

    def _cal_diff_wt_area(self):
        if self.__diff_wt_area is None:
            last_peak_wt_index = self._get_last_peak_wt_index()
            wt_data = self._get_wt_data()
            diff_wt = wt_data[2]

            last_peak_diff_wt = diff_wt[diff_wt.index <= last_peak_wt_index]

            last_peak_diff_wt = last_peak_diff_wt[last_peak_diff_wt < 3]
            near_zero_index = (
                None if len(last_peak_diff_wt) == 0 else last_peak_diff_wt.index[0]
            )
            if near_zero_index is None:
                self.__diff_wt_area = 0

            area_diff_wt = diff_wt[diff_wt.index >= near_zero_index]

            #
            # change_sign = (last_peak_diff_wt * last_peak_diff_wt.shift(-1)) < 0
            #
            # # Lấy index của điểm thay đổi dấu đầu tiên
            # peak_or_valley_index = change_sign.idxmax() if change_sign.any() else None
            # area_diff_wt = diff_wt[diff_wt.index >= peak_or_valley_index]
            #

            if self._get_current_trend_by_wt() == -1:
                self.__diff_wt_area = abs(area_diff_wt[area_diff_wt > 0].sum())
            else:
                self.__diff_wt_area = abs(area_diff_wt[area_diff_wt < -2.5].sum())
        return self.__diff_wt_area

    def _get_current_trend_by_wt(self):
        if self.__current_trend_by_wt is None:
            wt_data = self._get_wt_data()
            diff_wt = wt_data[2]

            # đỉnh/đáy gần nhất theo wt
            last_peak_wt_index = self._get_last_peak_wt_index()

            self.__current_trend_by_wt = (
                -1 if diff_wt[last_peak_wt_index] > diff_wt.iat[0] else 1
            )
        return self.__current_trend_by_wt

    def _check_trend_by_wt(self, is_up_trend: bool = True):
        """
        Kiểm tra trend hiện tại bằng cách xem trước nó gần nhất là đỉnh hay đáy
        Nếu là đỉnh thì sẽ có diff_wt > 0
        Còn nếu là đáy thì sẽ có diff_wt < 0
        :return:
        """
        if is_up_trend and self._get_current_trend_by_wt() == -1:
            # Đây là điều kiện check nhanh. Để là điểm mua thì phải là đáy của diff_wt, do đó giá trị đỉnh/đáy phải < 0
            return DecideInfo(
                open_pos=False, message="Hiện tại đang là down trend", priority=5
            )

        if not is_up_trend and self._get_current_trend_by_wt() == 1:
            return DecideInfo(
                open_pos=False, message="Hiện tại đang là up trend theo wt", priority=5
            )

    def _get_status_last_candlestick_by_wt(self):
        """
        Lấy status theo wt (có cache để không phải tính toán nhiều lần)
        :return:
        """
        if self.__last_candlestick_status_by_wt is None:
            wt_data = self._get_wt_data()
            diff_wt: pd.Series = wt_data[2]

            self.__last_candlestick_status_by_wt = {
                "negative": diff_wt.iat[1] <= 0,
                "positive": diff_wt.iat[1] >= 0,
            }

        return self.__last_candlestick_status_by_wt

    def _is_last_kline_diff_wt_negative(self):
        return (
            self._get_status_last_candlestick_by_wt().get("negative") == True
        )  # so sánh với pd

    def _is_last_kline_diff_wt_positive(self):
        return (
            self._get_status_last_candlestick_by_wt().get("positive") == True
        )  # so sánh với pd

    def _get_ref_price_by_wt(self, uptrend=False):
        """
        Trong khi tính toán hull, wt cần tính giá làm cho hull, wt thoả mãn 1 điều kiện nào đó thì đây chính là giá
        bắt đầu để loop

        :param uptrend: :return:
        """
        if self.__ref_price is None:
            df = self.get_kline()
            actual_min_max_price = self._get_actual_min_max_price_by_wt(uptrend=uptrend)

            # TODO: thay vì lấy giá open để tính toán thì sao không lấy giá min, giá min lúc nào cũng <= giá open,
            #  có thể cho 1 giá vào đẹp hơn
            # self.__ref_price = (
            #     df.at[df.index[0], "open"]
            #     if df.at[df.index[0], "open"] > actual_min_max_price[1]
            #     else actual_min_max_price[0]
            # )
            self.__ref_price = max(actual_min_max_price[0], df.at[df.index[0], "open"])

        return self.__ref_price

    @abstractmethod
    def run(self) -> DecideInfo:
        pass
