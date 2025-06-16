# Documentation to Read files

## Set up service

First of all, we have to set up the service:

```python
from tomodachi_core.tomodachi.services import PandasService

service = PandasService() # throws error because it needs the path
```

As of tomodachi 0.1.4 release, it does not work. It will raise the error, because
it expects the path variable passed to the constructor of the `PandasService`. As such,

```python
service = PandasService("path/to/csv") # or any other file
```

For example, nothing should stop us from 

```python
service = PandasService("path/to/python/module") 
```

or

```python
service = PandasService(data={"key":"val"}, path="path/to/csv") # future suggestions for the release 0.1.5
```

After you specified the correct path, you can call `load_csv_data` method on the service:

```python
service.load_csv_data()
```

This will load the CSV data using `Pandas.read_csv`. Nothing special here. 

## Using context manager

You can also access the data using the contextmanager:

```python
with PandasService("path/to/csv").connection() as df:
    print(df.head())

with PandasService("another/path/to/csv").use_cached_data() as df:
    print(df.describe())
```

## Conclusion

In order to read the file, we have to instantiate the service, provide the correct file and then load the data to the 
Pandas DataFrame, and then we can work with it

## Suggestion

I can enhance my context manager idea to include another one:

```python
class PandasService:
    def use_temporary_df(self, use_mock_data: bool = False) -> Generator[pd.DataFrame, None, None]:
        # create empty data frame
        if not use_mock_data:
            df = pd.DataFrame() # default
            yield df
        else:
            try:
                from tomodachi_core.tomodachi.tests.testdata import mock_data
                df = pd.DataFrame(data=mock_data)
                yield df
            except ImportError as e:
                # create test dictionary
                mock_data = [{"name": "Alice", "profession": "teacher", "salary": "3200 EURO"}, {"name": "John", "profession": "zookeeper", "salary": "4000 USD"}]
                yield pd.DataFrame(mock_data, index=["Employees"])
```

This example is a suggestion.


