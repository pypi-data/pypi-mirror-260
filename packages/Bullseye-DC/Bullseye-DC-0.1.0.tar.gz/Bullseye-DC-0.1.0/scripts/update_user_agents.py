from librecaptcha import USER_AGENTS
import json
import os.path
import re

SCRIPT_DIR = os.path.dirname(__file__)
OUT_PATH = os.path.join(SCRIPT_DIR, "..", "Bullseye", "user_agent_data.py")

HEADER = """\
# This file was automatically generated by update_user_agents.py using data
# from <https://techblog.willshouse.com/2012/01/03/most-common-user-agents/>.

# flake8: noqa
USER_AGENTS = \
"""

FOOTER = "\n"

SYSTEMS = [
    ("Mac OS X", r"\bMac OS X\b"),
    ("Linux", r"\bLinux\b"),
    ("Windows", r"\bWindows\b"),
]

BROWSERS = [
    ("Firefox", r"\bFirefox\b"),
    ("Microsoft Edge", r"\bEdge\b"),
    ("Chrome", r"\bChrome\b"),
    ("Safari", r"\bSafari\b"),
]

VERSIONS = [
    r"\bFirefox/([\d.]+)\b",
    r"\bEdge/([\d.]+)\b",
    r"\bChrome/([\d.]+)\b",
    r"\bVersion/([\d.]+)\b",
]

WINDOWS_VERSION_MAP = {
    "10.0": "10",
    "6.3": "8.1",
    "6.2": "8",
    "6.1": "Server 2008 R2 / 7",
}


def match_map(agent, patterns):
    for string, pattern in patterns:
        if re.search(pattern, agent):
            return string
    return None


def get_browser_version(agent):
    for pattern in VERSIONS:
        match = re.search(pattern, agent)
        if match:
            return match.group(1)
    return None


def get_os_version(agent):
    match = re.search(r"\bMac OS X ([\d_]+)\b", agent)
    if match:
        return match.group(1).replace("_", ".")
    match = re.search(r"\bWindows NT ([\d.]+)\b", agent)
    if match:
        return WINDOWS_VERSION_MAP.get(match.group(1))
    if re.search(r"\bLinux\b", agent):
        return ""
    return None


def get_super_props(agent):
    props = {}
    props["os"] = match_map(agent, SYSTEMS)
    props["browser"] = match_map(agent, BROWSERS)
    props["device"] = ""
    props["browser_version"] = get_browser_version(agent)
    props["os_version"] = get_os_version(agent)
    for key, value in props.items():
        if value is None:
            return None
    return props


def get_entry(agent):
    props = get_super_props(agent)
    if props is None:
        return None
    return (agent, props)


def write(file):
    print(HEADER, file=file, end="")
    entries = []
    for agent in USER_AGENTS:
        entry = get_entry(agent)
        if entry is not None:
            entries.append(entry)
    json.dump(entries, file, indent=4)
    print(FOOTER, file=file, end="")


def main():
    with open(OUT_PATH, "w") as f:
        write(f)


if __name__ == "__main__":
    main()
