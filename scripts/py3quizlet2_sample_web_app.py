#! /usr/bin/env python3

from flask import Flask, redirect, request
import os

from py3quizlet2 import Quizlet

app = Flask(__name__)

client_id = os.environ['QUIZLET_CLIENT_ID']
encoded_auth_str = os.environ['QUIZLET_ENCODED_AUTH_STR']
redirect_uri = 'http://localhost:5000'

# TODO(hammer): check state
@app.route("/")
def hello():
  q = Quizlet(client_id, encoded_auth_str, redirect_uri)

  # Redirect user to Quizlet's permissions request
  if not request.args:
    auth_url, state = q.generate_auth_url('read write_set')
    return redirect(auth_url)

  # TODO(hammer): handle denial of permissions
  q.request_token(request.args.get('code'))

  # GET the sets
  old_sets = q.get_sets()

  # POST a new set
  title = 'new_set'
  terms = ['nuovo', 'vecchio']
  definitions = ['new', 'old']
  lang_terms = 'it'
  lang_definitions = 'en'
  new_set = q.add_set(title, terms, definitions, lang_terms, lang_definitions)

  # GET the sets to confirm set was added
  new_sets = q.get_sets()

  # Write it all out
  return 'Old sets: %d\nNew set: %s\nNew sets:%d' % (len(old_sets),
                                                     new_set,
                                                     len(new_sets))


if __name__ == "__main__":
  app.run(debug=True)
