import globalPluginHandler
from winsound import PlaySound
import controlTypes, ui, os, speech, NVDAObjects
import config
from scriptHandler import script, getLastScriptRepeatCount
from . import sounddata
import addonHandler
addonHandler.initTranslation()


loc = os.path.abspath(os.path.dirname(sounddata.__file__))

roleSECTION = "TalkBack sound effect by Susant"
confspec = {
"sayRoles": "boolean(default=false)",
"rolesSounds": "boolean(default=true)"}
config.conf.spec[roleSECTION] = confspec
rolesSounds= config.conf[roleSECTION]["rolesSounds"]
sayRoles= config.conf[roleSECTION]["sayRoles"]
def getSpeechTextForProperties2(reason=NVDAObjects.controlTypes.OutputReason, *args, **kwargs):
	role = kwargs.get('role', None)
	if 'role' in kwargs and role in sounds and os.path.exists(sounds[role]) and sayRoles ==False:
		del kwargs['role']
	return old(reason, *args, **kwargs)

def play(role):
	"""plays sound for role."""
	f = sounds[role]
	if os.path.exists(f) and rolesSounds==True:
		PlaySound(f, 1)

#Add all the roles, looking for name.wav.
sounds = {}
for role in [x for x in dir(controlTypes) if x.startswith('ROLE_')]:
	r = os.path.join(loc, role[5:].lower()+".wav")
	sounds[getattr(controlTypes, role)] = r
 
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory= _( "TalkBack sound effect for NVDA")
	def __init__(self, *args, **kwargs):
		globalPluginHandler.GlobalPlugin.__init__(self, *args, **kwargs)
		global old
		old = speech.speech.getPropertiesSpeech


	def event_gainFocus(self, obj, nextHandler):
		if rolesSounds == True:
			speech.speech.getPropertiesSpeech = getSpeechTextForProperties2
			play(obj.role)
		nextHandler()

	@script(gesture="kb:NVDA+alt+v")
	def script_toggle(self, gesture):
		global rolesSounds, sayRoles
		isSameScript = getLastScriptRepeatCount()
		if isSameScript == 0:
			rolesSounds = not rolesSounds
			if rolesSounds==False:
				ui.message(_("Disable TalkBack sound effect"))
			else:
				ui.message(_("Enable TalkBack sound effect"))
		elif isSameScript ==1:
			sayRoles = not sayRoles
			if sayRoles ==False:
				ui.message(_("Disable sayRoles"))
			else:
				ui.message(_("Enable sayRoles"))
		config.conf[roleSECTION]["sayRoles"] = sayRoles
		config.conf[roleSECTION]["rolesSounds"] = rolesSounds
	script_toggle.__doc__= _("Pressing it once toggles between on and off object sounds, and Pressing twice  it toggles between reading and disabling object types.")
