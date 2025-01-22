ELSAfrailty
📚 Overview 📚
Rocking up with different ML methods to look at predictors of frailty in the UK using the ELSA wave 8 (for now) dataset.

🛠️ Prerequisites 🛠️
Python 3.x
Required Python packages: 'pandas', 'numpy',
🚀 What has been done so far 🚀
Categorize participants based on fraily status (n = 3180)
Wave 6 Wave 8
non-frail 1490 1406
pre-frail 1616 1646
frail 74 128
🚀 What needs to be done 🚀
Preprocessing

Extract relevant data from potential predictor variables
Naturally, use the primary key "idauniq" to reduce the df of this new df.
Remove all frailty values (and the ones that could also be used, but we didn't use. (e.g., BMIcat)
Figure out what variables to include. Determine missingness Machine Learning EDA
Balance data SMOTE?
multiple imputation by chained equations (MICE)?
How to run
Steps:

You need one h_elsa_g3.tab file put in the tab folder in the project
You need to install python packages which I will put in the requirements.txt
You can use the elsawave6and8_frailtycategorization.py to preprocess the raw data as well as extract some of the parameters.
