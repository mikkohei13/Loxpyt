import base64
import io
import json
import requests

import pprint
import math


# Based on https://cloud.google.com/vision/automl/docs/containers-gcs-tutorial
def container_predict(image_file_path, image_key):
  
  automlDockerServiceName = "automl-model"
  automlDockerPortNumber = "8501"

  """Sends a prediction request to TFServing docker container REST API.

  Args:
      image_file_path: Path to a local image for the prediction request.
      image_key: Your chosen string key to identify the given image.
      port_number: The port number on your device to accept REST API calls.
  Returns:
      The response of the prediction request.
  """

  with io.open(image_file_path, 'rb') as image_file:
      encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

  # The example here only shows prediction with one image. You can extend it
  # to predict with a batch of images indicated by different keys, which can
  # make sure that the responses corresponding to the given image.
  instances = {
          'instances': [
                  {'image_bytes': {'b64': str(encoded_image)},
                    'key': image_key}
          ]
  }

  # This example shows sending requests in the same server that you start
  # docker containers. If you would like to send requests to other servers,
  # please change localhost to IP of other servers.
  url = "http://" + automlDockerServiceName + ":" + automlDockerPortNumber + "/v1/models/default:predict"

  response = requests.post(url, data=json.dumps(instances))
  return response.json()



def leadingZeros(number):
  number = str(number)
  number = number.zfill(5)
  return number
  

def toDict(predictionJson):
  resultDict = {}
  resultDict["fileKey"] = predictionJson["predictions"][0]["key"]
  resultDict["labels"] = {}

  n = 0
  for i in predictionJson["predictions"][0]["labels"]:
    resultDict["labels"][i] = predictionJson["predictions"][0]["scores"][n]
    n = n + 1

  return resultDict

def toHumanReadable(predictionDict):
  text = predictionDict["fileKey"] + " "

  animalScoreInt = math.floor(predictionDict["labels"]["animal"] * 20)
  noAnimalScoreInt = math.floor(predictionDict["labels"]["no-animal"] * 20)
  scoreBar = ""

  for h in range(animalScoreInt):
    scoreBar += "#"
  
  for h in range(noAnimalScoreInt):
    scoreBar += "-"

#  scoreBar = scoreBar.ljust(22, " ")

  text += scoreBar + "   animal: " + str(round(predictionDict["labels"]["animal"], 2)) + ",  no-animal: " + str(round(predictionDict["labels"]["no-animal"], 2))
  return text


# --------------------------------------------

print("Start\n")

for x in range(0, 36):
  fileNumberString = leadingZeros(x)
  filePath = "../../_exports/20190505-06-Ks-SM4/HLO10_20190505_230000.wav." + fileNumberString + ".png"
  fileKey = fileNumberString

  # Predict
  predictionJson = container_predict(filePath, fileKey)

  # Format results
  resultDict = toDict(predictionJson)
  print(toHumanReadable(resultDict))

#  pp = pprint.PrettyPrinter(indent=2)
#  pp.pprint(resultDict)




#  print(json.dumps(resultDict, default_flow_style=False))

#  print(result.json())


#response = requests.get("http://localhost:8081")
#print(response)

print("\nEnd")

# Muutin tässä googlen ohjeeseen verrattuna: localhost -> service name
