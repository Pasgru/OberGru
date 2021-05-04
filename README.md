# OberGru - A Discord Bot
This is a custom bot used to counteract some of Discord's shortcomings. 
It is custom made for the [Weinfeinschmecker](https://discord.gg/g8y3CpE) 
Discord Server and does not work elsewhere. It is developed with 
[discord.py](https://discordpy.readthedocs.io/en/latest/).

## Features
### Removal of certain link previews
Most link previews are not informative and only clutter up the text channel.
The bot suppresses the embeds of every message if it contains a non whitelisted
Website. It does this in `#schwarzes-brett`, `#küchenpass` and `#feldstüberl`.
The whitelisted websites are:

- youtube.com/watch
- youtu.be
- redd.it
- imgur.com
- tenor.com/view

Additionally the following suffixes to an url are allowed:

- .png
- .jpg
- .gif

This feature is highly inconsistent and not reliable.

### Dynamic creation of voice channels
In the channel category `RÄUMLICHKEITEN` there is always EXACTLY one empty voice
channel. This is achieved by adding a new one every time someone joins the empty channel
and deleting a channel if everyone disconnects from it and it is not the last channel.
The names of the generated channels are constructed from a pool of prefixes and suffixes.

### Custom vanity role command
In the channel `#plattenspieler` you can assign yourself a custom vanity role. To do this
you use the command `/gru` this command takes two parameters `name` and `color`. There are
some restrictions for the parameters: `name` must start with an uppercase letter or a number
and `color` must be a six digit hexadecimal number beginning with a `#`. You can change your
role anytime by using the command again.

There is the option of removing your self assigned role aswell. This is done by invoking the 
command `/ungru`.
If you don't have administrative rights, you can only remove your own custom role. Admins,
on the other hand, have the ability to add optional `user` and `reason` parameters to
remove someone elses role. If an admin wants to remove someone elses role, there always has
to be a `user` provided but not necessarily a `reason`.
