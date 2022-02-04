from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QListWidget
import sys
import ssl
import json
import os
import requests
import pyperclip


class LocalClient(object):
    def __init__(self, reigon="na"):
        self.reigon = reigon
        self.lockfile = "".join(
            [os.getenv("LOCALAPPDATA"),
             r"\Riot Games\Riot Client\Config\lockfile"]
        )

        with open(self.lockfile, "r") as f:
            data = f.read().split(":")

        self.base_url = f"{data[4]}://127.0.0.1:{data[2]}"

        self.s = requests.Session()
        self.s.auth = ("riot", data[3])

    def _url(self, path: str) -> str:
        return self.base_url + path


client = LocalClient(reigon="ap")


def gett():
    data = client.s.get(client._url(
        "/chat/v5/messages"), verify=ssl.CERT_NONE)
    data = json.loads(data.content)['messages']
    listofmessages = []
    for i in data:
        listofmessages.append(i['game_name']+": "+i['body'])

    return listofmessages


list_of_messages = gett()

# gui


def run():
    app = QApplication(sys.argv)
    listWidget = QListWidget()

    # Resize width and height
    listWidget.resize(700, 700)
    for i in list_of_messages:
        listWidget.addItem(i)
    listWidget.itemDoubleClicked.connect(lambda w: pyperclip.copy(w.text()))

    listWidget.setWindowTitle('PyQT QListwidget Demo')

    listWidget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
