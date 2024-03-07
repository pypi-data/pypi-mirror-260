import pandas as pd
import openpyxl
import re

class ServeExl:
    def __init__(self, input_filename, output_filename):
        self.input_filename = input_filename
        self.output_filename = output_filename

    def process_tnsnames(self):
        """
        Reads the TNSnames file, extracts data, and saves it to an Excel file.
        """
        with open(self.input_filename, 'r') as file:
            content = file.read().strip().split('\n\n')

        # Combine processing steps into a single method call
        results = self._process_connection_structures(content)

        df = pd.DataFrame(results)
        df.to_excel(f'{self.output_filename}.xlsx', index=False, header=["Database Name", "Server Name"])

    def _process_connection_structures(self, connection_structures):
        """
        Processes the connection structures and extracts database and server information.
        """
        Server_Databases_list = ['"""\n' + structure + '\n""",' for structure in connection_structures]
        results = []
        for connection_structure in Server_Databases_list:
            database_name, server_name = self.extract_database_info(connection_structure)
            results.append({"Database Name": database_name, "Server Name": server_name})
        return results

    def extract_database_info(self, connection_structure):
        host_match = re.search(r'\(HOST = ([^\)]+)\)', connection_structure)
        service_name_match = re.search(r'\(SERVICE_NAME = ([^\)]+)\)', connection_structure)

        if host_match and service_name_match:
            server_name = host_match.group(1)
            database_name = service_name_match.group(1)
            return database_name, server_name
        else:
            return None, None
