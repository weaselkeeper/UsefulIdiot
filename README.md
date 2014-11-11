UsefulIdiot
===========

UsefulIdiot is a python re-implementation of the bits of Netfix's Simian Army I find useful to me, (https://github.com/Netflix/SimianArmy)

It is designed to be invoked remotely, by a tool like ansible, or locally, by directly invoking the UsefulIdiot.py script, with any appropriate options.  It's default behaviour in either case, is to randomly kill a process on the host.  Different plugins can be invoked instead of the pidkiller plugin. But that is the default action.

Currently, we have the following plugins.

pidkiller:	Kills a random pid
bouncer:	Bounces a random service.
cronripper:	Deletes the crontab of a valid, random user. All crontabs should be in puppet. Or other CMS
package_nuker:	Uninstall a random package (currently not very functional)
reboot:		Reboots the server.  Your clusters are HA, right?
runpuppet:	Forces a puppet run.  Hope you didn't make any changes and not update puppet
runchef:	Forces a chef run.  Hope you didn't make any changes and not update chef
tempreaper:	Removes files in /tmp.  Were they important?
toggle_selinux:	(En/Dis)able SELinux.  Puppet/chef/etc should set that right, right?
