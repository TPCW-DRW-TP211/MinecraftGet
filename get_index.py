import sys
import json
import urllib.request
import urllib.error

URL1 = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
URL2 = "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"
datastr = ""
data = ""


def getIndex():
    datastr = ""
    data = ""
    try:
        with urllib.request.urlopen(URL1) as response:
            datastr = response.read().decode("utf-8")
            data = json.loads(datastr)
    except Exception as e:
        print(str(e) + "\r\n[Master Index Get Failed]\r\n")
        datastr = ""
        data = ""
        try:
            with urllib.request.urlopen(URL2) as response:
                datastr = response.read().decode("utf-8")
                data = json.loads(datastr)
        except Exception as e:
            print(str(e) + "\r\n[Get Index Failed]\r\n")
            sys.exit(-1)

    if data is not None and len(data) > 0:
        return data
    # 反边界泄露
    sys.exit(-1)


if __name__ == "__main__":
    print(getIndex())
