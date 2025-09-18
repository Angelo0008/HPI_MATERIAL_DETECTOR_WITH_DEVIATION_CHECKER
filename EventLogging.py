import os
import logging

def logEvent(error):
    # fileDirectory = (r'\\192.168.2.19\ai_team\AI Program\Programs\Running\PlcCompilerLatest4.0\Event Logs')
    # os.chdir(fileDirectory)

    logging.basicConfig(
        filename='event_log.txt',               # Log file name
        level=logging.ERROR,                    # Log only errors and above (ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logging.error(error, exc_info=True)