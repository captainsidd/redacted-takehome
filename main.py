from flask import Flask
from server import Server

# initialize Flask app
app = Flask(__name__)

# initialize Application
server = Server()

@app.route('/')
def hello_world():
    return 'Compute App Running!'

@app.route('/fibonacci/<int:nth_number>')
def fibonacci_handler(nth_number: int) -> str:
  return server.fibonacci_handler(n=nth_number)

@app.route('/ackermann/<int:m_number>/<int:n_number>')
def ackermann_handler(m_number: int, n_number:int) -> int:
  return server.ackermann_handler(m=m_number, n=n_number)

@app.route('/factorial/<int:factorial_nth>')
def factorial_handler(factorial_nth: int):
  return server.factorial_handler(n=factorial_nth)

@app.route('/_metrics/')
def metrics_handler():
  return server.get_metrics()
