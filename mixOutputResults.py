def mixOutputResults():
    resultFile = open("results.txt", "w")
    for i in range(2, 10):
        with open('output/tlsredbadbehaviour1000_' + str(i) + '.txt') as fp:
            for line in fp:
                resultFile.write(line)
        fp.close()

    for i in range(1, 10):
        with open('output/tlsredgoodbehaviour1000_' + str(i) + '.txt') as fp:
            for line in fp:
                resultFile.write(line)
        fp.close()

mixOutputResults()