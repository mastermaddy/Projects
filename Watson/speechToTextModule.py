import json
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1

speech_to_text = SpeechToTextV1(
  username= "04659ee2-f648-4c91-b97a-8fc36fc9a92f",
  password= "Hk4vJ0nPZ0bA",
    x_watson_learning_opt_out=False
)


audio_file= open('/mnt/c/Users/dell/Desktop/Watson/test.wav','rb')


str=json.dumps(speech_to_text.recognize(
    audio_file, content_type='audio/wav', timestamps=True,
    word_confidence=True),indent=2)

dict=json.loads(str)

print(dict['results'][0]['alternatives'][0]["transcript"])




'''






{
  "results": [
    {
      "alternatives": [
        {
          "word_confidence": [
            [
              "testing",
              1.0
            ],
            [
              "one",
              1.0
            ],
            [
              "two",
              1.0
            ],
            [
              "three",
              1.0
            ],
            [
              "testing",
              0.961
            ],
            [
              "one",
              1.0
            ],
            [
              "two",
              1.0
            ],
            [
              "three",
              0.996
            ]
          ],
          "confidence": 0.993,
          "transcript": "testing one two three testing one two three ",
          "timestamps": [
            [
              "testing",
              0.29,
              0.82
            ],
            [
              "one",
              0.82,
              1.13
            ],
            [
              "two",
              1.13,
              1.39
            ],
            [
              "three",
              1.39,
              1.85
            ],
            [
              "testing",
              1.85,
              2.42
            ],
            [
              "one",
              2.45,
              2.82
            ],
            [
              "two",
              2.85,
              3.11
            ],
            [
              "three",
              3.11,
              3.8
            ]
          ]
        }
      ],
      "final": true
    }
  ],
  "result_index": 0
}
'''