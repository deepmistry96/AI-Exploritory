We want to be able to share compute resources so that we dont have to rent server time from companies like google or amazon. 

This should enable us to have more freedom with what we can do. 

Working with Rob we are going to add some new firewall rules on the testbed ultimate.

So we are adding a new inbound rule to the "New Inbound Rule Wizard" and we are going to set the protocol type to "Any"
    - This should allow for us to use a range of values
    - We identified that we have an Iv4 tunnel setup and so we know that the connection is private and we can be looser with the security
    - We are using the range function 
    - Rule was called "OpenVPN Custom Config Test"

What is IPSec? 


There is a possiblity to limit who can RDP into the testbed via the rule properties.
    - I dont see us neededing this but it might be a useful feature.


IP Mapping 
    - Our gateway is configured to 100.96.1.1

    - The testbed-ultimate is configed to 100.96.1.4

    - My mac laptop is configured to 100.96.1.2

