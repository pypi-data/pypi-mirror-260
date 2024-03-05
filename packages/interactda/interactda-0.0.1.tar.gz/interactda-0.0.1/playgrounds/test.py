import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import KBinsDiscretizer, Binarizer, MaxAbsScaler
from tabular.dataset import TabularDataset
from imblearn.over_sampling import RandomOverSampler, SMOTE, SMOTENC, ADASYN
import plotly.express as px

# df = pd.read_csv("housing-prices-dataset_train.csv")
# cat_cols = [
#     col for col, dtype in TabularDataset(df).dtypes.items() if dtype == "category"
# ]
# num_cols = [
#     col for col, dtype in TabularDataset(df).dtypes.items() if dtype == "number"
# ]
# ros = ADASYN()
# df[num_cols] = df[num_cols].fillna(df[num_cols].mean())
# X_train, y_train = ros.fit_resample(df, df["MSZoning"])
# df = pd.concat([X_train, y_train], axis=1)
# fig = px.histogram(y_train)
# fig.show()
#
# fig2 = px.histogram(df["MSZoning"])
# fig2.show()
# import pandas as pd
# from tabular.prep import Preprocessing
#
# df = pd.read_csv("example-kagge_house_price_prediction.csv")
# prep = Preprocessing()
# pipeline = [
#     {
#         "action": "missing_values",
#         "targeted_cols": "number",
#         "method": "simple_imputer",
#         "strategy": "mean",
#         "args": {},
#     },
#     {
#         "action": "sampling",
#         "targeted_cols": "all",
#         "method": "over_sampling",
#         "strategy": "smotenc",
#         "args": {
#             "target": "MSZoning",
#             "k_neighbors": 5,
#         },
#     },
# ]
#
# prep.setup_pipeline(pipeline)
# prep.fit(df)
# transfromed_dfs = prep.transform([df])
# print(transfromed_dfs[0])
import pydantic
import pandas as pd
import sklearn
import imblearn
import category_encoders
import numpy

print(
    pydantic.VERSION,
    pd.__version__,
    sklearn.__version__,
    imblearn.__version__,
    category_encoders.__version__,
    numpy.__version__,
)
