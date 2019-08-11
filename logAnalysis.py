
# A buggy web service in need of a database.

from flask import Flask, request, redirect, url_for

from newsdb import get_topArticle, get_topAuthor, get_mostError

app = Flask(__name__)

# HTML template for the forum page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>DB Forum</title>
    <style>
      h1, form { text-align: center; }
      textarea { width: 400px; height: 100px; }
      div.post { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
      hr.postbound { width: 50%%; }
      em.date { color: #999 }
    </style>
  </head>
  <body>
    <h1>News DB (%s)</h1>
    <!-- post content will go here -->
%s
  </body>
</html>
'''

# HTML template for an individual comment
POST = '''\
    <div class=post><em class=date>%s:  %s</em><br>%s:  %s</div>
'''

@app.route('/', methods=['GET'])
@app.route('/topArticle', methods=['GET'])
def main():
  '''Main page of the forum.'''
  posts = "".join(POST % ('title', title, 'views', views) for title, views in get_topArticle())
  html = HTML_WRAP % ('Top Article', posts)
  return html

@app.route('/topAuthor', methods=['GET'])
def topAuthor():
  '''Main page of the forum.'''
  posts = "".join(POST % ('name', name, 'views', views) for name, views in get_topAuthor())
  html = HTML_WRAP % ('Top Author',posts)
  return html

@app.route('/mostError', methods=['GET'])
def mostError():
  '''Main page of the forum.'''
  posts = "".join(POST % ('date', date, 'error_percentage', error_percentage) for date, error_percentage in get_mostError())
  html = HTML_WRAP % ('Most Error',posts)
  return html


# @app.route('/', methods=['POST'])
# def post():
#   '''New post submission.'''
#   message = request.form['content']
#   add_post(message)
#   return redirect(url_for('main'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)

