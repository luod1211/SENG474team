import re
import csv
import time

'''
Compute the jacccard similarity between two lists
which is intersection/union

parameter1: first list being compared
parameter2: second list being compared

return the float value of the jaccard similarity of two lists
'''
def jaccard(line1, line2):
    intersection = len(list(set(line1).intersection(set(line2))))
    union = (len(set(line1))+len(set(line2))-2) - intersection
    if union <= 0:
        return 0
    return float(intersection)/union

'''
parse the words from lines read to individual words for comparison

parameter1: the lines read from files
parameter2: the list for the parsed words
'''
def parse_words(lines ,questions):
    #counter for the lines
    lineCount = 0
    #confirm qids and questions exist, then parse the words
    for line in lines:
        if (len(line.split('\t')) == 2) and line.split('\t')[0].isdigit():
            questions.append([])
            questions[lineCount].append(line.split('\t')[0])
            for word in line.split('\t')[1].split(' '):
                #remove extra characters from words
                newWord = re.sub(r'[^\w]', '', word)
                questions[lineCount].append(newWord)
            lineCount += 1

def main():
    t0 = time.perf_counter()
    lines = [line.rstrip('\n') for line in open('./question_4k.tsv')]
    questions = []
    #parse lines so questions has individual words
    parse_words(lines,questions)

    #table with qids and corresponding similar ids
    simids = []
    idcount = 0

    #writing the results to tsv file
    output = open('./question_sim_4k.tsv', "w")
    output.write("qid" + '\t' + "similar-qids\n")
    tsv_writer = csv.writer(output, delimiter=',')
    for line in questions:
        output.write(line[0] + '\t')
        simids.append([])
        for line2 in questions:
            if (jaccard(line, line2) >= 0.6) and (line2[0] != line[0]):
                simids[idcount].append(line2[0])
        tsv_writer.writerow(simids[idcount])
        idcount += 1

    output.close()

    print(time.perf_counter()-t0)

main()