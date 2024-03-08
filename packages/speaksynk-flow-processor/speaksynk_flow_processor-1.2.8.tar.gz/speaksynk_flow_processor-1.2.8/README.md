# SpeakSynk Flow Processor


Parent class to create steps, ideally this will save us some common functions of the steps.


# Implementation


```
from speaksynk_flow_processor.AWSSpeakSynkFlowProcesor import AWSSpeakSynkFlowProcesor


class Implementation(AWSSpeakSynkFlowProcesor):
    def __init__(self):
        super().__init__()
        self.filekey = "break_time/%s" % self._identifier
        self.local_file = "out.txt"


    def run(self):
        super().run(self)
        self.download('xxxxx')
        '''
            Do your logic here
        '''
        self.upload('xxxx', 'xxxxx')

    def close(self):
        super().close(self)
        '''
            Do your close logic here
        '''


```

Ideally this save us some time in creating more steps and only taking care of the run method



# CLI

By default we have designed a CLI to run the steps, in order to run the steps you can run `poetry run speaksynk-steps run` this method will automalically instatiate the method and run the proper methods.


# Install

* `pip install poetry`
* `poetry install`

# Test

* `poetry run pytest`


# Use

* `poetry run speaksynk-steps run`