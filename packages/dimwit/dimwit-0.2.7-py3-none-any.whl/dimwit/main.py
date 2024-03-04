import datetime as dat
import dateutil

# Import matplotlib before pandas to avoid import ordering issues.
import matplotlib.pyplot as plt
import pandas as pd
import requests
import numpy as np


class NotionHeaders:
    def __init__(self, notion_token: str, notion_version: str = "2022-06-28"):
        self.__notion_token__ = notion_token
        self.__notion_version__ = notion_version

    def __repr__(self) -> str:
        return (
            "NotionHeaders(",
            'authorization="Bearer <SECRET_NOTION_TOKEN>", ',
            'content_type="application/json", ',
            f'notion_version="{self.__notion_version__}")',
        )

    def __str__(self) -> str:
        return (
            "NotionHeaders(",
            'authorization="Bearer <SECRET_NOTION_TOKEN>", ',
            'content_type="application/json", ',
            f'notion_version="{self.__notion_version__}")',
        )

    def to_dict(self) -> dict:
        return {
            "Authorization": "Bearer " + self.__notion_token__,
            "Content-Type": "application/json",
            "Notion-Version": f"{self.__notion_version__}",
        }


def get_notion_pages(url_endpoint, headers, num_pages=None, sort_by=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    get_all = num_pages is None
    # TODO: Logic for getting correct number of pages seems wrong. Check this.
    max_notion_pages_per_request = 100
    page_size = max_notion_pages_per_request if get_all else num_pages

    payload = {"page_size": page_size}
    if sort_by is not None:
        payload["sorts"] = sort_by

    response = requests.post(url_endpoint, json=payload, headers=headers)

    data = response.json()

    if response.status_code != 200:
        print(f"status: {response.status_code}")
        print(f"reason: {response.reason}")
        # Calling code can handle a failed request, so return an empty result.

    results = data.get("results", [])
    while data.get("has_more", False) and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        if sort_by is not None:
            payload["sorts"] = sort_by

        response = requests.post(url_endpoint, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results


# TODO: Update this to fetch by date range rather than a prescribed number of
# pages and a single database. Provisonally, store all related DBs in a dict,
# fetch from the ones with the relevant data, and paginate on any edge cases.
def get_notion_pages_from_db(
    db_id,
    headers,
    sort_column: str | None = "date",
    sort_direction: str = "ascending",
    num_pages=None,
):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{db_id}/query"

    # The 'date' column should be standard across all personal DBs in Notion.
    # However, it would be ideal to minimise the amount of data processing,
    # including sorting. If checking Notion personally, typically only need the
    # latest data, so having it stored in descending order makes sense. On the
    # other hand, most code assumes/prefers ascending order. Importantly, if
    # the data is always inserted in some sorted order, then re-sorting is
    # either trivial or not needed at all.
    # TODO: Decide how to deal with sorting.
    sort_by = [{"property": sort_column, "direction": sort_direction}]
    if sort_column is None:
        sort_by = None

    results = get_notion_pages(
        url,
        headers.to_dict(),
        num_pages=num_pages,
        sort_by=sort_by,
    )

    return results


def check_page_valid(page, idx):
    properties = page["properties"]
    if properties is None:
        raise Exception(f"Found empty entry at position {idx} (0-based index)")


def get_notion_date(page, property):
    properties = page["properties"]
    return dateutil.parser.isoparse(properties[property]["date"]["start"])


def get_notion_number(page, property):
    return page["properties"][property]["number"]


def get_notion_multi_select(page, property):
    items = page["properties"][property]["multi_select"]
    return [item["name"] for item in items]


def get_notion_text(page, property):
    properties = page["properties"]
    return properties[property]["rich_text"][0]["text"]["content"]


def extract_airflow_entry(timestamps, data, idx, page):
    check_page_valid(page, idx)
    ts = get_notion_date(page, "date")
    vals = [get_notion_number(page, f"recording_{i}") for i in [1, 2, 3]]
    timestamps.append(ts)
    data.append(vals)
    return None


def extract_categorical_entry(timestamps, data, idx, page):
    check_page_valid(page, idx)
    ts = get_notion_date(page, "date")
    categories = get_notion_multi_select(page, "category")
    for category in categories:
        timestamps.append(ts)
        data.append(category)
    return None


def extract_weight_entry(timestamps, data, idx, page):
    check_page_valid(page, idx)
    ts = get_notion_date(page, "date")
    weight = get_notion_number(page, "weight")
    categories = get_notion_multi_select(page, "category")
    timestamps.append(ts)
    data.append((weight, *categories))
    return None


def extract_sleep_entry(timestamps, data, idx, page):
    check_page_valid(page, idx)
    start = get_notion_date(page, "start_date")
    end = get_notion_date(page, "end_date")
    duration = get_notion_text(page, "duration")
    timestamps.append((start, end))
    data.append(duration)
    return None


def extract_pomodoro_entry(timestamps, data, idx, page):
    check_page_valid(page, idx)
    ts = get_notion_date(page, "date")
    pomodoro_length = get_notion_number(page, "pomodoro_length")
    break_length = get_notion_number(page, "break_length")
    score = get_notion_number(page, "score")
    comment = get_notion_text(page, "comment")
    timestamps.append(ts)
    data.append((pomodoro_length, break_length, score, comment))
    return None


def get_all_entries(pages, add_data_entry):
    timestamps, data = [], []

    for idx, page in enumerate(pages):
        add_data_entry(timestamps, data, idx, page)

    return timestamps, data


def get_n_weeks_ago(n):
    now = dat.datetime.now().astimezone()
    current_week_start = now - dat.timedelta(days=now.weekday())
    n_weeks_ago_start = current_week_start - dat.timedelta(weeks=n - 1)
    return n_weeks_ago_start


# TODO: Check how to perform copy-on padding with dataframes, in order to
# drop/simplify this function.
def get_moving_average_trend(data, k, padding="copy-on"):
    """
    Compute a moving average trend with window size `k` over over `data`.

    The padding used for the start and end is 'copy-on' - that is, the start
    and end values are duplicated akin to 'same' padding.
    """
    if padding != "copy-on":
        raise Exception("This type of padding is not supported!")

    if k % 2 == 0 or k == 1:
        raise Exception("k must be an odd number greater than 1!")

    j = (k - 1) / 2
    padded_data = np.concatenate(
        [np.repeat(data[0], j), data, np.repeat(data[-1], j)], axis=0
    )
    rolling_average = np.convolve(padded_data, np.ones(k) / k, "valid")
    return rolling_average


def get_basic_sleep_dataframe(
    ts: list[tuple],
    durations: list[str],
    target_sleep_start: str = "22:30:00",
    target_sleep_end: str = "06:30:00",
):
    N = len(ts)
    starts, ends = zip(*ts)
    all_aligned = len(starts) == len(ends) == len(durations) == N
    if not all_aligned:
        raise Exception(
            f"Unaligned start ({len(starts)} values), "
            f"end ({len(ends)} values), "
            f"duration ({len(durations)} values) columns"
        )
    data = {
        "start_date": starts,
        "end_date": ends,
        "durations": durations,
        "target_sleep_start": [target_sleep_start] * N,
        "target_sleep_end": [target_sleep_end] * N,
    }
    df = pd.DataFrame(data)
    return df


def compute_rounded_matrix(ts, events, rounding_unit, rounding_size):
    """
    Compute a matrix where each (sorted, ascending) row corresponds to a
    timestamp, and the columns the types of events, rounding timestamps
    according to `rounding`.

    Each entry corresponds to the number of events of a particular type
    occurring to the nearest rounded timestamp.

    Any NaNs are converted to 0s.
    """
    data = {"value": [1] * len(events), "categories": events, "date": ts}
    df = pd.DataFrame(data)
    # Make sure to set the date column to datetimes recognisable by pandas.
    df["date"] = pd.to_datetime(df["date"], utc=True)
    rounding_string = str(rounding_size) + rounding_unit
    # Need to use dt field, or else more lengthy to work with native datetimes.
    df["date"] = df["date"].dt.round(rounding_string)
    df = df.pivot_table(
        index="date", columns="categories", values="value", aggfunc="sum"
    )
    return df.fillna(0)


def zero_padded_df(num_rows, num_cols, index):
    return pd.DataFrame([[0] * num_cols] * num_rows, index=index)


def pad_out_table(df, pad_t, unit, pad_before=True, pad_after=True):
    # Pad out df with entries before and after boundary rows, to ensure correct
    # same- (or zero-) padding.
    pad_t_days = pd.Timedelta(pad_t, unit=unit)
    pad_before_start = df.index[0] - pad_t_days
    pad_after_start = df.index[-1] + pd.Timedelta(1, unit=unit)

    # The index in df cannot yet be assumed to be dense - so use a date range
    # with the earliest and latest entries as reference points.
    index_before = pd.date_range(pad_before_start, periods=pad_t, freq=unit)
    index_after = pd.date_range(pad_after_start, periods=pad_t, freq=unit)

    num_rows, num_cols = pad_t, len(df.columns)
    if pad_before:
        df = pd.concat([zero_padded_df(num_rows, num_cols, index_before), df])
    if pad_after:
        df = pd.concat([zero_padded_df(num_rows, num_cols, index_after), df])

    return df


# TODO: Enable different window sizes for different columns.
# Either this means returning a set of Series objects, or padding values in a
# single dataframe.
def compute_moving_average_matrix(
    ts, events, rounding_unit, rounding_size, window_size
):
    df = compute_rounded_matrix(ts, events, rounding_unit, rounding_size)
    categories = df.columns

    df_needs_padding = window_size > 1
    if df_needs_padding:
        pad_t = (window_size - 1) // 2
        df = pad_out_table(df, pad_t, rounding_unit)

    window_string = str(rounding_size) + rounding_unit
    dense_series = []
    for column in categories:
        # TODO: Fix annoying ImportError involving 'freq_to_period_freqstr'.
        sparse_column: pd.Series = df[column]
        dense_column = sparse_column.asfreq(freq=window_string)
        dense_column_no_nans = dense_column.fillna(0)
        dense_series.append(dense_column_no_nans)

    dense_df = pd.DataFrame(dense_series).T

    if not df_needs_padding:
        return dense_df

    averaged_df = dense_df.rolling(window_size, center=True).mean()
    # Skip the padding rows since they don't make much sense in the charts.
    return averaged_df.iloc[pad_t:-pad_t]


def get_aggregated_event_counts(ts, events, period):
    data = {"value": [1] * len(events), "categories": events, "date": ts}
    df = pd.DataFrame(data)
    # Make sure to set the date column to datetimes recognisable by pandas.
    df["date"] = pd.to_datetime(df["date"], utc=True)
    df = df.pivot_table(
        index="date", columns="categories", values="value", aggfunc="sum"
    )
    if period.lower() not in ["monthly", "weekly", "daily"]:
        raise Exception("Period argument not recognised")

    if period == "monthly":
        grouped_df = df.groupby([pd.Grouper(freq="ME")]).sum()

    if period == "weekly":
        df.index = df.index - pd.to_timedelta(7, unit="d")
        grouped_df = df.groupby([pd.Grouper(freq="W")]).sum()

    if period == "daily":
        grouped_df = df.groupby([pd.Grouper(freq="D")]).sum()

    return grouped_df


def populate_with_events(ax, events, from_date):
    for event in events:
        event_date, event_colour, event_style, event_label = event
        if event_date < from_date:
            continue
        ax.axvline(
            event_date,
            color=event_colour,
            linestyle=event_style,
            linewidth=1,
            label=event_label,
        )
    return ax


def plot_category(
    title, df, categories, window_size, round_size, round_unit, from_date=None
):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_title(title)
    for category in categories:
        if from_date is not None:
            ax = df[from_date:].plot(y=category, ax=ax)
        else:
            ax = df.plot(y=category, ax=ax)
    ax.set_xlabel("Time")
    ax.set_ylabel("Frequency")
    ax.legend(
        [
            f"{category} ({str(round_size) + round_unit}, k={window_size})"
            for category in categories
        ],
    )
    return fig, ax
