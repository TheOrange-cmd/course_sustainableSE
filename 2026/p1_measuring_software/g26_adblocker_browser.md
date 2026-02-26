---
author: Maria Cristescu, Nicolas Hornea, Daniël Rugge, Alexandru Verhoveţchi
group_number: 26
title: "Browser Energy Usage: The Effect of Ad Blocking"
image: "img/g26_adblocker_browser/project_cover.png"
date: 12/02/2026
summary: |-
  This project measures the energy consumption of different web browsers with and without UBlock Origin ad blocking. Using LibreHardwareMonitor on Windows, we compare power usage across browsers (i.e. Chrome, Firefox, Edge, Brave) and websites (i.e. Youtube, Netflix, Reddit, Nu.nl) to determine whether UBlock increases or decreases overall energy consumption.
identifier: p1_measuring_software_2026 # Do not change this
all_projects_page: "../p1_measuring_software" # Do not change this
---

A working POC can be found [here](https://github.com/TheOrange-cmd/course_sustainableSE/tree/adblock/2026/p1_measuring_software/POC).


# Browser Energy Usage: The Effect of Ad Blocking

## Introduction

As of 2024, the average person spends over six hours online every day, contributing to a global data usage of nearly 400 million terabytes per day (Statista, 2024). While much of the sustainability discussions focus on the massive energy influence of data centers, which accounted for example for 4% of US national energy consumption in 2023 (Shehabi et al., 2024), the energy usage by billions of end-user devices still has an essential impact. Every website load requires processing scripts, layout elements, and media.

However, some of the load is dedicated not to the content requested by the user, but to the "invisible" and sometimes not web advertisements and tracking scripts. Previous research suggests that these elements introduce a measurable overhead. For example, advertisements can add several watts of power consumption to a single browsing session (Simons & Pras, 2010).

Given the size of internet use, reducing the energy cost of loading a webpage can lead to significant savings in energy, as ad blockers like uBlock Origin claim to increase efficiency by preventing these scripts from ever loading. This project will try to experiment with that claim by comparing the energy consumption of four major browsers (Chrome, Firefox, Edge, and Brave) on different websites to determine if ads and script filtering can lower a device's carbon footprint.

### uBlock Origin
uBlock Origin is a free, open-source browser extension designed for advertisement filtering. Unlike many other ad blockers, it is marketed as one that prioritizes CPU and memory efficiency. Via filter lists, it intercepts requests from the browser to ad-related servers and prevents the execution of those scripts. We examine whether this reduction in network requests and script execution results directly in lower hardware use.

### LibreHardwareMonitor
LibreHardwareMonitor is an open-source tool that provides real-time access to the sensors in a Windows-based computer. For this project, it serves as the primary measurement instrument, allowing us to track the CPU Package Power and GPU Power in watts. By isolating these metrics during controlled browsing sessions, we can measure the exact energy cost of rendering specific websites with and without active advertisement filtering.

### Web Browsers
The efficiency of an ad blocker is often tied to the performance and functionality of the browser. In this study, we compare two primary architectures:
1. **Chromium** (Chrome, Edge, Brave): An open-source project by Google that powers the majority of modern browsers, which uses the V8 JavaScript engine and the Blink rendering engine.
2. **Gecko** (Firefox): Developed by Mozilla, this engine is known for its independent architecture and different approach to resource management and privacy.



## Expected Effects and Hypothesis

Prior work shows that online advertising introduces measurable overhead in web browsing workloads, which, in turn, increases device energy consumption. Simons and Pras (2010) demonstrate that advertisements can add several watts of power consumption to during browsing sessions. This establishes a clear mechanism through which ad blocking may reduce energy use.

Subsequent studies reinforce this expectation. Pearce (2020) reports page loading times being reduced with up to 28% when using common ad blockers, suggesting a meaningful decrease in computational work. Because CPU and GPU use are closely linked to power consumption, such reductions indicates corresponding energy savings. Direct measurements of Khan et al. (2024) further confirm this relation, showing average power reductions of around 40% on multimedia websites, when ad blockers are enabled. However, these effects vary substantially by website type (multimedia, news, etc.).

Given the variability reported in literature, the present study expects a mean reduction in power consumption of 15% (SD 10%) when ad blocking is enabled. This conservative estimate reflects the variability observed across different website categories and browsers, while remaining consistent with previously reported values.

Given the rapid evolution of web technologies, advertising practices, and browser architectures, it remains unclear whether previously reported energy impacts of online advertising still hold in contemporary browsing environments. This study revisits the effect of ad blocking using modern browsers and high-traffic websites.


The study is guided by the following research questions:

1. RQ1: What is the effect of enabling uBlock Origin on power consumption across different web browsers and websites?

2. RQ2: How much of the variation in browser power consumption can be explained by changes in downloaded data volume and processing load when using uBlock Origin?

RQ1 is evaluated using a confirmatory hypothesis test. The main hypothesis is:

1. H<sub>0</sub>: Enabling uBlock Origin does not significantly change mean browser power consumption.
2. H<sub>1</sub>: Enabling uBlock Origin reduces mean browser power consumption by 15%.

RQ2 is treated as exploratory. Prior literature provides limited quantitative guidance on the contribution of network and processing factors in modern browsers. Therefore, no formal hypothesis is specified for RQ2.

## Methodology

This section details the experimental setup and data collection protocol used to investigate the effect of ad blocking on browser power consumption. The methodology was designed to ensure reproducibility and to control for extraneous variables that could influence the measurements.

### Experimental Setup

All experiments were conducted on a single, dedicated machine to eliminate hardware variability as a confounding factor.

**Hardware and System Configuration:**
*   **Operating System:** Microsoft Windows, run with administrator privileges to access hardware sensors.
*   **Processor:** AMD Ryzen 7 5700U with Radeon Graphics (APU).
*   **System State:** To ensure a consistent baseline, the machine was prepared before each experimental session according to a strict protocol: all non-essential applications and background processes were closed, a wired Ethernet connection was used, the "High Performance" power plan was selected, and screen brightness was set to a fixed value.

**Software Configuration:**
*   **Browsers:** Three major web browsers were tested: Google Chrome and Microsoft Edge (both Chromium-based) and Mozilla Firefox (Gecko-based).
*   **Ad Blocker:** uBlock Origin was selected for its popularity and efficiency. The standard extension was used for Edge and Firefox, while uBlock Origin Lite was used for Chrome due to automation constraints.
*   **Automation:** Browser interactions were automated using the Playwright framework for Python. To better simulate human browsing and bypass simple bot-detection, the `playwright-stealth` library was applied to each browser instance.

### Collected data

Two primary categories of data were collected concurrently: hardware power consumption and network traffic metrics.

**Power Consumption:**
Hardware sensor data was collected by programmatically interfacing with LibreHardwareMonitor. The primary dependent variable for power consumption was the **CPU Package Power (Watts)**. For this integrated APU, this single metric represents the combined power draw of the CPU cores and the integrated Radeon Graphics, sampled at a frequency of 1 Hz. Unofrtunately, the device does not offer access to individual CPU and GPU power measurements, likely due to the graphics being integrated. 

**Network Traffic:**
To address RQ2, a custom monitoring component was integrated into the automation script. This component captured network events for each webpage to quantify:
*   Total data volume (bytes) and the total number of requests.
*   The subset of data volume and requests originating from domains on Peter Lowe's ad-serving blocklist (Lowe, 2026).
*   The number of requests actively intercepted and blocked by the browser extension.

### Experimental Design

The experiment followed a within-subjects factorial design, where each website was subjected to multiple conditions.

**Independent Variables (Factors):**
1.  **Website:** A set of 14 popular, high-traffic websites, primarily focused on the Dutch market: `Telegraaf.nl`, `Nu.nl`, `AD.nl`, `Bol.com`, `Marktplaats.nl`, `Aliexpress.com`, `Youtube.com`, `Reddit.com`, `Imgur.com`, `9gag.com`, `Dumpert.nl`, `Tweakers.net`, `Weeronline.nl`, and `Wikipedia.org` (as a non-ad control).
2.  **Browser:** Google Chrome, Microsoft Edge, Mozilla Firefox.
3.  **Ad Blocking:** Enabled (uBlock Origin active) vs. Disabled (no ad blocker installed).

This resulted in a total of 14 (websites) × 3 (browsers) × 2 (ad block conditions) = 84 unique experimental configurations.

### Data Collection Protocol

A fully automated script executed the experiment to ensure consistency.

1.  **Randomization:** All 84 configurations were replicated 20 times for a total of 1,680 trials. This entire list was then shuffled into a random order to mitigate time-dependent confounding variables (e.g., thermal drift).
2.  **Initialization:** Before the first run, browser user data directories were cleared to prevent caching between conditions. The system was warmed up for five minutes by running multithreaded exponential calculations to reach 80% CPU load to mitigate any startup-related effects.
3.  **Per-Trial Execution:** For each of the 1,680 trials:
    a. A `cooldown` period of 10 seconds was enforced.
    b. The appropriate browser was launched with the specified ad blocker configuration.
    c. The browser navigated to the target URL and executed pre-defined actions to handle elements like cookie banners.
    d. For a duration of 30 seconds, the script simulated a user scrolling the page to trigger lazy-loaded content and ads, except in the case of youtube where the main content is at the top of the page.
    e. During this 30-second interaction, hardware power and network data were recorded once per second and saved to a CSV file with corresponding metadata.
    f. The browser was closed.

### Pilot Study and Sample Size Determination

Prior to the main experiment, a pilot study was conducted with a small sample size (N=3) for each configuration to inform the selection of an appropriate sample size for the main study. An a priori power analysis was performed on this pilot data to calculate the sample size required to achieve a statistical power of 0.80 at a significance level (α) of 0.05.

The analysis revealed a wide variance in the ad blocker's effect size (Cohen's *d*) across configurations. For some configurations (e.g., `nu.nl` on Edge), the required sample size was as low as 3. For others where the effect was negligible (e.g., `youtube.com` on Chrome), the analysis suggested a required N in the thousands, confirming a very small effect. A large number of configurations required a sample size between 10 and 50.

Based on these findings and the practical time constraints of the project, a sample size of **N=20 trials per configuration** was chosen. This number represents a pragmatic balance, providing sufficient statistical power for the majority of configurations exhibiting a medium-to-large effect, while acknowledging that the study may be underpowered for configurations with very small true effect sizes. All 84 configurations were included in the main experiment regardless of their pilot study recommendation to ensure a complete dataset.



## Limitations and Future Work

Several limitations and possible extensions should be considered when interpreting the results of this study. First, the experiments were conducted on one machine and measured using LibreHardwareMonitor. Although this tool provides sensor data, software-based power readings may differ from external power meter measurements. Additionally, the results cannot be generalized for other hardware configurations, where power management behaviour can differ substantially. 

Secondly, the study evaluates a limited set of websites and browsers. Advertising intensity can vary widely across websites, which may lead to different energy impacts than observed in the current study. Similarly, only one ad blocker configuration (i.e. uBlock Origin) was tested. Alternative tools may produce different effects.

Thirdly, environmental and system factors were controlled, but only to the best of our ability. Variations in network conditions or background processes may introduce noise into the power measurements. While introducing randomization and repeated runs may mitigate some variability, unmeasured factors may still influence the results.

Future work may expand the range of websites, browsers, ad blocking tools and hardware configurations, to improve the generalizability of these findings.



# References

Khan, K. A., Iqbal, M. T., & Jamil, M. (2024). "Impact of Ad Blockers on Computer Power Consumption while Web Browsing: A Comparative Analysis". European Journal of Electrical Engineering and Computer Science, 8(5), 18–24. https://doi.org/10.24018/ejece.2024.8.5.650

Lowe, P. (2026). “Ad blocking with ad server hostnames and IP addresses.” [Online]. Available: https://pgl.yoyo.org/adservers/. [Accessed: 26 Feb 2026].

Pearce, J. M. (2020). "Energy Conservation with Open Source Ad Blockers. Technologies", 8(2), 18. https://doi.org/10.3390/technologies8020018

Shehabi et al. (2024). Shehabi, A., et al. (2024). "United States Data Center Energy Usage Report. Lawrence Berkeley National Laboratory".

Simons, R. J. G. &  Pras, A. (2010, August) "The Hidden Energy Cost of Web Advertising".

Statista. (2024). "Volume of data created, captured, copied, and consumed worldwide from 2010 to 2025".
