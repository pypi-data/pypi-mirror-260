# MultiTerm

_A framework for breaking a terminal window into seperate instaces, in the same window._

# Warning from an included Package regarding mouse input:
*From the [asciimatics docs](https://asciimatics.readthedocs.io/en/latest/io.html#input)*  
```
Warning

In general, Windows will report all of these straight out of the box. Linux will only report mouse events if you are using a terminal that supports mouse events (e.g. xterm) in the terminfo database. Even then, not all terminals report all events. For example, the standard xterm function is just to report button clicks. If you need your application to handle mouse move events too, you will need to use a terminal that supports the additional extensions - e.g. the xterm-1003 terminal type. See Mouse support not working for more details on how to fix this. 
```