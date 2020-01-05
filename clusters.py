#!/usr/bin/env python3
from math import sqrt
import dendrogram

debug = 0

class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.vec = vec
        self.left = left
        self.right = right
        self.distance = distance
        self.id = id

def readfile(filename):
    with open(filename) as fd: 
        lines = [line for line in fd] 
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        #First column in each row is the rowname
        rownames.append(p[0])
        #The data for this row is the remainder
        data.append([float(x) for x in p[1:]])
    
    return rownames, colnames, data

def euclideansqrt(v1, v2):
    return sum(map(lambda x: (x[0]-x[1])**2, zip(v1,v2)))

def euclidean(v1, v2):
    return euclideansqrt(v1,v2)

def pearson(v1, v2):
    # Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    # Sums of the squares
    sum1Sq = sum([pow(v,2) for v in v1])
    sum2Sq = sum([pow(v,2) for v in v2])

    # Sums of the products
    pSum = sum([v1[i]*v2[i] for i in range(len(v1))])

    # Calculate r (Pearson score)
    num = pSum-(sum1*sum2/len(v1))
    den = sqrt((sum1Sq-pow(sum1,2)/len(v1)) * (sum2Sq-pow(sum2,2)/len(v1)))
    if den==0: return 0

    return 1.0-num/den

def hcluster(rows, distance=pearson):
    distances={} # cache of distance calculations
    currentclustid=-1 # non original clusters have negative id

    # Clusters are initially just the rows
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]
    while len(clust)>1: #Stop when there is only one cluster left
        lowestpair = (0,1)
        closest = distance(clust[0].vec, clust[1].vec)
        #loop through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i+1, len(clust)):
                # distances is the cache of distance calculations
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)
                
                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i,j)
        
        # calculate the average of the two clusters
        mergevec = [ (clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i])/2.0
                for i in range(len(clust[0].vec))]
        # create new cluster
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]], 
                right=clust[lowestpair[1]], distance = closest, id = currentclustid)
        currentclustid-=1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]

def printclust(clust, labels=None, n=0):
    # indent to make a hierarchy layout
    for _ in range(n): print(" ", end='')
    if clust.id < 0:
        # negative id means that this is branch
        print("-")
    else:
        # positive id means that this is endpoint
        if labels == None: print(clust.id, end='')
        else: print(labels[clust.id], end='')
        
    # now print the left and right branches
    if clust.left != None:
        printclust(clust.left, labels=labels, n=n+1)
    if clust.right != None:
        printclust(clust.right, labels=labels, n=n+1)

def rotatematrix(data):
    return [list(a) for a in list(zip(*data[::-1]))]

def debugger(message):
    if(debug == 1): print(message)

def dend(data, label = None, filename = None):
    debugger("Clustering the data")
    clust = hcluster(data)
    debugger("Drawing the dendrogram")
    dendrogram.drawdendrogram(clust, labels = label, jpeg="imageclust.jpg")
    debugger("Finnished")

if __name__=='__main__':
    blognames, words, data = readfile("blogdata.txt")
    dend(rotatematrix(data), words)







