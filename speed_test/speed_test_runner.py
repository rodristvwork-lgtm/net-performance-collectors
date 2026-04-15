import asyncio
import json
import logging

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

        # stderr contains license messages, not real errors
        if stderr:
            logging.debug(stderr.decode())

        # Parse JSON
        result = json.loads(stdout.decode())

        # Print JSON nicely
        print(json.dumps(result, indent=4))

        return result

    except Exception as e:
        logging.error(f"Speedtest failed: {e}")
        return None


# Allow running as: python speedtest.py
if __name__ == "__main__":
    asyncio.run(run_speedtest_json())