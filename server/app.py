from config import app
from config import create_app

import controllers

app = create_app()

if __name__ == '__main__':

    app.run(debug=True, threaded=True)



