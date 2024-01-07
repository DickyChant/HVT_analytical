import os
import numpy as np
import pandas as pd
from model import HVT


def get_csv_file(Vprime, mass=None, gv=None, gf=None, gh=None):
    dir_ = f"BRs/"
    csv_file = f"BRs_{Vprime}"
    if mass != None:
        dir_ += f"{Vprime}/"
        csv_file += f"_M{mass}"
    if gv != None:
        dir_ += f"mass_{mass}/"
        csv_file += f"_gv{gv}"
    if gf != None:
        dir_ += f"gv_{gv}/"
        csv_file += f"_gf{gf:.3f}"
    if gh != None:
        dir_ += f"gf_{gf:.3f}/"
        csv_file += f"_gh{gh:.3f}"
    csv_file += ".csv"
    return dir_ + csv_file


def filterCondition(data, infos):
    condition = None
    for key, value in infos.items():
        if condition is None:
            condition = data[key] == value
        else:
            condition &= data[key] == value
    return condition


def get_BRs_from_df(df, mass, gv, gf, gh):
    df_selected = None
    infos = {"M0": mass, "gh": gh, "gf": gf, "gv": gv}
    condition = filterCondition(df, infos)
    if len(df[condition]) != 0:
        df_selected = df[condition]
    return df_selected


def BRs_in_df(df_name, mass, gv, gf, gh):
    df_selected = None
    if os.path.exists(df_name):
        df = pd.read_csv(df_name)
        df_selected = get_BRs_from_df(df, mass, gv, gf, gh)
    return df_selected


def do_calculations(mass, gv, gf, gh, Vprime):
    hvt = HVT(MVz=mass, gv=gv, gf=gf, gh=gh)
    hvt.setup()
    if abs(gf) == 0 and abs(gh) == 0:
        return None
    print(f"Calculating BR for mass: {mass} gv: {gv} gf: {gf} gh: {gh}")
    if Vprime == "Zprime":
        tot = hvt.ZprimeTot.real
    if Vprime == "Wprime":
        tot = hvt.WprimeTot.real
    if tot == 0:
        return None
    if Vprime == "Zprime":
        entry = {
            "M0": mass,
            "g": hvt.g_su2,
            "gv": hvt.gv,
            "gh": hvt.gh,
            "gf": hvt.gf,
            "ch": hvt.ch,
            "cl": hvt.cq,
            "GammaTot": tot,
            "BRWW": hvt.ZprimeWW.real / tot,
            "BRhZ": hvt.ZprimeZH.real / tot,
            "BRee": hvt.Zprimeee.real / tot,
            "BRmumu": hvt.Zprimemm.real / tot,
            "BRtautau": hvt.Zprimetautau.real / tot,
            "BRnunu": hvt.Zprimevv.real / tot,
            "BRuu": hvt.Zprimeuu.real / tot,
            "BRdd": hvt.Zprimedd.real / tot,
            "BRcc": hvt.Zprimecc.real / tot,
            "BRss": hvt.Zprimess.real / tot,
            "BRbb": hvt.Zprimebb.real / tot,
            "BRtt": hvt.Zprimett.real / tot,
        }
        entry["BRll"] = entry["BRee"] + entry["BRmumu"]
        entry["BRqq"] = entry["BRuu"] + entry["BRdd"] + entry["BRcc"] + entry["BRss"]
        entry["BRjets"] = entry["BRqq"] + entry["BRbb"] + entry["BRtt"]
    if Vprime == "Wprime":
        entry = {
            "M0": mass,
            "g": hvt.g_su2,
            "gv": hvt.gv,
            "gh": hvt.gh,
            "gf": hvt.gf,
            "ch": hvt.ch,
            "cl": hvt.cq,
            "GammaTot": tot,
            "BRWH": hvt.WprimeHW.real / tot,
            "BRWZ": hvt.WprimeWZ.real / tot,
            "BReve": hvt.Wprimeeve.real / tot,
            "BRmvm": hvt.Wprimemvm.real / tot,
            "BRtauvt": hvt.Wprimetauvt.real / tot,
            "BRud": hvt.Wprimeud.real / tot,
            "BRus": hvt.Wprimeus.real / tot,
            "BRcd": hvt.Wprimecd.real / tot,
            "BRcs": hvt.Wprimecs.real / tot,
            "BRtb": hvt.Wprimetb.real / tot,
        }
        entry["BRlnu"] = entry["BReve"] + entry["BRmvm"]
        entry["BRqqbar"] = entry["BRud"] + entry["BRus"] + entry["BRcd"] + entry["BRcs"]
        entry["BRjets"] = entry["BRqqbar"] + entry["BRtb"]
    return entry


def store_df(df, fname):
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    df = df.astype("float32")
    df.to_csv(fname, index=False)
    print("Created", fname)


def get_masses():
    m_values = [1000, 2000, 3000, 4000]
    # m_values = [1000]
    return m_values


def get_gVs():
    gV_values = [1]
    return gV_values


def get_gFs():
    gF_values = [data["gf"] for data in benchmarks.values()]
    gF_values += list(np.arange(0.01, 0.1 + 0.01, 0.001))
    gF_values += list(np.arange(0.1, 0.5 + 0.01, 0.005))
    gF_values += list(np.arange(0.5, 1.6 + 0.1, 0.1))
    gF_values = list(sorted(set([round(x, 3) for x in gF_values])))
    return gF_values


def get_gHs():
    gH_values = [data["gh"] for data in benchmarks.values()]
    gH_values += list(np.arange(-2.0, 2.0 + 0.01, 0.01))
    gH_values += list(np.arange(-8.0, 8.0 + 0.5, 0.5))
    gH_values = list(sorted(set([round(x, 3) for x in gH_values])))
    return gH_values


benchmarks = {
    "modelA": {"ch": -0.556, "cq": -1.316, "gv": 1, "gh": -0.556, "gf": -0.562},
    "modelB": {"ch": -0.976, "cq": 1.024, "gv": 3, "gh": -2.928, "gf": 0.146},
    "modelC": {"ch": 1, "cq": 0, "gv": 1, "gh": 1.0, "gf": 0.0},
}

decay_modes = {
    "Zprime": {
        "GammaTot": "#Gamma",
        "BRhZ": "ZH",
        "BRWW": "WW",
        "BRll": "ll",
        "BRnunu": "#nu#nu",
        "BRjets": "qq",
        "BRtt": "tt",
    },
    "Wprime": {
        "GammaTot": "#Gamma",
        "BRWH": "WH",
        "BRWZ": "WZ",
        "BRlnu": "l#nu",
        "BRjets": "qq",
    },
}
