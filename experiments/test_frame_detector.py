#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
import subprocess
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os

def get_actual_frame_count(video_path):
    """Get ground truth frame count using ffprobe"""
    cmd = ['ffprobe', '-v', 'quiet', '-count_frames', '-select_streams', 'v:0',
           '-show_entries', 'stream=nb_read_frames', '-of', 'json', video_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return int(data['streams'][0]['nb_read_frames'])

def test_browser_detector(video_path):
    """Test the browser frame detector"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--allow-file-access-from-files')

    driver = webdriver.Chrome(options=options)

    try:
        # Load the HTML file
        html_path = f"file://{os.path.abspath('experiments/num_frame_detector.html')}"
        driver.get(html_path)

        # Upload the video file
        file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        file_input.send_keys(os.path.abspath(video_path))

        # Wait for processing and get result
        time.sleep(5)  # Give it time to process
        result_div = driver.find_element(By.ID, 'result')
        result_text = result_div.text

        # Extract frame count from result
        if 'Frames:' in result_text:
            detected_frames = int(result_text.split('Frames:')[1].strip().split()[0])
            return detected_frames

    finally:
        driver.quit()

    return None

if __name__ == "__main__":
    video_path = "/Users/ryan/Downloads/wan_gwtf_test__deg=0.75__steps=20__T=49.mp4"

    print(f"Testing video: {video_path}")

    actual = get_actual_frame_count(video_path)
    detected = test_browser_detector(video_path)

    print(f"Actual frames (ffprobe): {actual}")
    print(f"Detected frames (browser): {detected}")
    print(f"Accuracy: {'✓' if actual == detected else '✗'}")