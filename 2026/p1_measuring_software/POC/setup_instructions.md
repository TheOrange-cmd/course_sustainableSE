These are instructions for running the test script which is tested on Windows, running a chrome browser through playwright. Note playwright-stealth adds functionality to make the browser look more 'human'. 

These instructions assume conda is installed, alternatively you can create a venv, use mamba, uv, poetry, whatever you want. 

You can add instructions for Mac and other browsers below or in a separate file. 

Note: if using VS Code, I recommend to use a cmd terminal and not powershell with conda. 

Clone the CLI package repo into project folder:
'''
git clone https://github.com/effeect/LibreHardwareMonitorCLI.git
''' 

Install librehardwaremonitor:
'''
winget install LibreHardwareMonitor.LibreHardwareMonitor --source winget
'''

Create env:

'''
# Create the env itself using conda
conda create -n SSE python pythonnet numpy pandas playwright playwright-stealth
conda activate SSE
# Download the browsers for playwright to simulate browsing
python -m playwright install 
'''

Download the ublock origin lite extension (note, ublock origin is not supported anymore on chrome) for chrome by going to:

'''
https://crxviewer.com/?crx=https://chrome.google.com/webstore/detail/ddkjiahejlhfcafbddmgiahcphecmpfh
'''

Click 'download as zip', unzip and then place the folder in a subfolder of the project folder: extensions/ublock_chrome

To run, make sure this is run as admin as libremonitor needs admin access. E.g. with vs code, launch vs code as admin and then activate the environment and launch the script. 

''' 
conda activate SSE
# Modify this path of course
cd C:\Users\danie\Documents\GitHub\course_sustainableSE\2026\p1_measuring_software\POC
# Modify the paths in the script first, then run it! Paths are always a bitch in python, for now I have them hardcoded.
python ./browse.py
''' 

Note the diagnostics.py file can be used to figure out what sensors the library exposes. You may need to run this and then edit the browse.py file to use the appropriate sensors. Ideally we can run this automatically. 