from errors import ComputationError
import json
import time

LATENCY_PRECISION = 6

"""
Class object that implements required fibonacci, ackermann, factorial functions.
Includes wrapper functions for required functions called by API layer.
Stores metrics about function executions for observability.
"""
class Klarna():

  def __init__(self):
    # initialize storage for fibonacci numbers
    self.fibo = [0, 1]
    self.max_fibo = 2

    # remember ackermann numbers because computationally expensive
    self.ackermann_memos = {}

    # metrics object for telemetry
    self.metrics = {
      "fibonacci": {
        "invocations_success": 0,
        "invocations_error": 0,
        "invocations_total": 0,
        "averages": {
          "latency": -1,
          "latency_units": "seconds",
        },
      },
      "ackermann": {
        "invocations_success": 0,
        "invocations_error": 0,
        "invocations_total": 0,
        "averages": {
          "latency": -1,
          "latency_units": "seconds",
        },
      },
      "factorial": {
        "invocations_success": 0,
        "invocations_error": 0,
        "invocations_total": 0,
        "averages": {
          "latency": -1,
          "latency_units": "seconds",
        },
      },
    }


  def fibonacci_handler(self, n:int) -> str:
    """
    Wraps the Fibonacci function
    Stores the values of all numbers generated to reduce resource utilization
    """
    latency_start = time.time()
    if type(n) is not int or n <= 0:
      self.update_metrics(method="fibonacci", latency=time.time()-latency_start, success=False)
      return "Invalid parameters: `fibonacci` takes in non-negative integers"
    try:
      result = self.fibonacci(n)
      self.update_metrics(method="fibonacci", latency=time.time()-latency_start, success=True)
      return str(result)
    except ComputationError:
      self.update_metrics(method="fibonacci", latency=time.time()-latency_start, success=False)
      return "Unable to compute fibonacci of {}".format(n)
    except:
      self.update_metrics(method="fibonacci", latency=time.time()-latency_start, success=False)
      return "Unknown error for `fibonacci`"


  def fibonacci(self, n: int) -> int:
    """
    Implements generation of the nth Fibonacci number for a given n
    Stores all previous Fibonacci numbers generated for optimization reasons
    Raises ComputationError if errors occur
    """
    try:
      if n > self.max_fibo:
        count = self.max_fibo
        while count < n:
          self.fibo.append(self.fibo[-1] + self.fibo[-2])
          count += 1
        self.max_fibo = count
        return self.fibo[-1]
      else:
        return self.fibo[n-1]
    except:
      raise ComputationError


  def ackermann_handler(self, m, n) -> str:
    """
    Wraps the Ackermann function implemented recursively
    Stores the values of previous calls to reduce resource utilization
    """
    latency_start = time.time()
    if type(m) is not int or type(n) is not int or m <= 0 or n <= 0:
      self.update_metrics(method="ackermann", latency=time.time()-latency_start, success=False)
      return "Invalid parameters: `ackermann` takes in non-negative integers"
    try:
      m_n_key =  "{}_{}".format(m, n)
      if m_n_key in self.ackermann_memos:
        return str(self.ackermann_memos[m_n_key])
      new_memo = self.ackermann_recurse(m, n)
      self.ackermann_memos[m_n_key] = new_memo
      self.update_metrics(method="ackermann", latency=time.time()-latency_start, success=True)
      return str(new_memo)
    except ComputationError:
      self.update_metrics(method="ackermann", latency=time.time()-latency_start, success=False)
      return "Unable to compute Ackermann number for m: {} and n: {}".format(m, n)
    except:
      self.update_metrics(method="ackermann", latency=time.time()-latency_start, success=False)
      return "Unknown error for `ackermann`"


  def ackermann_recurse(self, m, n):
    """
    Ackermann function A(m, n) defined as:
      n + 1               if m = 0
      A(m-1, 1)           if m > 0 and n == 0
      A(m-1, A(m, n-1))   if m > 0 and n > 0
    Simple recursion approach is resource intensive
    Raises ComputationError if errors occur
    """
    try:
      if m == 0:
        return n + 1
      if m > 0 and n == 0:
        return self.ackermann_recurse(m -1, 1)
      if m > 0 and n > 0:
        return self.ackermann_recurse(m-1, self.ackermann_recurse(m, n-1))
    except:
      raise ComputationError


  def factorial_handler(self, n:int) -> str:
    """
    Wraps the Factorial function
    """
    latency_start = time.time()
    if type(n) is not int or n <= 0:
      self.update_metrics(method="factorial", latency=time.time()-latency_start, success=False)
      return "Invalid parameters: `factorial` takes in non-negative integers"
    try:
      result = self.factorial(n)
      self.update_metrics(method="factorial", latency=time.time()-latency_start, success=True)
      return str(result)
    except ComputationError:
      self.update_metrics(method="factorial", latency=time.time()-latency_start, success=False)
      return "Unable to compute factorial of {}".format(n)
    except:
      self.update_metrics(method="factorial", latency=time.time()-latency_start, success=False)
      return "Unknown error for `factorial`"


  def factorial(self, n: int) -> int:
    """
    Iteratively computes the nth factorial for the given n
    Raises ComputationError if errors occur
    """
    try:
      count = 1
      result = 1
      while count <= n:
        result = result * count
        count += 1
      return result
    except:
      raise ComputationError

  def update_metrics(self, method: str, latency: int, success: bool):
    """
    Updates internal metrics for the given method with given latency and success
    """
    self.metrics[method]["invocations_total"] += 1
    if success:
      self.metrics[method]["invocations_success"] += 1
    else:
      self.metrics[method]["invocations_error"] += 1
    # clear default latency
    curr_avg_latency = self.metrics[method]["averages"]["latency"]
    if curr_avg_latency == -1:
      new_avg_latency = latency/self.metrics[method]["invocations_total"]
      self.metrics[method]["averages"]["latency"] = round(new_avg_latency, LATENCY_PRECISION)
    else:
      old_latency_sum = curr_avg_latency * (self.metrics[method]["invocations_total"] - 1)
      new_avg_latency = (old_latency_sum + latency)/self.metrics[method]["invocations_total"]
      self.metrics[method]["averages"]["latency"] = round(new_avg_latency, LATENCY_PRECISION)


  def get_metrics(self):
    """
    Returns metrics about all executions to this Class object
    """
    return json.dumps(self.metrics)

