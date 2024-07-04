We were using a library called yamsspy We have a couple copies of the folder, but the main coach should live on the Mac

I can't find an easy way to use the PS4 controller with [[python]] on the Mac. It seems to be something with the way the devices are managed by the OS.

The big issue used to be Bluetooth and so we actually went with a wired choice instead. Alternatively, we can use the Jetson nano, The jetson however, doesn't have Bluetooth built-in like the Mac

input device on the mac seems to be /Dev/CU.Bluetooth–incoming–port Whenever I try to connect to that, it just doesn't seem to do much


In the end, we were able to get the repository yamspy to work for us Every platform that we needed it to, so it was working on the Mac and the linux Jetson

We got the thermal camera running on the Jetson nano and then we called it a day. 

Something that we would later find. The problem is that we would not have a way to power the Judson from the battery, and so we had to come up with a solution to change the voltage of the battery from being a A value that changes over time to a stable 5 V. If we were to draw directly from the battery, we would be at the mercy of the voltage of the battery. 

This leads into some interesting problem that we ran into while we were trying to get the Jetson  into work. 

In our attempt to make sure that the Jetson has a constant 5 V we ordered a buck converter off of some online site, and when we went to use it, we were having issues on startup. Essentially it would turn on and last for about a number of seconds, and then the Jetson would turn off again. This only happened when we were trying to use the battery. However, we used a stable power supply. This was not an issue at all. We are not sure exactly why this was happening when we switched our converter to a different type of hardware things settled out. We think what was going on is that it was pulling too much power at start up

