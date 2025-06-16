from sklearn.impute import SimpleImputer
from tomodachi_core.tomodachi.utils import analyze_and_fill_missing_values
from tomodachi_core.common_types.result import Result, Ok, Err
from tomodachi_core.common_types.option import Some, Option
from pandas import DataFrame, to_numeric
from pandas.api.types import is_numeric_dtype
from numpy.typing import NDArray

# preprocessing libraries
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer


class Preprocess:
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.df = DataFrame(X)
        self.num_transformer = StandardScaler()
        self.mini_max_scaler = MinMaxScaler()
        self.cat_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        self.pipeline = None

        # Save feature groups to use later
        self.num_features = None
        self.mini_max_feature = None
        self.cat_features = None

    def set_feature_groups(self, num_features=None, mini_max_feature=None, cat_features=None):
        self.num_features = num_features
        self.mini_max_feature = mini_max_feature
        self.cat_features = cat_features


    def _build_pipeline(self):
        transformers = []

        if self.num_features:
            transformers.append(('num', self.num_transformer, self.num_features))

        if self.mini_max_feature:
            transformers.append(('specific', self.mini_max_scaler, self.mini_max_feature))

        if self.cat_features:
            transformers.append(('cat', self.cat_transformer, self.cat_features))

        if not transformers:
            self.pipeline = make_pipeline(self.num_transformer)
        else:
            column_transformer = ColumnTransformer(transformers=transformers, remainder='drop')
            self.pipeline = make_pipeline(column_transformer)


    def fit_transform(self, X):
        self.X = X
        self._build_pipeline()
        return self.pipeline.fit_transform(self.X)


    def transform(self, X):
        if self.pipeline is None:
            raise ValueError("Pipeline is not fitted. Call fit_transform() first.")
        return self.pipeline.transform(X)
        

    def imputer_preprocess(self, strategy: str = 'mean', fill_value=None) -> Result[DataFrame, Exception]:
        """
        Imputes missing values in the dataset (self.X) based on the specified strategy.
        Also attempts to coerce invalid values (like strings in numeric columns) to NaN.

        Args:
            strategy (str): The imputation strategy: 'mean', 'median', 'most_frequent', or 'constant'.
            fill_value: The value to use when strategy='constant'.

        Returns:
            Ok(pd.DataFrame) or Err(Exception)
        """
        try:
            # Attempt to convert all numeric columns to float (non-convertible ones become NaN)
            self.X = self.X.apply(to_numeric, errors='coerce')

            imputer = SimpleImputer(strategy=strategy, fill_value=fill_value)
            imputed_data = imputer.fit_transform(self.X)

            # Replace original X with the cleaned version
            self.X = DataFrame(imputed_data, columns=self.X.columns)
            return Ok(self.X)
        except Exception as e:
            return Err(e)




class PreprocessData:
    @staticmethod
    def process_dataframe(df: DataFrame) -> DataFrame:
        return analyze_and_fill_missing_values(df)
    

    @staticmethod
    def preprocess(X, y):
        return Preprocess(X, y)


    @staticmethod
    def preprocess_df(df: DataFrame, strategy: Option[str], columns: Option[list[str]]) -> Result[DataFrame, Exception]:
        try:
            df_numeric = df.copy()
            
    
            all_numeric_cols = df.select_dtypes(include='number').columns.tolist()
            

            selected_cols = (
                [col for col in columns if col in all_numeric_cols]
                if columns is not None
                else all_numeric_cols
            )

            if not selected_cols:
                return Ok(df_numeric)
            
            # Coerce to numeric and impute
            numeric_data = df_numeric[selected_cols].apply(to_numeric, errors='coerce')
            imputer = SimpleImputer(strategy=strategy or "mean")
            imputed_array = imputer.fit_transform(numeric_data)
            imputed_df = DataFrame(imputed_array, columns=selected_cols, index=df_numeric.index)

            df_numeric[selected_cols] = imputed_df
            
            return Ok(df_numeric)
        except Exception as e:
            return Err(e)


        