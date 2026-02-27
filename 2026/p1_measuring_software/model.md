# Example Integration (Model)

This document serves as a "model" or draft of exactly how the new text could be written within the `g26_adblocker_browser.md` file based on the analysis.

---

### [Add this to the end of your "Methodology" section]

### Data Analysis
Energy consumption was calculated by estimating the integral of the CPU Package Power over the 30-second measurement window using the trapezoidal rule. Outliers (defined as having a Z-score > 3) were removed prior to hypothesis testing, resulting in the exclusion of 3 out of 1680 runs (0.2%).

The Shapiro-Wilk test was used to assess normality for each browser-website combination's distribution. For normally distributed groups (72.6% of data), Welch's t-test and Cohen's *d* were used for hypothesis testing. For non-normal groups (27.4%), the non-parametric Mann-Whitney U test and Common Language Effect Size (CLES) were applied. To control the false positive rate while evaluating 42 unique browser-website combinations, the Benjamini-Hochberg False Discovery Rate (FDR) correction was utilized with $q = 0.05$.

---

### [Insert this entire block immediately after Methodology]

## Results

### RQ1: Effect of uBlock Origin on Power Consumption
The primary hypothesis ($H_1$), positing a 15% reduction in mean browser power consumption from enabling uBlock Origin, was **rejected** across all tested browsers. Furthermore, the aggregate results yielded unexpected variations heavily dependent on the browser architecture:
*   **Chrome**: Enabling uBlock Origin resulted in a statistically significant 11.8% energy *increase* (worse efficiency) ($p_{corrected} < 0.001$, CLES = 0.36).
*   **Edge**: Yielded a non-significant 2.6% energy decrease ($p_{corrected} = 1.000$, CLES = 0.52).
*   **Firefox**: Showed a statistically significant but very minor 2.9% energy decrease ($p_{corrected} = 0.032$, CLES = 0.56).

While Chrome and Firefox exhibited statistically significant differences overall (allowing for a partial rejection of the null hypothesis $H_0$), neither browser achieved the 15% hypothesized savings. Note that due to Manifest V3 restrictions, Chrome was forced to use *uBlock Origin Lite*. This lighter extension protocol represents a structural difference compared to the standard extension running on Firefox, and is the likely driver of Chrome's energy penalty.

![Energy Distribution by Browser](../../p1_adblock_energy/results/violin_energy_j_by_browser.png)

### Network Traffic Savings
Despite the mixed power outcomes, network payload measurements strongly supported the extension's efficacy in network filtering. Across the board, uBlock Origin significantly reduced both total HTTP requests and transferred bytes, particularly on ad-heavy websites like *weeronline* and *telegraaf*.

![Network Traffic: Adblock vs No Adblock](../../p1_adblock_energy/results/network_savings.png)

### RQ2: Contributors to Browser Power Variation
To understand whether network data flow or processing load drove the variation in power consumption, a multiple linear regression was conducted ($R^2 = 0.910$). 

The structural model revealed that differing hardware processing loads heavily dictated the final energy footprint:
*   Changes in Average CPU Load ($\Delta CPU$) and Memory Load ($\Delta Memory$) were both highly significant predictors ($p < 0.001$).
*   Changes in Data Volume ($\Delta Data$ MB) and GPU Load ($\Delta GPU$) were not statistically significant predictors ($p = 0.346$ and $p = 0.470$, respectively).

This confirms that while ad blockers reduce network payload, it is the net change in CPU processing—either saved from executing ad scripts or expended by running the adblocker's logic—that fundamentally determines the energy outcome.

### Site-Specific Adblock Efficiency (FDR-Corrected)
Analysis of the 42 browser-website pairs revealed a distinct interaction between website ad-density and extension efficiency. Of the 42 pairs, 12 showed statistically significant differences after FDR correction.

Ad-blockers provided significant energy savings primarily on ad-heavy sites. For instance, Firefox saved 34.8% energy on *9gag* ($p < 0.001$, $d = +3.60$) and 20.3% on *weeronline* ($p < 0.001$, $d = +1.50$). Conversely, on ad-light sites, the extension universally cost more energy. On *Wikipedia*, Edge incurred a 28.7% penalty ($p < 0.001$, CLES = 0.16), while on *Youtube*, Chrome incurred a 26.5% penalty ($p = 0.002$, CLES = 0.21).

![Energy Savings Percentage by Website](../../p1_adblock_energy/results/energy_diff_pct.png)

---

### [Edits to make inside the "Discussion" section]

*   **Change 1:** Update `Firefox achieved a 5.1% overall reduction` to `Firefox achieved a 2.9% overall reduction`.
*   **Change 2:** Update `nearly 12% more energy` regarding Chrome to `11.8% more energy`.
*   **Change 3:** Ensure the text points out that Chrome forced the use of **Manifest V3 / uBlock Origin Lite**.
*   **Change 4:** When discussing why ad-heavy domains see savings, directly reference the regression from RQ2: "This is supported by our regression model, which confirms that average CPU Load ($\Delta CPU$) and Memory explain the majority of the energy variance (rather than raw data payload size)."
*   **Change 5:** Update `massive 25.9% energy increase seen on Edge when browsing Wikipedia` to `massive 28.7% energy increase seen on Edge`.

---

### [Edits to make inside the "Limitations and Future Work" section]

*   **Addition:** Add a paragraph stating: "Finally, the experimental design utilized a fixed 30-second measurement window for every trial. Because the duration was artificially fixed, time-dependent efficiency metrics like the Energy Delay Product (EDP) could not comprehensively capture time-to-interactive differences. Future experiments should allow page loads to complete naturally rather than cutting them off, accurately assessing if adblocking delivers a tangible user-experience speed improvement that translates into a genuinely lower Energy Delay Product."
