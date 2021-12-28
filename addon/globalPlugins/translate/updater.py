# *-* coding: utf-8 *-*
import logHandler
import versionInfo
import config
ADDON_NAME = "translate"
UPDATE_CHECK_INTERVAL = 3600

import threading
import time
import queue
import urllib
import json
import os

class ExtensionUpdater(threading.Thread):
    quit = False
    queue = queue.Queue()

    def run(self):
        self.lastCheck = 0
        while self.quit is False:
            time.sleep(1)
            if time.time() - self.lastCheck < UPDATE_CHECK_INTERVAL:
                continue
            try:
                res = urllib.request.urlopen("http://www.mtyp.fr/nvda")
                data = res.read()
                packet = json.loads(data)
                mod = packet.get(ADDON_NAME, None)
                if mod is not None:
                    new_version = self.getLatestVersion(mod)
                    if new_version is not None:
                        logHandler.log.info("%s update available: %s" %(ADDON_NAME, new_version["version"]))
                        self.queue.put({"update": new_version})
                        self.download(new_version)
            except Exception as ex:
                logHandler.log.exception("Failed to retrieve update list: %s" %(ex))
            self.lastCheck = time.time()

            
            
                
                                       
        logHandler.log.info("%s: exiting update thred..." %(ADDON_NAME))
    def getLatestVersion(self, mod):
        import addonHandler
        actual = None
        for addon in addonHandler.getAvailableAddons():
            if addon.name == ADDON_NAME:
                actual = addon
        if actual is None:
            return None








        target = None
        for version in mod["versions"]:
            if version["version"] > actual.version:
                meta = version.get("metadata", None)
                logHandler.log.info("Metadata: %s" %(meta))
                if meta is not None and meta != "false" and meta != False:
                    if meta["minimumNVDAVersion"] > versionInfo.version or meta["lastTestedNVDAVersion"] < versionInfo.version:
                        logHandler.log.debug("Discarding version %s: incompatible version" %(version["version"]))
                        continue
                if target is not None and target["version"] < version["version"]:
                    target = version
                elif target is None:
                    target = version
        return target
    
    def download(self, mod):
        tmp = os.path.join(config.getUserDefaultConfigPath(), ADDON_NAME + ".nvda-addon")
        try:
            f = open(tmp, "wb")
            res = urllib.request.urlopen(mod["url"])
            f.write(res.read())
            f.close()
        except Exception as ex:
            logHandler.log.error("%s: failed to download %s: %s" %(ADDON_NAME, mod["url"], ex))
            return False
        self.queue.put({"download": tmp,
                        "version": mod["version"]})
        return True
    
                                 
