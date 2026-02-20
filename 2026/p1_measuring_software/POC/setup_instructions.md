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
conda create -n SSE python pythonnet numpy pandas playwright playwright-stealth matplotlib seaborn numba
conda activate SSE
# Download the browsers for playwright to simulate browsing
python -m playwright install 
'''

Download the ublock origin lite extension (note, ublock origin is not supported anymore on chrome) for chrome by going to:

'''
https://crxviewer.com/?crx=https://chrome.google.com/webstore/detail/ddkjiahejlhfcafbddmgiahcphecmpfh
'''

Click 'download as zip', unzip and then place the folder in a subfolder of the project folder: extensions/ublock_chrome

For edge, the approach is:

'''
Find the extension link, e.g.:
https://microsoftedge.microsoft.com/addons/detail/ublock-origin/odfafepnkmbhccpbejgmiehpchacaeak
Extract the identifier at the end: 
odfafepnkmbhccpbejgmiehpchacaeak
Insert into this link:
https://edge.microsoft.com/extensionwebstorebase/v1/crx?response=redirect&x=id%3D[EXTENSIONID]%26installsource%3Dondemand%26uc
So you get:
https://edge.microsoft.com/extensionwebstorebase/v1/crx?response=redirect&x=id%3Dodfafepnkmbhccpbejgmiehpchacaeak%26installsource%3Dondemand%26uc

Download this and open with 7zip as archive, then extract the contents into a folder. 

To run, make sure this is run as admin as libremonitor needs admin access. E.g. with vs code, launch vs code as admin and then activate the environment and launch the script. 

''' 
conda activate SSE
# Navigate to the path where the code is, e.g. for me:
cd C:\Users\danie\Documents\GitHub\course_sustainableSE\2026\p1_measuring_software\POC
python ./browse.py
# Run the initial analysis
python ./analysis.py
''' 


You may need to enable long path support in Windows for the firefox browser. Run the following in an admin powershell:

'''
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
'''