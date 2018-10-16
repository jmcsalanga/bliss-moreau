"""This program takes any number of .maoi files and converts them into .csv files,
using regular expressions to parse .maoi files, the csv module for writing to csv
files, and the sys module for taking in command-line arguments."""

import re
import csv
import sys


def parse_list(regex, elem, list_to_change):
    x = re.findall(regex, elem)
    for elem in x:
        list_to_change.append(elem)
    return list_to_change


def clean_list(arg1, arg2, list_to_clean):
    list_to_clean = [a.replace(arg1, arg2) for a in list_to_clean]
    return list_to_clean


def create_csv(filename):
    # csv file created is "[filename].csv"
    csv_file_name = filename.split(".")[0] + ".csv"
    open(csv_file_name, "a").close()
    return csv_file_name


def write_csv(csv_file, list_of_aois, list_of_dicts):
    with open(csv_file, "w") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL)
        column_title_row = ["Frame", "AOI", "Vertices", "Coordinates"]
        aoi_types = ", ".join(list_of_aois)
        aoi_row = [aoi_types]  # gives information about the polygons
        wr.writerow(aoi_row)
        wr.writerow(column_title_row)

        for aoi1, aoi2 in zip(list_of_dicts, list_of_dicts[1:]):
            common_keys = set(aoi1.keys()) & set(aoi2.keys())
            for key in sorted(common_keys):  # keys in ascending numeral order
                wr.writerow([key, aoi1[key][0][0], aoi1[key][0][1],
                             aoi1[key][1:]])
                wr.writerow([key, aoi2[key][0][0], aoi2[key][0][1],
                             aoi2[key][1:]])


def main():
    file_num = 1
    for fn in sys.argv[1:]:                     # command-line functionality
        with open(fn, "r") as f:
            x_coords = []
            y_coords = []
            aoi_list = []
            aoi_dicts_list = []
            frames_list = []
            frames_dict = {}
            data = f.readlines()
            data_string = "".join(data)
            fr_data_index = re.search('\n\n', data_string).start()
            frame_data = data_string[(fr_data_index+7):(len(data_string)-1)]    # frames with coordinates
            aoi_data = data_string[:fr_data_index]                              # data about the shape of aois
    
            frame_data_list = frame_data.split("\n")
            aoi_data_list = aoi_data.split("\n")
        
            for elem in aoi_data_list:
                aoi_list = parse_list('\t([A-Z]*?\s[0-9]*?\t[a-z]+)[0-9]*', elem, aoi_list)
                aoi_list = parse_list('\t([A-Z]*?\s[0-9]*?\s\t[a-z]+)[0-9]*', elem, aoi_list)

            aoi_list = clean_list('\t', ' ', aoi_list)

            cnt = 0
            for elem in frame_data_list:
                y = re.findall('-?\d+,|-?\d+:', elem)                           # find the coordinates
                frames_list = parse_list('(\d+)\t', elem, frames_list)          # find the frame number

                for count, item in enumerate(y):
                    if count % 2 == 0:
                        x_coords.append(item)
                    else:
                        y_coords.append(item)

                x_coords = clean_list(',', '', x_coords)
                y_coords = clean_list(':', '', y_coords)
                y_coords = clean_list(',', '', y_coords)

                points = list(zip(x_coords, y_coords))
                frame_index = frames_list[cnt]
                # dict holds the coordinates of each aoi related to a frame
                frames_dict[frame_index] = points

                x_coords.clear()
                y_coords.clear()
                cnt += 1

            cnt_ = 1
            for aoi in aoi_list:
                aoi_dict = {}
                for key, value in frames_dict.items():
                    if int(value[0][0]) is cnt_:
                        # amount of coordinates up to the number of aoi vertices
                        aoi_dict[key] = value[:(int(value[0][1])+1)]
                        # update the frame dictionary so it moves forward (from aoi 1 to aoi 2)
                        frames_dict[key] = value[(int(value[0][1])+1):]
                aoi_dicts_list.append(aoi_dict)
                cnt_ += 1

        csv_f = create_csv(sys.argv[file_num])
        write_csv(csv_f, aoi_list, aoi_dicts_list)
        file_num += 1

main()
