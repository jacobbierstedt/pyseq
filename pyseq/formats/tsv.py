import os
import json
import ast

class TsvFormatException(Exception): pass

class Tsv(object):
    """
    Class to parse and handle data from tabular files. The data is stored in
    a list of dictionaries keyed by the name of the column names in the file.
    """
    DEFAULT_SEP = "\t"
    DEFAULT_NA_VALUE = None
    def __init__(self):
        super(Tsv, self).__init__()
        self.info      = []
        self.sep       = Tsv.DEFAULT_SEP
        self.na_values = [Tsv.DEFAULT_NA_VALUE, "None", "null", "", ".", "-"]
        self.na_value  = Tsv.DEFAULT_NA_VALUE
        self._n_fields = 0
        self.columns   = []

    def load_from_file(self, path, sep = "\t"):
        """
        Load Tsv object from file. Guess types and handle na values.
        :param path: path to file
        :param sep: field separator
        """
        self.sep = sep
        with open(path, "r") as f:
            self.columns = f.readline().strip().split(self.sep)
            self._n_fields = len(self.columns)
            for line in f:
                lss = line.strip().split(self.sep)
                if len(lss) != self._n_fields:
                    raise TsvFormatException(
                        f"Number of elements in row does not match number of elements in header. Offending line: {line}")
                data = {}
                for i in range(0, len(self.columns)):
                    val = self._get_type(lss[i])
                    data.update({self.columns[i] : val})
                self.info.append(data)

    def write_file(self, output_file: str, sep = "\t"):
        """
        Write output file.
        :param output_file: path to output file
        :param sep: field separator
        """
        with open(output_file, "w") as f:
            f.write(f"{sep.join(self.columns)}\n")
            for row in self.info:
                f.write(f"{sep.join([self._get_type_out(row[column]) for column in self.columns])}\n")


    def _get_type(self, value: str):
        """
        Method for guessing type of provided value
        :param value: string to guess type of
        """
        if len(value) < 1:
            return self.na_value
        if value[0] == "[" and value[-1] == "]":
            return json.loads(value)
        if value[0] == "{" and value[-1] == "}":
            return json.loads(value)
        try:
            value = ast.literal_eval(value)
        except:
            pass
        if any([value == i for i in self.na_values]):
            return self.na_value
        return value

    def _get_type_out(self, value) -> str:
        """
        Take value of any type and return it as string
        :param value: value to coerce to string
        """
        if any([value == i for i in self.na_values]):
            return str(self.na_value)
        if isinstance(value, dict) or isinstance(value, list):
            return json.dumps(value)
        if isinstance(value, set):
            return json.dumps(list(value))
        return str(value)

    def __str__(self):
        headers = self.sep.join([str(i) for i in self.info[0].keys()])
        values = "\n".join([self.sep.join([str(i) for i in row.values()]) for row in self.info])
        return headers + "\n" + values


# def main():
#
#     its = Tsv()
#     its.load_from_file("demo_tsv.tsv")
#     print(its)
#
#
#
# if __name__ == '__main__':
#     main()
