import base64
import io
import json
import requests


# Based on https://cloud.google.com/vision/automl/docs/containers-gcs-tutorial
# Changes: localhost -> service name

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


def toDict(predictionJson):
  resultDict = {}
  resultDict["segment"] = predictionJson["predictions"][0]["key"]
  resultDict["labels"] = {}

  n = 0
  for i in predictionJson["predictions"][0]["labels"]:
    resultDict["labels"][i] = predictionJson["predictions"][0]["scores"][n]
    n = n + 1

  return resultDict


def predict(segmentFilePath, segment):
  predictionJson = container_predict(segmentFilePath, segment)
  predictionDict = toDict(predictionJson)

# TODO maybe later: If doing batch predictions, need to return dict with key and prediction value
#  return predictionDict

  # return single score
  return predictionDict["labels"]["animal"]


