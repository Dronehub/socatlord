# socatlord

socatlord is a tool to manage multiple socats

You feed it with a config file placed at
`/etc/socatlord` that has the syntax like:

```
# this is a comment

9.9.9.9:80 -> 123.23.4.3.:81
80 -> 192.168.224.20:80
udp 0.0.0.0:23 -> 192.168.224.20:23
```

TCP is the default protocol.
Socatlord will spawn as many socats as necessary.

# Usage

After you put this file, call `socatlord install`. This will install and enable socatlord to start
during your startups (only if you're using Systemd).
`/etc/socatlord` will be created about then.

Note that installation itself will not start socatlord! After installation put your configuration in
`/etc/socatlord`.

Later call either `socatlord run` 
or `systemctl start socatlord.service` to terminate currently running socats and launch your own.
This may terminate your SSH connection, if you're using a socat to proxy it though, however it will destroy them
and restart in one go.

You can also call `socatlord stop` to stop all socats.


You can provide an optional argument of `-v` to see what commands are launched.
You can provide an optional explicit path to config file, if `/etc/socatlord` is meant not to be used.
socatlord must be run as root. A check will be made for this.

# Changelog

## v1.2

* socatlord uses argparse
* socatlord will check if it's ran as root

## v1.1

* socat's will be silenced if the mode is not verbose
* better default `/etc/socatlord`

## v1.0

First formal release
