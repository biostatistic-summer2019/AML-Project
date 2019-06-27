import csv
import random
import math
import operator


def loadDataset(filename, splitOne, splitTwo, trainingSet=[], testSet=[], noTouchSet =[]):
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file, delimiter = ',')
        
        genes = next(csv_reader)
        #print(len(genes))
        dataset = list(csv_reader)
        count1 = 0
        count2 = 0
        for x in range(len(dataset)):
            rand = random.random()
            for z in range(0,1):
                if x < 45:
                    dataset[x][z] = "0"
                else:
                    dataset[x][z] = "1"
                
            for y in range(1,472):
                dataset[x][y] = float(dataset[x][y])

            if rand < splitOne:
                count1 += 1
                trainingSet.append(dataset[x])

            if rand > splitOne and rand < splitTwo:
                count2 += 1
                testSet.append(dataset[x])

            if rand > splitTwo:

                noTouchSet.append(dataset[x])


def euclideanDistance(instance1, instance2):
    distance = 0
    for x in range(1, 472): 
        distance += pow((instance1[x] - instance2[x]), 2)
        
    return math.sqrt(distance)


def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance)-1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x])
        distances.append((trainingSet[x], dist))
    distances.sort(key = operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][0]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][0] == predictions[x]:
            correct += 1
    return (correct/float(len(testSet))) * 100.0
        





def main():
    trainingSet = []
    testSet = []
    noTouchSet = []

    splitOne = 0.60
    splitTwo = 0.85

    loadDataset("clinical_9A_standard_low_risk_sd3_CSV.csv", splitOne, splitTwo, trainingSet, testSet, noTouchSet)

    print("Train set: " + str(len(trainingSet)))
    print("Test set: " + str(len(testSet)))
    print("No Touch set " + str(len(noTouchSet)))

    # Generate predictions
    predictions = []
    k = 5
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
        #print("> predicted = " + repr(result) + ", actual = " + repr(testSet[x][0]))
    accuracy = getAccuracy(testSet, predictions)
    noTouchAccuracy = getAccuracy(noTouchSet, predictions)
    print("Accuracy: " + repr(accuracy) + "%")
    print("No Touch Accuracy: " + repr(noTouchAccuracy) + "%")
    return [accuracy, noTouchAccuracy]
    
main()


