# House Pricing

A simple python utility to download & parse the Australian auction results data provided by www.domain.com.au each week.


## Running

1. Configure a PostgreSQL instance & create a table based on `/sql/table_creation.sql`

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Execute the job
```bash
python domain_scraper.py
```

Results come out ~7pm AEST every Saturday so this can be scheduled to run around that time if desired.