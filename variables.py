import pandas as pd


df = pd.read_csv("https://raw.githubusercontent.com/shogoBCN/datasets/main/churn_data.csv")
df.dropna(inplace=True)
df.drop(columns=["RowNumber", "CustomerId", "Surname"], inplace=True)

bins_age = [0, 25, 35, 65, 110]
labels_age = ["graduade", "regular", "senior", "retired"]
df["Age-Cat"] = pd.cut(df["Age"], bins=bins_age, labels=labels_age, right=False)

bins_ten = [0, 2, 4, 7, 100]
labels_ten = ["short", "mid", "long", "vip"]
df["Tenure-Cat"] = pd.cut(df["Tenure"], bins=bins_ten, labels=labels_ten, right=False)

bins_ten = [0, 579, 669, 739, 799, 900]
labels_ten = ["very poor", "poor", "good", "very good", "excellent"]
df["Score-Cat"] = pd.cut(df["CreditScore"], bins=bins_ten, labels=labels_ten, right=False)

for cat in [ "Age-Cat", "Tenure-Cat", "Score-Cat" ]:
    df[cat] = df[cat].str.title()

new_col_names = {
    "CreditScore": "Credit Score",
    "NumOfProducts": "Product Count",
    "HasCrCard": "Credit Card",
    "IsActiveMember": "Active Member",
    "EstimatedSalary": "Estimated Salary",
    "Exited": "Churned",
    "Age-Cat": "Age Class",
    "Tenure-Cat": "Tenure Class",
    "Score-Cat": "Credit Score Class"
    }

df.rename(columns = new_col_names, inplace = True)

table_dict_list = [ {"name": feature, "id": feature} for feature in df.columns ]

option_dict = {}
for cat in df.select_dtypes(include=["object", "category"]).columns:
    key = cat
    val = [ "All", *df[cat].unique() ]
    option_dict.update({key: val})

option_dict_num = {}
for cat in df.select_dtypes(include=["float64", "int64"]).columns:
    key = cat
    val = [ "All", *df[cat].unique() ]
    option_dict_num.update({key: val})

option_dict_all = {}
for cat in df.columns:
    key = cat
    val = [ "All", *df[cat].unique() ]
    option_dict_all.update({key: val})

churn_rate_list = [ "Geography", "Gender", "Credit Score Class", "Age", "Age Class", "Tenure", "Tenure Class", "Product Count" ]

dist_list = [ "Geography", "Credit Score", "Credit Score Class", "Age", "Age Class", "Tenure", "Tenure Class", "Product Count", "Balance", "Estimated Salary", "Churned" ]

scatter_list = [ "Credit Score", "Age", "Balance", "Estimated Salary"]

print(df.info())