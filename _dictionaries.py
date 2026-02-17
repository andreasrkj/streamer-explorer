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

candidate_dir = {
      6  : [(250, 410, ["face-on", "edge-on-A"], ["h2co", "c18o"]), 
            (470, 600, ["face-on", "edge-on-A"], ["h2co", "c18o"]), 
            (580, 690, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"]), 
            (710, 780, ["face-on", "edge-on-A"], ["h2co", "c18o"]), 
            (820, 900, ["face-on", "edge-on-B"], ["h2co", "c18o"]), 
            (960, 1050, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "13co", "c18o"])],

      13 : [(440, 620, ["face-on", "edge-on-B"], ["h2co", "c18o"]),
            (820, 1050, ["edge-on-A", "edge-on-B"], ["h2co", "c18o"]),
            (1010, 1110, ["face-on", "edge-on-A", "edge-on-B"], ["h2co"]),
            (1100, 1230, ["face-on", "edge-on-B"], ["h2co", "c18o"]),
            (1340, 1500, ["face-on", "edge-on-B"], ["h2co", "c18o"]),
            (1630, 1740, ["face-on", "edge-on-A"], ["h2co", "c18o"]),
            (1930, 2150, ["face-on", "edge-on-A"], ["h2co", "c18o"])],

      24 : [(240, 500, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "13co", "c18o"]),
            (560, 640, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"]),
            (810, 970, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "13co", "c18o"]),
            (810, 1110, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"]),
            (1050, 1150, ["face-on", "edge-on-B"], ["h2co", "c18o"]),
            (1220, 1340, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"])],

      82 : [(330, 470, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"]),
           (330, 500, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"]),
           (540, 710, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"]),
           (800, 1130, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"])],

      122: [(370, 600, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"]),
            (700, 1100, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"]),
            (700, 1100, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"])],

      162: [(460, 500, ["face-on", "edge-on-B"], ["h2co", "c18o"]),
            (480, 500, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"]),
            (540, 950, ["face-on", "edge-on-B"], ["h2co", "c18o"]),
            (540, 720, ["face-on", "edge-on-B"], ["h2co", "c18o"]),
            (1030, 1120, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"]),
            (1200, 1450, ["face-on", "edge-on-B"], ["h2co", "c18o"]),
            (1200, 1450, ["face-on", "edge-on-B"], ["h2co", "c18o"]),
            (1460, 1490, ["face-on", "edge-on-B"], ["h2co", "c18o"]),
            (1670, 2040, ["face-on", "edge-on-A"], ["h2co", "c18o"]),
            (1960, 2040, ["face-on", "edge-on-B"], ["h2co", "c18o"])],
      
      180: [(460, 550, ["face-on", "edge-on-A", "edge-on-B"], ["h2co"]),
            (720, 1490, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"]),
            (1280, 1520, ["face-on", "edge-on-A"], ["h2co", "c18o"])],

      225: [(600, 950, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"]),
            (610, 690, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"]),
            (750, 920, ["face-on", "edge-on-A", "edge-on-B"], ["h2co", "c18o"]),
            (980, 1310, ["face-on", "edge-on-A"], ["h2co", "c18o"]),
            (1110, 1260, ["edge-on-A", "edge-on-B"], ["h2co", "13co", "c18o"]),
            (1250, 1310, ["face-on", "edge-on-A"], ["c18o"])]
}

candidatenote_dir = {
      6  : ["East in both face on + edge on (A). Rotates -90 degrees at 340->350, so changes velocity in (A)",
            "East in both face on + edge on (A). Turns to north so possibly in edge on (B) too",
            "Flips 180 degrees at 600->610, starts S->NW (face-on), so left in both (A) and (B)",
            "Continuation of above, but dips out in 700, so separated event. Now W in both face on and (A)",
            "Maybe starts in 790, but then disappears a bit. South in face on, E in (B). Flips a couple times",
            "If N in face on then W in edge on (A), but if S in face on then both in (A) and (B) in W and E"],

      13 : ["S spiral in face on, E in (B). Flips to N and W from 450->460.",
            "SW in (A) and SE in (B). Not that visible in face on. Flips 180 in 1000->1010. Dissolves in 1050",
            "Spirals in from N in face on, slightly NW in (A) and slightly NE in (B)",
            "Spiral seen best in C18O on eastern side in face on, shows on western side in (B)",
            "Similar to above, spiral on southeastern side, shown on western side in (B)",
            "South spiral/arm thing in face on and (A). Maybe also in (B) on eastern side?",
            "NE in face on, E in (A), might also be visible in (B) due to spiral structure?"],

      24 : ["Northeastern spiral seen in east in both (A) and (B)",
            "Northwestern spiral in face on, east in both (A) and (B)",
            "Southern thing in face on, seen east in (B). Moves slightly north to south, not a strong gradient",
            "Northern in face on, related to E in (A) and W in (B). Turns 90 degrees over time and collimates",
            "Long strand thing in NE of (B), slightly visible south in face on",
            "Eastern thing in face on, moves slightly north, visible in NE part of (A) and NW of (B)"],

      82 : ["Northwest in face on, west in (A) and east in (B). Turns north. Disappears in (A) ~450",
            "Southeast in face on, east in edge on (A) and west in edge on (B). Turns south",
            "North in face on, the south one seems transient. East in (A). Becomes more visible in (B)",
            "Slightly NW in face on. Seen west in (B). Event turns counterclockwise, shows up west in (A)"],

      122: ["South in face on, east in (B). Turns clockwise to near west face on and shows up west in (A)",
            "Northeast in face on, east in (A), west in (B). Rotates towards N and disappears from (A)",
            "Not that visible in face on, but shows up eventually SW. Strong in west (B) and also in (A) east"],

      162: ["Northern spiral in face on. Seen west in (B)",
            "Southern spiral in face on. Seen west in (A) and east in (B)",
            "North in face on, west in (B). Turns NW in face on. Shows up in (A) but tangled with below",
            "South in face on, east in (B). Turns SW in face on, shows up in (A) but tangled with above",
            "North in face on. Flips 180 degrees 1060->1070. Moves W->E in (A). Also shows up in (B)",
            "North in face on. West in (B). Disappears a bit in the surrounding emission sometimes",
            "South in face on. East in (B). Same as above, disappears and gradient sometimes not strong",
            "Technically two in east, but dominant SE collimated thing in (B). Possibly S in face on",
            "Northwest in face on, west in (A). Turns west in face on over time.",
            "North in face on. Can't figure out where exactly in (B) but I definitely see a gradient."],
      
      180: ["W in both face on and (A). Extends slightly NW, so also seen W in (B).",
            "Periodically visible in face on (arm SW), otherwise (A) in SW and (B) in SE. Best in C18O",
            "Flips 180 degrees a couple times. Starts in SE of face on, SE of (A). Maybe merges with above?"],

      225: ["SE in face on, SE in (A) and (B). Flips straight south. Flips 910->920",
            "NE in face on, SSW/S in (A) and W in (B). Flips straight north",
            "Northeast in face on, West in (B). Possibly East in (A)?  Flips 910->920",
            "Almost east in face on (upper of the clump), lower east in (A). Also strong signal in C18O",
            "Swoops in south in (A), slightly to the east in (B). Possibly northern spiral in face on?",
            "Long spiral east in face on, east in (A) but hidden in emission."]
}