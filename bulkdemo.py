import json
import os
import logging
from pprint import pformat

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(module)s -%(levelname)s- %(message)s"
)
logger = logging.getLogger(__name__)


def process_objects(myobject: object, mytarget: list, mydict: dict):
    for elem in myobject:
        if "action" in elem:
            action = elem["action"]
            logger.info(action)
            mytarget.append(action)
            ingress = elem["ingress"] if "ingress" in elem else None
            egress = elem["egress"] if "egress" in elem else None
            body = elem["body"] if "body" in elem else {}

            # process ingress data and add to dict if present
            if ingress:
                for key, value in ingress.items():
                    data = mydict[key] if key in mydict else None
                    body[value] = data
                logger.info(msg=f"enriched body: {pformat(body)}")

            # process data based on the "action" word
            # if action = "Managed Webserver Create" then else if .....

            # Extract response code, response body, response header from our action
            response_code = response_body = response_header = None

            # process egress data
            if egress:
                for key, value in egress.items():
#                    response_body={"server-id":"gul-dukat"}
                    if response_body:
                        data = response_body[key] if key in response_body else None
                    else:
                        data = None # oder gar nicht erst in dict aufnehmen
                    mydict[value] = data
                    logger.info(msg=f"Storing {value} with value {data}")
                    logger.info(msg=pformat(mydict))

        if "dependencies" in elem:
            process_objects(elem["dependencies"], mytarget=mytarget, mydict=mydict)


if __name__ == "__main__":
    _filename = "data.json"
    if not os.path.isfile(_filename):
        raise ValueError("Input file does not exist")

    try:
        with open(file=_filename, mode="r") as f:
            myjson = "".join(line.rstrip() for line in f)
    except:
        raise ValueError("Cannot read file")

    thejson = json.loads(myjson)
    target_list = []
    master_dictionary = {}
    process_objects(myobject=thejson, mytarget=target_list, mydict=master_dictionary)
    logger.info(pformat(target_list))