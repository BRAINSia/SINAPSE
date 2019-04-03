import glob
import csv

if __name__ == "__main__":
    # TODO: IF NEEDED, Replace glob.glob("pattern") with your own pattern to get your desired putamen files
    putamen_files = glob.glob("/Shared/johnsonhj/2018Projects/20181002_LesionMappingBAW/20181017_niftinet_data_inputs/images/*putamen_dense_seg.png")
   # TODO: IF NEEDED, Replace the csv_file variable with your desired output variable 
    csv_file = "/Shared/johnsonhj/2018Projects/20181112_RecodeLabelMaps/src/Identify_Putamen/available_putamen.csv"
    with open(csv_file, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(["file_path"])
        i = 0
        for file_path in putamen_files:
            writer.writerow([file_path])
            i += 1
        writer.writerow(["0"])
    print("Wrote {0} file paths".format(i))
    print("done")
