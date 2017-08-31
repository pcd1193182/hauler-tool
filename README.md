# Hauler Packing Tool

This project is a small ESI application that can help you haul things in EVE Online.

## Problem statement

What do you do if you have 1 million m3 worth of loot, totalling 30 billion isk? You could stick it all in a cargo expanded freighter, but then [this](https://zkillboard.com/kill/64240535/) happens. You could pay for shipping services, but they'll charge hundreds of millions of isk even for short distances. What you need is a way to quickly and painlessly move the highest value cargo in your safest transport, like a blockade runner or a covops nullified t3. That reduces your risk and your shipping costs dramatically. However, figuring out the best items to take isn't easy, and dragging dozens or hundreds of items by hand into your cargo hold is even worse.

## Solution

What you need is this tool. This application runs in heroku, on a free tier instance. You can also use an existing instance [here](https://hauler-packing-tool.herokuapp.com/) (be patient, the free tier is slow and goes into hibernate after 30 minutes) if you don't want to set up your own. After using SSO to grant access to your fittings, the tool will gather and present all your saved fittings in EVE Online. You then select a fitting, paste an evepraisal link (created in whatever way you prefer), and enter the total cargo size available in that fit. Then, click submit! The tool will automatically determine the most value it can fit in the given cargo size, respecting CCP's 255 items/saved fit limit, and create and export a modified version of the fit that contains that list of items in the cargo hold. Then all you have to do is log into EVE, get in the ship whose fit you selected, and right click on your new fit and hit "Fit to Active Ship". EVE will then pull all the items into your cargo hold, and you're ready to set off!

To use the example above, that freighter could have moved a full 7.7 billion isk of its load with a single blockade runner. After that, you stick 5b in a DST or 13b in a jump freighter, and suddenly your freighter full of loot is much smaller and much less risky to carry. And this tool could make that happen in seconds, without tedious calculation or dragging.

## Technical stuff

The base code for this is shamelessly cribbed from [the esipy + flask example project](https://github.com/Kyria/flask-esipy-example). We also use gunicorn to launch the app in heroku, functools to make some comparison generation automatic, and bootstrap to make it not ugly as sin. It's easy enough to set up yourself in heroku, though you need to change a number of settings in config.py, add the postgress hobby-dev addon to the heroku project, and set up your own application through CCP. You could also run it locally with virtualenv.

### Future work

There are a number of known issues with this project.

* Currently, the database that stores login tokens will grow until it hits the limit for free postgress databases in heroku, at which point I imagine bad things will happen.
* It should be possible to automatically calculate the cargo hold size given the fitting imported. For industrials, this would require adding the character skills scope and doing more math.
* The application looks ok, but could definitely use some work. It was created on a bit of a time crunch.
* There's probably some security issues here somewhere.
* There's probably a bunch of really bad error handling failures too. There's probably overlap between the two!
* Probably all of this code is horribly unpythonic, un-javascripty, and generally gross. I'm a C developer, I don't do this "webdev" stuff very often.


Patches and issues welcome, although this isn't my day job, so expect some delays in responses.
