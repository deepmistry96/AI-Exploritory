 in order to send images back-and-forth we're gonna probably use a [[UDP connection]] the Mac And the Jetson

 The IP address for the Jetson is going to be 192.168.50.235
 The The Mac's IP address is going to be 192.168.50.131

 A lot of this code is going to be in the repo that we will name albatross

 There is Some code in a folder, called UDP_comms And it seems to at least send something out and receive a ping. 

 One of the common issues that we've had is that the firewall permissions on the different operating systems can get in the way. We are constantly having to deal with issues where on linux and Mac we don't have to Have a [[firewall]], but when we are on the windows, we do need to have a firewall. We could turn the firewall But then we would have issues with security, so it is not seen as as a best practice. 

 The firewall is disabled by default on the Mac

 It looks like the firewall doesn't even exist on Linux 
    There is a Command called ```sudo ufw [enable, disable, reset]```
    
    On my set up, it looks like the enable does not work the disable and the reset do so essentially traffic is blocked when the firewall is enabled.

    However, like chromium, still do work with the firewall enabled

    This is going to be a problem for me, but it's not some thing that's not solvable there should be a way for me to also be unblocked when the firewall is enabled if we need the firewall to be enabled.


So we think we might have found a pretty decent streaming solution for getting our footage from the Jetson nano to the main computer that's going to be doing the computer vision. It looks like [[mediaMTX]] is going to be used to set up the server, Peg is going to set up the stream to a /dev/video Device somewhere on our machine. That's gonna be the pathway that the [[modprobe]] + [[V4l2loopback]] is going to use, And then we're going to use [[pyfakewebcam]] As the final one for the virtual WebCam and the destination machine. 

The steps to start up seem to be starting mediaMTX followed by [[FFMPeg]], followed by V4L2Loopback, followed by the [[pythermal camera repository]] running the TC001V4 [[python]] script and then using the repository called testing on Mac where we have a python script, that is running the [[detect.py script]]


