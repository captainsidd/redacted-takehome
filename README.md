# Klarna Take Home

A server implementing Fibonacci, Ackermann, and Factorial functions. Includes monitoring.

## Setup

This project was built with Python 3.8.0, but should work with 3.6.0+. To install required packages, run:

`$ pip install -r requirements.txt`

## Usage

To start the app, run:

`$ FLASK_APP=main.py flask run`

This will start the program on port 5000. A series of sample curl commands to the webserver can be found in `requests.sh`. Alternatively, navigate to the available paths in your browser.


### Available Paths

* `/fibonacci/<int:nth_number>`

Returns the `n`th number of the Fibonacci series. Expected to error out if given value is not a non-negative integer.

* `/ackermann/<int:m_number>/<int:n_number>`

Returns the result of the Ackermann function for given `m` and `n` numbers. Expected to error out if given values are not non-negative integers. Computationally limited to small values because of the nature of the Ackermann function.

* `/factorial/<int:factorial_nth>`

Returns the nth factorial of the given integer parameter `n`. Expected to error out if given value is not a non-negative integer.

* `/_metrics/`

This endpoint exposes basic metrics about the program. The structure of the metric object returned is as follows:

```json
{
  "<method>": {
    "invocations_success": "value: int",
    "invocations_error": "value: int",
    "invocations_total": "value: int",
    "averages": {
      "latency": "value: float",
      "latency_units": "seconds",
    },
  }...<repeated for each non-metric method>
}
```

## Decisions

First I started off with implementing the Ackermann function, because that was the one function that I was not familiar with mathematically. Looking at [Wikipedia](https://en.wikipedia.org/wiki/Ackermann_function) to find the mathematical definition was simple, but quickly realized that the naive recursive approach bumped up against recursion and heap size limits. I then attempted to try to find a dynamic programming solution, and started work on reproducing the table found in the Wikipedia article using the methodology explained in Wikipedia:

```
Computing the Ackermann function can be restated in terms of an infinite table. First, place the natural numbers along the top row. To determine a number in the table, take the number immediately to the left. Then use that number to look up the required number in the column given by that number and one row up. If there is no number to its left, simply look at the column headed "1" in the previous row.
```

I tried to implement this table, but found I still had to recurse in order to populate parts of the table, as Ackermann will require the generation of multiple tables to find the values that need to be input into the function. I'm sure there's a mathematical function for how to generate those values, but I couldn't figure it out after a few hours, esp without using Google to look up other people's work. I scrapped the dynammic programming option and decided to live with the simple recursive approach. Later, I added my dynamic programming approach back into my program in an unused function so you all can see how far I got.

Moving on, I quickly implemented factorial and fibonacci in iterative rather than recursive approaches. Knowing that I would need to stand up a webserver, I opted to store the entire Fibonacci sequence generated so that if a request came in for a number that had already needed to be generated for a previous request, it would be extremely quick to look up (O(1) lookup time).

I created a class to store the generated Fibonacci sequence, as well as adding memoization to my Ackermann approach. This way, I wouldn't need to re-recurse given an input - if I had received it before I could return the result with O(1) lookup time. I also added wrapper functions around the actual computational functions, which I set to private, because of all the clean code benefits - it would be easier for testing, observability, and also allows for changes to computational implementations (such as a dynamic programming solution to Ackermann).

Then I added monitoring to the wrapper methods, so that we could surface those metrics through an endpoint. I added counters for total, successful, and erroneous requests, and also added latency measurements for each method as well. I made sure to specify the units for latency, as well as round those values.

Obviously, there's a lot of room for improvement here - specifically with improving the implementation of the Ackermann function. Better monitoring could also be done, with data about memory/heap usage, more granular information for the last few requests, and better error reporting. Also, adding unit and integration tests would be helpful.
