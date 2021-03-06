## @file buildIndex.py
#  @brief Simple setup and building of index for ES using Python.
#

FILE_URL = "http://googledrive.com/host/0B351HZYtYt77fm1JclhTUGttLVktdGh6STRRdHV1WDNzN1VwQ0hsQWZoTGM3ZThuSHRVbDA/outputIndex.csv"
ES_HOST = {
    "host" : "localhost", 
    "port" : 9200
}

INDEX_NAME = 'imagerepo'
TYPE_NAME = 'image'

ID_FIELD = 'imagename'

import csv
import urllib2
import cv2

from elasticsearch import Elasticsearch

# Read the URL
response = urllib2.urlopen(FILE_URL)
# Store the csv object from index csv file
csvFileObject = csv.reader(response, delimiter='|')

# Extract the header from the csv file
header = csvFileObject.next()
header = [item.lower() for item in header]




bulkData = []
# Move the data into dictionary format that ES python likes
for row in csvFileObject:
    print row
    dataDict = {}
#     dataDict['color'] = {}
    for i in range(len(row)):
        if 'im' not in row[i]:
            dataDict[header[i]] = int(row[i])
        else:
            dataDict[header[i]] = row[i]
    print "data", dataDict
    # Meta data dictionary for the operation
    optDict = {
        "index": {
                  "_index": INDEX_NAME, 
                  "_type": TYPE_NAME, 
                  "_id": dataDict[ID_FIELD] 
                  }
               }
    # Populate bulk data dictionary 
    bulkData.append(optDict)
    bulkData.append(dataDict)
    
# Create ES client with index
es = Elasticsearch(hosts = [ES_HOST])

# If index already exists, delete and recreate
if es.indices.exists(INDEX_NAME):
    print("deleting '%s' index..." % (INDEX_NAME))
    res = es.indices.delete(index = INDEX_NAME)
    print(" response: '%s'" % (res))
    
# Local client with one shard configuration
requestBody = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}

print("creating '%s' index..." % (INDEX_NAME))

# Create the index 
res = es.indices.create(index = INDEX_NAME, body = requestBody)
print(" response: '%s'" % (res))

# bulk index the data
print "bulk indexing..."
res = es.bulk(index = INDEX_NAME, body = bulkData, refresh = True)

# sanity check
# res = es.search(index = INDEX_NAME, size=2, body={"query": {"match_all": {}}})
# print(" response: '%s'" % (res))
# 
# print "results:"
# for hit in res['hits']['hits']:
#     print(hit["_source"])

res = es.search(index = INDEX_NAME, size=7000, body={    
    "query": {
        "bool": {
            "must": [
                {
                    "range": {
                        "h1": {
                            "gt": "280",
                            "lt": "340"
                        }
                    }
                },
                {
                    "range": {
                        "s1": {
                            "gt": "20"
                        }
                    }
                },     
                {
                    "range": {
                        "v1": {
                            "gt": "50"
                        }
                    }
                },
                    
                
            ]
        }
    }
            })
print(" response: '%s'" % (res))


hits = []
for hit in res['hits']['hits']:
    print("h1:", hit["_source"]["h1"])
    hits.append((hit["_source"]["imagename"]))


print(len(hits), 'hits') 
print(es.count(index='imagerepo')['count'], 'documents in index')

for img in hits:
    myImage = cv2.imread( "../../images/flickr/"+img)
    cv2.imshow("result", myImage)
    cv2.waitKey(500)

    
    

    
