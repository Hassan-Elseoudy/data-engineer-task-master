# Data Engineer Task

For the assignment, you have to process a file and enrich it with data provided by an API in order to provide high-level aggregate info.

Our goal is to see how you implement the missing parts of the API and how you deal with file processing and data structures manipulation.

As we use to containerize our applications please add a Dockerfile for running the api.

Provide the code in a way that you would push to production ;)

## Description

### API

There are two endpoints that need to be implemented, one that searches for the `user_status` on a given date and another one that returns a `city` based on the provided IP.

#### Endpoint user_status
`/user_status/<user_id>?date=2017-10-10T10:00:00`

On this endpoint please provide an implementation that searches the records and returns the correct `user_status` at the given date.
You can imagine the records as single events which get fired on a user status change. If a user starts paying, there will be one record stored with status `paying`, whereas if this user stops paying, there will be another record added with status `cancelled`. Consequently a user remains in status `paying` until the next `cancelled` event.
In case there is no status available for a specific date, simply return `non-paying`.
The valid responses that should be provided are: `paying`, `cancelled` or `non-paying`.

#### Endpoint city
`/ip_city/10.0.0.0`
On this endpoint please provide an implementation that searches the provided IP ranges and returns the correct city based on the IP.
In case the IP range is not within any of the provided cities, **unknown** should be returned.

### File Processing

Please read the file `transactions.json` and enrich it with the data given by the API.
The output of the script should provide an aggregate containing the sum of `product_price` grouped by `user_status` and `city`.

## Setup

There is a simple API which you'll need to install.
To run the API just run the api.py file.

```
pip install -r requirements.txt
python api.py
```


### Delivery

Please provide a zip or tar file containing your complete implementation.
