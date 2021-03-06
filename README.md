# properties-dashboard
My [Streamlit](https://streamlit.io/) app for properties pricing data visualization

## Intro

[Streamlit](https://streamlit.io/) is a great tool to develop data visualization. It's written in Python which is also a language widely used in data analysis and engineering.
What you'll see here is my take on a way to quickly find properties of interest by glancing their prices in a city map.
The prices were obtained by means of *[scraping](https://en.wikipedia.org/wiki/Web_scraping) a certain website*, in the beginning of October 21'. To get them in an automated manner, a spider was built with the Python [Scrapy](https://scrapy.org/) module and it generated a .csv file, after submitting the scraped data through a few pipelines.

## Usage

To enjoy the dashboard, you must load the .csv file (there's a button on the dashboard for that purpose).
After loading the data, if the visualization is still cluttered, use the slider bar on the left menu. It will filter the prices according to the [minimum-maximum] range found.
The main visual feature idea was to map properties by columns which are proportional to their prices.
A color code to help locating prices according to price ranges was created (the prices grow according to the frequency of the color, inspired by the rainbow color sequence). That code also helps differentiating properties when they are located too close to each other. Another measure to help visualization was to give the more expensive a properties columns more transparency (but that's still not the ideal). Hovering the mouse over a property will show both it's ID and price.

## Look
![Long live the dark themes!](.github/Price_mapper.png)

## Future features
There's also a few metrics like average price, number of properties found, and number of properties who did not get mapped because they lack coordinate information.
As of October 21' no history of pricing is being kept as I'm still working on my SQL studies. I also plan on improving how the overlapping price columns behave in order to give a better viewing experience.
