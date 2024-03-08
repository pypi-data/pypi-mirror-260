from Orange.data import ContinuousVariable, DiscreteVariable
from Orange.data.io import FileFormat
from scipy.io import arff
import pandas as pd
from Orange.data.pandas_compat import table_from_frame, table_to_frame
import Orange.canvas.__main__


class ARFFReader(FileFormat):
    """Reader for ARFF files"""
    EXTENSIONS = ('.arff',)
    DESCRIPTION = 'ARFF file'
    SUPPORT_SPARSE_DATA = True

    def __init__(self, filename):
        super().__init__(filename)

    def read(self):
        data = arff.loadarff(self.filename)
        df = pd.DataFrame(data[0])
        out_data = table_from_frame(df)
        return out_data

    @classmethod
    def write_file(cls, filename, data):
        f = open(filename, "w")
        f.write("@relation " + data.name + "\n\n")
        for c in data.domain:
            f.write("@attribute " + str(c).replace(" ", "_") + " ")
            if isinstance(c, ContinuousVariable):
                f.write("real\n")
            elif isinstance(c, DiscreteVariable):
                f.write("{" + ",".join(c.values) + "}\n")
        f.write("\n@data\n")
        for i, elem in enumerate(data.X_df.iloc):
            f.write(",".join([str(x) for x in elem]))
            if not data.Y_df.empty:
                f.write("," + list(data.Y_df.orange_variables.values())[0].values[int(data.Y_df.iloc[i].iloc[0])])
            f.write("\n")
        f.close()


if __name__ == '__main__':
    Orange.canvas.__main__.main()
