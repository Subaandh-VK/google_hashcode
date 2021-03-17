# Mind Chasers
# Subaandh Sambharathan Vellakinar Krishnakumar
# Audrey Chrysler
# Lin An
# Sreeja Lella

import argparse

class Scorer():

    def __init__(self,input_file,sub_file):

        self.frameglasses = {}
        self.sub = open(sub_file,"r")
        self.actual_frameglass = []
        self.prev_frameglass = []
        self.score = 0
        self.debug = False

        f = open(input_file, "r")
        for count, i in enumerate(f.readlines()[1:]):
            self.frameglasses[count] = i.split()

    def frameglass_checking(self,frameglass_elements):

        if len(frameglass_elements) == 1:
            if self.frameglasses[int(frameglass_elements[0])][0] == "L":
                tags = self.frameglasses[int(frameglass_elements[0])][2:]
                return tags
            else:
                print("ERROR WITH THE TYPE OF PAINTING")
        elif len(frameglass_elements) == 2:
            if self.frameglasses[int(frameglass_elements[0])][0] == "P" and self.frameglasses[int(frameglass_elements[1])][0] == "P":
                tags = list(set(self.frameglasses[int(frameglass_elements[0])][2:]+self.frameglasses[int(frameglass_elements[1])][2:]))
                return tags
            else:
                print("ERROR WITH THE TYPE OF PAINTING")
        else:
            print("ERROR WITH THE TYPE OF PAINTING")

    def exhibition_walk(self):

        for frame in self.sub.readlines()[1:]:

            self.actual_frameglass = self.frameglass_checking(frame.strip().split())
            if self.prev_frameglass != []:
                self.scorer(self.actual_frameglass, self.prev_frameglass)
            self.prev_frameglass = self.actual_frameglass

    def scorer(self,frame1,frame2):

        intersection = list(set(frame1).intersection(frame2))
        val1 = len(intersection)
        val2 = len(frame1)-len(intersection)
        val3 = len(frame2)-len(intersection)
        self.score += min(val1,val2,val3)

def main():
    parser = argparse.ArgumentParser(description="Script to check the score")
    parser.add_argument("input", type=str, help="The path to the input file")
    parser.add_argument("submit", type=str, help="The path to the submitted file")

    args = parser.parse_args()

    score = Scorer(args.input, args.submit)
    score.exhibition_walk()
    print("Final score = %s" %score.score)

if __name__ == "__main__":
    main()