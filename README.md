# NeXus Central 

I renamed my monorepo! However, for consistency, I keep the old name "Tomodachi" still operable. Soon, I will fix it.

## Deployed:

You can check out the first release (I am still processing): [tomodachi](https://test.pypi.org/project/tomodachi/0.1.4/)

To install, you can open up Git Bash and enter

```sh
pip install -i https://test.pypi.org/simple/ tomodachi==0.1.4
```

Using Python 3.13.2, it will install the package. You can confirm by 

```sh
python
```

- a command for the Git Bash. Then you can enter the Python shell:

```python
from tomodachi_core.tomadachi.services import PandasService

try:
	service = PandasService("some path")
	service.load_csv_data()
	df = service.df
	print(df.head())
except PathNotFoundError as e:
	print("Path was not found")
	# we can develop more functionality to the service
	# to process no path scenario
	exit()
```

So, as you can see, the package works as long as you provide the path. Tests were NOT added to the file, hence we can see it is the correct way of working with Python package. So, our code will work, as tests show `Ok`.

## Docs

Please, refer to the [documentation](/docs/README.md) for further information
