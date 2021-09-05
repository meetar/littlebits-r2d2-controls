README.md

littlebits r2d2 bluetooth controller

SO I bought the littlebits droid inventor kit for my daughter.
HOWEVER it requires an app.
HOWEVER: the app is no longer available.

SO: I decided to try to make a new interface so my daughter could control r2d2 from her ipad.

The app isn't available because littlebits was bought by sphereo and sphero pulled support for the kit and the app.

HOWEVER: littlebits made another kit called the space rover inventor kit, which uses similar parts, and includes an app.

HOWEVER: the space rover inventor kit app doesn't support the droid inventor hardware, and won't connect to the droid inventor kit control hub.

HOWEVER: the space rover control hub is very similar to the droid inventor control hub. as far as I can tell, the only difference is the model number:
w33 vs [w32](http://terg.is/projects/controlhub/). (I'm sure [Andrew](http://terg.is/#about) knows.)

SO: i bought the space rover inventor kit, and got the space rover inventor app.

THEN: i used bluetooth sniffing to capture the control messages from the app to the control hub, following this guide: https://mezdanak.de/2019/07/12/ios-bluetooth-packet-logging/

first I had to setup a bluetooth debugging profile on my iPhone: https://www.bluetooth.com/blog/a-new-way-to-debug-iosbluetooth-applications/

THEN: i connected my computer to the droid inventor control hub with bluetooth and tried sending the same control messages, and IT WORKED! kind of.

the space rover kit includes a few sounds, maybe 5? which are triggered by sending certain command sequences.

each of those command sequences also triggers sounds on the r2 unit.

HOWEVER: the r2 unit was advertised to include 20 sounds.

SO: i started looking closely at the control sequences for triggering the space rover sounds.

I converted the sequences from hex to decimal and started looking for relationships.
https://www.rapidtables.com/convert/number/hex-to-decimal.html?x=1402020F8A82

You can also do this in excel using =HEX2DEC(), which is faster.

I noticed by subtracting them from each other that they seemed to be separated by a few common intervals, numerically.

SO: i started extrapolating out along the number line, looking for other numbers in the same sequence. and I found more sounds!

HOWEVER: there was a gap in the number sequence, and also one more important sound missing.

SO: i brute forced-it, and found the sound!

THEN: i captured all the control sequences for controlling the two drive motors on the spare rover, and determined that they also worked for the r2 unit.

HOWEVER: there didn't seem to be any simple function that determined the control sequences, they were more-or-less arbitrary numbers in a sorted array.

360 degrees of turn, and 62 different drive motor speeds.

there were lots of duplicates in the captured commands, so i deduped them using this trick in vscode: https://stackoverflow.com/questions/37992493/how-can-i-remove-duplicate-lines-in-visual-studio-code

i determined that there were really only a few important values, and the others were duplicates. 32 important turn values, and 62 important drive values.

THEN i put those values into an array.

THEN i connected a web browser to the r2 unit control hub with bluetooth.
THEN i made a javascript interface on a webpage, and connected sliders to the commands. this mostly worked!

Then I used a joystick controller I found at https://www.cssscript.com/touch-joystick-controller/ and used it in a similar way.

Then I tried to use the controls on a mobile device.

HOWEVER: it turns out most modern browsers don't offer the same web bluetooth support on mobile devices.

HOWEVER: there are custom third-party browsers that do. I downloaded WebBLE and Bluefy.

WebBLE has an output console, but costs $2 and has hinky controls.
Bluefy doesn't support local ip addresses, but is more reliable once you get it started.

SO: i made an interface that worked in these mobile browsers, mostly.

HOWEVER: there were serioud performance problems, caused by overloading the control hubs.

SO: i throttled the commands so the control hub wouldn't be overloaded.

THEN: my daughter designed an interface, and we coded it up together.

here it is!