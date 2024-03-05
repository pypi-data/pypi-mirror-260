import arrow
import pandas as pd
from pandas import DataFrame
from reactivex import combine_latest, interval
from reactivex.subject import BehaviorSubject

from metastock.modules.core.logging.logger import AppLogger
from metastock.modules.core.util.r.handle_error import handle_error
from metastock.modules.core.util.r.schedule_one_thread import (
    schedule_subscribe_one_thread,
)
from metastock.modules.mbinance.exchange.connector.base.api_data_connector_base import (
    ApiDataConnectorBase,
)
from metastock.modules.mbinance.um.api_schema.event.kline_event import (
    KlineEvent,
)
from metastock.modules.mbinance.um.exchange.history.api.get_klines import get_klines
from metastock.modules.mbinance.um.exchange.um_socket_manager import UMSocketManager
from metastock.modules.mbinance.um.util.data.kline_mapping import candlestick_to_kline
from metastock.modules.mbinance.um.value.um_event_type import UMEventType
from metastock.modules.mbinance.um.value.um_value import UMValue
from metastock.modules.mbinance.util.is_testnet import is_testnet
from metastock.modules.mbinance.value.common import TimeInterval
from collections import deque


class UMApiDataConnector(ApiDataConnectorBase):
    KLINE_HISTORY_SIZE = 60

    def __init__(
        self,
        interval: TimeInterval,
        um_socket_manager: UMSocketManager,
        logger: AppLogger,
    ):
        super().__init__(logger)
        self._um_socket_manager = um_socket_manager
        self._interval = interval

        self.__kline: DataFrame | None = None
        """ 
            - KHÔNG SIMULATE
            - Sẽ refresh kline history liên tục để có đủ dữ liệu lịch sử của N nến gần nhất 
            - Có 2 cách để có dữ liệu nến, một là chỉ lấy lần đầu, sau dựa vào dữ liệu realtime để cập nhật những cây nến
            tiếp theo nhưng như thế sẽ phải viết thêm logic phức tạp. 
            - Mình chọn cách là sẽ refresh dữ liệu của N cây nến gần nhất liên tục, thay thế cây nến cuối cùng nếu bằng với
            dữ liệu realtime, hoặc chèn dữ liệu realtime vào nếu nó mới hơn và cách ĐÚNG 1 phút
            - Cần phải check logic chỗ này để đảm bảo dữ liệu luôn chính xác, 
            nếu có sai sót thì có thể chấp nhận việc sai sót bao nhiêu lần? Tối đa là bao nhiêu giây?
        """
        self.__kline_history_ob: BehaviorSubject[pd.DataFrame | None] = BehaviorSubject(
            value=None
        )

        """
            - KHÔNG SIMULATE
            - Dữ liệu Kline từ stream
        """
        self.__kline_stream_ob: BehaviorSubject[pd.DataFrame | None] = BehaviorSubject(
            value=None
        )

        """
            - KHÔNG SIMULATE
            - Là dataframe lưu trữ N KlineData từ stream
        """
        self.__kline_event_history_df: pd.DataFrame | None = None

        self.__kline_event_deque = deque(maxlen=UMApiDataConnector.KLINE_HISTORY_SIZE)
        self.__refresh_kline_subscriber = None
        self.__refresh_api_data_subscriber = None

        self.__initialized = False

    def initialize(self) -> None:
        if self.__initialized:
            return

        self.__config_get_market_data()

        self.__initialized = True

    def __config_get_market_data(self):
        # Publish kline history every 1 second
        symbol = UMValue.SYMBOL()

        def __get_kline_history_from_api(_):
            try:
                current_candlesticks = get_klines(
                    pair=symbol,
                    start_time=int(
                        arrow.now().shift(minutes=-self.KLINE_HISTORY_SIZE).timestamp()
                        * 1000
                    ),
                    time_interval=self._interval,
                )

                sorted_candlesticks = sorted(
                    current_candlesticks.data,
                    key=lambda candlestick: candlestick.open_time,
                    reverse=True,
                )

                # Luôn coi nến cuối cùng  là chưa close
                df_kline_history = pd.DataFrame(
                    [
                        candlestick_to_kline(
                            sorted_candlesticks[0], is_closed=False
                        ).model_dump()
                    ]
                    + [
                        candlestick_to_kline(candlestick, is_closed=True).model_dump()
                        for candlestick in sorted_candlesticks[1:]
                    ]
                )
                df_kline_history.set_index(
                    "open_time", verify_integrity=True, inplace=True
                )
                df_kline_history.sort_index(ascending=False, inplace=True)
                # self._logger.debug("publishing df_kline_history")
                self.__kline_history_ob.on_next(df_kline_history)
            except Exception as e:
                self._logger.exception(e)

        if self.__refresh_kline_subscriber is None:
            self.__refresh_kline_subscriber = (
                interval(2 if self._interval == TimeInterval.ONE_MINUTE.value else 5)
                .pipe(schedule_subscribe_one_thread())
                .subscribe(on_next=__get_kline_history_from_api, on_error=handle_error)
            )
            # trigger first time
            __get_kline_history_from_api(None)

        # Resolve latest api data
        def __resolve_latest_api_data(data):
            self._logger.debug("Resolving latest api data")
            if (
                type(data) is tuple
                and len(data) == 2
                and type(data[0]) is DataFrame
                and type(data[1]) is DataFrame
            ):
                df_kline_data: DataFrame = data[0]
                df_kline_history: DataFrame = data[1]

                if self.__kline is None:
                    self._logger.info("Initializing Kline data from kline histories")
                    self.__kline = df_kline_history

                last_kline_open_time = self.__kline.index.max()

                df_new_kline_records = df_kline_history[
                    df_kline_history.index > last_kline_open_time
                ]
                size_of_new_kline_records = len(df_new_kline_records)

                if size_of_new_kline_records > 0:
                    self._logger.debug(
                        "Number of new kline records: {}".format(
                            size_of_new_kline_records
                        )
                    )

                    # Chỗ này expected là không được chạy vào đây.
                    # Lý do là dữ liệu hiện tại luôn luôn phải update hơn dữ liệu lấy từ history
                    self._logger.info(
                        "Vì dữ liệu từ history còn mới hơn dữ liệu hiện tại, nên lấy nó làm nguồn"
                    )
                    self._logger.debug(df_new_kline_records)
                    self.__kline = df_kline_history

                    return

                df_new_kline_event_records = df_kline_data[
                    df_kline_data.index >= last_kline_open_time
                ]

                size_of_new_kline_event_records = len(df_new_kline_event_records)
                self._logger.debug(
                    "Number of new kline socket event records compare with local: {}".format(
                        size_of_new_kline_event_records
                    )
                )

                if size_of_new_kline_event_records == 1:
                    if (
                        self.__kline.loc[last_kline_open_time]["is_closed"] is False
                        and last_kline_open_time
                        < df_new_kline_event_records.iloc[0]["open_time"]
                    ):
                        """
                        - Case này rất hi hữu nhưng vẫn có thể xảy ra
                        - Trường hợp lấy bằng api ở giây cuối cùng của phút đó, data trả về chưa phải là nến kết thúc,
                        trong khi đó data event lại trả về cây nến mới tiếp theo, => có 2 cây nến chưa kết thúc ở cuối
                        - Sẽ skip đợi lần resolve sau
                        """
                        self.__kline = None
                        self._logger.info(
                            "Skipping resolve api data, wait to next update"
                        )
                        return

                    # Nếu number of trade của event mà còn bé hơn của dữ liệu hiện tại chứng tỏ data event outdate,
                    # lỗi dữ liệu nghiêm trọng
                    if (
                        self.__kline.loc[last_kline_open_time]["number_of_trades"]
                        > df_new_kline_event_records.iloc[0]["number_of_trades"]
                    ):
                        self._logger.info(
                            f"klines {self.__kline.loc[last_kline_open_time]}"
                        )
                        self._logger.info(
                            f"event kline {df_new_kline_event_records.iloc[0]}"
                        )
                        self._logger.warning(
                            "Nếu number_of_trades của event mà còn bé hơn của dữ liệu hiện tại chứng tỏ event out date "
                            "so với local. Lỗi này có thể là do trong 1 thời điểm nào đó, dữ liệu trả về từ api còn "
                            "mới hơn từ socket event. Sẽ theo dõi thêm"
                        )
                        self.__kline = None
                        return
                    elif (
                        self.__kline.loc[last_kline_open_time]["number_of_trades"]
                        < df_new_kline_event_records.iloc[0]["number_of_trades"]
                    ):
                        self.__kline = df_new_kline_event_records.combine_first(
                            self.__kline
                        )
                        need_publish_kline = True
                    else:
                        self._logger.debug(
                            "Skipping publish kline due to no update data"
                        )
                        return
                elif size_of_new_kline_event_records == 2:
                    # Khi kết thúc mỗi phút, sẽ có 2 kline từ event mới hơn dữ liệu hiện tại
                    self._logger.debug(
                        "Expected 2 new kline events as we transition into the next minute."
                    )

                    # self._logger.debug(
                    #     "Current kline data: {}".format(
                    #         self._klines[["is_closed"]]
                    #     )
                    # )
                    #
                    # self._logger.debug(
                    #     "Filling data from event {}".format(
                    #         df_new_kline_event_records[["is_closed"]]
                    #     )
                    # )

                    is_existed_closed_kline_data = (
                        len(
                            df_new_kline_event_records[
                                df_new_kline_event_records["is_closed"] == True
                            ]
                        )
                        == 1
                    )

                    if is_existed_closed_kline_data is False:
                        self._logger.error(
                            "??? Dữ liệu nến phút trước đó PHẢI ở trạng thái đóng. Lỗi này không thực tế nên sẽ clear "
                            "dữ liệu klines để resolve lại"
                        )
                        self.__kline = None
                        return

                    self.__kline = df_new_kline_event_records.combine_first(
                        self.__kline
                    )
                    need_publish_kline = True
                else:
                    if is_testnet() and len(df_new_kline_event_records) == 0:
                        return

                    # Kline data bị outdate quá 2 phút
                    # Nếu là production thì có thể chạy lại bằng cách xóa dữ liệu kline hiện tại và sẽ chạy lại luồng
                    self._logger.error(f"current_klines {self.__kline}")
                    self._logger.error(
                        f"df_new_kline_event_records {df_new_kline_event_records}"
                    )
                    self._logger.error("Kline data out date more than 2 minutes")
                    self.__kline = None
                    return

                if need_publish_kline:
                    self.__kline.sort_index(ascending=False, inplace=True)
                    if len(self.__kline) > self.KLINE_HISTORY_SIZE:
                        self.__kline = self.__kline.head(self.KLINE_HISTORY_SIZE)

                    self._api_market_data_ob.on_next(
                        {
                            "kline_data": {
                                "kline": self.__kline,
                                "kline_event_deque": self.__kline_event_deque,
                                "interval": self._interval,
                            }
                        }
                    )

        if self.__refresh_api_data_subscriber is None:
            self.__refresh_api_data_subscriber = (
                combine_latest(self.__kline_stream_ob, self.__kline_history_ob)
                .pipe(schedule_subscribe_one_thread())
                .subscribe(on_next=__resolve_latest_api_data, on_error=handle_error)
            )

        socket = self._um_socket_manager.get_socket()

        # register handler when receive data from stream
        self._um_socket_manager.register_handler(
            UMEventType.CONTINUOUS_KLINE.value, self.__handle_kline_event_message
        )

        # register stream
        # self.socket.agg_trade(symbol=UMValue.SYMBOL)
        socket.continuous_kline(
            pair=symbol,
            contractType="perpetual",
            interval=self._interval,
        )

    def __handle_kline_event_message(self, message):
        if message.get("e") != UMEventType.CONTINUOUS_KLINE.value:
            return

        try:
            kline_event = KlineEvent(**message)
            self._logger.debug("Received socket kline event: {}".format(kline_event))

            self.__kline_event_deque.append(kline_event.k.model_dump())

            if self.__kline_event_history_df is None:
                self.__kline_event_history_df = pd.DataFrame(
                    [kline_event.k.model_dump()]
                )
                self.__kline_event_history_df.set_index("open_time", inplace=True)

            if kline_event.k.is_closed is True:
                self._logger.debug("Received closed kline")

            df_new_kline = pd.DataFrame([kline_event.k.model_dump()])
            df_new_kline.set_index("open_time", inplace=True)

            self.__kline_event_history_df = df_new_kline.combine_first(
                self.__kline_event_history_df
            )

            if (
                len(self.__kline_event_history_df)
                > UMApiDataConnector.KLINE_HISTORY_SIZE
            ):
                self.__kline_event_history_df.sort_index(ascending=False, inplace=True)
                self.__kline_event_history_df = self.__kline_event_history_df.head(
                    UMApiDataConnector.KLINE_HISTORY_SIZE
                )

            # self._logger.debug("Dispatching kline event history")
            self.__kline_stream_ob.on_next(self.__kline_event_history_df)

        except Exception as e:
            self._logger.exception(e)

    def stop(self):
        self._um_socket_manager.stop()
        if self.__refresh_kline_subscriber is not None:
            self.__refresh_kline_subscriber.dispose()

        if self.__refresh_api_data_subscriber is not None:
            self.__refresh_api_data_subscriber.dispose()
