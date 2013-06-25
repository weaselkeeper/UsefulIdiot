UsefulIdiot
===========

UsefulIdiot is a python re-implementation of the bits of Netfix's Simian Army I find useful to me, (https://github.com/Netflix/SimianArmy)

It is designed to be invoked remotely, by a tool like ansible, or locally, by directly invoking the UsefulIdiot.py script, with any appropriate options.  It's default behaviour in either case, is to randomly kill a process on the host.  Different plugins can be invoked instead of the pidkiller plugin. But that is the default action.
