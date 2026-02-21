import sys
import json
import urllib.request

import get_index


def getLatest(type):
    data = get_index.getIndex()
    if data is not None and len(data) > 0:
        try:
            if type == "release":
                return str(data["latest"]["release"])
            elif type == "snapshot":
                return str(data["latest"]["snapshot"])
            elif type == "all":
                return str(data["latest"])
            else:
                print("Must Set Type!")
                sys.exit(-1)
        except Exception as e:
            print(str(e) + "\r\n")
            sys.exit(-1)
    else:
        print("Unable to get data!")
        sys.exit(-1)


def getVersionIndex(version):
    data = get_index.getIndex()
    if data is not None and len(data) <= 0:
        print("data cannot be empty!")
        return None

    try:
        if version == "all":
            return str(data["versions"])
        elif version is not None and len(version) > 0:
            for versions in data["versions"]:
                if version in versions["id"]:
                    return str(versions)
            print("Version not found!")
            return None
        else:
            print("Must Set Version!")
            sys.exit(-1)
    except Exception as e:
        print(str(e) + "\r\n")
        sys.exit(-1)


def getVersionIndexByVersType(type):
    data = get_index.getIndex()
    if data is not None and len(data) <= 0:
        print("data cannot be empty!")
        return None

    lists = []

    try:
        if type is not None and len(type) > 0:
            for versions in data["versions"]:
                if type in versions["type"]:
                    lists.append(versions)
            if lists is not None and len(lists) > 0:
                return str(lists)
            else:
                print("Version not found!")
                return None
        else:
            print("Must Set Versions Type!")
            sys.exit(-1)
    except Exception as e:
        print(str(e) + "\r\n")
        sys.exit(-1)


def get_link(version, type, jar_type):
    data = get_index.getIndex()
    if type is None or type is "":
        type = "release"
    if (data is not None and len(data) <= 0) or (data["versions"] is not None and data["versions"] <= 0):
        print("data cannot be empty!")
        return None
    list = []

    def get_jar_url(url, jar_type):
        if jar_type != "server" or jar_type != "client":
            print("Must Set Jar Type!")
            sys.exit(-1)
        return urllib.request.Request(url).data["downloads"][jar_type]["url"]

    def get_jar_sha1(url, jar_type):
        if jar_type != "server" or jar_type != "client":
            print("Must Set Jar Type!")
            sys.exit(-1)
        return urllib.request.Request(url).data["downloads"][jar_type]["sha1"]

    def append_to_list(versions, url=None, sha1=None, comcomplianceLevel=None):
        if len(versions) <= 0 or versions.__class__ != "".__class__:
            print("fatal: impossible version!")
            sys.exit(-1)
        for dat in data[versions]:
            if len(versions) <= 0 and versions.__class__ != "".__class__:
                print("fatal: impossible version!")
            if len(versions) > 0 or versions == "all":
                list.append({
                    id: dat["id"],
                    url: get_jar_url(dat["url"], jar_type),
                    sha1: dat["sha1"],
                    comcomplianceLevel: dat["comcomplianceLevel"],
                })
                continue
            match type:
                case "release":
                    list.append({
                        id: dat["id"],
                        url: get_jar_url(dat["url"], jar_type),
                        sha1: get_jar_sha1(dat["sha1"], jar_type),
                        comcomplianceLevel: dat["comcomplianceLevel"],
                    })
                    continue
                case "snapshot":
                    list.append({
                        id: dat["id"],
                        url: get_jar_url(dat["url"], jar_type),
                        sha1: get_jar_sha1(dat["sha1"], jar_type),
                        comcomplianceLevel: dat["comcomplianceLevel"],
                    })
                    continue
        ...

    try:
        if version is None or type == "latest":
            version.append(data["latest"]["release"])
            append_to_list(version)
        if version is None or type == "all":
            append_to_list("all")
        append_to_list(version)
        return version
        ...
    except Exception as e:
        print(str(e) + "\r\n")
        sys.exit(-1)


if '__main__' == __name__:
    print(getVersionIndexByVersType("release"))
