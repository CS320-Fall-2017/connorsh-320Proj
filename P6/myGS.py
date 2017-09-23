import sys
import json
import time
import generate_problems

class Man:
    name = ""
    prefList = []
    currentMatch = "False"

    def __init__(self, name, prefList):
        self.name = name
        self.prefList = prefList

class Woman:
    name = ""
    prefList = []
    currentMatch = "False"

    def __init__(self, name, prefList):
        self.name = name
        self.prefList = prefList

def write_json(obj, filename):
    with open(filename, mode='w') as f:
        json.dump(obj, f)

def read_json(filename):
    with open(filename) as f:
        return json.load(f)

def galeShapely(unMatchedMen,allWomen,allMen):

    matches = {}

    while len(unMatchedMen) > 0:
        findMatch(unMatchedMen.pop(),unMatchedMen,matches,allWomen,allMen)

    return matches

def findMatch(Man,unMatchedMen,matches,allWomen,allMen):

    while len(Man.prefList) > 0:

        nextHighestGirl = Man.prefList.pop()
        nextHighestGirl = findPerson(nextHighestGirl,allWomen)

        if womanAcceptsMan(Man, nextHighestGirl, unMatchedMen,allMen):

            Man.currentMatch = nextHighestGirl.name
            nextHighestGirl.currentMatch = Man.name
            matches[Man.name] = nextHighestGirl.name
            #unMatchedMen.remove(Man)

            return


def womanAcceptsMan(Man, Woman,unMatchedMen,allMen):
    if Woman.currentMatch == "False":
        return True
    elif Woman.prefList.index(Man.name) > Woman.prefList.index(Woman.currentMatch):
        current = findPerson(Woman.currentMatch,allMen)
        unMatchedMen.append(current)
        current.currentMatch = "False"
        return True
    else:
        return False

def findPerson(name, allWomen):
    for x in range (len(allWomen)):
        if(allWomen[x].name == name):
            return allWomen[x]

if __name__ == "__main__":

    #generate_problems.create_random_problems_json_file('myIn.json',2,[3000,5000],[{'group1':'a', 'group2':'b','verbose':True},{'group1':'j', 'group2':'k','verbose':True}],pretty_print=True)
    myInput = read_json(sys.argv[1])
    start_time = time.process_time()
    final_matches = []

    for x in range(0, len(myInput)):

        unMatchedMen = []
        allWomen = []
        allMen = []
        menList = list(myInput[x][0].keys())
        prefs = list(myInput[x][0].values())
        allWomenKeys = list(myInput[x][1].keys())
        womenPref = list(myInput[x][1].values())

        for y in range (len(menList)):

            tempWoman = Woman(allWomenKeys[y],womenPref[y])
            tempWoman.prefList.reverse()
            allWomen.append(tempWoman)

            tempMan = Man(menList[y], prefs[y])
            tempMan.prefList.reverse()
            unMatchedMen.append(tempMan)
            allMen.append(tempMan)

        final_matches.append(galeShapely(unMatchedMen,allWomen,allMen))


    end_time = time.process_time()

    print (final_matches)
    write_json(final_matches,sys.argv[2])

    print("\nRan in: {:.5f} secs".format(end_time - start_time))

