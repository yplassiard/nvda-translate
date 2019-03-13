# *-* coding: utf-8 *-*
# translate/__init__.py
#A part of the NVDA Translate add-on
#Copyright (C) 2018 Yannick PLASSIARD
#This file is covered by the GNU General Public License.
#See the file LICENSE for more details.
#This add-on also uses the following external libraries:
#markupbase, htmlentitydefs, HTMLParser: Come from the Python2 standard installation.
#mtranslate: MIT License

# Moreover, the mtranslate package relies on URLLib, part of Python2 standard installation to
# connect to the Google Translate server.



import os, sys, time, io
import globalVars
import globalPluginHandler, logHandler
import api, controlTypes
import ui, wx, gui, core, config, speech
import json
sys.path.append(os.path.dirname(__file__))
import markupbase
import htmlentitydefs
import HTMLParser
import mtranslate
del sys.path[-1]
import addonHandler, languageHandler
addonHandler.initTranslation()

#
# Global variables
#

_translationCache = {}
_nvdaSpeak = None
_nvdaGetSpeechTextForProperties = None
_gpObject = None
_lastError = 0
_enableTranslation = False


def translate(text):
    """translates the given text to the desired language.
Stores the result into the cache so that the same translation does not asks Google servers too often.
"""
    global _translationCache, _enableTranslation, _gpObject

    if _gpObject is None or _enableTranslation is False:
        return None
    msg = "Cache Dump:\n"
    for key in _translationCache:
        msg += "    %s => %s\n" %(key, _translationCache[key])
    logHandler.log.debugWarning(msg)
    translated = _translationCache.get(text, None)
    if translated is not None:
        return translated
    try:
        prepared = text.encode('utf8', ':/')
        translated = mtranslate.translate(prepared, _gpObject.language)
    except Exception as e:
        _translationCache[text] = text
        return text
    _translationCache[text] = translated
    return translated


#
## Extracted and adapted from nvda/sources/speech.py
#

def speak(speechSequence,symbolLevel=None):
    global _enableTranslation

    if _enableTranslation is False:
        return _nvdaSpeak(speechSequence, symbolLevel)
    newSpeechSequence = []
    for val in speechSequence:
        if isinstance(val, basestring):
            v = translate(val)
            newSpeechSequence.append(v if v is not None else val)
        else:
            newSpeechSequence.append(val)
    _nvdaSpeak(newSpeechSequence, symbolLevel)

#
## This is overloaded as well because the generated text may contain already translated text by
## the NVDA's locale system. In this overloaded function, we only translate text which is not
## already localized, such as object's name, value, or description
#

def getSpeechTextForProperties(reason=controlTypes.REASON_QUERY,**propertyValues):
    oldTreeLevel = speech.oldTreeLevel
    oldTableID = speech.oldTableID
    oldRowNumber = speech.oldRowNumber
    oldRowSpan = speech.oldRowSpan
    oldColumnNumber = speech.oldColumnNumber
    oldColumnSpan = speech.oldColumnSpan

    global _enableTranslation

    if not _enableTranslation:
        return _nvdaGetSpeechTextForProperties(reason, **propertyValues)
    textList=[]
    name=propertyValues.get('name')
    if name:
        textList.append(translate(name.replace("&", "")))
    if 'role' in propertyValues:
        role=propertyValues['role']
        speakRole=True
    elif '_role' in propertyValues:
        speakRole=False
        role=propertyValues['_role']
    else:
        speakRole=False
        role=controlTypes.ROLE_UNKNOWN
    value = propertyValues.get('value') if role not in controlTypes.silentValuesForRoles else None
    cellCoordsText=propertyValues.get('cellCoordsText')
    rowNumber=propertyValues.get('rowNumber')
    columnNumber=propertyValues.get('columnNumber')
    includeTableCellCoords=propertyValues.get('includeTableCellCoords',True)
    if role==controlTypes.ROLE_CHARTELEMENT:
        speakRole=False
    roleText=propertyValues.get('roleText')
    if speakRole and (roleText or reason not in (controlTypes.REASON_SAYALL,controlTypes.REASON_CARET,controlTypes.REASON_FOCUS) or not (name or value or cellCoordsText or rowNumber or columnNumber) or role not in controlTypes.silentRolesOnFocus) and (role!=controlTypes.ROLE_MATH or reason not in (controlTypes.REASON_CARET,controlTypes.REASON_SAYALL)):
        textList.append(translate(roleText) if roleText else controlTypes.roleLabels[role])
    if value:
        textList.append(translate(value))
    states=propertyValues.get('states',set())
    realStates=propertyValues.get('_states',states)
    negativeStates=propertyValues.get('negativeStates',set())
    if states or negativeStates:
        textList.extend(controlTypes.processAndLabelStates(role, realStates, reason, states, negativeStates))
    if 'description' in propertyValues:
        textList.append(translate(propertyValues['description']))
    if 'keyboardShortcut' in propertyValues:
        textList.append(propertyValues['keyboardShortcut'])
    if includeTableCellCoords and cellCoordsText:
        textList.append(cellCoordsText)
    if cellCoordsText or rowNumber or columnNumber:
        tableID = propertyValues.get("_tableID")
        # Always treat the table as different if there is no tableID.
        sameTable = (tableID and tableID == oldTableID)
        # Don't update the oldTableID if no tableID was given.
        if tableID and not sameTable:
            oldTableID = tableID
            rowSpan = propertyValues.get("rowSpan")
            columnSpan = propertyValues.get("columnSpan")
            if rowNumber and (not sameTable or rowNumber != oldRowNumber or rowSpan != oldRowSpan):
                rowHeaderText = propertyValues.get("rowHeaderText")
                if rowHeaderText:
                    textList.append(translate(rowHeaderText))
                    if includeTableCellCoords and not cellCoordsText: 
                        # Translators: Speaks current row number (example output: row 3).
                        textList.append(_("row %s")%rowNumber)
                        if rowSpan>1 and columnSpan<=1:
                            # Translators: Speaks the row span added to the current row number (example output: through 5).
                            textList.append(_("through %s")%(rowNumber+rowSpan-1))
                    oldRowNumber = rowNumber
                    oldRowSpan = rowSpan
            if columnNumber and (not sameTable or columnNumber != oldColumnNumber or columnSpan != oldColumnSpan):
                columnHeaderText = propertyValues.get("columnHeaderText")
                if columnHeaderText:
                    textList.append(translate(columnHeaderText))
                    if includeTableCellCoords and not cellCoordsText:
                        # Translators: Speaks current column number (example output: column 3).
                        textList.append(_("column %s")%columnNumber)
                        if columnSpan>1 and rowSpan<=1:
                            # Translators: Speaks the column span added to the current column number (example output: through 5).
                            textList.append(_("through %s")%(columnNumber+columnSpan-1))
                    oldColumnNumber = columnNumber
                    oldColumnSpan = columnSpan
            if includeTableCellCoords and not cellCoordsText and rowSpan>1 and columnSpan>1:
                # Translators: Speaks the row and column span added to the current row and column numbers
                #                       (example output: through row 5 column 3).
                textList.append(_("through row {row} column {column}").format(
                    row=rowNumber+rowSpan-1,
                    column=columnNumber+columnSpan-1
                ))
    rowCount=propertyValues.get('rowCount',0)
    columnCount=propertyValues.get('columnCount',0)
    if rowCount and columnCount:
        # Translators: Speaks number of columns and rows in a table (example output: with 3 rows and 2 columns).
        textList.append(_("with {rowCount} rows and {columnCount} columns").format(rowCount=rowCount,columnCount=columnCount))
    elif columnCount and not rowCount:
        # Translators: Speaks number of columns (example output: with 4 columns).
        textList.append(_("with %s columns")%columnCount)
    elif rowCount and not columnCount:
        # Translators: Speaks number of rows (example output: with 2 rows).
        textList.append(_("with %s rows")%rowCount)
    if rowCount or columnCount:
        # The caller is entering a table, so ensure that it is treated as a new table, even if the previous table was the same.
        oldTableID = None
    ariaCurrent = propertyValues.get('current', False)
    if ariaCurrent:
        try:
            textList.append(controlTypes.isCurrentLabels[ariaCurrent])
        except KeyError:
            log.debugWarning("Aria-current value not handled: %s"%ariaCurrent)
            textList.append(controlTypes.isCurrentLabels[True])
    placeholder = propertyValues.get('placeholder', None)
    if placeholder:
        textList.append(placeholder)
    indexInGroup=propertyValues.get('positionInfo_indexInGroup',0)
    similarItemsInGroup=propertyValues.get('positionInfo_similarItemsInGroup',0)
    if 0<indexInGroup<=similarItemsInGroup:
        # Translators: Spoken to indicate the position of an item in a group of items (such as a list).
        # {number} is replaced with the number of the item in the group.
        # {total} is replaced with the total number of items in the group.
        textList.append(_("{number} of {total}").format(number=indexInGroup, total=similarItemsInGroup))
    if 'positionInfo_level' in propertyValues:
        level=propertyValues.get('positionInfo_level',None)
        role=propertyValues.get('role',None)
        if level is not None:
            if role in (controlTypes.ROLE_TREEVIEWITEM,controlTypes.ROLE_LISTITEM) and level!=oldTreeLevel:
                textList.insert(0,_("level %s")%level)
                oldTreeLevel=level
            else:
                # Translators: Speaks the item level in treeviews (example output: level 2).
                textList.append(_('level %s')%propertyValues['positionInfo_level'])
    speech.oldTreeLevel = oldTreeLevel
    speech.oldTableID = oldTableID
    speech.oldRowNumber = oldRowNumber
    speech.oldRowSpan = oldRowSpan
    speech.oldColumnNumber = oldColumnNumber
    speech.oldColumnSpan = oldColumnSpan
    return speech.CHUNK_SEPARATOR.join([x for x in textList if x])

#
## End of NVDA sources/speech.py functions.
#

#
## Main global plugin class
#

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _("Translate")
    language = None

    def __init__(self):
        """Initializes the global plugin object."""
        super(globalPluginHandler.GlobalPlugin, self).__init__()
        global _nvdaSpeakText, _nvdaGetSpeechTextForProperties, _nvdaSpeak, _gpObject
        
        # if on a secure Desktop, disable the Add-on
        if globalVars.appArgs.secure: return
        _gpObject = self
        try:
            self.language = config.conf["general"]["language"]
        except:
            self.language = None
            pass
        if self.language is None or self.language == 'Windows':
            try:
                self.language = languageHandler.getWindowsLanguage()[:2]
            except:
                self.language = 'en'
                
        logHandler.log.info("Translate module initialized, translating to %s" %(self.language))
        _nvdaSpeak = speech.speak
        _nvdaGetSpeechTextForProperties = speech.getSpeechTextForProperties
        speech.speak = speak
        speech.getSpeechTextForProperties = getSpeechTextForProperties
        self.loadLocalCache()
        

    def terminate(self):
        """Called when this plugin is terminated, restoring all NVDA's methods."""
        global _nvdaSpeakText, _nvdaGetSpeechTextForProperties, _nvdaSpeak
        speech.speak = _nvdaSpeak
        speech.getSpeechTextForProperties = _nvdaGetSpeechTextForProperties
        self.saveLocalCache()

    def loadLocalCache(self):
        global _translationCache

        path = os.path.join(config.getInstalledUserConfigPath(), "translation-cache.json")
        try:
            cacheFile = io.FileIO(path, "r")
        except:
            return
        try:
            values = json.load(cacheFile)
            cacheFile.close()
        except Exception as e:
            logHandler.log.error("Cannot read or decode data from {path}: {e}".format(path=path, e=e))
            return
        _translationCache = values
    def saveLocalCache(self):
        global _translationCache

        path = os.path.join(config.getInstalledUserConfigPath(), "translation-cache.json")
        try:
            cacheFile = io.FileIO(path, "w")
            json.dump(_translationCache, cacheFile)
            cacheFile.close()
        except Exception as e:
            logHandler.log.error("Failed to save translation cache to {file}: {error}".format(file=path, error=e))
            return
        
            


    def script_toggleTranslate(self, gesture):
        global _enableTranslation
        
        _enableTranslation = not _enableTranslation
        if _enableTranslation:
            ui.message(_("Translation enabled."))
        else:
            ui.message(_("Translation disabled."))

    script_toggleTranslate.__doc__ = _("Enables translation to the desired language.")
            

    __gestures = {
        "kb:nvda+shift+control+t": "toggleTranslate",
    }
