import pytest
from tomodachi_core.tomodachi.services.high_low_profit_service import HighLowProfit
from tomodachi_core.testing.testdata.mockdata import people_data
from pandas import DataFrame

# Imported: people data from testing
# And then we create mock dataframe
df = DataFrame(people_data["people"])

# Do not forget to add DataFrame there
def test_high_low_service_init():
    service = HighLowProfit(df)
    assert service is not None

