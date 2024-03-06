import pandas as pd


class KawaComputations:

    def __init__(self, kawa_client):
        self._k = kawa_client

    # TODO: Implement it, this is for demo purpose
    def compute(self,
                datasource_name,
                aggregation_method,
                measure,
                dimension,
                top=10,
                filtering=None):
        result = [
            {
                'director_name': 'Michael Bay',
                'budget': 1460000000
            },
            {
                'director_name': 'Steven Spielberg',
                'budget': 1450000000
            },
            {
                'director_name': 'Ridley Scott',
                'budget': 1130000000
            },
            {
                'director_name': 'Gore Verbinski',
                'budget': 1071000000
            },
            {
                'director_name': 'Robert Zemeckis',
                'budget': 1070000000
            },
            {
                'director_name': 'Christopher Nolan',
                'budget': 1005000000
            },
            {
                'director_name': 'Ron Howard',
                'budget': 954000000
            },
            {
                'director_name': 'Tim Burton',
                'budget': 947000000
            },
            {
                'director_name': 'Bryan Singer',
                'budget': 938000000
            },
            {
                'director_name': 'Martin Scorsese',
                'budget': 929600000
            }
        ][:top]

        return pd.DataFrame.from_records(result, index=['director_name'])
