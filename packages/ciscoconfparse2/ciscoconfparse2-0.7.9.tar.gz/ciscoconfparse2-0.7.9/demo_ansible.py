import contextlib
import json
import io

import ansible_runner

def unpack_ansible_results(json_data: list[dict]) -> str:

    # Magic failure string...
    stdout = "__FAILURE__"

    for jsonl in json_data:

        # Get all event_data...
        event_data = jsonl.get("event_data")
        if isinstance(event_data, dict):
            # Check if the result is in event_data...
            result = event_data.get("res")

            if isinstance(result, dict) and "stdout" in result.keys():
                stdout = result["stdout"]

    return stdout

def main():

    success = False

    # Sometimes ansible runs fail, this runs in a loop until 
    #     it succeeds.  A simple modification to this might be limiting
    #     the number of retries.
    while not success:
        ooo = io.StringIO()
        with contextlib.redirect_stdout(ooo):

            # ansible_runner.run(json_mode=True) sends something similar 
            #      to jsonl lines to stdout
            runner = ansible_runner.run(private_data_dir=".",
                                        # send ouptut to stdout as json
                                        json_mode=True,
                                        inventory='ansible_inventory.ini',
                                        playbook='ansible_playbook.yml')

        #######################################################################
        # Get ansible_runner stdout from contextlib
        #######################################################################

        #     Build a json string from the returned ansible jsonl lines...
        json_string = "[" + ",".join(ooo.getvalue().strip().splitlines()) + "]"

        json_data = None
        try:
            json_data = json.loads(json_string)
            success = True
        except json.decoder.JSONDecodeError:
            print("FAILURE!")

    processed = runner.stats.get('processed')
    for host in processed:
        print("GOOD", host)

    failed = runner.stats.get('failures')
    for host in failed:
        print("FAIL", host)

    stdout = unpack_ansible_results(json_data)
    print(stdout)
    
if __name__ == "__main__":
    main()
