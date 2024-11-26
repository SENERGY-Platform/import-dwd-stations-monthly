# import-dwd-stations-monthly

Allows you to import data from DWD weather stations with a monthly resolution. If configured in that way, historic data will be imported first.
Afterwards, the latest data will be imported every day.

## Outputs
*Outputs may contain the value -999 to indicate invalid or missing data.*
* temperature_2m_avg_celsius (float): Average temperature
* temperature_2m_avg_max_celsius (float): Average daily maximum temperature
* temperature_2m_avg_min_celsius (float): Average daily minimum temperature
* temperature_2m_max_celsius (float): Absoulte maximum temperature
* temperature_2m_min_celsius (float): Absolute minimum temperature
* sun_total_hours (float): Total sunshine hours
* precipiation_sum_mm (float): Total recipitation
* precipiation_max_mm (float): Maximum precipitation during one day
* meta (Object): 
  + name (string): station name
  + id (string): station id
  + lat (float): station latitude
  + long (float): station longitude
  + height (float): station height
  

## Configs
 * BBOXES (List): You can chain multiple bounding boxes to import multiple areas of interest. Make sure to choose these big enough to include at least one DWD station!
   You may use a tool like [this](http://bboxfinder.com/#51.294988,12.319794,51.370066,12.456779) to simplify the creation of these boxes.
   A map of all DWD stations is available [here](https://www.dwd.de/DE/leistungen/klimadatendeutschland/mnetzkarten/messnetz_tu.pdf?__blob=publicationFile&v=12).
   If not set, data of all stations will be imported. No default value available.
   +  Element (List of 4 floats): a bounding box in epsg 4326 projection, for example [12.178688,51.247304,12.572479,51.439885] covers parts of Leipzig.
 * HISTORIC (bool): If true, all available historic data will be imported. Default: false

---

This tool uses publicly available data provided by Deutscher Wetterdienst.
