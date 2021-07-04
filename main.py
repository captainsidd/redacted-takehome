from flask import Flask
from klarna import Klarna

# initialize Flask app
app = Flask(__name__)

# initialize Application
klarna = Klarna()

@app.route('/')
def hello_world():
    return 'Klarna App Running!'

@app.route('/fibonacci/<int:nth_number>')
def fibonacci_handler(nth_number: int) -> str:
  return klarna.fibonacci_handler(n=nth_number)

@app.route('/ackermann/<int:m_number>/<int:n_number>')
def ackermann_handler(m_number: int, n_number:int) -> int:
  return klarna.ackermann_handler(m=m_number, n=n_number)

@app.route('/factorial/<int:fibo_nth>')
def factorial_handler(fibo_nth: int):
  return klarna.factorial_handler(n=fibo_nth)

@app.route('/_metrics/')
def metrics_handler():
  return klarna.get_metrics()


