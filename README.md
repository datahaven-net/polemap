# polemap

This Django Application serves a small Web Page that accepts Anguila Pole Numbers as input and then redirects user to the corresponding GPS location on GoogleMaps.

Visit www.polemap.ai to open the web app in your browser.


## Pole Numbers in Anguilla

If you can see a power pole, you can't claim to be lost in Anguilla anymore!

All the poles are being stenciled with a code that gives their GPS location - very useful on an island with few street names and no street numbers.
Bring your GPS on your next visit to Anguilla.

This project was managed by Griffin Webster/Weblinks for [Anglec](http://www.anglec.com/), the Anguilla Electricity Company. He started using Anguillian students working for the summer at Beachtech to read the GPS, compute the code using a Palm Pilot and record the data into an Access database (Indah Wallace, Csaes Watley and Aldo Jackson). By the end of the summer the GPS reading and coding were turned over to the painting crew: Irwin Proctor and Ras Isamaus Jahnya.

![powerpole02.jpg](https://news.ai/ref/images/powerpole02.jpg "powerpole02.jpg")


## How it works?

Here is the key for decoding the pole labels to GPS locations.

The label is made up of two parts. The top part is the North-South location and the bottom part is the East-West location. Each part of the label is made up of one letter and two digits.

Using the tables below, the letters can be decoded to a number that gives the Hours and Minutes. Then you add the two digits to it, giving a precise GPS location.

| North-South | East-West |
| ----------- | --------- |
| 18:17=Q     | 63:10=A   |
| 18:16=R     | 63:09=B   |
| 18:15=S     | 63:08=C   |
| 18:14=T     | 63:07=D   |
| 18:13=U     | 63:06=E   |
| 18:12=V     | 63:05=F   |
| 18:11=W     | 63:04=G   |
| 18:10=X     | 63:03=H   |
| 18:09=Y     | 63:02=I   |
|             | 63:01=J   |
|             | 63:00=K   |
|             | 62:59=L   |
|             | 62:58=M   |
|             | 62:57=N   |


Note that the letters in the North-South table do not conflict with those in the East-West table. This is to ensure that there is no confusion with the translation.

![powerpole01.jpg](https://news.ai/ref/images/powerpole01.jpg "powerpole01.jpg")


For example, the picture above shows the pole outside the News.ai office: S17 over J44, translates as 18:15.17N 63:01.44W, or 18 degrees 15.17 minutes North, 63 degrees 01.44 minutes West.

Note. Some GPS's can show the locations as XXX.yyyy degrees as well. To determine the location in this format, first convert to XX degrees yy.yy minutes. Then get a mathematician to show you how to convert base 60 numbers to decimal. 


Original source of that doc page can be found here: https://news.ai/ref/polenumbers.html
