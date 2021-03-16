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

