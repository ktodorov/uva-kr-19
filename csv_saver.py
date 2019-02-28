import utils
import statistics

class CSVSaver():
    def __init__(self, file_name: str, value_lists: list):
        self.file_name = file_name
        self.value_lists = value_lists

    def average_experiment_dict(self, experiment_dict):
        max_chunks = 250
        for i in range(10):
            if len(experiment_dict[i]) > 0:
                experiment_dict[i] = utils.average_chunks(experiment_dict[i], max_chunks)

        return experiment_dict

    def save_to_file(self, title: str):
        output_file_1 = open(self.file_name, "w")

        output_file_1.write(f'{title}\n')
        output_file_1.write("\n")
        output_file_1.write("max,min,median,stdev,mean,whole_list,\n")

        for value_list in self.value_lists:

            listbuilder = ""
            for element in value_list:
                listbuilder = listbuilder + str(element) + ","

            max_value = max(value_list)
            min_value = min(value_list)
            median = statistics.median(value_list)
            mean = statistics.mean(value_list)
            stdev = statistics.stdev(value_list)

            bin_output = f'{max_value},{min_value},{median},{stdev},{mean},{listbuilder},\n'
            output_file_1.write(bin_output)

        output_file_1.write("\n")
        output_file_1.write("\n")
        output_file_1.close()