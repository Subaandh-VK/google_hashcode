# Author: Subaandh

import subprocess
import Port_Landscape_main

def main():
    path = "./"
    files = ['0_example.txt', '10_computable_moments.txt', '11_randomizing_paintings.txt', '110_oily_portraits.txt', '1_binary_landscapes.txt']
    # files = ['0_example.txt', '10_computable_moments.txt']

    score = 0;

    for i in files:
        file_path = path + i
        Port_Landscape_main.main(file_path)

    i = 0;

    cmd = 'python score_checker.py '
    for i in files:
        path = cmd + i + " output_" + i
        print(path)
        output = subprocess.check_output(path)
        print("Score for :",i,"is: ", output.strip().decode())

        if (len(output.strip().decode().split()) == 4):
            score += int(output.strip().decode().split(" ")[3])
        else:
            print(output.strip().decode())

    print("***************Final Score: ", score ,"********************")
if __name__ == "__main__":
    main()