import time
from speaksynk_flow_processor.utils.logger import logger
def track_method(method):
    def wrapper(self, *args, **kwargs):
        logger.debug(f"Pre-processing for method: {method.__name__}")
        start_time = time.time()
        result = method(self, *args, **kwargs)
        end_time = time.time() 
        execution_time = end_time - start_time
        self.track_data["stepName"] =  {
            'S': self.__class__.__name__.capitalize()
        }
        if (method.__name__ in self.track_data["methods"]):
            self.track_data["methods"]['M'][method.__name__]['L'].append({
                "M": 
                {
                    'start_time': {
                        'N': f"{start_time}"
                    },
                    'end_time': {
                        'N': f"{end_time}"
                    },
                    'execution_time': {
                        'N': f"{execution_time}"
                    },
                }
            })
        else:
            self.track_data["methods"]['M'][method.__name__] = {
                'L': [{
                    'M': {
                        'start_time': {
                            'N': f"{start_time}"
                        },
                        'end_time': {
                            'N': f"{end_time}"
                        },
                        'execution_time': {
                            'N': f"{execution_time}"
                        },
                    }
                }]
            }
        logger.debug(f"Method '{method.__name__}' took {execution_time:.4f} seconds to execute.")
        return result

    return wrapper
