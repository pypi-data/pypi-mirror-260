class UMBuyStrategyValue:
    TP_PRICE_PERCENT = 0.08
    CL_PRICE_PERCENT = 0.08

    # ___ Điều kiện I của WT ___
    # trường hợp cây nến trước đó đang âm vượt quá giá trị đầu tiên, thì cây nến sau đó không nhất thiết phải về 0 mà
    # chỉ cần về dưới giá trị thứ 2 là được thì coi như pass
    #
    NEGATIVE_NEAR_ZERO = [
        -6,
        -2,
    ]

    # ___ Điều kiện II của WT ___
    #
    # Bắt buộc chênh lệch giữa 2 wt_diff phải lớn hơn phần tử đầu tiên, và giá trị hiện tại của nó phải lớn hơn phần
    # tử thứ 2 tức là tiến về DƯƠNG(UPTREND)
    BUY_WT_DIFF = [3, -2]
    # AND_, hệ số góc của WT1
    BUY_WT1_DIFF = 3  # Mua tai muc gia lam WT1 toi thieu vuot qua gia tri nay
