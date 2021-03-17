# Author: Subaandh

import argparse
import random
import operator
import os
import concurrent.futures

class Painting():
    def __init__ (self, p_type, tag_size, tags, flag, index):
        self.p_type = p_type
        self.tag_size = tag_size
        self.tags = tags
        self.flag = flag
        self.index = index

class Store():
    def __init__(self, index, tags, flag):
        self.index = index;
        self.tags = tags;
        self.flag = flag

class Result():
    def __init__(self, index):
        self.index = index

def scorer(frame1,frame2):

        if len(frame1) == 0:
            return 0

        if len(frame2) == 0:
            return 0

        score = 0
        intersection = list(set(frame1).intersection(frame2))
        val1 = len(intersection)
        val2 = len(frame1)-len(intersection)
        val3 = len(frame2)-len(intersection)
        score += min(val1, val2, val3)

        return score

def find_painting(type, p_list):
    for i in reversed(range(len(p_list))):
        if p_list[i].flag == 1 or p_list[i].p_type != type:
            continue
        return i;

    return -1

def write_output(result):
    output = open("output_"+filename, "w")

    output.write(str(len(result)))
    output.write("\n")

    for i in result:
        for j in i.index:
            output.write(str(j))
            output.write(" ")
        output.writelines("\n")

    output.close()

def find_neighbour(prev, paint_list):
    max_index = []

    for i in range(len(paint_list)):
        if paint_list[i].p_type == 'P' and paint_list[i].flag == 0:
            vals = []
            tags = paint_list[i].tags
            vals.append(paint_list[i].index)
            paint_list[i].flag = 1

            index = find_painting('P', paint_list)
            tags.extend(x for x in paint_list[index].tags if x not in tags)
            vals.append(paint_list[index].index)
            paint_list[i].flag = 0

            score = scorer(prev.tags, tags)
            if score >= 1:
                max = score
                max_index.clear()
                max_index = vals
                paint_list[index].flag = 1
                paint_list[i].flag = 1
                del paint_list[index]
                del paint_list[i]

                return max_index

        else:
            score = scorer(prev.tags, paint_list[i].tags)

            if score >= 1:
                max = score
                max_index.clear()
                val = paint_list[i].index
                max_index.append(val)
                paint_list[i].flag = 1
                del paint_list[i]

                return max_index

    # If not able to find any index with score 1 return a random value
    i = random.randint(0, len(paint_list) - 1)
    val = paint_list[i].index
    max_index.append(val)
    paint_list[i].flag = 1

    if paint_list[i] == 'P':
        index = find_painting('P', paint_list)
        val = paint_list[index].index
        max_index.append(val)
        paint_list[index].flag = 1
        del paint_list[index]

    del paint_list[i]

    return max_index;

def compute1(p_list):
    result_list = []
    count = 0
    portrait = []

    for i in range(0, len(p_list)):
        if p_list[i].flag == 1:
            continue

        if p_list[i].p_type == 'L':
            result_list.append(Result([i]))
            p_list[i].flag == 1
        elif p_list[i].p_type == 'P':
            portrait.append(i)
            p_list[i].flag == 1

            if (len(portrait) == 2):
                result_list.append(Result(portrait.copy()))
                portrait.clear()

    return result_list

def only_landscape(p_list, l_list):
    score_prediction = 0
    result_list = []
    paint_list = l_list.copy()

    # Loop until length is zero
    while len(paint_list) > 0:
        print("Size: ", len(paint_list), '>', filename)
        index = 0
        if len(result_list) != 0:
            index = random.randint(0, len(paint_list) - 1)
        painting = paint_list[index]
        vals = []

        # Saving painting index tags and values if the result list is empty
        if len(result_list) == 0:
            vals.append(painting.index)
            tags = painting.tags

            result_list.append(Store(vals, tags, 0))
            del paint_list[index]

        else:
            # If result list is not empty we compare the next best score and add it
            prev_elem = result_list[len(result_list) - 1]

            max = 0
            max_index = []
            del_index = 0

            for i in range(len(paint_list)):
                current_elem = paint_list[i]
                score = scorer(prev_elem.tags, current_elem.tags)
                if score >= max:
                    max = score
                    max_index.clear()
                    val = current_elem.index
                    max_index.append(val)
                    del_index = i
                    if score > 1:
                        break

            score_prediction += max
            result_list.append(Store(max_index, p_list[max_index[0]].tags, 0))
            del paint_list[del_index]

    return result_list

def only_portrait(p_list, l_list):
    score_prediction = 0
    result_list = []
    paint_list = l_list.copy()

    # Loop until length is zero
    while len(paint_list) > 0:
        print("Size: ", len(paint_list), '>', filename)
        index = 0
        if len(result_list) != 0:
            index = random.randint(0, len(paint_list) - 1)

        painting = paint_list[index]

        vals = []
        tags = []

        # Saving painting index tags and values if the result list is empty
        if len(result_list) == 0:
            vals.append(painting.index)
            tags = painting.tags

            paint_list[index].flag = 1
            del paint_list[index]
            find_index = find_painting('P', paint_list)

            vals.append(paint_list[find_index].index)
            tags.extend(x for x in paint_list[find_index].tags if x not in tags)
            result_list.append(Store(vals, tags, 0))
            del paint_list[find_index]

        else:
            # If result list is not empty we compare the next best score and add it
            prev_elem = result_list[len(result_list) - 1]

            i = 0
            max = 0
            max_index = []
            del_index1 = 0
            del_index2 = 0

            while i < len(paint_list) - 1:
                current_elem1 = paint_list[i]
                current_elem2 = paint_list[i + 1]

                tags = current_elem1.tags
                tags.extend(x for x in current_elem2.tags if x not in tags)

                score = scorer(prev_elem.tags, tags)
                if score >= max:
                    max = score
                    max_index.clear()
                    max_index.append(current_elem1.index)
                    max_index.append(current_elem2.index)
                    del_index1 = i
                    del_index2 = i + 1

                    if len(current_elem2.tags) > len(current_elem1.tags):
                        break

                    if score > 4:
                        break
                i += 1

            result_list.append(Store(max_index, tags, 0))
            del paint_list[del_index1 : del_index2 + 1]

    return result_list

def compute_split(p_list):
    land_list = []
    port_list = []

    for i in p_list:
        if i.p_type == 'L':
            land_list.append(i)
        else:
            port_list.append(i)

    land_list.sort(key=operator.attrgetter('tag_size'))
    result_list = []

    # Version 1
    # result_list = only_landscape(p_list, land_list)

    # Version 2 (Best Score for all landscapes)
    divisor = 1
    if len(land_list) > 1000:
        divisor = 16
    middle = len(land_list) // divisor
    print(middle)
    chunks_list = []
    i = 0

    while i + middle < len(land_list) - 1:
        chunks_list.append(land_list[i: (i + middle)])
        i += middle

    chunks_list.append(land_list[i: ])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        process_list = [0 for i in range(len(chunks_list))]

        for i in range(0, len(chunks_list)):
            process_list[i] = executor.submit(only_landscape, p_list, chunks_list[i])

        for i in process_list:
            result_list.extend(i.result())

    # Version 1
    port_list.sort(key=operator.attrgetter('tag_size'))
    # i = 0
    # port_result = []
    # while i < (len(port_list) - 1):
    #     vals = []
    #
    #     vals.append(port_list[i].index)
    #     vals.append(port_list[i + 1].index)
    #
    #     tags = port_list[i].tags
    #     tags.extend(x for x in port_list[i+1].tags if x not in tags)
    #
    #     port_result.append(Store(vals, tags, 0))
    #     i += 2

    # random.shuffle(port_result)

    # Version 2 (Compute best score for portraits)
    divisor = 1
    if len(port_list) >= 10000:
        divisor = 16
    middle = len(port_list) // divisor
    print(middle)
    chunks_list = []
    i = 0

    while i + middle < len(port_list):
        chunks_list.append(port_list[i: (i + middle)])
        i += middle

    if i < len(port_list):
        chunks_list.append(port_list[i: len(port_list)])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        process_list = [0 for x in range(len(chunks_list))]

        for i in range(0, len(chunks_list)):
            process_list[i] = executor.submit(only_portrait, p_list, chunks_list[i])

        for i in process_list:
            result_list.extend(i.result())


    write_output(result_list)


def parse_painting(ip, count):
    p_type = ip.split(' ')[0]
    tag_size = int(ip.split(' ')[1])

    tags = [0 for i in range(tag_size)]
    for x in range(0, tag_size):
        tags[x] = ip.strip().split(' ')[2 + x]

    print(p_type, tag_size, tags)
    painting = Painting(p_type, tag_size, tags, 0, count)
    return painting

def main(path):
    global size, filename

    # Open File
    filename = os.path.basename(os.path.normpath(path))
    print("Filename is: ", filename)
    f = open(path)

    # Initialise Painting list object for input size
    size = int(f.readline())
    p_list = [0 for i in range(size)]
    selector_list = [i for i in range(size)]
    print("Number of Entries: ", size)
    count = 0

    # Loop through all lines
    for i in f.readlines():
        if (len(i.split(" ")) >= 2):
            # Parse and store values inside the painting object
            p_list[count] = parse_painting(i, count)
            count = count + 1

    compute_split(p_list)

if __name__ == "__main__":
    main()