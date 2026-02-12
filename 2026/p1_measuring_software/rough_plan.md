Project: Investigate energy use by browsers with and without ad blocking / privacy features enabled

1. OS
	a. Windows 			- yes? 
	b. Apple   			- Investigate
	c. Linux   			- probably not - low market share (4% according to wikipedia)
	d. Phones/Android   - definitely not
2. Browsers
	a. Chrome (like original paper)
	b. Firefox with privacy tracking protection
	c. Edge (any special features?)
	d. Brave (maybe with energy saver mode?) 
	e. Safari if using Mac
    f. That's probably enough! 
3. Ad blockers
	a. None 
	b. Ublock origin
	c. Other adblockers from paper could be done, but do people actually use them?  
4. Websites
	a. Youtube
	b. Netflix
	c. Reddit
	d. Nu.nl, AD.nl 
	e. Bol.com, marktplaats.nl 
	f. instagram/facebook/linkedin? 
	g. chatgpt? 
5. Multiple devices? 
	a. Not necessary according to prof, but nice to have and helps with shared development
6. Measurement tools
	a. hwinfo like in the paper? No: free option does not support" any scripting
	b. Socket tool? Probably not: Costs money, especially for one that we can read from a script, unless we get one from the prof
	c. Librehardwaremonitor + LibreHardwareMonitorReporter python package: seems ideal, free and open source with python wrapper already built, proof of concept is working, see POC folder. 
		i: https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/blob/master/README.md -> note, needs admin access
		ii: https://github.com/effeect/LibreHardwareMonitorCLI