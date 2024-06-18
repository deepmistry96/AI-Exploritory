We were looking into the routing rules and that brought up the topic of where the core of the issue may lay.

Rob was initially thinking that it was that the IP routes had not been setup, 
Deep was thinking that the core of the issue was closer to the firewalls
A simple test was run where we disabled the firewalls to see if the routes did exist or not.

We determined that the Public Firewall on the Windows side, was the firewall that was restricting traffic. 
    - The interesting thing that Rob was thinking was that, well if we are using a local IPv4 subnet that is private, why is the public firewall giving us a headache? 
    - A possible explaination for this is that the "gateway" machine mapped to 100.96.1.1 is somewhere else on the internet. Therefore the traffic must be routed via the public firewall
    - What if we enabled that specific app to route traffic though the public firewall? 



Routing a specific app though the filewall
    - Unfortunately we setup the inbound and outbound rules to allow for the OpenVPNConnect.exe client to allow for traffic to flow though the firewall, we made sure to select to apply this rule to the public firewall, but we were unsuccessful.



