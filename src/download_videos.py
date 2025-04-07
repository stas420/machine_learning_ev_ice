import datetime as dt
import os
import urllib.request
import ssl

START_DATE = dt.date(2024, 1, 29)
END_DATE = dt.date(2025, 4, 4)

URL_PREFIX = "https://storage.sbg.cloud.ovh.net/v1/AUTH_06ca1283ce304b2f9196a035aac07edc/timelapses/zalewo-fontanna/"
URL_SUFFIX = ".mp4"
OUTPUT_DIR = "videos"

# Create an unverified SSL context
ssl._create_default_https_context = ssl._create_unverified_context

def get_urls(start_date, end_date) -> list[tuple[str, str]]:
    urls = []
    # this will give you a list containing all of the dates
    all_dates = [start_date + dt.timedelta(days=x) for x in range((end_date-start_date).days + 1)]

    for date in all_dates:
        # format the date to match the URL pattern
        formatted_date = date.strftime("%Y-%m-%d")
        # construct the URL
        url = f"{URL_PREFIX}{formatted_date}{URL_SUFFIX}"
        urls.append((url, f"{formatted_date}.mp4"))
    return urls

def download_video(url: str, filename: str) -> None:
    # create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # construct the full path for the output file
    output_file = os.path.join(OUTPUT_DIR, filename)

    print(f"Downloading {url} to {output_file}...")
    try:
        # download the file
        urllib.request.urlretrieve(url, output_file)
        print(f"Downloaded {filename} successfully.")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")


if __name__ == "__main__":
    urls = get_urls(START_DATE, END_DATE)
    for url, filename in urls:
        download_video(url, filename)