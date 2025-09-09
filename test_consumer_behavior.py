import pandas as pd


def test_data_loads():
    df = pd.read_csv("Ecommerce_Consumer_Behavior_Analysis_Data.csv")
    assert not df.empty
