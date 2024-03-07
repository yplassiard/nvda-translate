# nvda-translate with DeepL
Make NVDA translate any spoken text to the desired language using DeepL. This addon is based largely on the excellent work of Yannick Plassiard.  While the addon is perfectly functional, I am a hobbiest programmer making things that I need for myself. Major code cleanup is needed.

## IMPORTANT: AN API KEY IS REQUIRED!

If you try to enable translation without specifying a valid API key, bad things will happen to you.  However, the good news is that getting an API key is free, accessible, and easy. A valid credit card is required, but it's only to prevent people creating multiple accounts. It will not be charged without warning.  To get your API key:

- Visit [this website](https://www.deepl.com/pro?utm_source=github&utm_medium=github-python-readme#developer)
- Press the button that says "sign up for free".
- Fill out your email address, set a password, and input your credit card info (remember: you will not be charged).
- Once your account is created, find the "account tab" and select it.
- This page should display an authorization key. Copy it to a safe place, you're going to need it in a minute!

## Installation

This add-on installs like any other add-on: Press enter on the "translate-x.y.nvda-addon" file, and answer "Yes" to all asked questions.  Once NVDA restarts, you *must* enter the valid API key that you got in the section above. To do that, head to the NVDA preferences dialogue (nvda+n, preferences, settings). Scroll down the list to find the translate section.  This section only contains one option: a text box to enter your DeepL API Key.

## Usage
When installed, the add-on will detect the language your NVDA installation is set to, or will get the Windows active language as a fallback. This language will be used to translate any spoken text, when the feature is activated.
**Note:** It is currently not possible to set this manually within a Preferences dialog, this may however be implemented in a future release. Also, we don't currently check to make sure DeepL supports translating to your NVDA language. Remember when I said major code cleanup is needed?  

Then, to enable or disable the translation, press NVDA+Shift+Control+T. This gesture can be modified within NVDA Preferences menu -> Command Gestures dialog.

### Gestures
The following gestures are defined (and can be changed within the Gesture commands dialog):
- NVDA+Shift+Control+T: Activates / deactivates the translation.
- NVDA+Shift+F (twice quickly): Clears the cache for the current application.
- NVDA+Shift+Control+F (twice quickly): Clear all caches for all translations for all applications.

## About Cache
To increase performance (see below), each translated text is stored within a cache file. A cache file is created for each application the translation has been activated in, and is located in the "translation-cache" directory within your NVDA's user configuration directory.

## How it works

When active, the add-on will intercept any spoken text and connect to the DeepL system to translate it to the desired language. This means that any text can be translated, from any app or game that uses NVDA to speak text, to websites.

## Privacy

Please, be aware that when the feature is active, any spoken text is sent to the DeepL service. It means that any spoken information will be sent, whatever this could be (a simple sentence, file names within your Windows Explorer, mail content, contacts, phone numbers, or even credit card numbers). It is therefore important to activate this feature only when you're certain of which text your NVDA will speak. This module has been primarily developped to be used within games, so no privacy concerns are present. You're free to use it with whatever you want, but at your own risk.

## About Performance
You may notice that when the feature is active, there is a delay between each spoken text. This is due to the translate API: because the add-on needs to connect to DeepL's servers over the Internet, an HTTP connection is made each and every time a text has to be translated. Therefore, an 8mbps Internet connection is recommended for this feature to work correctly.
Of course, the more bandwidth you have, the faster the translation will happen.  As well, purchasing a pro account at DeepL (for seven dollars a month) may result in faster translations.

## Contact and bug reports
- If you encounter any issue while using this add-on, please create a GitHub issue so that it will be easily trackable.
- Of course, Pull Requests are also welcomed if you want to extend the add-on or fix any issue.
- To contact me, you can use the address: [contact author](mailto:samuel@interfree.ca)


## Contributors
Thanks to everyone who made this extension a reality, including all of you who spent some time testing and reporting bugs.

Among others, I'd like give a special thank you to Hxebolax, who found and fixed the bug that prevented the add-on to work for months in 2020.
