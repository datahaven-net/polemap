# polemap

Pole Numbers in Anguilla

This Django Application serves a small Web Page that accepts Anguila Pole Numbers as input and then redirects user to the corresponding GPS location on GoogleMaps.

Here is a description of how the poll numbers map to GPS locations in Anguilla: https://news.ai/ref/polenumbers.html

Visit www.polemap.ai to open the web app in your browser.

You can also use Rest API to get GPS location encoded as a JSON:

		curl https://polemap.ai?input=S22J44
		{
			"lat": 1234,
			"lon": 1234,
			"url": ""
		}
