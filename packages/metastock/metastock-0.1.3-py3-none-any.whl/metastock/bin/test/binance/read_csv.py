import os

import pandas as pd


def read_result(file: str):
    current_directory = os.getcwd()
    results_folder_path = os.path.join(current_directory, "test_results")
    df = pd.read_csv(f"{results_folder_path}/{file}")
    a = 1


#
#
# # ____________________________________________________________________________________________________
# read_result("2024-02-14_2024-02-21_3.csv")
read_result("BTCUSDT_30m_2024-01-30_2024-03-01_results.csv")
