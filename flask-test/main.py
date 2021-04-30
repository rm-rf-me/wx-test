import sys
import time
import os

if __name__ == "__main__":
    from core import app
    print('正在打开服务器...')
    app.run(host='0.0.0.0', port=80,debug = True)