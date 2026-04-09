"""
stat_helpers.py
統計分析輔助工具模組

包含:
- create_codebook: 建立資料字典
- UnivariateAnalysisModule: 單變量自動化檢定框架
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import normaltest
from statsmodels.stats.multitest import multipletests
import seaborn as sns
import matplotlib.pyplot as plt


def create_codebook(df, units_dict=None, detailed_labels=None):
    """建立資料字典 (codebook)，包含變數摘要、缺失值、離群值警告等。"""
    rows = []
    outlier_columns = []

    for col in df.columns:
        data_type = type(df[col].iloc[0])

        if pd.api.types.is_numeric_dtype(df[col]):
            measure = 'Scale'
            decimals = 2 if df[col].dtype == 'float64' else 0
            column_width = df[col].astype(str).str.len().max()
        elif isinstance(df[col].iloc[0], (str, list)):
            measure = 'Nominal'
            decimals = 0
            column_width = df[col].astype(str).str.len().max()
        else:
            measure = 'Nominal'
            decimals = 0
            column_width = len(str(df[col].iloc[0]))

        missing_values = df[col].isnull().sum()
        missing_rate = round(missing_values / len(df) * 100, 2)

        label = (
            detailed_labels[col]
            if detailed_labels and col in detailed_labels
            else col
        )

        if measure == 'Nominal':
            unique_vals = df[col].unique()
            values = ', '.join([str(val) for val in unique_vals])
            imbalance_warning = (
                "Yes"
                if df[col].value_counts(normalize=True).max() > 0.8
                else "No"
            )
            outlier_warning = 'N/A'
        else:
            values = 'Scale data - None'
            imbalance_warning = 'N/A'
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = (
                (df[col] < lower_bound) | (df[col] > upper_bound)
            ).sum()
            outlier_rate = outliers / len(df[col]) * 100
            outlier_warning = "Yes" if outlier_rate > 5 else "No"
            if outlier_warning == "Yes":
                outlier_columns.append(col)

        align = 'Right' if pd.api.types.is_numeric_dtype(df[col]) else 'Left'

        if measure == 'Scale':
            mean_val = (
                round(df[col].mean(), 2)
                if pd.api.types.is_numeric_dtype(df[col])
                else 'N/A'
            )
            min_val = df[col].min()
            max_val = df[col].max()
            std_dev = round(df[col].std(), 2)
            median_val = df[col].median()
        else:
            mean_val = min_val = max_val = std_dev = median_val = 'N/A'

        unit = units_dict[col] if units_dict and col in units_dict else 'N/A'

        rows.append({
            'Name': col, 'Type': str(data_type), 'Width': column_width,
            'Decimals': decimals, 'Label': label, 'Values': values,
            'Missing': missing_values, 'MissingRate': f'{missing_rate}%',
            'Align': align, 'Measure': measure, 'Mean': mean_val,
            'Min': min_val, 'Max': max_val, 'StdDev': std_dev,
            'Median': median_val, 'Unit': unit,
            'ImbalanceWarning': imbalance_warning,
            'OutlierWarning': outlier_warning,
        })

    codebook = pd.concat(
        [pd.DataFrame([row]) for row in rows], ignore_index=True
    )

    if outlier_columns:
        _plot_outlier_columns(df, outlier_columns)

    return codebook


def _plot_outlier_columns(df, outlier_columns):
    """繪製有離群值欄位的 KDE 圖。"""
    n_cols_per_row = 2
    n_outliers = len(outlier_columns)
    n_rows = (n_outliers + n_cols_per_row - 1) // n_cols_per_row

    fig, axes = plt.subplots(n_rows, n_cols_per_row, figsize=(12, 3 * n_rows))
    if n_rows == 1 and n_cols_per_row == 1:
        axes = np.array([axes])
    axes = np.array(axes).flatten()

    for i, col in enumerate(outlier_columns):
        ax = axes[i]
        sns.kdeplot(df[col].dropna(), color='blue', label=f"{col} KDE", fill=True, ax=ax)
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        stat, p_value = normaltest(df[col].dropna())
        mean_val = round(df[col].mean(), 2)
        std_dev = round(df[col].std(), 2)
        ax.set_title(
            f'KDE Plot of {col} with Outliers\n'
            f'Mean: {mean_val}, StdDev: {std_dev}\n'
            f'Normality Test p-value: {p_value:.4f}'
        )
        ax.axvline(x=lower_bound, color='green', linestyle='--', label='Lower Bound')
        ax.axvline(x=upper_bound, color='red', linestyle='--', label='Upper Bound')
        outliers_data = df[
            (df[col] < lower_bound) | (df[col] > upper_bound)
        ]
        ax.scatter(
            outliers_data[col], np.zeros(len(outliers_data)),
            color='red', label='Outliers', zorder=5,
        )
        ax.legend()

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


class UnivariateAnalysisModule:
    """單變量自動化統計檢定框架。

    根據資料特性自動選擇適當的統計檢定方法：
    - 兩組: t-test / Welch's t / Mann-Whitney U
    - 多組: ANOVA / Kruskal-Wallis
    含 Bonferroni 多重比較校正。
    """

    def __init__(self, alpha=0.05):
        self.alpha = alpha
        self.results = []

    def calculate_statistics(self, data):
        return {
            'mean': data.mean(),
            'std': data.std(),
            'median': data.median(),
            'iqr': stats.iqr(data),
        }

    def cohen_d(self, x, y):
        return (x.mean() - y.mean()) / np.sqrt((x.var() + y.var()) / 2)

    def normality_test(self, data):
        if len(data) < 3:
            return False, np.nan
        stat, p_value = stats.shapiro(data)
        return p_value > 0.05, p_value

    def variance_homogeneity_test(self, group_data):
        if len(group_data) < 2:
            return np.nan
        return stats.levene(*group_data)[1]

    def analyze_variable(self, df, group_col, var):
        groups = df[group_col].unique()
        group_data = [
            df[df[group_col] == group][var].dropna() for group in groups
        ]
        n_groups = len(groups)
        levene_p = 'N/A'
        shapiro_p1 = 'N/A'
        shapiro_p2 = 'N/A'

        if n_groups == 2:
            data_group1, data_group2 = group_data
            shapiro_p1 = (
                stats.shapiro(data_group1)[1]
                if len(data_group1) >= 3
                else np.nan
            )
            shapiro_p2 = (
                stats.shapiro(data_group2)[1]
                if len(data_group2) >= 3
                else np.nan
            )
            levene_p = self.variance_homogeneity_test(
                [data_group1, data_group2]
            )

            if shapiro_p1 > 0.05 and shapiro_p2 > 0.05:
                if levene_p > 0.05:
                    t_stat, p_value = stats.ttest_ind(
                        data_group1, data_group2, equal_var=True
                    )
                    test_used = "t 檢定"
                    effect_size = self.cohen_d(data_group1, data_group2)
                else:
                    t_stat, p_value = stats.ttest_ind(
                        data_group1, data_group2, equal_var=False
                    )
                    test_used = "Welch's t 檢定"
                    effect_size = self.cohen_d(data_group1, data_group2)
            else:
                u_stat, p_value = stats.mannwhitneyu(
                    data_group1, data_group2
                )
                test_used = "Mann-Whitney U 檢定"
                n1, n2 = len(data_group1), len(data_group2)
                effect_size = (u_stat - (n1 * n2) / 2) / (n1 * n2 / 2)

        elif n_groups > 2:
            normal, _ = self.normality_test(group_data[0])
            if normal:
                levene_p = self.variance_homogeneity_test(group_data)
                if levene_p > 0.05:
                    stat_val, p_value = stats.f_oneway(*group_data)
                    test_used = "ANOVA"
                else:
                    stat_val, p_value = stats.kruskal(*group_data)
                    test_used = "Kruskal-Wallis 檢定"
            else:
                stat_val, p_value = stats.kruskal(*group_data)
                test_used = "Kruskal-Wallis 檢定"
            effect_size = 'N/A'
        else:
            raise ValueError(
                f"需要至少兩組資料，目前只有 {n_groups} 組"
            )

        result = "是" if p_value < self.alpha else "否"
        self.results.append({
            'Variable': var,
            'Shapiro p (Group 1)': shapiro_p1,
            'Shapiro p (Group 2)': shapiro_p2,
            "Levene's p-value": levene_p,
            'Test Used': test_used,
            'p-value': p_value,
            'Effect Size': effect_size,
            'Result': result,
        })

    def run_analysis(self, df, group_col, variables):
        """對指定變數群進行自動化檢定分析。"""
        self.results = []
        for var in variables:
            self.analyze_variable(df, group_col, var)

        df_results = pd.DataFrame(self.results)

        pvals = df_results['p-value'].dropna().values
        if len(pvals) > 0:
            _, pvals_corrected, _, _ = multipletests(
                pvals, alpha=self.alpha, method='bonferroni'
            )
            df_results.loc[
                df_results['p-value'].notna(), 'p-value_corrected'
            ] = pvals_corrected
            df_results['Result_corrected'] = [
                '是' if p < self.alpha else '否' for p in pvals_corrected
            ]

        return df_results
