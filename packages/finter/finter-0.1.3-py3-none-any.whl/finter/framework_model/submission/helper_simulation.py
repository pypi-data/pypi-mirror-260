import json
from enum import Enum

import pandas as pd

from finter.framework_model.simulation import adj_stat_container_helper
from finter.utils.timer import timer


@timer
def run_simulation(model_info, start, end, **kwargs):
    defaults = {
        "volcap_pct": 1,
        "decay": 1,
        "cost_list": ["hi_low", "fee_tax"],
        "slippage": 10,
        "return_calc_method": "arithmetic",
        "turnover_calc_method": "diff",
        "booksize": 1e8,
        "close": True,
        "adj_dividend": False,
    }

    for key, value in defaults.items():
        kwargs.setdefault(key, value)

    model_stat = adj_stat_container_helper(
        model_info=model_info, start=start, end=end, **kwargs
    )

    return ModelStat(model_stat)


class ModelStat:
    class Frequency(Enum):
        WholePeriod = "WholePeriod"
        Yearly = "Yearly"
        HalfYearly = "HalfYearly"
        Quarterly = "Quarterly"
        Monthly = "Monthly"
        Weekly = "Weekly"
        Daily = "Daily"

    def __init__(self, model_stat):
        """Initialize the ModelStat object with statistical data.

        Parameters:
        - statistics: A dictionary containing statistical data.
        """
        self.model_stat = model_stat

    def extract_statistics(self, frequency):
        """Extracts statistics for a given frequency.

        This method transforms statistical data into a DataFrame based on the specified frequency.

        Parameters:
        - frequency (str): The frequency for the statistical data. Must be one of the following:
            - 'WholePeriod'
            - 'Yearly'
            - 'HalfYearly'
            - 'Quarterly'
            - 'Monthly'
            - 'Weekly'
            - 'Daily'

        Returns:
        - A pandas DataFrame containing the statistical data for the specified frequency.

        Raises:
        - ValueError: If the frequency is not one of the valid options.
        """
        try:
            frequency = self.Frequency(frequency).value
        except ValueError:
            valid_options = ", ".join(
                [f"'{option.value}'" for option in self.Frequency]
            )
            raise ValueError(
                f"Frequency must be one of the following: {valid_options}. Please choose one."
            ) from None

        parsed_json = json.loads(self.model_stat["statistics"][frequency])

        df = pd.DataFrame(
            parsed_json["data"],
            columns=parsed_json["columns"],
            index=pd.to_datetime(parsed_json["index"]),
        )
        df.index = pd.to_datetime(df.index).to_series().apply(lambda x: x.date())

        return df

    def cummulative_return(self):
        cum_ret = pd.read_json(self.model_stat["cum_ret"], orient="records").set_index(
            "index"
        )["data"]
        cum_ret.index = (
            pd.to_datetime(cum_ret.index).to_series().apply(lambda x: x.date())
        )
        cum_ret.plot()

        return cum_ret
