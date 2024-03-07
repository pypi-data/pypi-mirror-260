import csv
import logging
import os

from .file_utils import calculate_md5, get_file_creation_date
from .sqlite3_utils import (
    create_database,
    create_provenance_table,
    create_columnmaps_table,
    create_records_table,
    create_table,
    insert_columnmaps_table,
    insert_provenance_table,
    insert_records_table,
    insert_record,
)

DEFAULT_VERBOSE = False
DEFAULT_HEADER_LINE_NUMBER = 1
DEFAULT_NO_COLUMN_MAPPING = False


class Manager:
    """Class for parsing a tab-delimited file and loading its contents into a
    SQLite3 database instance."""

    def __init__(self, **kwargs):
        """Constructor for Manager."""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.database_file = kwargs.get("database_file", None)
        self.header_line_number = kwargs.get("header_line_number", DEFAULT_HEADER_LINE_NUMBER)
        self.infile = kwargs.get("infile", None)
        self.logfile = kwargs.get("logfile", None)
        self.no_column_mapping = kwargs.get("no_column_mapping", DEFAULT_NO_COLUMN_MAPPING)
        self.outdir = kwargs.get("outdir", None)
        self.table_name = kwargs.get("table_name", None)
        self.verbose = kwargs.get("verbose", DEFAULT_VERBOSE)

        if self.table_name is None:
            self.table_name = self._get_normalized_name(os.path.splitext(os.path.basename(self.infile))[0])
            logging.info(f"table_name was not defined and therefore was set to '{self.table_name}'")

        self.ignore_column_lookup = {}
        self._load_ignore_columns_lookup()

        logging.info(f"Instantiated Manager in file '{os.path.abspath(__file__)}'")

    def _load_ignore_columns_lookup(self) -> None:
        ignore_columns_list = self.config.get("ignore_columns", {})
        ctr = 0
        for column in ignore_columns_list:
            ctr += 1
            self.ignore_column_lookup[column] = True

        if ctr > 0:
            logging.info(f"Loaded '{ctr}' column names into the ignore column lookup")

    def load_records(self) -> None:
        """Parse the tab-delimited file and load into a SQLite3 database
        instance."""
        create_database(self.database_file)
        create_provenance_table()
        self._insert_provenance()

        if self.no_column_mapping:
            self._create_table_using_column_names()
        else:
            create_columnmaps_table()
            create_records_table()

            self._create_table_using_column_mappings()

    def _create_table_using_column_names(self) -> None:
        infile = self.infile

        if not os.path.exists(infile):
            raise Exception(f"file '{infile}' does not exist")

        header_to_position_index_lookup = {}
        position_index_to_header_lookup = {}
        column_names = []

        with open(infile) as f:
            reader = csv.reader(f, delimiter="\t")

            row_ctr = 0

            ignore_column_position_lookup = {}

            for row in reader:
                row_ctr += 1

                if row_ctr == self.header_line_number:
                    for column_position, column_name in enumerate(row):
                        if column_name in self.ignore_column_lookup:
                            logging.info(f"Ignoring column '{column_name}'")
                            ignore_column_position_lookup[column_position] = column_name
                            continue
                        normalized_name = self._get_normalized_name(column_name)
                        header_to_position_index_lookup[column_name] = column_position
                        position_index_to_header_lookup[column_position] = column_position
                        column_names.append(normalized_name)

                        # column_names.append("line_number")
                    create_table(self.table_name, column_names, self.config)

                    logging.info(f"Processed the header of tsv file '{infile}'")
                else:
                    line_ctr = row_ctr + 1

                    record = []
                    for column_position, value in enumerate(row):
                        if column_position in ignore_column_position_lookup:
                            continue

                        record.append(str(value))
                    # record.append(line_ctr)
                    insert_record(self.table_name, column_names, record, line_ctr)

            logging.info(f"Processed '{row_ctr}' records in tsv file '{infile}'")


    def _create_table_using_column_mappings(self) -> None:
        infile = self.infile

        if not os.path.exists(infile):
            raise Exception(f"file '{infile}' does not exist")

        with open(infile) as f:
            reader = csv.reader(f, delimiter="\t")

            row_ctr = 0

            ignore_column_position_lookup = {}

            for row in reader:
                row_ctr += 1

                if row_ctr == 1:
                    for column_position, column_name in enumerate(row):
                        if column_name in self.ignore_column_lookup:
                            logging.info(f"Ignoring column '{column_name}'")
                            ignore_column_position_lookup[column_position] = column_name
                            continue
                        normalized_name = self._get_normalized_name(column_name)
                        insert_columnmaps_table(
                            column_position, column_name, normalized_name
                        )

                    logging.info(f"Processed the header of tsv file '{infile}'")
                else:
                    line_ctr = row_ctr + 1

                    for column_position, value in enumerate(row):
                        if column_position in ignore_column_position_lookup:
                            continue
                        insert_records_table(line_ctr, column_position, value)

            logging.info(f"Processed '{row_ctr}' records in tsv file '{infile}'")

    def _get_normalized_name(self, column_name: str) -> str:
        """Derive a normalized column name for the column.

        This will replace all punctuation, symbols and spaces with underscores

        Args:
            column_name (str): the original column name

        Returns:
            str: the normalized column name
        """
        return (
            column_name.replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
            .replace("(", "_")
            .replace(")", "_")
            .replace("*", "_")
            .replace("&", "_")
            .replace("@", "_")
            .replace("#", "")
            .replace("!", "_")
            .replace("?", "_")
            .replace(".", "_")
            .replace("+", "_")
            .replace("-", "_")
            .replace("~", "_")
            .replace("[", "_")
            .replace("]", "_")
            .replace("{", "_")
            .replace("}", "_")
            .replace("|", "_")
            .replace(",", "_")
            .replace(";", "_")
            .replace("'", "_")
            .replace('"', "_")
        )

    def _insert_provenance(self) -> None:
        bytesize = os.path.getsize(self.infile)
        checksum = calculate_md5(self.infile)
        date_created = get_file_creation_date(self.infile)

        insert_provenance_table(
            bytesize, checksum, date_created, os.path.abspath(self.infile)
        )

    def add_header(self, outfile: str = None) -> None:

        count = 0

        with open(self.infile, 'r', encoding='utf-8') as file, open(outfile, 'w') as of:
            for line in file:
                count += 1
                line = line.rstrip("\n")

                if count == 1:
                    # Read the first line to determine the number of columns
                    columns = line.split('\t')
                    count = len(columns)
                    logging.info(f"Determined that there are '{count}' columns from the first line in the input file '{self.infile}'")
                    header_row = []
                    for i in range(count):
                        num = i + 1
                        header_row.append(f"col_{num}")
                    header = "\t".join(header_row)
                    of.write(f"{header}\n")
                of.write(f"{line}\n")


        logging.info(f"Wrote header row to file '{outfile}'")
        if self.verbose:
            print(f"Wrote header row to file '{outfile}'")

