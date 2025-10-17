"""Story templates for the Story Builder app.

Each template contains MICE cards and Try/Fail cycles for a specific genre.
Templates are structured data that can be loaded into the database.
"""

TEMPLATES = {
    "mystery": {
        "mice_cards": [
            {
                "code": "M",
                "opening": "Detective arrives in fog-shrouded coastal town where everyone seems suspicious",
                "closing": "Detective leaves the town, now peaceful and welcoming, mystery solved",
                "nesting_level": 1
            },
            {
                "code": "I",
                "opening": "Who killed the wealthy lighthouse keeper? Why was the body moved?",
                "closing": "The killer was the keeper's business partner, hiding embezzlement scheme",
                "nesting_level": 2
            },
            {
                "code": "C",
                "opening": "Detective haunted by unsolved case from her past, struggles to trust her instincts",
                "closing": "Detective learns to trust herself again, finds closure on both cases",
                "nesting_level": 3
            },
            {
                "code": "E",
                "opening": "Hurricane warning issued - all evidence must be gathered before evacuation",
                "closing": "Hurricane passes, evidence preserved, arrest made just in time",
                "nesting_level": 4
            }
        ],
        "try_cards": [
            {
                "type": "Success",
                "order_num": 1,
                "attempt": "Detective interviews all townspeople for alibis",
                "failure": "Everyone has an alibi, but stories have inconsistencies",
                "consequence": "Realizes someone is lying, narrows suspects to three people"
            },
            {
                "type": "Failure",
                "order_num": 2,
                "attempt": "Searches lighthouse for physical evidence before storm",
                "failure": "Storm hits early, evidence washed away by flooding",
                "consequence": "Must rely on testimonies and deduction instead of forensics"
            },
            {
                "type": "Trade-off",
                "order_num": 3,
                "attempt": "Confronts prime suspect publicly to force confession",
                "failure": "Suspect denies everything, town turns against detective",
                "consequence": "Gains access to suspect's financial records in the chaos"
            }
        ]
    },
    "adventure": {
        "mice_cards": [
            {
                "code": "M",
                "opening": "Hero leaves peaceful village to journey through dangerous enchanted forest",
                "closing": "Hero returns home victorious, village saved and celebrating",
                "nesting_level": 1
            },
            {
                "code": "I",
                "opening": "What ancient artifact can defeat the dragon threatening the kingdom?",
                "closing": "The artifact is the hero's family heirloom - a dragon-forged blade",
                "nesting_level": 2
            },
            {
                "code": "C",
                "opening": "Reluctant hero doubts their worthiness, fears they'll fail like their father",
                "closing": "Hero accepts their destiny, realizes courage isn't absence of fear",
                "nesting_level": 3
            },
            {
                "code": "E",
                "opening": "Dragon awakens early, attacks begin - kingdom will fall in seven days",
                "closing": "Dragon defeated, ancient threat ended, peace restored to the land",
                "nesting_level": 4
            }
        ],
        "try_cards": [
            {
                "type": "Success",
                "order_num": 1,
                "attempt": "Hero seeks wise hermit's guidance on finding the artifact",
                "failure": "Hermit speaks only in riddles, no clear answer given",
                "consequence": "Hero deciphers one clue - must seek the mountain temple"
            },
            {
                "type": "Failure",
                "order_num": 2,
                "attempt": "Climbs treacherous mountain to reach ancient temple",
                "failure": "Avalanche destroys path, temple guardian refuses entry",
                "consequence": "Forced to prove worth through dangerous trial by combat"
            },
            {
                "type": "Trade-off",
                "order_num": 3,
                "attempt": "Makes bargain with forest spirits for magical protection",
                "failure": "Protection works but hero owes the spirits a future favor",
                "consequence": "Gains power needed but at unknown cost to be paid later"
            }
        ]
    },
    "romance": {
        "mice_cards": [
            {
                "code": "M",
                "opening": "City lawyer forced to spend summer in small coastal town for work",
                "closing": "Lawyer chooses to stay in the town, makes it her permanent home",
                "nesting_level": 1
            },
            {
                "code": "I",
                "opening": "Can two people from completely different worlds find common ground?",
                "closing": "Love transcends backgrounds - they complement each other perfectly",
                "nesting_level": 2
            },
            {
                "code": "C",
                "opening": "Guarded workaholic afraid to open her heart after painful divorce",
                "closing": "Learns to trust again, opens herself to love and vulnerability",
                "nesting_level": 3
            },
            {
                "code": "E",
                "opening": "Town's beloved community center faces demolition - she must defend it",
                "closing": "Community center saved through partnership, becomes symbol of their love",
                "nesting_level": 4
            }
        ],
        "try_cards": [
            {
                "type": "Success",
                "order_num": 1,
                "attempt": "She agrees to coffee with handsome local boat captain",
                "failure": "They argue about city vs. small-town life constantly",
                "consequence": "Realizes their debates are actually playful chemistry, not conflict"
            },
            {
                "type": "Failure",
                "order_num": 2,
                "attempt": "Plans romantic beach picnic to show she's changing",
                "failure": "Storm ruins picnic, she loses composure and pushes him away",
                "consequence": "He sees her vulnerability for first time, understands her fear"
            },
            {
                "type": "Moral",
                "order_num": 3,
                "attempt": "Uses legal loophole to save community center temporarily",
                "failure": "Wins case but betrays town's trust by using manipulative tactics",
                "consequence": "Must choose between winning and being the person he fell for"
            }
        ]
    }
}
