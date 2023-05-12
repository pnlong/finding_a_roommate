# finding\_a\_roommate

Creates an Instagram bot in charge of posting pictures and informational snippets received via DM. Meant for use as a college acceptance page.

## Background

I was recently admitted to UC San Diego as a Computer Science major in Muir College. Various Instagram accounts exist (for every college) that are meant to connect incoming freshmen with one another, with both the aim of finding new friends and discovering potential roommates. For UCSD specifically, the most prominent of many accounts is called @[ucsandiego.2027](https://www.instagram.com/ucsandiego.2027/). Posting over 10 times a day, countless incoming freshmen share snippets and pictures of themselves to this account. 

However, UCSD's college system makes it difficult to find potential roommates -- my main objective -- on this account. For one, I can't dorm with someone of the opposite gender, and secondly, I can't dorm with someone who is not in my college (Muir, one of *eight* colleges at UCSD). This renders the significant majority of the posts on @**ucsandiego.2027** irrelevant (for my purposes). The page is chaotic to say the least...

My solution to this problem is to create a new Instagram account just for UCSD Muir College Class of 2027 admits. There are many advantages to this:

1. **Numbers**: There will be much less people posted to this account, which will make the page much *less* chaotic and much *more* readable. Even if it is mostly females posting on the new account, at least everyone posted will be in Muir College, making many more of the posts relevant for me.
2. **Tighter Community**: Because the new Instagram account has much less people, it is easier to connect with others and make friends going into Fall Quarter.
3. **Reducing Backlog**: The @**ucsandiego.2027** account is severely backlogged, and its account owner claims that it will take over a month to post someone's information. In fact, the account owner has resorted to asking submittees to pay a $5 fee in order to expedite the process. This separate account for Muir College will reduce the strain on the main account.

Hopefully this project will make it easier for me to find a roommate, hence the name.

---

## Gameplan
This project must do a variety of things. It must...

1. *Find other Muir College admittees*. This can be done by scraping the captions of every post on @**ucsandiego.2027**. If the caption includes some form of the word `Muir`, take note of that user's instagram account handle, which will probably be the string that follows the `@` character. This step should output a list of Instagram users for the bot to follow. For every user in this list, congratulate them on their acceptance, and then ask if they would like to send their info to be posted to the bot account. Perhaps the bot can fully automate the process and simply screenshot the user's post on @**ucsandiego.2027**, making the process very easy for those who have already posted; however, this could be difficult and stepping towards an invasion of privacy.
2. For users found via the "*Find other Muir College admittees*" method, there is no need to check that they have been admitted to Muir, since @**ucsandiego.2027** has vetted them for us already. However, for those who have requested to follow the account, they must verify they were admitted to Muir by sending a screenshot of their acceptance letter. The bot will use OCR to read in their acceptance letter and check for a string indicating that they have been admitted to Muir.
3. *Read Instagram DMs* and post what has been DMed to the account. The bot must DM all Muir College admittees -- whether vetted by us or @**ucsandiego.2027** -- and ask them to post. This will be the bulk of the work for this project.

Hopefully this project will be done by May 15th, which is the beginning of the housing selection process.

---

## Programs
The various programs that will help me find a roommate. These programs seem to require a strong internet connection, since on weak connections, Selenium tries to perform actions before a page is fully loaded, causing the code to break.


### *login.py*
Contains a class which creates a Selenium window and logs into instagram. Instances of this class can then be used by other programs in `finding_a_roommate`. This program has no arguments, though it does require Selenium Chrome Web Driver to be installed ([download here](https://chromedriver.chromium.org/downloads)). The Chrome Web Driver version **must** match that of Chrome on your local device.


### *bot.py*
The main bot that reads Instagram DMs and posts snippets and pictures of admittees to the Instagram account. Run with:
```
python ~/finding_a_roommate/bot.py driver_address username password
```
where:

- `driver_address` is the filepath to a Selenium Chrome Web Driver. *Note that Chrome Driver version must match the version of Chrome installed on the computer*, or `bot.py` will not be able to run correctly.
- `username` is the username of the account which `bot.py` will take control of.
- `password` is the password to the aforementioned account.


### *find_accounts.py*
Scrapes the @**ucsandiego.2027** account to find incoming Muir students, and makes note of their Instagram handles. Run with:
```
python ~/finding_a_roommate/find_accounts.py driver_address username password username_to_scrape output_directory
```
where:

- `username_to_scrape` is the username to the Instagram account that will be scraped for information.
- `output_directory` is the filepath to the folder that `find_accounts.py` will output to.

`driver_address`, `username`, and `password` are the same as for `bot.py`. See above for those arguments.


### *initiate_contact.py*
As the name suggests, this program tries to DM Instagram accounts found using `find_accounts.py`, asking these accounts for permission to post on the new Muir account. Run with:
```
python ~/finding_a_roommate/initiate_contact.py driver_address username password accounts_to_dm
```
where:

- `accounts_to_dm` is the filepath to the list of Muir accounts generated by `find_accounts.py`. This filepath (specifically, the directory in which the file is in) will be used to output a list of successfully contacted accounts.

`driver_address`, `username`, and `password` are the same as for `bot.py`. See above for those arguments.

