import os
from Consumer_Behavior import (
    load_data,
    clean_engagement,
    filter_smartphone_users,
    group_device_ads_mean,
    plot_device_ads,
    prepare_ml_frame,
    train_and_eval_logreg,
    ENGAGEMENT_MAP,
)

DATA_PATH = "Ecommerce_Consumer_Behavior_Analysis_Data.csv"


def test_data_loads():
    df = load_data(DATA_PATH)
    assert not df.empty


def test_clean_engagement_creates_score_and_types():
    df = clean_engagement(load_data(DATA_PATH))
    assert "Engagement_with_Ads" in df.columns
    assert str(df["Engagement_with_Ads"].dtype) == "string"
    assert "Engagement_with_Ads_Score" in df.columns
    valid = set(ENGAGEMENT_MAP.values())
    non_null = set(df["Engagement_with_Ads_Score"].dropna().unique().tolist())
    assert non_null.issubset(valid)


def test_groupby_sorted_and_nonempty():
    s = group_device_ads_mean(clean_engagement(load_data(DATA_PATH)))
    assert not s.empty
    assert all(s.values[i] >= s.values[i + 1] for i in range(len(s) - 1))


def test_plot_creates_png(tmp_path):
    s = group_device_ads_mean(clean_engagement(load_data(DATA_PATH)))
    out = tmp_path / "ads_by_device.png"
    plot_device_ads(s, out_path=str(out))
    assert out.exists() and out.stat().st_size > 0


def test_ml_pipeline_runs_and_accuracy_range():
    X, y = prepare_ml_frame(clean_engagement(load_data(DATA_PATH)))
    assert len(X) == len(y) and y.isna().sum() == 0
    model, acc = train_and_eval_logreg(X, y, random_state=42)
    assert hasattr(model, "coef_")
    assert 0.0 <= acc <= 1.0
