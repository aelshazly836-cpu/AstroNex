AstroNex – NASA Inspiration4 Biomarker Analysis



1\. Research Objective



This exploratory study investigates changes in selected blood biomarkers across pre-flight and post-flight sampling periods in the four Inspiration4 participants.



The primary objective is to examine changes in:



\- Hemoglobin concentration.

\- Red blood cell (RBC) count.



The study also explores the relationship between these two biomarkers and evaluates whether participant-level differences between pre-flight and post-flight measurements are statistically significant.



2\. Dataset Description



The data were obtained from NASA's Open Science Data Repository (OSDR) and consist of three transformed datasets:



1\. Complete Blood Count (CBC).

2\. Comprehensive Metabolic Panel (CMP).

3\. Multiplex Serum Cardiovascular Panel (EvePanel).



The datasets were matched and merged using participant identifiers and sampling timepoints.



Dataset characteristic| Description

Participants| 4

Sampling timepoints per participant| 7

Total sample observations| 28

Merged dataset columns| 136

Missing values| 102



Sampling Timeline



The seven sampling timepoints were:



\- L-92

\- L-44

\- L-3

\- R+1

\- R+45

\- R+82

\- R+194



The prefix L refers to measurements collected before launch, while R refers to measurements collected after return. Therefore, these observations represent pre-flight and post-flight sampling periods rather than continuous measurements during spaceflight.



3\. Methodology



The analysis was conducted using Python and the following libraries:



\- Pandas: data processing and organization.

\- NumPy: numerical calculations.

\- Matplotlib: data visualization.

\- SciPy: statistical testing.



The analysis followed these steps:



1\. Loaded and examined the three transformed NASA datasets.

2\. Matched records using participant identifiers and sampling timepoints.

3\. Merged the datasets into a unified table.

4\. Organized observations according to their sampling timeline.

5\. Calculated mean biomarker values at each timepoint.

6\. Calculated individual percentage changes relative to the L-92 baseline.

7\. Compared pre-flight and post-flight measurements at the participant level.

8\. Calculated Pearson correlation between hemoglobin and RBC count.

9\. Performed paired t-tests, calculated effect sizes, and estimated 95% confidence intervals.



Participant-Level Comparison



To avoid treating repeated observations from the same participant as independent individuals, the pre-flight observations were averaged for each participant. The same procedure was applied to post-flight observations.



This produced four participant-level pre-flight and post-flight pairs for the statistical analysis.



4\. Descriptive Results



4.1 Hemoglobin Timeline



The mean hemoglobin values across the seven sampling timepoints were:



Timepoint| Mean value

L-92| 14.38

L-44| 14.68

L-3| 14.08

R+1| 14.20

R+45| 14.48

R+82| 14.50

R+194| 14.15



The mean hemoglobin values showed fluctuations across the sampling timeline. The post-flight observations did not show a consistent increase or decrease across all timepoints.



4.2 Red Blood Cell Count Timeline



The mean RBC counts were:



Timepoint| Mean RBC count

L-92| 4.720

L-44| 4.742

L-3| 4.578

R+1| 4.770

R+45| 4.820

R+82| 4.800

R+194| 4.748



The mean RBC count varied across the timeline, with the highest mean observed at R+45.



5\. Correlation Analysis



Pearson correlation was used to examine the relationship between hemoglobin and RBC count across the 28 matched sample observations.



Result:



\- Pearson correlation coefficient: r = 0.972.



This indicates a strong positive association between hemoglobin and RBC count in the analyzed observations.



However, this correlation does not establish causation. The observations include repeated measurements from only four participants, so they should not be interpreted as 28 independent individuals.



6\. Participant-Level Pre-flight and Post-flight Comparison



The mean values for each participant were calculated separately for the pre-flight and post-flight phases.



6.1 Hemoglobin Participant| Pre-flight mean| Post-flight mean| Difference

C001| 14.567| 14.700| +0.133

C002| 12.500| 12.125| -0.375

C003| 13.633| 13.950| +0.317

C004| 16.800| 16.550| -0.250



The average participant-level difference was -0.0438, corresponding to an average percentage change of approximately -0.31%.



The direction of change differed between participants.



6.2 Red Blood Cell Count



Participant| Pre-flight mean| Post-flight mean| Difference

C001| 4.707| 4.788| +0.081

C002| 4.003| 3.997| -0.006

C003| 4.527| 4.822| +0.296

C004| 5.483| 5.530| +0.047



The average participant-level difference was +0.1044, corresponding to an average percentage change of approximately +2.24%.



Three participants showed an increase, while one showed a very small decrease.



7\. Statistical Analysis



Paired t-tests were performed using the four participant-level pre-flight and post-flight differences.



Biomarker| Mean difference| t-statistic| p-value

Hemoglobin| -0.0438| -0.2707| 0.8042

RBC count| +0.1044| 1.5752| 0.2133



Using a significance level of 0.05, neither comparison was statistically significant.



Effect Size



Cohen's dz was calculated to estimate the standardized magnitude of the paired differences.



Biomarker| Cohen's dz

Hemoglobin| -0.1353

RBC count| +0.7876



The hemoglobin effect size was small. The RBC effect size was larger in magnitude, but it must be interpreted cautiously because it was estimated from only four participants.



95% Confidence Intervals



Biomarker| Mean difference| 95% confidence interval

Hemoglobin| -0.0438| \[-0.5582, +0.4707]

RBC count| +0.1044| \[-0.1065, +0.3152]



Both confidence intervals include zero, which is consistent with the non-significant paired t-test results.



8\. Interpretation



The analyzed data show individual variation in hemoglobin and RBC count across the sampling timeline.



The average participant-level hemoglobin difference between the pre-flight and post-flight phases was small and negative. The average RBC difference was positive.



However, neither difference reached statistical significance. The results therefore do not provide sufficient evidence of a consistent phase-related change in these two biomarkers among the four participants.



The strong positive correlation between hemoglobin and RBC count is consistent with the fact that these measurements are biologically related. It should be interpreted as an association within this small repeated-measures dataset.



9\. Limitations



Several limitations should be considered:



1\. Small sample size: Only four participants were included, limiting statistical power.

2\. Repeated measurements: The 28 observations represent repeated samples from four participants, not 28 independent individuals.

3\. Exploratory analysis: The results should be considered preliminary and descriptive.

4\. Missing data: The merged dataset contains missing values in some variables. Missing values were not treated as zero.

5\. Limited biomarker scope: Although three datasets were merged, the statistical analysis presented here focuses primarily on hemoglobin and RBC count.

6\. Sampling intervals: The data represent discrete sampling timepoints, not continuous monitoring.

7\. Causal interpretation: The analysis cannot establish that spaceflight caused any observed biomarker changes.



10\. Conclusion



This exploratory analysis examined hemoglobin and red blood cell count measurements from four Inspiration4 participants across seven pre-flight and post-flight sampling timepoints.



The results showed individual variation and a strong positive correlation between the two biomarkers. However, participant-level paired statistical tests did not identify statistically significant differences between the pre-flight and post-flight phases.



The findings highlight the importance of analyzing individual variation and accounting for repeated measurements when studying astronaut health data.



A larger dataset with more participants and additional validated biomarkers would be necessary to investigate these patterns more reliably.



11\. Data Source NASA Open Science Data Repository (OSDR):

https://osdr.nasa.gov/



The analysis used the transformed Inspiration4 CBC, Comprehensive Metabolic Panel, and cardiovascular panel datasets available through the repository.

