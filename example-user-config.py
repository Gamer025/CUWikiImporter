# This is an automatically generated file. You can find more
# configuration parameters in 'config.py' file or refer
# https://doc.wikimedia.org/pywikibot/master/api_ref/pywikibot.config.html

# The family of sites to be working on.
# Pywikibot will import families/xxx_family.py so if you want to change
# this variable, you have to ensure that such a file exists. You may use
# generate_family_file to create one.
family = 'scavwiki'

# The site code (language) of the site to be working on.
mylang = 'en'

# The dictionary usernames should contain a username for each site where you
# have a bot account. If you have a unique username for all sites of a
# family , you can use '*'
usernames['scavwiki']['en'] = 'NameOfBot'

# The list of BotPasswords is saved in another file. Import it if needed.
# See https://www.mediawiki.org/wiki/Manual:Pywikibot/BotPasswords to know how
# use them.
password_file = "user-password.cfg"

# ############# LOGFILE SETTINGS ##############

# Defines for which scripts a logfile should be enabled. Logfiles will be
# saved in the 'logs' subdirectory.
#
# Example:
#     log = ['redirect', 'replace', 'weblinkchecker']
# It is also possible to enable logging for all scripts, using this line:
#     log = ['*']
# To disable all logging, use this:
#     log = []
# Per default, no logging is enabled.
# This setting can be overridden by the -log or -nolog command-line arguments.
log: list[str] = []
# filename defaults to modulename-bot.log
logfilename: str | None = None
# maximal size of a logfile in kilobytes. If the size reached that limit the
# logfile will be renamed (if logfilecount is not 0) and the old file is filled
# again. logfilesize must be an integer value
logfilesize = 1024
# Number of rotating logfiles are created. The older files get the higher
# number. If logfilecount is 0, no logfile will be archived but the current
# logfile will be overwritten if the file size reached the logfilesize above.
logfilecount = 5
# set to 1 (or higher) to generate "informative" messages to terminal
verbose_output = 0
# set to True to fetch the pywiki version online
log_pywiki_repo_version = False
# if True, include a lot of debugging info in logfile
# (overrides log setting above)
debug_log: list[str] = []

# ############# SETTINGS TO AVOID SERVER OVERLOAD ##############

# Slow down the bot so that it never issues two API requests within
# 'minthrottle' seconds. This delay may be increased if the server is slow
# or requests are limited by bot policy, but never beyond 'maxthrottle'
# seconds. When running multiple bots in parallel, the effective waiting
# time is increased accordingly. The default setting is 0.1 seconds per
# https://wikitech.wikimedia.org/wiki/Robot_policy.
#
# 'maxlag' is used to control the rate of server access (see below).
# Set minthrottle to non-zero to use a throttle on read access.
minthrottle = 0.1
maxthrottle = 60

# Slow down the robot such that it never makes a second page edit within
# 'put_throttle' seconds.
put_throttle: int | float = 10

# Sometimes you want to know when a delay is inserted. If a delay is larger
# than 'noisysleep' seconds, it is logged on the screen.
noisysleep = 3.0

# Defer bot edits during periods of database server lag. For details, see
# https://www.mediawiki.org/wiki/Manual:Maxlag_parameter
# You can set this variable to a number of seconds, or to None (or 0) to
# disable this behavior. Higher values are more aggressive in seeking
# access to the wiki.
# Non-Wikimedia wikis may or may not support this feature; for families
# that do not use it, it is recommended to set minthrottle (above) to
# at least 1 second.
maxlag = 5

# Maximum of pages which can be retrieved at one time from wiki server.
# -1 indicates limit by api restriction
step = -1

# Maximum number of times to retry an API request before quitting.
max_retries = 15
# Minimum time to wait before resubmitting a failed API request.
retry_wait = 5
# Maximum time to wait before resubmitting a failed API request.
retry_max = 120

