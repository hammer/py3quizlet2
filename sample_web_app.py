from flask import Flask, redirect, request
from pyquizlet import Quizlet

app = Flask(__name__)

# TODO(hammer): pick this up from environment
client_id = ''
encoded_auth_str = ''

# TODO(hammer): check state
@app.route("/")
def hello():
  q = Quizlet(client_id, encoded_auth_str)
  if not request.args:
    redirect_url, state = q.generate_auth_url('read')
    return redirect(redirect_url)

  auth_code = request.args.get('code')
  q.request_token(auth_code, 'http://localhost:5000')

  sets = q.make_request('users/lltools/sets/')
  return "Hello sets: %s" % sets


if __name__ == "__main__":
  app.run(debug=True)
