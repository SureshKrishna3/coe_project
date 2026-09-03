import math
from typing import List, Dict, Any
import numpy as np
from scipy import stats

class StatisticalAnalyzer:
    @staticmethod
    def analyze_paired_metrics(
        metric_name: str,
        baseline_values: List[float],
        proposed_values: List[float]
    ) -> Dict[str, Any]:
        """
        Computes descriptive & inferential statistics for paired evaluation measurements:
          - Sample size (N)
          - Descriptive stats for Baseline, Proposed, and Differences (Mean, Median, Std Dev, Min, Max)
          - Normality test (Shapiro-Wilk)
          - Hypothesis test (Paired t-test if normal, else Wilcoxon signed-rank test)
          - p-value & Statistical Significance flag (alpha = 0.05)
          - 95% Confidence Interval of paired mean difference
          - Cohen's d effect size & qualitative interpretation
        """
        b_arr = np.array(baseline_values, dtype=float)
        p_arr = np.array(proposed_values, dtype=float)
        diffs = p_arr - b_arr
        n = len(diffs)

        if n < 2:
            return {"error": "Insufficient sample size for statistical testing"}

        # 1. Descriptive Statistics
        b_mean = float(np.mean(b_arr))
        b_std = float(np.std(b_arr, ddof=1)) if n > 1 else 0.0
        b_med = float(np.median(b_arr))

        p_mean = float(np.mean(p_arr))
        p_std = float(np.std(p_arr, ddof=1)) if n > 1 else 0.0
        p_med = float(np.median(p_arr))

        diff_mean = float(np.mean(diffs))
        diff_std = float(np.std(diffs, ddof=1)) if n > 1 else 0.0
        diff_med = float(np.median(diffs))

        # 2. Normality Check (Shapiro-Wilk)
        if np.all(diffs == diffs[0]):
            is_normal = False
            shapiro_p = 1.0
        else:
            _, shapiro_p = stats.shapiro(diffs)
            is_normal = shapiro_p > 0.05

        # 3. Hypothesis Test (Paired t-test vs Wilcoxon)
        if np.all(diffs == 0):
            test_name = "Paired t-test"
            stat_val = 0.0
            p_val = 1.0
        elif is_normal:
            test_name = "Paired t-test"
            t_res = stats.ttest_rel(p_arr, b_arr)
            stat_val = float(t_res.statistic)
            p_val = float(t_res.pvalue)
        else:
            test_name = "Wilcoxon signed-rank test"
            try:
                w_res = stats.wilcoxon(p_arr, b_arr)
                stat_val = float(w_res.statistic)
                p_val = float(w_res.pvalue)
            except Exception:
                test_name = "Paired t-test"
                t_res = stats.ttest_rel(p_arr, b_arr)
                stat_val = float(t_res.statistic)
                p_val = float(t_res.pvalue)

        is_significant = p_val < 0.05

        # 4. 95% Confidence Interval
        se = diff_std / math.sqrt(n) if n > 0 else 0.0
        if diff_std > 0:
            ci_low, ci_high = stats.t.interval(0.95, df=n-1, loc=diff_mean, scale=se)
            ci_low = float(ci_low)
            ci_high = float(ci_high)
        else:
            ci_low = diff_mean
            ci_high = diff_mean

        # 5. Cohen's d Effect Size
        if diff_std > 0:
            cohens_d = float(diff_mean / diff_std)
        else:
            cohens_d = 0.0

        abs_d = abs(cohens_d)
        if abs_d < 0.2:
            effect_interp = "Negligible effect"
        elif abs_d < 0.5:
            effect_interp = "Small effect size"
        elif abs_d < 0.8:
            effect_interp = "Medium effect size"
        else:
            effect_interp = "Large / Substantial effect size"

        # Formulate human readable summary
        if p_val < 0.001:
            p_str = "p < 0.001"
        else:
            p_str = f"p = {p_val:.4f}"

        interp = (
            f"Statistically significant difference ({test_name}, {p_str}, Cohen's d = {cohens_d:.2f}, {effect_interp}). "
            f"Proposed system achieved a mean gain of {diff_mean:+.2f} over baseline (95% CI [{ci_low:.2f}, {ci_high:.2f}])."
            if is_significant else
            f"No statistically significant difference detected ({test_name}, {p_str})."
        )

        return {
            "metric_name": metric_name,
            "sample_size": n,
            "baseline": {
                "mean": round(b_mean, 2),
                "median": round(b_med, 2),
                "std_dev": round(b_std, 2),
                "min": round(float(np.min(b_arr)), 2),
                "max": round(float(np.max(b_arr)), 2)
            },
            "proposed": {
                "mean": round(p_mean, 2),
                "median": round(p_med, 2),
                "std_dev": round(p_std, 2),
                "min": round(float(np.min(p_arr)), 2),
                "max": round(float(np.max(p_arr)), 2)
            },
            "paired_difference": {
                "mean_diff": round(diff_mean, 2),
                "median_diff": round(diff_med, 2),
                "std_dev_diff": round(diff_std, 2),
                "ci_95": [round(ci_low, 2), round(ci_high, 2)]
            },
            "hypothesis_testing": {
                "test_used": test_name,
                "statistic_value": round(stat_val, 4),
                "p_value": p_val,
                "p_value_formatted": p_str,
                "is_statistically_significant": is_significant,
                "cohens_d": round(cohens_d, 2),
                "effect_size_interpretation": effect_interp
            },
            "interpretation_summary": interp
        }
