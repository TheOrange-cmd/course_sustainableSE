# How to Integrate the Analysis Results into the Report

This document outlines **what** needs to be added or changed in the `g26_adblocker_browser.md` file, serving as a structural guide to write your final report. 

---

## 1. Add a "Data Analysis" Subsection
*Location: At the end of the `### Methodology` section.*

**What to include:**
- Explain how energy was calculated (Trapezoidal rule on CPU Package Power).
- State the outlier removal criteria (Z-score > 3) and how many were removed (3 runs, 0.2%).
- Explain the statistical tests used for normality (Shapiro-Wilk) and the differing tests for independent samples (Welch's t-test for normal, Mann-Whitney U for non-normal).
- Mention the Benjamini-Hochberg False Discovery Rate (FDR) correction used to control for the 42 browser-website combinations.

## 2. Create the "Results" Section
*Location: Insert a new `## Results` header right after the `## Methodology` section.*

### Sub-section: RQ1 Findings (Power Consumption)
*   **Core Finding**: State clearly that H1 (15% savings) is rejected across all browsers. H0 is partially rejected because Chrome and Firefox showed significant differences, but mostly not in the expected direction.
*   **Stats**: 
    - Chrome: +11.8% energy *increase* (worse). Mention *uBlock Origin Lite* was used due to Manifest V3.
    - Edge: -2.6% (not statistically significant).
    - Firefox: -2.9% energy *decrease* (significant).
*   **Visual**: Reference the `violin_energy_j_by_browser.png` image here.

### Sub-section: Network Traffic Savings
*   **Core Finding**: Acknowledge that despite the energy overhead, uBlock Origin successfully does what it advertises: dramatically reducing HTTP requests and payload (especially on ad-heavy sites like weeronline and telegraaf).
*   **Visual**: Reference the `network_savings.png` image here.

### Sub-section: RQ2 Findings (Regression)
*   **Core Finding**: Discuss the linear regression ($R^2 = 0.910$).
*   **Stats**: 
    - Emphasize that hardware processing loads ($\Delta CPU$, $p=0.0003$ and $\Delta Memory$, $p<0.001$) significantly dictate the energy footprint.
    - Raw downloaded data volume ($\Delta Data$, $p=0.346$) does *not* significantly predict energy variance. It's the processing cost that matters.

### Sub-section: Site-Specific Efficiency (FDR-Corrected)
*   **Core Finding**: Explain the interaction between ad density and extension efficiency.
*   **Stats**:
    - Describe where Adblock saved energy (e.g., Firefox on 9gag saved 34.8%; Edge on 9gag saved 24.9%).
    - Describe where Adblock wasted energy (e.g., Edge on Wikipedia paid a 28.7% penalty; Chrome on Youtube paid a 26.5% penalty).
*   **Visual**: Reference the `energy_diff_pct.png` image here.

---

## 3. Update the "Discussion" Section
*Location: Inside the existing `## Discussion` section.*

**What to edit:**
- You had outdated pilot numbers in your draft. Specifically:
  - Firefox's reduction should be changed from 5.1% to **2.9%**.
  - Chrome's penalty is nearly **11.8%** (not 12%).
  - Edge's penalty on Wikipedia is **28.7%** (not 25.9%).
- Mention how your RQ2 findings support your discussion points: since computational load ($\Delta CPU$) determines energy, ad-light sites cause the extension to "waste" energy inspecting clean code.

---

## 4. Add a point to "Limitations"
*Location: In the `## Limitations and Future Work` section.*

**What to add:**
- Acknowledge that your experiment used a **fixed 30-second measurement window**.
- Explain that because you forced a 30-second window, you couldn't effectively measure time-to-interactive or variations in the Energy Delay Product (EDP). Future work should measure natural page loads to calculate EDP properly.
