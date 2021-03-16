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

Later call `socatlord run` to terminate currently running socats and launch your own.
This may terminate your SSH connection, if you're using a socat to proxy it though.

You can also call `socatlord stop` to stop all socats.

You can provide an optional argument of `-v` to see what commands are launched

# Changelog

## head

* socat's will be silenced if the mode is not verbose

## v1.0

First formal release
