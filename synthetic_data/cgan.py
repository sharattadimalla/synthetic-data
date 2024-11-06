import pandas as pd
from sdv.single_table import CTGANSynthesizer
from sdv.metadata import Metadata


class CTGANSyntheticData:

    def __init__(self, df: pd.DataFrame = None, num_records: int = 200):
        print(f"INFO: Intializing CTGANSynethicData class")
        self.df = self._get_data()
        self.num_records = num_records
        self.metadata = self._get_metadata()
        self.synthetic_data = self._generate_ctgan_sample()

    def _get_data(self):
        df = pd.read_csv("output/customer_synthetic_data.csv")
        print(f"INFO: df sample data")
        df.head()
        return df

    def _get_metadata(self):
        metadata = Metadata.detect_from_dataframe(data=self.df, table_name="person")
        print(f"INFO: Metadata {metadata}")
        return metadata

    def _generate_ctgan_sample(self):
        synthesizer = CTGANSynthesizer(self.metadata)
        synthesizer.fit(self.df)
        print(f"INFO: Completed Training CTGAN")
        synthetic_data = synthesizer.sample(num_rows=self.num_records)
        print(f"INFO: Completed sample generation using CTGAN")
        return synthetic_data
