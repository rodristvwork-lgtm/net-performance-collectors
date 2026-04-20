import asyncio
import json
import logging
import os
from datetime import datetime

RESULTS_DIR = "results"

async def run_speedtest_json():
    """
    Runs speedtest-cli and prints the raw JSON result.
    Command:
        speedtest -f json --output-header --accept-license --accept-gdpr
    """
    cmd = [
        "/usr/bin/speedtest",
        "-f", "json",
        "--output-header",
        "--accept-license",
        "--accept-gdpr"
    ]

    logging.info("Running speedtest...")

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if stderr:
            logging.debug(stderr.decode())

        result = json.loads(stdout.decode())

        print(json.dumps(result, indent=4))

        # Save JSON result
        save_result_json(result)

        return result

    except Exception as e:
        logging.error(f"Speedtest failed: {e}")
        return None
    
def save_result_json(result: dict):
    
    # Directory where THIS script resides
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_path = os.path.join(script_dir, RESULTS_DIR)

    # Create directory if missing
    os.makedirs(results_path, exist_ok=True)

    # Build base filename
    now = datetime.now()
    base_name = f"speed_test_{now.day:02d}_{now.month:02d}_{now.year}.json"
    file_path = os.path.join(results_path, base_name)

    # If exists, append counter
    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(
            results_path,
            f"speed_test_{now.day:02d}_{now.month:02d}_{now.year}_{counter}.json"
        )
        counter += 1

    # Save JSON
    with open(file_path, "w") as f:
        json.dump(result, f, indent=4)

    logging.info(f"Saved speedtest result to: {file_path}")
    return file_path

if __name__ == "__main__":
    asyncio.run(run_speedtest_json())