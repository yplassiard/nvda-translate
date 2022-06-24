# nvda-translate
Make NVDA translate any spoken text to the desired language.
## Download
- Stable (NVDA 2021.1+): [translate-2021.12.28](http://www.mtyp.fr/nvda/translate/translate-2022.06.24.nvda-addon).
- Discontinued (NVDA 2019.3 to 2020.4): [translate-2021.01.3](http://www.mtyp.fr/nvda/translate/translate-2021.01.3.nvda-addon).

## Installation

This add-on installs like any other add-un: Press enter on the "translate-x.y.nvda-addon" file, and answer "Yes" to all asked questions.

## Usage
When installed, the add-on will detect the language your NVDA installation is set to, or will get the Windows active language as a fallback. This language will be used to translate any spoken text, when the feature is activated.
**Note:** It is currently not possible to set this manually within a Preferences dialog, this may however be implemented in a future release.

Then, to enable or disable the translation, press NVDA+Shift+Control+T. This gesture can be modified within NVDA Preferences menu -> Command Gestures dialog.

### Gestures
The following gestures are defined (and can be changed within the Gesture commands dialog):
- NVDA+Shift+Control+T: Activates / deactivates the translation.
- NVDA+Shift+F (twice quickly): Clears the cache for the current application.
- NVDA+Shift+Control+F (twice quickly): Clear all caches for all translations for all applications.

## About Cache
To increase performances (see below), each translated text is stored within a cache file. A cache file is created for each application the translation has been activated in, and is located in the "translation-cache" directory within your NVDA's user configuration directory.

## How it works

When active, the add-on will intercept any spoken text and connect to the Google Translate system to translate it to the desired language. This means that any text can be translated, from any app or game that uses NVDA to speak text, to websites.

## Privacy

Please, be aware that when the feature is active, any spoken text is sent to the Google Translate service. It means that any spoken information will be sent, whatever this could be (a simple sentence, file names within your Windows Explorer, mail content, contacts, phone numbers, or even credit card numbers). It is therefore important to activate this feature only when you're certain of which text your NVDA will speak. This module has been primarily developped to be used within games, so no privacy concerns are present. You're free to use it with whatever you want, but at your own risks.

## About Performances
You may notice that when the feature is active, there is a delay between each spoken text. This is due to the translate API: because the add-on do not use the non-free Google Translate API SDK, an HTTP connection is made each and every time a text has to be translated. Therefore, a 8mbps Internet connection is recommended for this feature to work correctly.
Of course, the more bandwidth you have, the faster the translation will happen.

## Contact and bug reports
- If you encounter any issue while using this add-on, please create a GitHub issue so that it will be easily trackable.
- Of course, Pull Requests are also welcomed if you want to extend the add-on or fix any issue.
- To contact me, you can use the address: [contact author](mailto:podcastcecitek@gmail.com)


## Contributors
Thanks to everyone who made this extension a reality, including all of you who spent some time testing and reporting bugs.

Among others, I'd like give a special thank you to Hxebolax, who found and fixed the bug that prevented the add-on to work for months in 2020.
