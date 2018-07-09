from classes.converters.converter import Converter
import sqlite3
import pandas as pd
from classes.commons.utils import print_debug, get_data_sql_query

class ARCMAConverter(Converter):

    def load_data(self):
        #Carregando os arquivos
        self.load_csv_files(0, ",")

        #Percorrendo os arquivos carregados e armazenando as linhas
        time = 0
        for index_csv, csv_file in enumerate(self.csv_files):
            for index_row, row in enumerate(csv_file):
                self.readings.append({"time": time, "x": row[1], "y": row[2], "z": row[3], "activity": row[4]})
                time = time + 1

        print_debug(self.readings[0])
        print_debug("Readings length: {}".format(len(self.readings)))
        print_debug("Converting to DataFrame...")
        self.data_frame = pd.DataFrame(self.readings)
        print_debug("Conversion completed!")

    def save_to_sql(self, filename, dataset_name):
        print_debug("Connect to SQLITE...")
        dataset = sqlite3.connect(filename)
        print_debug("Converting DataFrame to SQL...")
        self.data_frame.to_sql(dataset_name, dataset, if_exists='replace', index=False)
        print_debug("SQLITE Conversion completed!")
        dataset.close()

    #filename = name of sqlite db file
    def get_readings_by_activity(self, filename, activity):
        dataset = sqlite3.connect(filename)
        query = "select * from arcma where activity = {} order by time".format(activity)
        print(query)
        return get_data_sql_query(query, dataset)