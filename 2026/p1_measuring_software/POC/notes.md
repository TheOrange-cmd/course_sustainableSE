Google has advanced robot detection where we have to click on a "click here if you're not a robot" button, might have to skip altogether, even though it's the most popular website. Playwright stealth can't deal with it. 

Wikipedia is popular but has no real ads - but maybe we'll see it takes more energy? No cookie consent form appears on this page. I picked a specific URL that is popular in NL right now, the page on Charlie Kirk. Not that I'm particularly a fan of his ideals ... 

Telegraaf.nl works
Weeronline.nl works
Nu.nl works
Ad.nl works 
Marktplaats.nl works 
Youtube.com works (using a random nature doc video)
Reddit.com works 
Aliexpress.com works
Bol.com works 
imgur.com works
9gag.com works
dumpert.nl works
Tweakers.net works

Though note that of these, not every website shows the same amount of ads. Script now includes some code to read how much data is downloaded and links it to a known ad URL list. Not sure how reliable this is. 

Other interesting pages:
Facebook: Requires clicking away the signin popup, doable, but not sure how many ads appear on a common profile (e.g. profile page for christiano ronaldo) - where do ads actually appear on facebook? Clicking around with adblock disabled doesn't get me any ads on his page
Instagram: Similar issue as facebook, ads tend to appear when scrolling reels but this requires a login
Pinterest: Same as Facebook and Instagram 
    --- all three above, probably skip! 
Illegal streaming sites: problematic as it requires a VPN to use, though these show a LOT of scammy ads in general, so is valuable scientifically, but not feasible for this project
Porn sites: Legal, show a lot of ads, but problematic for obvious reasons. 
Email sites like live.com and gmail.com: Requires an account with complicated login screen behavior, too complex. 

Pilot study shows that for quite a few sites we can get away with less than 10 trials, and with 20 we include a good amount of them. With 30 we don't catch that many more, we'd have to go to 100 or 200 for that which is infeasible. Report can include a mention of the pilot study and mention likelihood of low statistical power for some configurations. 

Current demo analysis does NOT look at temperature readings. The sensors do seem to measure temperature, so we might be able to include it as a cofounding factor in the final analysis. 
