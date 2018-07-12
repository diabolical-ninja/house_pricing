# House Pricing

A simple python utility to download & parse the Australian auction results data provided by www.domain.com.au each week.

Results come out ~7pm AEST every Saturday so this can be scheduled to run around that time if desired.

## Running

1. Configure a PostgreSQL instance & create a table based on `/sql/table_creation.sql`

2. Create a configuration file based off `conf_sample.yaml`

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Execute the job
```bash
python domain_scraper.py
```




## Known Issues
1. The data is only as good as that provided by Domain.com. There are quite often data quality issues, eg prices listed as $40,000 rather than $400,000
2. The first 1-3 results are often missed in the scraping. I suspect this is due to how tabula is used. Possibly an alternate scraping mechanism is required?
3. The mechanism to identify the top of the results table can get stuck in an infinite loop when there are little to no results present.