"""Configuration for the mainframe_paxo module."""
import os.path

# Data drive is the big physical drive with all dev data on it

# folder on the data drive that we use
data_drive_dev_folder = os.path.join("/", "paxdei_dev")
data_drive_ddc_folder = os.path.join("/", "paxdei_DDC")
data_drive_git_depends = os.path.join("/", "ue_gitdeps")

# the drive letter we use for the subst
# the letter P: has been taken to be used by Pipeline.  Let's use W: instead.
work_drive_name = "W:"


# p4 fingerprints for the different servers
p4_fingerprints = {
    "aws": "7F:24:67:0B:62:7B:9F:3A:ED:5F:26:32:23:82:8F:20:EE:13:8B:03",
    "rvk": "8C:07:9D:29:F8:03:CC:76:C0:3B:26:41:20:3D:4C:B0:F0:A4:5E:B8",
    "rvk-old": "B9:62:8C:DA:75:B7:85:0E:B1:2B:02:1A:AE:11:5B:25:7D:C8:72:CF",
    "hel": "62:95:05:A0:B4:AD:1A:61:12:F6:06:07:9A:D3:5C:83:85:A6:67:C9",
}

# configurations for the different locations
locations: dict[str, dict[str, str | None]] = {
    "rvk-office": {
        "desc": "Reykjavík office",
        "p4port": "ssl:p4-rvk.mainframe.zone:1666",
        "p4trust": p4_fingerprints["rvk"],
        "ddc": r"\\ddc-rvk.mainframe.zone\DDC",
    },
    "rvk-ext": {
        "desc": "Reykjavík, working from home, tailscale recommended",
        "p4port": "ssl:p4-rvk.x.mainframe.zone:1666",
        "p4trust": p4_fingerprints["rvk"],
        # DDC access is via tailscale to lundi
        "ddc": r"\\lundi.turtle-ray.ts.net\DDC",
    },
    "hel-office": {
        "desc": "Helsinki office",
        "p4port": "ssl:p4-hel.mainframe.zone:1666",
        "p4trust": p4_fingerprints["hel"],
        "ddc": r"\\ddc-hel.mainframe.zone\DDC",
    },
    "hel-ext": {
        "desc": "Helsinki, working from home, tailscale recommended",
        "p4port": "ssl:p4-hel.x.mainframe.zone:1666",
        "p4trust": p4_fingerprints["hel"],
        # ddc is to lunni directly
        "ddc": r"\\lunni.turtle-ray.ts.net\DDC",
    },
    "tailscale": {
        "desc": "working over tailscale network, e.g. from home",
        "p4port": "ssl:p4.t.mainframe.zone:1666",
        "p4trust": p4_fingerprints["aws"],
        # DDC in amazon.  higher latency
        "ddc": r"\\ddc.t.mainframe.zone\DDC",
    },
    "external": {
        "desc": "working from the internet without VPN",
        "p4port": "ssl:perforce.x.mainframe.zone:1666",
        "p4trust": p4_fingerprints["aws"],
        "ddc": None,
    },
}
