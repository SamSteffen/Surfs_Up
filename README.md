# Surfs_Up
## Overview
The following is an analysis of Oahu weather data for investor buy-in on a Hawaii-based surf/ice-cream shop, using SQLite, SQL Alchemy, and Flask. Because the investor expressed concern about precipitation in the proposed location (Oahu), our initial analysis pulled the daily precipitation levels from 9 separate weather stations within the Aug. 23, 2016 - Aug. 23, 2017 timeframe. We then put this data into a dataframe and mapped it using matplotlib dependencies. The following shows the results of this query.

<img width="305" alt="precip_barchart" src="https://user-images.githubusercontent.com/104729703/182048780-c43e519e-10a0-4b47-9814-4a1405c4007e.png">

Once the precipitation data was gathered, we identified the weather station that had the greatest number of data points ('USC00519281') and filtered the dataset to see only data gatherd from this weather station. We then wrote another query to get temperature data from the same timeframe as above, using only the weatherstation with the greatest number of data points. The following is a histogram, illustrating the findings of this search in a histogram, seperated into 12 temperature bins:

<img width="326" alt="temp_histogram" src="https://user-images.githubusercontent.com/104729703/182048784-0ce692d8-39f1-4437-8e66-e5fc472901e2.png">

Following this initial analysis, further information was requested, specifically temperature information in Oahu for the months of June and December, in order to determine if the surf and ice cream shop business is sustainable year-round. To find this, further analysis was necessary.

## Results
To determine the summary statistics for the month of June, we set up our query session using the sqlalchemy dependencies. We then wrote a query that filtered the date column from the Measurement table to retrieve all the temperatures for the month of June from the entire data set, which hosts records from 01-01-2010 to 8-23-2017. We added this info to a pandas dataframe and then generated the summary statistics using the .describe() method. The following table resulted:

<img width="109" alt="June_temps" src="https://user-images.githubusercontent.com/104729703/182048791-04394f6d-485a-43f4-8ad5-60052080127c.png">

Once we discovered the data for June, the above process was repeated, refactoring the code to pull only data for the month of December. The resulting statistics from the .describe() method on the December data yielded the following table:

<img width="134" alt="December_temps" src="https://user-images.githubusercontent.com/104729703/182048796-bc7aefc9-fc89-4bef-ba10-669c4eb62b4c.png">

By comparing the data in the two tables above, we can see that:
- The average temperature for the month of June is 74.9 degrees Fahrenheit, with a standard deviation of 3.25 degrees, indicating relative consistency, while the average temperature for the month of December is 71 degrees Fahrenheit, with a standard deviation of 3.74 degrees, indicating relative consistency.
- The minimum temperature for the month of June is 64 degrees Fahrenheit while the minimum temperature for the month of December is 56 degrees Fahrenheit.
- The maximum temperature for the month of June is 85 degrees Fahrenheit while the maximum temperature for the month of December is 83 degrees Fahrenheit.

## Summary
It's worth mentioning at the outset that the sizes of the two datasets for the above analysis are not the same; the June data was the result of 1,700 data points and the December data contains 1,517 data points. In spite of this, the two datasets still represent a robust set for a 30-day month (June) and a 31-day month (December) at opposite seasons of the year. 
While it has not been stated explicitly what average temperature should be used to measure whether people will want to surf and have ice cream year-round, the above analysis of Oahu temperature data for the months of June 2010-2017 and December 2010-2016 shows the following:
- Becuase there is roughly 4 degrees difference in the average temperature of June versus December, it is likely that temperature will not affect the success or failure of the business.

To determine additional queries that we could perform on the dataset, we can review what data is available to us in the "measurement" class, by running the following:

    ```
    results = session.query(Measurement)
    print(results)
    ```

This shows that contained in the measurement class are: ID, station, date, precipitation and temperature measurements. Knowing this, we can determine other queries to run on the datasets for the months of June and December. For instance, we could determine the average precipitation for the month of June by running the following script:
    
```
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(extract('month', Measurement.date)==6)
    June_precip_df = pd.DataFrame(results, columns=['date', 'June Precip'])
    June_precip_df.describe()
```

We could then refactor this code to determine the average precipitation for the month of December. 

```
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(extract('month', Measurement.date)==12)
    Dec_precip_df = pd.DataFrame(results, columns=['station', 'date', 'December Precip'])
    Dec_precip_df = June_precip_df.drop(columns=['station'])
    Dec_precip_df.describe()
```

From the above code, the following tables result:

<img width="113" alt="June_precip" src="https://user-images.githubusercontent.com/104729703/182048813-5f18e7d5-aa7b-4865-a115-bfafc3317e50.png">  <img width="132" alt="December_precip" src="https://user-images.githubusercontent.com/104729703/182048828-bb685afd-eda6-44c9-9583-76e7a8c9490a.png">

- A comparison of the above shows that the average rainfall in June is 0.13 inches and less than 4.43 inches at the maximum recording. 
- For December, average rainfall is 0.21 inches and less than 6.4 inches at the maximum recording.

It would also be interesting to look at tourism information and see whether Oahu has more tourists visiting in the summer or winter months, as this information probably could impact the success of the business and might be a better indicator of projected success.

- Additionally, to determine with certainty how or whether temperature impacts ice-cream sales, we could gather data on other similar businesses in places with temperature fluctuations to determine a "measure for success" marker--that is, an average temperature above which it would be safe to say that an ice-cream business could remain open all winter long.
