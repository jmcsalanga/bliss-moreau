"""This program takes any number of .maoi files and converts them into .csv files,
using regular expressions to parse .maoi files, the csv module for writing to csv
files, and the sys module for taking in command-line arguments."""

import re
import csv
import sys

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
            x = re.findall('\t([A-Z]*?\s[0-9]*?\t[a-z]+)[0-9]*', elem)          
            x2 = re.findall('\t([A-Z]*?\s[0-9]*?\s\t[a-z]+)[0-9]*', elem)
            for elem in x:
                aoi_list.append(elem)
            for elem in x2:
                aoi_list.append(elem)

        aoi_list = [a.replace('\t', ' ') for a in aoi_list]                 # clean up aoi information

        cnt = 0
        for elem in frame_data_list:
            y = re.findall('-?\d+,|-?\d+:', elem)                           # find the coordinates
            frame = re.findall('(\d+)\t', elem)                             # find the frame number
            
            for elem in frame:
                frames_list.append(elem)

            for count, item in enumerate(y): 
                if (count % 2 == 0):
                    x_coords.append(item)
                else:
                    y_coords.append(item)

            x_coords = [x.replace(',', '') for x in x_coords]               # clean up coordinates
            y_coords = [y.replace(':', '') for y in y_coords]
            y_coords = [y.replace(',', '') for y in y_coords]

            points = list(zip(x_coords, y_coords))
            frame_index = frames_list[cnt]      
            frames_dict[frame_index] = points                               # dict holds the coordinates of each aoi related to a frame

            x_coords.clear()                                                
            y_coords.clear()
            cnt += 1

        cnt_= 1
        for aoi in aoi_list:
            aoi_dict = {}
            for key, value in frames_dict.items():
                if int(value[0][0]) is cnt_:
                    aoi_dict[key] = value[:(int(value[0][1])+1)]            # amount of coordinates up to the number of aoi vertices
                    frames_dict[key] = value[(int(value[0][1])+1):]         # update the frame dictionary so it moves forward (from aoi 1 to aoi 2)
            aoi_dicts_list.append(aoi_dict)
            cnt_ += 1

    csv_f = sys.argv[file_num].split(".")[0] + ".csv"                       # csv file created is "(name of input file).csv"
    open(csv_f, "a").close()
    
    with open(csv_f, "w") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL)
        column_title_row = ["Frame", "AOI", "Vertices", "Coordinates"]
        aoi_types = ", ".join(aoi_list)
        aoi_row = [aoi_types]                                               #gives information about the polygons
        wr.writerow(aoi_row)
        wr.writerow(column_title_row)
        
        for aoi1, aoi2 in zip(aoi_dicts_list, aoi_dicts_list[1:]):
            common_keys = set(aoi1.keys()) & set(aoi2.keys())
            for key in sorted(common_keys):                                 # keys in ascending numeric order
                wr.writerow([key, aoi1[key][0][0], aoi1[key][0][1],
                         aoi1[key][1:]])
                wr.writerow([key, aoi2[key][0][0], aoi2[key][0][1],
                         aoi2[key][1:]])
    file_num += 1

