# AutomaticScreenshotBot

AutomaticScreenshotBot is a Python script that uses Selenium to visit a list of webpages, take screenshots, and save them. A lifesaver for a vital yet repetitive task for online marketing folks.

It's best used by media buyers to see where their ads have been running. As you likely know, all DSPs allow you to pull performance by top-level domain (ex: [https://www.topixoffbeat.com](https://www.topixoffbeat.com), but to get page-level domain [https://www.topixoffbeat.com/slideshow/17550/slide94]( https://www.topixoffbeat.com/slideshow/17550/slide94), you usually need access to log-level data. This script helps you actually check / see the actual pages that your ads are running on without having to visit them all individually. Because that would be impossible. Programmatic media buying happens at such a vast scale that tools such as this one are necessary.

You of course can take screenshots of regular webpages too.

## What it Does

Using the popular Selenium browser automation framework, the program launches a Chrome browser, then the browser:

* visits these pages
* takes a screenshot, and saves it to the “screenshots” directory as a .png file.
* waits five seconds
* scrolls down the page
* takes / saves another screenshot

Until five screenshots were taken, and then it goes on to the next url. Once all the screenshots are done, you can view the images quickly, and find out what the ad environment looked like. If there is too much clutter, the content is bad, or it doesn’t look like the page has any ads… that’s a problem. I would suggest re-visiting the page in a normal (ie non-automated) browser.

Using the command line, a user can also add in additional parameters:
* Running the program headlessly / with the screen running in the background
* Change the number of seconds to wait before scroll
* Change the number of screenshots taken on the page.

## Usage

To use it:
* Have a Windows OS on your computer (Mac / Linux not currently supported)
* Download the latest version of Chrome
* Have Python v3.7+ installed. 
* Download the code from this [git repo](https://github.com/wrny/automatic_screenshot_bot). 

* Add a urls.txt file with the pages you want to visit / screenshot, separated by line. Note that all urls must begin with an http:// or https://, else the program will skip them and add them to the “failed_urls” file.
* Open a command prompt
* navigate to the directory the program is in.
* if it's your first time using the program, type: pip install -r requirements.txt (that will download all of the additional modules needed to run the program).
* Once you’ve done that (only need to do it once) type in: 

```python automatic_screenshot_bot.py```

* for additional parameters:

    * -H for headless mode True / False
    * -s for number of screenshots
    * -t for time between screenshots

type in: 

```python automatic_screenshot_bot.py -H True -s 3 -t 10```

* Note that some companies will block headless browsers from loading page content, or block ads from appearing. If you are using this program to view ads / ad placements, headless mode is not recommended. This is a very obvious bot, and so if a site is blocking bots from seeing ads, then the ads won't load.

If you’re checking through thousands of URLs, it’s inevitable that the program will break in some way--either losing Internet connectivity, accidentally closing your laptop monitor, etc. This program is designed to pick up where you left off, and if a page is in the “completed_urls” file, it’ll skip that URL. Note that means that once the program is done, you need to physically delete the failed_urls and completed_urls files. Else the program will open up an automated browser and then close almost immediately after.

I use the program pretty regularly to blacklist sites, especially in conjunction with my computer vision / ad clutter identifier script. I’ll try to post that one too at some point.

I hope you get some use out of the program!


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
