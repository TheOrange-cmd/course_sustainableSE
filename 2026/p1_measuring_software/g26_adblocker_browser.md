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

## Expected Effects and Hypothesis

Prior work shows that online advertising introduces measurable overhead in web browsing workloads, which, in turn, increases device energy consumption. Simons and Pras[^web-ads] demonstrate that advertisements can add several watts of power consumption to during browsing sessions. This establishes a clear mechanism through which ad blocking may reduce energy use.

Subsequent studies reinforce this expectation. Pearce[^load-time] reports page loading times being reduced with up to 28% when using common ad blockers, suggesting a meaningful decrease in computational work. Because CPU and GPU use are closely linked to power consumption, such reductions indicates corresponding energy savings. Direct measurements of Khan et al.[^measure-paper] further confirm this relation, showing average power reductions of around 40% on multimedia websites, when ad blockers are enabled. However, these effects vary substantially by website type (multimedia, news, etc.).

Given the variability reported in literature, the present study expects a mean reduction in power consumption of 15% (SD 10%) when ad blocking is enabled. This conservative estimate reflects the variability observed across different website categories and browsers, while remaining consistent with previously reported values.

Therefore, the main hypothesis is:

1. H<sub>0</sub>: Enabling uBlock Origin does not significantly change mean browser power consumption.
2. H<sub>1</sub>: Enabling uBlock Origin reduces mean browser power consumption by 15%.

The study is guided by the following research questions:

1. RQ1: What is the effect of enabling uBlock Origin on power consumption across different web browsers and websites?

2. RQ2: How much of the variation in browser power consumption can be explained by changes in downloaded data volume and processing load when using uBlock Origin?




# References

[^web-ads] R. J. G. Simons and A. Pras, “The Hidden Energy Cost of Web Advertising”, Aug. 2010.

[^load-time] J. M. Pearce, “Energy Conservation with Open Source Ad Blockers,” Technologies, vol. 8, no. 2, p. 18, Mar. 2020, doi: 10.3390/technologies8020018.

[^measure-paper] K. A. Khan, M. T. Iqbal, and M. Jamil, “Impact of Ad Blockers on Computer Power Consumption while Web Browsing: A Comparative Analysis,” EJECE, vol. 8, no. 5, pp. 18–24, Oct. 2024, doi: 10.24018/ejece.2024.8.5.650.



<!-- This problem takes another level if we are counting on these measurements to make **groundbreaking research contributions** in this area. Some research projects in the past have underestimated this issue and failed to produce replicable findings. Hence, this article presents a roadmap on how to properly set up a scientific methodology to run energy efficiency experiments. It mostly stems from my previous work on [doing research and publishing](/publications) on Green Software.


This article is divided into two main parts: 1) how to set up energy measurements with minimum bias, and 2) how to analyse and take scientific conclusions from your energy measurements.
Read on so that we can get your paper accepted in the best scientific conference.

--- 
#### 👉 Note 1:
If you are a **software developer** enthusiastic about energy efficiency but you are not particularly interested in scientific experiments, this article is still useful for you. It is not necessary to do "everything by the book" but you may use one or two of these techniques to reduce the likelihood of making wrong decisions regarding the energy efficiency of your software.

--- 

## Unbiased Energy Data ⚖️

There are a few things that need to be considered to minimise the bias of the energy measurements. Below, I pinpoint the most important strategies to minimise the impact of these biases when collecting the data.

### Zen mode 🧘🏾‍♀️

The first thing we need to make sure of is that the only thing running in our system is the software we want to measure. Unfortunately, this is impossible in practice – our system will always have other tasks and things that it will run at the same time. Still, we must at least minimise all these competing tasks:

- all applications should be closed, notifications should be turned off;
- only the required hardware should be connected (avoid USB drives, external disks, external displays, etc.);
- turn off notifications;
- remove any unnecessary services running in the background (e.g., web server, file sharing, etc.);
- if you do not need an internet or intranet connection, switch off your network;
- prefer cable over wireless – the energy consumption from a cable connection is more stable than from a wireless connection.

### Freeze your settings 🥶

It is not possible to shut off the unnecessary things that run in our system. Still, we need to at least make sure that they will behave the same across all sets of experiments. Thus, we must fix and report some configuration settings. One good example is the brightness and resolution of your screen – report the exact value and make sure it stays the same throughout the experiment. Another common mistake is to keep the automatic brightness adjustment on – this is, for example, an awful source of errors when measuring energy efficiency in mobile apps.

---

### 

Nevertheless, using statistical metrics to measure effect size is not enough – there should be a discussion of the **practical effect size**. More important than demonstrating that we came up with a new version that is more energy efficient, you need to demonstrate that the benefits will actually be reflected in the overall energy efficiency of normal usage of the software. For example, imagine that the results show that a given energy improvement was only able to save one joule of energy throughout a whole day of intensive usage of your cloud software. This perspective can hardly be captured by classic effect-size measures. The statistical approach to effect size (e.g., mean difference, Cohen's-*d*, and so on) is agnostic of the context of the problem at hand. -->



