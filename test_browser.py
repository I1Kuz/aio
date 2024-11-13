import webview
from time import sleep
w = webview.create_window('', 'http://localhost:5173/', height=500, width=500,resizable=False, )

webview.start()
# if __name__ == '__main__':
#     while True:
#         w.evaluate_js('window.location.reload()')
#         sleep(5)



