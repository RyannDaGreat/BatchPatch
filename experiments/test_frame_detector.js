const { execSync } = require('child_process');
const fs = require('fs');
const puppeteer = require('puppeteer');
const path = require('path');

async function getActualFrameCount(videoPath) {
    const cmd = `ffprobe -v quiet -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "${videoPath}"`;
    return parseInt(execSync(cmd, { encoding: 'utf8' }).trim());
}

async function testBrowserDetector(videoPath) {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    const htmlPath = `file://${path.resolve('experiments/num_frame_detector.html')}`;
    await page.goto(htmlPath);

    // Upload file
    const input = await page.$('input[type="file"]');
    await input.uploadFile(videoPath);

    // Wait for result
    await page.waitForFunction(() => {
        const result = document.getElementById('result');
        return result && result.innerText.includes('Frames:');
    }, { timeout: 10000 });

    const result = await page.$eval('#result', el => el.innerText);
    await browser.close();

    const match = result.match(/Frames:\s*(\d+)/);
    return match ? parseInt(match[1]) : null;
}

async function main() {
    const videoPath = '/Users/ryan/Downloads/wan_gwtf_test__deg=0.75__steps=20__T=49.mp4';

    console.log(`Testing video: ${videoPath}`);

    const actual = await getActualFrameCount(videoPath);
    const detected = await testBrowserDetector(videoPath);

    console.log(`Actual frames (ffprobe): ${actual}`);
    console.log(`Detected frames (browser): ${detected}`);
    console.log(`Accuracy: ${actual === detected ? '✓' : '✗'}`);
}

main().catch(console.error);