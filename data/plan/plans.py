medieval_tasks = {
    "common_tasks": [
        {
            "task": "Morning prayer",
            "time": 1,
            "needs": ["prayer book"],
            "gives": ["blessing", "morale"]
        },
        {
            "task": "Evening prayer", 
            "time": 1,
            "needs": ["prayer book"],
            "gives": ["blessing", "morale"]
        },
        {
            "task": "Prepare meals",
            "time": 2,
            "needs": ["pot", "food", "wood"],
            "gives": ["meal", "energy"]
        },
        {
            "task": "Clean workspace",
            "time": 1,
            "needs": ["broom", "cloth"],
            "gives": ["clean space"]
        }
    ],

    "warrior": [
        {
            "task": "Morning training",
            "time": 3,
            "needs": ["sword", "armor"],
            "gives": ["combat skill", "strength"] 
        },
        {
            "task": "Weapon maintenance",
            "time": 2,
            "needs": ["cloth", "oil"],
            "gives": ["maintained weapons"]
        },
        {
            "task": "Armor cleaning",
            "time": 2,
            "needs": ["cloth", "oil"],
            "gives": ["clean armor"]
        },
        {
            "task": "Guard duty",
            "time": 6,
            "needs": ["sword", "armor"],
            "gives": ["coins", "experience"]
        },
        {
            "task": "Horse care",
            "time": 2,
            "needs": ["brush", "food"],
            "gives": ["healthy horse"]
        },
        {
            "task": "Patrol",
            "time": 4,
            "needs": ["sword", "armor"],
            "gives": ["coins", "experience"]
        }
    ],

    "blacksmith": [
        {
            "task": "Light forge",
            "time": 1,
            "needs": ["wood", "tools"],
            "gives": ["hot forge"]
        },
        {
            "task": "Repair weapons",
            "time": 4,
            "needs": ["metal", "tools", "wood"],
            "gives": ["coins", "repaired items"]
        },
        {
            "task": "Make tools",
            "time": 5,
            "needs": ["metal", "tools", "wood"],
            "gives": ["coins", "new tools"]
        },
        {
            "task": "Shoe horses",
            "time": 2,
            "needs": ["metal", "tools"],
            "gives": ["coins", "shod horse"]
        },
        {
            "task": "Make weapons",
            "time": 6,
            "needs": ["metal", "tools", "wood"],
            "gives": ["coins", "weapons"]
        },
        {
            "task": "Make armor",
            "time": 8,
            "needs": ["metal", "tools", "leather"],
            "gives": ["coins", "armor"]
        }
    ],

    "healer": [
        {
            "task": "Gather herbs",
            "time": 3,
            "needs": ["basket", "knife"],
            "gives": ["herbs", "knowledge"]
        },
        {
            "task": "Make medicine",
            "time": 4,
            "needs": ["herbs", "pot", "tools"],
            "gives": ["coins", "potions"]
        },
        {
            "task": "Treat patients",
            "time": 5,
            "needs": ["potions", "cloth", "tools"],
            "gives": ["coins", "experience"]
        },
        {
            "task": "Make bandages",
            "time": 2,
            "needs": ["cloth", "tools"],
            "gives": ["bandages"]
        },
        {
            "task": "Study remedies",
            "time": 3,
            "needs": ["book", "herbs"],
            "gives": ["knowledge"]
        },
        {
            "task": "Visit sick",
            "time": 4,
            "needs": ["potions", "tools"],
            "gives": ["coins", "experience"]
        }
    ],

    "merchant": [
        {
            "task": "Open shop",
            "time": 1,
            "needs": ["goods", "coins"],
            "gives": ["ready shop"]
        },
        {
            "task": "Trade goods",
            "time": 8,
            "needs": ["goods", "coins"],
            "gives": ["coins", "new goods"]
        },
        {
            "task": "Inventory check",
            "time": 2,
            "needs": ["book", "goods"],
            "gives": ["knowledge"]
        },
        {
            "task": "Negotiate",
            "time": 3,
            "needs": ["goods", "coins"],
            "gives": ["better prices"]
        },
        {
            "task": "Travel trade",
            "time": 12,
            "needs": ["goods", "coins", "horse"],
            "gives": ["coins", "new goods"]
        },
        {
            "task": "Market day",
            "time": 10,
            "needs": ["goods", "coins"],
            "gives": ["coins", "new goods"]
        }
    ]
}

# Lista podstawowych przedmiotów używanych w grze:
basic_items = [
    "sword",
    "armor", 
    "tools",
    "cloth",
    "wood",
    "metal",
    "herbs",
    "potions",
    "coins",
    "book",
    "horse",
    "goods",
    "pot",
    "knife",
    "basket",
    "oil",
    "broom",
    "brush",
    "leather",
    "food"
]


all_gives = [
    "blessing",
    "morale", 
    "meal",
    "energy",
    "clean space",
    "combat skill",
    "strength",
    "maintained weapons", 
    "clean armor",
    "coins",
    "experience",
    "healthy horse",
    "hot forge",
    "repaired items",
    "new tools",
    "shod horse",
    "weapons",
    "armor",
    "herbs",
    "knowledge",
    "potions",
    "bandages",
    "ready shop",
    "new goods",
    "better prices"
]