
#Log Analysis Project

The following directions describe how to prepare the VM using this repository, create necessary views, and run the app to generate results

###Prepare the virtual machine

Download and install Vagrant and VirtualBox.

Download zip and open onto your local machine.  

Navigate to the project directory using terminal.

Launch virtual machine by using the command ```vagrant up```

Start session using command ```vagrant ssh```

Navigate to Vagrant directory ```cd /vagrant```

Load data from SQL file in zip ```psql -d news -f newsdata.sql```

Connect to DB ```psql -d news```

###Add the following views:

List of errors
```
CREATE VIEW errors AS
SELECT DATE(time) as day,
       CAST(COUNT(status) AS FLOAT) AS errors
FROM log
WHERE NOT status='200 OK' GROUP BY day ORDER BY day;
```

List of total requests
```
CREATE VIEW requests AS SELECT DATE(time) AS day, CAST(COUNT(status) AS FLOAT) AS requests FROM log GROUP BY day ORDER BY day;
```
List of the total errors by day plus percenge of the whole
```
CREATE VIEW errorpercentages AS
SELECT requests.day,
       requests.requests AS numall,
       errors.errors AS numfailed,
       errors.errors::double precision/requests.requests::double precision * 100 AS dailyrate
FROM requests
JOIN errors
ON requests.day = errors.day;
```

###Run The App

Disconnect from DB using ```\q```

Run application and see results```python3 app.py```
