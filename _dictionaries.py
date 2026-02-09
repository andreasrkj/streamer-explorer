sink_dict = {
    "6"  : (170,1080),
    "13" : (230,2600),
    "24" : (220,1370),
    "82" : (240,1310),
    "122": (350,1100),
    "162": (410,2040),
    "180": (410,1520),
    "225": (450,1330)
}

unconverged_sinkdict = {
    "6"  : [],
    "13" : [2210,2220,2230,2240,2250,2260,2270,2280,2290,2300,2310,2320,2330,2430,2440,2450,2460,2470,2480,2490,2500,2510,2520,2530,2540,2550,2560,2570,2580,2590,2600],
    "24" : [390,400,410,420,430,440,450,460,470,480,490,1010],
    "82" : [1140,1150,1160,1170,1180,1240,1260,1270,1290],
    "122": [],
    "162": [],
    "180": [],
    "225": []
}

view_keys = {
    "Face On": "face-on",
    "Edge On (A)": "edge-on-A",
    "Edge On (B)": "edge-on-B"
}

mol_keys = {
    "H$_2$CO J = 3$_{0,3}$-2$_{0,2}$": "ph2co", 
    "$^{13}$CO J = 2-1": "13co", 
    "C$^{18}$O J = 2-1": "c18o"
}

total_calculation_time = { # total CPU hours
    "6"  : 83369.79,
    "13" : 150414.5199,
    "24" : 146770.4968,
    "82" : 77031.37545,
    "122": 93333.53278,
    "162": 85745.96947,
    "180": 41178.78426,
    "225": 58922.46438
}

questioned_events = {
    "6"  : [],
    "13" : [(440, 480, ["edge-on-B"], ["c18o"]),
            (2400, 2600, ["edge-on-A"], ["13co", "c18o"]),
            (2400, 2600, ["edge-on-B"], ["c18o"])],

    "24" : [(550, 580, ["edge-on-A"], ["h2co", "c18o"]),
            (580, 600, ["face-on", "edge-on-B"], ["h2co", "13co", "c18o"]),
            (650, 710, ["edge-on-B"], ["h2co", "c18o"]),
            (810, 1030, ["face-on", "edge-on-A"], ["13co", "c18o"]),
            (890, 1040, ["edge-on-B"], ["13co", "c18o"]),
            (1080, 1140, ["face-on"], ["c18o"])],

    "82" : [(540, 620, ["face-on", "edge-on-A"], ["h2co", "c18o"])],

    "122": [],
    "162": [],
    "180": [],
    "225": []
}

event_list = { # Format (nstart, nend, [views], [molecules])
    "6"  : [(250, 410, ["face-on", "edge-on-A"], ["ph2co", "13co", "c18o"]),
            (470, 490, ["face-on", "edge-on-A"], ["ph2co", "c18o"]),
            (520, 600, ["face-on", "edge-on-A"], ["ph2co", "c18o"]),
            (610, 690, ["face-on", "edge-on-A"], ["ph2co", "c18o"]),
            (710, 740, ["face-on", "edge-on-B"], ["ph2co", "c18o"]),
            (850, 900, ["face-on", "edge-on-B"], ["ph2co", "c18o"]),
            (960, 1050, ["face-on", "edge-on-A"],["ph2co", "13co", "c18o"])],

    "13" : [(440, 480, ["edge-on-B"], ["c18o"]),
            (820, 1050, ["edge-on-A", "edge-on-B"], ["h2co", "c18o"]),
            (1010, 1110, ["face-on", "edge-on-A", "edge-on-B"], ["h2co"]),
            (1100, 1230, ["face-on", "edge-on-B"], ["c18o"]),
            (1340, 1500, ["face-on", "edge-on-B"], ["h2co", "c18o"]),
            (1630, 1700, ["face-on", "edge-on-B"], ["h2co", "c18o"]),
            (1630, 1740, ["face-on", "edge-on-A"], ["h2co", "c18o"]),
            (1930, 2080, ["face-on", "edge-on-A"], ["h2co", "c18o"]),
            (2400, 2600, ["edge-on-A"], ["13co", "c18o"]),
            (2400, 2600, ["edge-on-B"], ["c18o"])],

    "24" : [(240, 340, ["face-on", "edge-on-A"], ["h2co", "13co", "c18o"]),
            (470, 500, ["face-on", "edge-on-A"], ["h2co"]),
            (550, 580, ["edge-on-A"], ["h2co", "c18o"]),
            (580, 600, ["face-on", "edge-on-B"], ["h2co", "13co", "c18o"]),
            (590, 640, ["face-on", "edge-on-A", "edge-on-B"], ["c18o"]),
            (650, 710, ["edge-on-B"], ["h2co", "c18o"]),
            (810, 850, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "13co", "c18o"]),
            (810, 1030, ["face-on", "edge-on-A"], ["13co", "c18o"]),
            (890, 1040, ["edge-on-B"], ["13co", "c18o"]),
            (1050, 1140, ["face-on", "edge-on-B"], ["h2co", "c18o"]),
            (1080, 1140, ["face-on"], ["c18o"]),
            (1080, 1120, ["face-on", "edge-on-A"], ["h2co", "c18o"]),
            (1130, 1210, ["face-on", "edge-on-A"], ["13co", "c18o"]),
            (1140, 1160, ["face-on", "edge-on-B"], ["c18o"]),
            (1120, 1240, ["face-on", "edge-on-B"], ["h2co", "c18o"]),
            (1230, 1270, ["face-on", "edge-on-B"], ["h2co", "c18o"]),
            (1320, 1370, ["face-on", "edge-on-B"], ["c18o"])],

    "82" : [(330, 410, ["face-on", "edge-on-A"], ["h2co"]),
            (350, 400, ["face-on", "edge-on-B"], ["h2co"]),
            (430, 500, ["face-on", "edge-on-A"], ["h2co", "c18o"]),
            (540, 620, ["face-on", "edge-on-A"], ["h2co", "c18o"]),
            (620, 1120, ["face-on", "edge-on-A"], ["h2co"]),
            (830, 880, ["face-on", "edge-on-B"], ["c18o"]),
            (860, 940, ["face-on", "edge-on-B"], ["c18o"]),
            (1040, 1130, ["face-on", "edge-on-B"], ["h2co", "c18o"])],

    "122": ["No events yet"],
    "162": ["No events yet"],
    "180": ["No events yet"],
    "225": ["No events yet"]
}