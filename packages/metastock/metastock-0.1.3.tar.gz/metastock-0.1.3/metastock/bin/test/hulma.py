import matplotlib.pyplot as plt

from metastock.bin.test.get_history_data import get_history_data
from metastock.modules.com.technical_indicator.hullma import Hullma
from metastock.modules.trade.util.predict_trend_change import predict_trend_change_v1


def calculate_hullma(n: int = 80):
    history_data = get_history_data(symbol='VHC')

    hullma = Hullma(history=history_data, symbol='VHC')
    hulma_data = hullma.get_data().head(n)

    return hulma_data


def plot_hullma_diff():
    hulma_data = calculate_hullma()
    hulma_data_rer = hulma_data.iloc[::-1]
    # Tính diff()
    s_diff = hulma_data_rer.diff()
    s_diff = s_diff.iloc[::-1]
    plt.subplot(1, 2, 2)
    plt.title('Stock Price Difference')
    plt.plot(s_diff.index, s_diff.values, marker='o', color='r')
    plt.xlabel('Date')
    plt.ylabel('Price Difference')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.gca().set_xticks(s_diff.index)  # Đặt tất cả các nhãn ngày

    plt.tight_layout()
    plt.show()


def predict_trend():
    hulma_data = calculate_hullma()
    predict = predict_trend_change_v1(hulma_data)

    return predict


plot_hullma_diff()
