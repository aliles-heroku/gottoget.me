import base64
import os

import requests
from flask import Flask, render_template, request


app = Flask(__name__)


MAX_REQUEST = 1024 * 1024 * 10


@app.route('/', methods=['GET', 'POST'])
def index():
    # find url if present
    url = request.args.get('url')
    if request.method == 'POST':
       url = request.form['url']
    # download data if requested
    datauri = None
    if url:
        try:
            resource = requests.get(url, prefetch=False)
            if int(resource.headers['content-length']) < MAX_REQUEST:
                mimetype = resource.headers.get('content-type', '')
                content = base64.b64encode(resource.content)
                datauri = 'data:{0};base64,{1}'.format(mimetype, content)
        except requests.RequestException:
            datauri = None
    return render_template('index.html', url=url, datauri=datauri)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
