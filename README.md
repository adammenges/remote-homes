# remote-homes
Every time I travel, I do the same thing. Hunt around on a few sites for
a reasonably priced place with good reviews, specifically looking at the
reviewers thoughts on the wifi, because there's no way for me to work
remotely without solid Internet. It's quite the task for me to find a
place factoring in all these variables. Well, no longer.


This script many sources, more then I could ever check, and ranks them based
on the variables above. Uses Sentiment Analysis for determining the reviewers
feeling on the wifi.


Sources: 
* airbnb
* alwaysonvacation
* apartmentsapart
* bedycasa
* bookingpal
* citiesreference
* edomizil
* geronimo
* gloveler
* holidayvelvet
* homeaway
* homestay
* hostelworld
* housetrip
* interhome
* nflats
* roomorama
* stopsleepgo
* theotherhome
* travelmob
* vacationrentalpeople
* vaycayhero
* waytostay
* webchalet
* zaranga


## Running
Run with `ipy -i run.py`, it'll print out some stuff, then look around the results within `homes`. Open a listing with `webbrowser.open(home['provider']['url'])`.
