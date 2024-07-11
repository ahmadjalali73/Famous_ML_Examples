In this dataset, we have some data about Loan Approval.  List of columns are:

|NUM|Column|Non-Null|Count|Dtype|
|---|------|--------|-----|-----|
|0|Loan_ID|614|non-null|object| 
|1|Gender|601| non-null|object| 
| 2|Married            |611| non-null|    object |
| 3|Dependents         |599| non-null|   object |
| 4|Education          |614| non-null|    object |
| 5|Self_Employed      |582| non-null|    object |
| 6|ApplicantIncome    |614| non-null|    int64  |
| 7|CoapplicantIncome  |614| non-null|    float64|
| 8|LoanAmount         |592| non-null|    float64|
| 9|Loan_Amount_Term   |600| non-null|    float64|
| 10|Credit_History     |564| non-null|    float64|
| 11|Property_Area      |614| non-null|    object |
| 12|Loan_Status        |614| non-null|    object |

 we are trying to guess "Loan_Status" column. In our code we will try many famous models and select the best model for our dataset. our metrics are accuracy and F1-Score.

 For using this code, you should have 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn' and 'xgboost'.
 you can install them using pip. 

 our final result is:
 
 |Model|F1-Score|Accuracy|
 |-----|--------|--------|
 |XGBClassifier|76%|74%|