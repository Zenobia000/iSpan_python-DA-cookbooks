"""
stat_helpers.py
Utility functions for inferential statistics course.
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import normaltest


def create_codebook(df, units_dict=None, detailed_labels=None):
    """
    Generate a codebook (data dictionary) for the given DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to describe.
    units_dict : dict, optional
        Mapping of column names to unit strings.
    detailed_labels : dict, optional
        Mapping of column names to human-readable labels.

    Returns
    -------
    pd.DataFrame
        A codebook with metadata for every column.
    """
    rows = []
    outlier_columns = []

    for col in df.columns:
        data_type = type(df[col].iloc[0])

        if pd.api.types.is_numeric_dtype(df[col]):
            measure = "Scale"
            decimals = 2 if df[col].dtype == "float64" else 0
        elif isinstance(df[col].iloc[0], (str, list)):
            measure = "Nominal"
            decimals = 0
        else:
            measure = "Nominal"
            decimals = 0

        column_width = df[col].astype(str).str.len().max()

        missing_values = df[col].isnull().sum()
        missing_rate = round(missing_values / len(df) * 100, 2)

        label = (
            detailed_labels[col]
            if detailed_labels and col in detailed_labels
            else col
        )

        if measure == "Nominal":
            unique_vals = df[col].unique()
            values = ", ".join([str(val) for val in unique_vals])
            imbalance_warning = (
                "Yes"
                if df[col].value_counts(normalize=True).max() > 0.8
                else "No"
            )
            outlier_warning = "N/A"
        else:
            values = "Scale data - None"
            imbalance_warning = "N/A"

            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            outlier_rate = outliers / len(df[col]) * 100
            outlier_warning = "Yes" if outlier_rate > 5 else "No"

            if outlier_warning == "Yes":
                outlier_columns.append(col)

        align = "Right" if pd.api.types.is_numeric_dtype(df[col]) else "Left"

        if measure == "Scale":
            mean_val = (
                round(df[col].mean(), 2)
                if pd.api.types.is_numeric_dtype(df[col])
                else "N/A"
            )
            min_val = df[col].min()
            max_val = df[col].max()
            std_dev = round(df[col].std(), 2)
            median_val = df[col].median()
        else:
            mean_val = min_val = max_val = std_dev = median_val = "N/A"

        unit = units_dict[col] if units_dict and col in units_dict else "N/A"

        rows.append(
            {
                "Name": col,
                "Type": str(data_type),
                "Width": column_width,
                "Decimals": decimals,
                "Label": label,
                "Values": values,
                "Missing": missing_values,
                "MissingRate": f"{missing_rate}%",
                "Align": align,
                "Measure": measure,
                "Mean": mean_val,
                "Min": min_val,
                "Max": max_val,
                "StdDev": std_dev,
                "Median": median_val,
                "Unit": unit,
                "ImbalanceWarning": imbalance_warning,
                "OutlierWarning": outlier_warning,
            }
        )

    codebook = pd.concat(
        [pd.DataFrame([row]) for row in rows], ignore_index=True
    )

    if outlier_columns:
        _plot_outlier_columns(df, outlier_columns)

    return codebook


def _plot_outlier_columns(df, outlier_columns):
    """Plot KDE with outlier markers for columns flagged by create_codebook."""
    n_cols_per_row = 2
    n_outliers = len(outlier_columns)
    n_rows = (n_outliers + n_cols_per_row - 1) // n_cols_per_row

    fig, axes = plt.subplots(
        n_rows, n_cols_per_row, figsize=(12, 3 * n_rows)
    )
    if n_rows == 1 and n_cols_per_row == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    for i, col in enumerate(outlier_columns):
        ax = axes[i]
        sns.kdeplot(df[col], color="blue", label=f"{col} KDE", fill=True, ax=ax)

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        stat, p_value = normaltest(df[col].dropna())
        mean_val = round(df[col].mean(), 2)
        std_dev = round(df[col].std(), 2)

        ax.set_title(
            f"KDE Plot of {col} with Outliers\n"
            f"Mean: {mean_val}, StdDev: {std_dev}\n"
            f"Normality Test p-value: {p_value:.4f}"
        )
        ax.axvline(
            x=lower_bound, color="green", linestyle="--", label="Lower Bound"
        )
        ax.axvline(
            x=upper_bound, color="red", linestyle="--", label="Upper Bound"
        )

        outliers_df = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        ax.scatter(
            outliers_df[col],
            np.zeros(len(outliers_df)),
            color="red",
            label="Outliers",
            zorder=5,
        )
        ax.legend()

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()
