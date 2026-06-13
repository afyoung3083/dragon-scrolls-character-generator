# ============================================================
# D&D DATA TABLES
# Lists and dictionaries for names, classes, species,
# backgrounds, alignments, traits, skills, weapons, equipment,
# spells, class features, and ability bonuses.
#
# This file should NOT create GUI widgets.
# This file should NOT save files.
# This file should only hold reusable game data.
# ============================================================

name_starts = [
    "Ael", "Ara", "Bel", "Bra", "Cal", "Cor", "Daer", "Dorn",
    "Ela", "Faer", "Gal", "Gor", "Hal", "Ily", "Kael", "Lor",
    "Mal", "Mor", "Naer", "Orin", "Rael", "Sar", "Ther", "Vor"
]

name_middles = [
    "an", "ar", "el", "en", "eth", "ia", "il", "in",
    "ir", "or", "ra", "rin", "th", "tor", "va", "wen"
]

name_endings = [
    "a", "ae", "an", "ar", "as", "el", "en", "eth",
    "ia", "ion", "is", "or", "os", "ra", "ric", "wyn"
]

name_profiles = {
    "Human": {
        "starts": ["Al", "Ben", "Cor", "Dar", "Ed", "Gar", "Jon", "Mar", "Pet", "Sam", "Tom", "Wil"],
        "middles": ["a", "an", "ar", "en", "er", "il", "on", "or"],
        "endings": ["ard", "as", "en", "ic", "in", "on", "us"]
    },
    "Elf": {
        "starts": ["Ael", "Aer", "Ara", "Eli", "Faer", "Ily", "Lia", "Naer", "Quel", "Sae", "Syl", "Tha"],
        "middles": ["an", "ar", "el", "ia", "iel", "ion", "las", "riel", "thae"],
        "endings": ["a", "ae", "iel", "ion", "las", "lith", "riel", "wyn"]
    },
    "Dwarf": {
        "starts": ["Bal", "Bar", "Brom", "Dain", "Dol", "Dur", "Far", "Gar", "Gim", "Grund", "Kaz", "Thar"],
        "middles": ["a", "ar", "grim", "in", "or", "rak", "rum", "un"],
        "endings": ["ak", "ar", "din", "grim", "in", "or", "rak", "rum"]
    },
    "Halfling": {
        "starts": ["Bil", "Bim", "Cor", "Dob", "Fin", "Hob", "Mar", "Mer", "Ned", "Pip", "Sam", "Tob"],
        "middles": ["a", "bo", "da", "il", "in", "lo", "mi", "per"],
        "endings": ["bin", "by", "do", "kin", "ley", "lin", "lo", "wise"]
    },
    "Half-Elf": {
        "starts": ["Ael", "Cor", "Dar", "Eli", "Faer", "Jon", "Kael", "Lia", "Mar", "Naer", "Sar", "Ther"],
        "middles": ["an", "ar", "el", "en", "ia", "il", "or", "riel"],
        "endings": ["a", "an", "en", "iel", "ion", "is", "or", "wyn"]
    },
    "Dragonborn": {
        "starts": ["Arj", "Bal", "Dra", "Ghesh", "Hes", "Kriv", "Med", "Nad", "Pand", "Rhog", "Sham", "Tor"],
        "middles": ["a", "ar", "ash", "esh", "gar", "ir", "kesh", "rax"],
        "endings": ["ar", "ash", "ax", "esh", "gar", "ir", "rax", "ul"]
    },
    "Tiefling": {
        "starts": ["Ak", "Az", "Dam", "Ex", "Kaz", "Lil", "Mal", "Mor", "Nyx", "Ori", "Rav", "Zar"],
        "middles": ["a", "ar", "eth", "ia", "is", "or", "ra", "ven"],
        "endings": ["a", "eth", "ia", "is", "or", "ra", "ven", "yx"]
    },
    "Gnome": {
        "starts": ["Bim", "Dab", "Fiz", "Glim", "Jeb", "Kip", "Nib", "Pip", "Quib", "Tink", "Wiz", "Zib"],
        "middles": ["a", "ble", "bo", "da", "fiz", "i", "lo", "wick"],
        "endings": ["bin", "ble", "bo", "fiz", "kin", "lo", "wick", "zle"]
    },
    "Half-Orc": {
        "starts": ["Brak", "Drog", "Gor", "Grum", "Hak", "Karg", "Mog", "Rok", "Thok", "Ug", "Varg", "Zog"],
        "middles": ["a", "ag", "ar", "g", "or", "ug", "um"],
        "endings": ["ag", "ar", "g", "nak", "og", "ug", "um"]
    }
}

surname_profiles = {
    "Human": [
        "Blackwood", "Brightwater", "Dunfield", "Greycastle", "Hawthorne",
        "Ironford", "Marshfield", "Redmont", "Stormwell", "Westbridge"
    ],
    "Elf": [
        "Amastacia", "Duskwhisper", "Evenstar", "Moonbrook", "Nightbreeze",
        "Silverleaf", "Starweaver", "Sunshadow", "Thornvale", "Windlore"
    ],
    "Dwarf": [
        "Anvilborn", "Bronzebeard", "Deepdelver", "Forgeheart", "Granitefist",
        "Ironvein", "Stonehammer", "Strongale", "Underforge", "Warshield"
    ],
    "Halfling": [
        "Appleblossom", "Brushgather", "Goodbarrel", "Greenbottle", "Hilltopple",
        "Meadowbrook", "Smallburrow", "Tealeaf", "Underbough", "Warmhearth"
    ],
    "Half-Elf": [
        "Brightvale", "Dawnmere", "Evenwood", "Greybrook", "Lightfoot",
        "Moonfield", "Silvermere", "Starling", "Wyndale", "Youngblood"
    ],
    "Dragonborn": [
        "of Clan Ashscale", "of Clan Emberfang", "of Clan Flamebrow", "of Clan Ironclaw",
        "of Clan Stormhorn", "of Clan Thunderjaw", "of Clan Vipercrest", "of Clan Warwing"
    ],
    "Tiefling": [
        "Ash", "Chance", "Desire", "Echo", "Fate",
        "Glory", "Hope", "Mercy", "Silence", "Truth"
    ],
    "Gnome": [
        "Bafflestone", "Copperwidget", "Fizzlebang", "Gearwhistle", "Nimblefuse",
        "Quickspanner", "Sparklegem", "Tinkertonk", "Underwhistle", "Wobblewick"
    ],
    "Half-Orc": [
        "Bloodtusk", "Bonebreaker", "Darkfist", "Gorehand", "Ironjaw",
        "Redscar", "Skullsplitter", "Stormrage", "Thornhide", "Warborn"
    ]
}

classes = [
    "Fighter",
    "Wizard",
    "Rogue",
    "Cleric",
    "Ranger",
    "Paladin",
    "Barbarian",
    "Bard",
    "Monk",
    "Sorcerer",
    "Warlock"
]

ability_order = [
    "Strength",
    "Dexterity",
    "Constitution",
    "Intelligence",
    "Wisdom",
    "Charisma"
]

species = [
    "Human",
    "Elf",
    "Dwarf",
    "Halfling",
    "Half-Elf",
    "Dragonborn",
    "Tiefling",
    "Gnome",
    "Half-Orc"
]

backgrounds = [
    "Acolyte",
    "Charlatan",
    "Criminal",
    "Entertainer",
    "Folk Hero",
    "Guild Artisan",
    "Hermit",
    "Noble",
    "Outlander",
    "Sage",
    "Sailor",
    "Soldier",
    "Urchin"
]

alignments = [
    "Lawful Good",
    "Neutral Good",
    "Chaotic Good",
    "Lawful Neutral",
    "True Neutral",
    "Chaotic Neutral",
    "Lawful Evil",
    "Neutral Evil",
    "Chaotic Evil"
]

sex_options = [
    "Male",
    "Female"
]

level_options = [
    "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15",
    "16", "17", "18", "19", "20"
]

roll_method_options = [
    "4d6 Drop Lowest",
    "3d6 Straight",
    "Heroic 2d6+6",
    "Standard Array",
    "Point Buy"
]

personality_traits = [
    "I am always calm, even under pressure.",
    "I ask too many questions.",
    "I am suspicious of strangers.",
    "I try to make friends wherever I go.",
    "I speak plainly and directly.",
    "I enjoy telling stories about my past.",
    "I am slow to trust, but loyal once trust is earned.",
    "I laugh at danger, sometimes at the wrong time.",
    "I collect small trophies from places I visit.",
    "I speak in dramatic warnings, even about ordinary things.",
    "I am polite to a fault, even toward enemies.",
    "I constantly compare new places to my homeland.",
    "I prefer action over long debate.",
    "I keep a journal of names, debts, and promises.",
    "I test people with small questions before trusting them.",
    "I enjoy riddles, codes, and hidden meanings.",
    "I treat meals as sacred moments of peace.",
    "I often stare into the distance as if remembering another life."    
]

ideals = [
    "Justice. The guilty should be held accountable.",
    "Freedom. No one should live under tyranny.",
    "Knowledge. Truth is worth seeking at any cost.",
    "Compassion. The strong should protect the weak.",
    "Glory. I want my deeds to be remembered.",
    "Duty. I keep my promises, no matter the cost.",
    "Redemption. No one is beyond a second chance.",
    "Power. Strength is the only language the world respects.",
    "Honor. My word is worth more than gold.",
    "Balance. Too much power in one place invites ruin.",
    "Tradition. The old ways preserve hard-won wisdom.",
    "Discovery. The world is full of secrets waiting to be found.",
    "Mercy. Victory without compassion is hollow.",
    "Courage. Fear is real, but it must not rule me.",
    "Loyalty. I do not abandon those who depend on me.",
    "Independence. I must be free to choose my own path.",
    "Sacrifice. Some goods are worth suffering for.",
    "Order. Peace requires discipline, law, and restraint."    
]

bonds = [
    "I owe my life to an old mentor.",
    "I am searching for a lost family member.",
    "I carry a token from someone I failed to save.",
    "My hometown is in danger, and I intend to protect it.",
    "I serve a temple, guild, order, or military company.",
    "I seek revenge against someone who wronged me.",
    "I am trying to restore my family's honor.",
    "I protect a secret that could change many lives.",
    "I carry a map given to me by someone who vanished.",
    "A rival adventurer is always one step ahead of me.",
    "I must repay a debt to a dangerous patron.",
    "I protect the last heir of a fallen house.",
    "An ancient symbol has followed me since childhood.",
    "I made a vow at a grave and intend to keep it.",
    "I am responsible for a younger sibling, student, or apprentice.",
    "My family name opens doors in some places and closes them in others.",
    "I seek the truth behind a curse placed on my bloodline.",
    "I once saw a vision, and I believe my journey is part of it."    
]

flaws = [
    "I have trouble admitting when I am wrong.",
    "I sometimes act before thinking.",
    "I am too quick to trust a sob story.",
    "I hold grudges longer than I should.",
    "I am tempted by gold, status, or power.",
    "I avoid difficult emotional conversations.",
    "I underestimate people who seem weak.",
    "I panic when innocent people are in danger.",
    "I assume silence means disapproval.",
    "I hide fear behind sarcasm.",
    "I cannot resist proving I am the smartest person in the room.",
    "I make promises faster than I can keep them.",
    "I become reckless when someone questions my courage.",
    "I struggle to forgive betrayal.",
    "I trust traditions even when circumstances have changed.",
    "I am easily distracted by mysteries and secrets.",
    "I treat every disagreement like a contest to win.",
    "I sometimes mistake stubbornness for faithfulness."    
]

class_ability_priorities = {
    "Fighter": ["Strength", "Constitution", "Dexterity", "Wisdom", "Charisma", "Intelligence"],
    "Wizard": ["Intelligence", "Constitution", "Dexterity", "Wisdom", "Charisma", "Strength"],
    "Rogue": ["Dexterity", "Intelligence", "Charisma", "Constitution", "Wisdom", "Strength"],
    "Cleric": ["Wisdom", "Constitution", "Strength", "Charisma", "Dexterity", "Intelligence"],
    "Ranger": ["Dexterity", "Wisdom", "Constitution", "Strength", "Intelligence", "Charisma"],
    "Paladin": ["Strength", "Charisma", "Constitution", "Wisdom", "Dexterity", "Intelligence"],
    "Barbarian": ["Strength", "Constitution", "Dexterity", "Wisdom", "Charisma", "Intelligence"],
    "Bard": ["Charisma", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Strength"],
    "Monk": ["Dexterity", "Wisdom", "Constitution", "Strength", "Charisma", "Intelligence"],
    "Sorcerer": ["Charisma", "Constitution", "Dexterity", "Wisdom", "Intelligence", "Strength"],
    "Warlock": ["Charisma", "Constitution", "Dexterity", "Wisdom", "Intelligence", "Strength"]
}

class_saving_throw_proficiencies = {
    "Fighter": ["Strength", "Constitution"],
    "Wizard": ["Intelligence", "Wisdom"],
    "Rogue": ["Dexterity", "Intelligence"],
    "Cleric": ["Wisdom", "Charisma"],
    "Ranger": ["Strength", "Dexterity"],
    "Paladin": ["Wisdom", "Charisma"],
    "Barbarian": ["Strength", "Constitution"],
    "Bard": ["Dexterity", "Charisma"],
    "Monk": ["Strength", "Dexterity"],
    "Sorcerer": ["Constitution", "Charisma"],
    "Warlock": ["Wisdom", "Charisma"]
}

skill_ability_map = {
    "Athletics": "Strength",
    "Acrobatics": "Dexterity",
    "Sleight of Hand": "Dexterity",
    "Stealth": "Dexterity",
    "Arcana": "Intelligence",
    "History": "Intelligence",
    "Investigation": "Intelligence",
    "Nature": "Intelligence",
    "Religion": "Intelligence",
    "Animal Handling": "Wisdom",
    "Insight": "Wisdom",
    "Medicine": "Wisdom",
    "Perception": "Wisdom",
    "Survival": "Wisdom",
    "Deception": "Charisma",
    "Intimidation": "Charisma",
    "Performance": "Charisma",
    "Persuasion": "Charisma"
}

class_skill_proficiencies = {
    "Fighter": ["Athletics", "Intimidation"],
    "Wizard": ["Arcana", "History"],
    "Rogue": ["Stealth", "Sleight of Hand", "Acrobatics", "Investigation"],
    "Cleric": ["Religion", "Insight"],
    "Ranger": ["Nature", "Perception", "Survival"],
    "Paladin": ["Athletics", "Persuasion"],
    "Barbarian": ["Athletics", "Survival"],
    "Bard": ["Performance", "Persuasion", "Deception"],
    "Monk": ["Acrobatics", "Insight"],
    "Sorcerer": ["Arcana", "Persuasion"],
    "Warlock": ["Arcana", "Deception"]
}

class_hit_dice = {
    "Fighter": 10,
    "Wizard": 6,
    "Rogue": 8,
    "Cleric": 8,
    "Ranger": 10,
    "Paladin": 10,
    "Barbarian": 12,
    "Bard": 8,
    "Monk": 8,
    "Sorcerer": 6,
    "Warlock": 8
}

species_speeds = {
    "Human": 30,
    "Elf": 30,
    "Dwarf": 25,
    "Halfling": 25,
    "Half-Elf": 30,
    "Dragonborn": 30,
    "Tiefling": 30,
    "Gnome": 25,
    "Half-Orc": 30
}

class_starting_weapons = {
    "Fighter": ["Longsword"],
    "Wizard": ["Quarterstaff"],
    "Rogue": ["Shortsword", "Shortbow"],
    "Cleric": ["Mace"],
    "Ranger": ["Longbow", "Shortswords"],
    "Paladin": ["Longsword"],
    "Barbarian": ["Greataxe", "Handaxes"],
    "Bard": ["Rapier"],
    "Monk": ["Shortsword", "Darts"],
    "Sorcerer": ["Dagger", "Light Crossbow"],
    "Warlock": ["Dagger", "Light Crossbow"]
}

weapon_rules = {
    "Longsword": {
        "ability": "Strength",
        "damage": "1d8 slashing"
    },
    "Quarterstaff": {
        "ability": "Strength",
        "damage": "1d6 bludgeoning"
    },
    "Shortsword": {
        "ability": "Dexterity",
        "damage": "1d6 piercing"
    },
    "Shortbow": {
        "ability": "Dexterity",
        "damage": "1d6 piercing"
    },
    "Mace": {
        "ability": "Strength",
        "damage": "1d6 bludgeoning"
    },
    "Longbow": {
        "ability": "Dexterity",
        "damage": "1d8 piercing"
    },
    "Rapier": {
        "ability": "Dexterity",
        "damage": "1d8 piercing"
    },
    "Greataxe": {
        "ability": "Strength",
        "damage": "1d12 slashing"
    },
    "Handaxes": {
        "ability": "Strength",
        "damage": "1d6 slashing"
    },
    "Shortswords": {
        "ability": "Dexterity",
        "damage": "1d6 piercing"
    },
    "Dagger": {
        "ability": "Dexterity",
        "damage": "1d4 piercing"
    },
    "Darts": {
        "ability": "Dexterity",
        "damage": "1d4 piercing"
    },
    "Light Crossbow": {
        "ability": "Dexterity",
        "damage": "1d8 piercing"
    }
}

class_starting_equipment = {
    "Fighter": ["Chain Mail", "Longsword", "Shield", "Explorer's Pack"],
    "Wizard": ["Quarterstaff", "Spellbook", "Component Pouch", "Scholar's Pack"],
    "Rogue": ["Leather Armor", "Shortsword", "Shortbow", "Burglar's Pack", "Thieves' Tools"],
    "Cleric": ["Scale Mail", "Mace", "Shield", "Holy Symbol", "Priest's Pack"],
    "Ranger": ["Leather Armor", "Longbow", "Shortswords", "Explorer's Pack"],
    "Paladin": ["Chain Mail", "Longsword", "Shield", "Holy Symbol", "Explorer's Pack"],
    "Barbarian": ["Greataxe", "Handaxes", "Explorer's Pack"],
    "Bard": ["Leather Armor", "Rapier", "Lute", "Diplomat's Pack"],
    "Monk": ["Shortsword", "Darts", "Explorer's Pack"],
    "Sorcerer": ["Dagger", "Light Crossbow", "Component Pouch", "Explorer's Pack"],
    "Warlock": ["Dagger", "Light Crossbow", "Arcane Focus", "Scholar's Pack"]    
}

class_features = {
    "Fighter": ["Fighting Style", "Second Wind"],
    "Wizard": ["Spellcasting", "Arcane Recovery"],
    "Rogue": ["Expertise", "Sneak Attack", "Thieves' Cant"],
    "Cleric": ["Spellcasting", "Divine Domain"],
    "Ranger": ["Favored Enemy", "Natural Explorer"],
    "Paladin": ["Divine Sense", "Lay on Hands"],
    "Barbarian": ["Rage", "Unarmored Defense"],
    "Bard": ["Spellcasting", "Bardic Inspiration"],
    "Monk": ["Unarmored Defense", "Martial Arts"],
    "Sorcerer": ["Spellcasting", "Sorcerous Origin"],
    "Warlock": ["Otherworldly Patron", "Pact Magic"]    
}

class_features_by_level = {
    "Fighter": {
        1: ["Fighting Style", "Second Wind"],
        2: ["Action Surge"],
        3: ["Martial Archetype"],
        4: ["Ability Score Improvement"],
        5: ["Extra Attack"],
        9: ["Indomitable"],
        11: ["Extra Attack (2)"],
        20: ["Extra Attack (3)"]
    },
    "Wizard": {
        1: ["Spellcasting", "Arcane Recovery"],
        2: ["Arcane Tradition"],
        4: ["Ability Score Improvement"],
        5: ["3rd-Level Spells"],
        9: ["5th-Level Spells"],
        11: ["6th-Level Spells"],
        17: ["9th-Level Spells"],
        18: ["Spell Mastery"],
        20: ["Signature Spells"]
    },
    "Rogue": {
        1: ["Expertise", "Sneak Attack", "Thieves' Cant"],
        2: ["Cunning Action"],
        3: ["Roguish Archetype"],
        4: ["Ability Score Improvement"],
        5: ["Uncanny Dodge"],
        7: ["Evasion"],
        11: ["Reliable Talent"],
        14: ["Blindsense"],
        15: ["Slippery Mind"],
        18: ["Elusive"],
        20: ["Stroke of Luck"]
    },
    "Cleric": {
        1: ["Spellcasting", "Divine Domain"],
        2: ["Channel Divinity"],
        4: ["Ability Score Improvement"],
        5: ["Destroy Undead"],
        10: ["Divine Intervention"],
        17: ["Improved Divine Intervention"]
    },
    "Ranger": {
        1: ["Favored Enemy", "Natural Explorer"],
        2: ["Fighting Style", "Spellcasting"],
        3: ["Ranger Archetype"],
        4: ["Ability Score Improvement"],
        5: ["Extra Attack"],
        8: ["Land's Stride"],
        10: ["Hide in Plain Sight"],
        14: ["Vanish"],
        18: ["Feral Senses"],
        20: ["Foe Slayer"]
    },
    "Paladin": {
        1: ["Divine Sense", "Lay on Hands"],
        2: ["Fighting Style", "Spellcasting", "Divine Smite"],
        3: ["Sacred Oath", "Divine Health"],
        4: ["Ability Score Improvement"],
        5: ["Extra Attack"],
        6: ["Aura of Protection"],
        10: ["Aura of Courage"],
        11: ["Improved Divine Smite"],
        14: ["Cleansing Touch"]
    },
    "Barbarian": {
        1: ["Rage", "Unarmored Defense"],
        2: ["Reckless Attack", "Danger Sense"],
        3: ["Primal Path"],
        4: ["Ability Score Improvement"],
        5: ["Extra Attack", "Fast Movement"],
        7: ["Feral Instinct"],
        9: ["Brutal Critical"],
        11: ["Relentless Rage"],
        15: ["Persistent Rage"],
        18: ["Indomitable Might"],
        20: ["Primal Champion"]
    },
    "Bard": {
        1: ["Spellcasting", "Bardic Inspiration"],
        2: ["Jack of All Trades", "Song of Rest"],
        3: ["Bard College", "Expertise"],
        4: ["Ability Score Improvement"],
        5: ["Font of Inspiration"],
        6: ["Countercharm"],
        10: ["Magical Secrets"],
        20: ["Superior Inspiration"]
    },
    "Monk": {
        1: ["Unarmored Defense", "Martial Arts"],
        2: ["Ki", "Unarmored Movement"],
        3: ["Monastic Tradition", "Deflect Missiles"],
        4: ["Ability Score Improvement", "Slow Fall"],
        5: ["Extra Attack", "Stunning Strike"],
        7: ["Evasion", "Stillness of Mind"],
        10: ["Purity of Body"],
        14: ["Diamond Soul"],
        15: ["Timeless Body"],
        18: ["Empty Body"],
        20: ["Perfect Self"]
    },
    "Sorcerer": {
        1: ["Spellcasting", "Sorcerous Origin"],
        2: ["Font of Magic"],
        3: ["Metamagic"],
        4: ["Ability Score Improvement"],
        5: ["3rd-Level Spells"],
        10: ["Additional Metamagic"],
        17: ["9th-Level Spells"],
        20: ["Sorcerous Restoration"]
    },
    "Warlock": {
        1: ["Otherworldly Patron", "Pact Magic"],
        2: ["Eldritch Invocations"],
        3: ["Pact Boon"],
        4: ["Ability Score Improvement"],
        5: ["3rd-Level Pact Magic"],
        11: ["Mystic Arcanum (6th Level)"],
        13: ["Mystic Arcanum (7th Level)"],
        15: ["Mystic Arcanum (8th Level)"],
        17: ["Mystic Arcanum (9th Level)"],
        20: ["Eldritch Master"]
    }
}

class_subclass_levels = {
    "Fighter": 3,
    "Wizard": 2,
    "Rogue": 3,
    "Cleric": 1,
    "Ranger": 3,
    "Paladin": 3,
    "Barbarian": 3,
    "Bard": 3,
    "Monk": 3,
    "Sorcerer": 1,
    "Warlock": 1
}


class_subclasses = {
    "Fighter": [
        "Champion",
        "Battle Master",
        "Eldritch Knight"
    ],
    "Wizard": [
        "School of Evocation",
        "School of Abjuration",
        "School of Divination"
    ],
    "Rogue": [
        "Thief",
        "Assassin",
        "Arcane Trickster"
    ],
    "Cleric": [
        "Life Domain",
        "Light Domain",
        "War Domain",
        "Knowledge Domain"
    ],
    "Ranger": [
        "Hunter",
        "Beast Master",
        "Gloom Stalker"
    ],
    "Paladin": [
        "Oath of Devotion",
        "Oath of the Ancients",
        "Oath of Vengeance"
    ],
    "Barbarian": [
        "Path of the Berserker",
        "Path of the Totem Warrior",
        "Path of the Zealot"
    ],
    "Bard": [
        "College of Lore",
        "College of Valor",
        "College of Glamour"
    ],
    "Monk": [
        "Way of the Open Hand",
        "Way of Shadow",
        "Way of the Four Elements"
    ],
    "Sorcerer": [
        "Draconic Bloodline",
        "Wild Magic",
        "Divine Soul"
    ],
    "Warlock": [
        "The Fiend",
        "The Archfey",
        "The Great Old One"
    ]
}

subclass_features_by_level = {
    "Champion": {
        3: ["Improved Critical"],
        7: ["Remarkable Athlete"],
        10: ["Additional Fighting Style"],
        15: ["Superior Critical"],
        18: ["Survivor"]
    },
    "Battle Master": {
        3: ["Combat Superiority", "Student of War"],
        7: ["Know Your Enemy"],
        10: ["Improved Combat Superiority"],
        15: ["Relentless"]
    },
    "Eldritch Knight": {
        3: ["Weapon Bond", "Eldritch Knight Spellcasting"],
        7: ["War Magic"],
        10: ["Eldritch Strike"],
        15: ["Arcane Charge"],
        18: ["Improved War Magic"]
    },

    "School of Evocation": {
        2: ["Evocation Savant", "Sculpt Spells"],
        6: ["Potent Cantrip"],
        10: ["Empowered Evocation"],
        14: ["Overchannel"]
    },
    "School of Abjuration": {
        2: ["Abjuration Savant", "Arcane Ward"],
        6: ["Projected Ward"],
        10: ["Improved Abjuration"],
        14: ["Spell Resistance"]
    },
    "School of Divination": {
        2: ["Divination Savant", "Portent"],
        6: ["Expert Divination"],
        10: ["The Third Eye"],
        14: ["Greater Portent"]
    },

    "Thief": {
        3: ["Fast Hands", "Second-Story Work"],
        9: ["Supreme Sneak"],
        13: ["Use Magic Device"],
        17: ["Thief's Reflexes"]
    },
    "Assassin": {
        3: ["Bonus Proficiencies", "Assassinate"],
        9: ["Infiltration Expertise"],
        13: ["Impostor"],
        17: ["Death Strike"]
    },
    "Arcane Trickster": {
        3: ["Arcane Trickster Spellcasting", "Mage Hand Legerdemain"],
        9: ["Magical Ambush"],
        13: ["Versatile Trickster"],
        17: ["Spell Thief"]
    },

    "Life Domain": {
        1: ["Bonus Proficiency", "Disciple of Life"],
        2: ["Channel Divinity: Preserve Life"],
        6: ["Blessed Healer"],
        8: ["Divine Strike"],
        17: ["Supreme Healing"]
    },
    "Light Domain": {
        1: ["Bonus Cantrip", "Warding Flare"],
        2: ["Channel Divinity: Radiance of the Dawn"],
        6: ["Improved Flare"],
        8: ["Potent Spellcasting"],
        17: ["Corona of Light"]
    },
    "War Domain": {
        1: ["Bonus Proficiencies", "War Priest"],
        2: ["Channel Divinity: Guided Strike"],
        6: ["Channel Divinity: War God's Blessing"],
        8: ["Divine Strike"],
        17: ["Avatar of Battle"]
    },
    "Knowledge Domain": {
        1: ["Blessings of Knowledge"],
        2: ["Channel Divinity: Knowledge of the Ages"],
        6: ["Channel Divinity: Read Thoughts"],
        8: ["Potent Spellcasting"],
        17: ["Visions of the Past"]
    },

    "Hunter": {
        3: ["Hunter's Prey"],
        7: ["Defensive Tactics"],
        11: ["Multiattack"],
        15: ["Superior Hunter's Defense"]
    },
    "Beast Master": {
        3: ["Ranger's Companion"],
        7: ["Exceptional Training"],
        11: ["Bestial Fury"],
        15: ["Share Spells"]
    },
    "Gloom Stalker": {
        3: ["Gloom Stalker Magic", "Dread Ambusher", "Umbral Sight"],
        7: ["Iron Mind"],
        11: ["Stalker's Flurry"],
        15: ["Shadowy Dodge"]
    },

    "Oath of Devotion": {
        3: ["Oath Spells", "Channel Divinity"],
        7: ["Aura of Devotion"],
        15: ["Purity of Spirit"],
        20: ["Holy Nimbus"]
    },
    "Oath of the Ancients": {
        3: ["Oath Spells", "Channel Divinity"],
        7: ["Aura of Warding"],
        15: ["Undying Sentinel"],
        20: ["Elder Champion"]
    },
    "Oath of Vengeance": {
        3: ["Oath Spells", "Channel Divinity"],
        7: ["Relentless Avenger"],
        15: ["Soul of Vengeance"],
        20: ["Avenging Angel"]
    },

    "Path of the Berserker": {
        3: ["Frenzy"],
        6: ["Mindless Rage"],
        10: ["Intimidating Presence"],
        14: ["Retaliation"]
    },
    "Path of the Totem Warrior": {
        3: ["Spirit Seeker", "Totem Spirit"],
        6: ["Aspect of the Beast"],
        10: ["Spirit Walker"],
        14: ["Totemic Attunement"]
    },
    "Path of the Zealot": {
        3: ["Divine Fury", "Warrior of the Gods"],
        6: ["Fanatical Focus"],
        10: ["Zealous Presence"],
        14: ["Rage Beyond Death"]
    },

    "College of Lore": {
        3: ["Bonus Proficiencies", "Cutting Words"],
        6: ["Additional Magical Secrets"],
        14: ["Peerless Skill"]
    },
    "College of Valor": {
        3: ["Bonus Proficiencies", "Combat Inspiration"],
        6: ["Extra Attack"],
        14: ["Battle Magic"]
    },
    "College of Glamour": {
        3: ["Mantle of Inspiration", "Enthralling Performance"],
        6: ["Mantle of Majesty"],
        14: ["Unbreakable Majesty"]
    },

    "Way of the Open Hand": {
        3: ["Open Hand Technique"],
        6: ["Wholeness of Body"],
        11: ["Tranquility"],
        17: ["Quivering Palm"]
    },
    "Way of Shadow": {
        3: ["Shadow Arts"],
        6: ["Shadow Step"],
        11: ["Cloak of Shadows"],
        17: ["Opportunist"]
    },
    "Way of the Four Elements": {
        3: ["Disciple of the Elements"],
        6: ["Elemental Discipline Improvement"],
        11: ["Elemental Discipline Improvement"],
        17: ["Elemental Discipline Improvement"]
    },

    "Draconic Bloodline": {
        1: ["Dragon Ancestor", "Draconic Resilience"],
        6: ["Elemental Affinity"],
        14: ["Dragon Wings"],
        18: ["Draconic Presence"]
    },
    "Wild Magic": {
        1: ["Wild Magic Surge", "Tides of Chaos"],
        6: ["Bend Luck"],
        14: ["Controlled Chaos"],
        18: ["Spell Bombardment"]
    },
    "Divine Soul": {
        1: ["Divine Magic", "Favored by the Gods"],
        6: ["Empowered Healing"],
        14: ["Otherworldly Wings"],
        18: ["Unearthly Recovery"]
    },

    "The Fiend": {
        1: ["Expanded Spell List", "Dark One's Blessing"],
        6: ["Dark One's Own Luck"],
        10: ["Fiendish Resilience"],
        14: ["Hurl Through Hell"]
    },
    "The Archfey": {
        1: ["Expanded Spell List", "Fey Presence"],
        6: ["Misty Escape"],
        10: ["Beguiling Defenses"],
        14: ["Dark Delirium"]
    },
    "The Great Old One": {
        1: ["Expanded Spell List", "Awakened Mind"],
        6: ["Entropic Ward"],
        10: ["Thought Shield"],
        14: ["Create Thrall"]
    }
}

subclass_image_flavor = {
    "Champion": "Emphasize athletic confidence, heroic posture, polished weapons, and a straightforward martial presence.",
    "Battle Master": "Emphasize tactical intelligence, battlefield command, disciplined stance, weapon mastery, and a veteran officer-like presence.",
    "Eldritch Knight": "Emphasize a blend of martial armor and arcane energy, with a weapon ready and subtle magical runes or glowing effects.",

    "School of Evocation": "Emphasize controlled destructive magic, glowing elemental energy, and a confident arcane battle-mage presence.",
    "School of Abjuration": "Emphasize protective wards, arcane shields, defensive runes, and a calm guardian-like magical presence.",
    "School of Divination": "Emphasize mystical foresight, star-like symbols, an observant expression, and subtle prophetic or cosmic imagery.",

    "Thief": "Emphasize nimble movement, practical gear, climbing tools, quick hands, and a streetwise opportunist look.",
    "Assassin": "Emphasize shadow, precision, concealed weapons, quiet menace, and a dangerous controlled expression.",
    "Arcane Trickster": "Emphasize a mischievous rogue with subtle illusion magic, glowing mage hand energy, and clever eyes.",

    "Life Domain": "Emphasize a holy healer presence, warm divine light, protective compassion, and sacred symbols of restoration.",
    "Light Domain": "Emphasize radiant light, flame-like divine energy, brightness against darkness, and a confident holy caster presence.",
    "War Domain": "Emphasize battle-priest imagery, heavy armor, sacred weaponry, martial confidence, and divine authority.",
    "Knowledge Domain": "Emphasize scrolls, books, sacred scholarship, thoughtful eyes, and divine wisdom rather than brute force.",

    "Hunter": "Emphasize a rugged monster-hunter look, wilderness gear, alert posture, and practical weapons suited for tracking prey.",
    "Beast Master": "Emphasize a bond with nature and an animal companion presence, even if the animal is only suggested in the background.",
    "Gloom Stalker": "Emphasize shadowy wilderness, underground or twilight mood, stealth, dark cloak, and predator-like alertness.",

    "Oath of Devotion": "Emphasize noble knightly virtue, bright armor, sacred symbols, and a classic honorable paladin presence.",
    "Oath of the Ancients": "Emphasize nature-themed holy power, old forest magic, vines, ancient light, and a guardian of life mood.",
    "Oath of Vengeance": "Emphasize grim determination, intense eyes, darker armor, righteous fury, and a relentless avenger presence.",

    "Path of the Berserker": "Emphasize raw fury, battle scars, wild intensity, heavy weaponry, and barely contained rage.",
    "Path of the Totem Warrior": "Emphasize spiritual animal symbolism, tribal or wilderness elements, and a primal guardian presence.",
    "Path of the Zealot": "Emphasize holy rage, divine fire, battle fervor, and a warrior driven by sacred purpose.",

    "College of Lore": "Emphasize scholarly bardic charm, books or scrolls, clever expression, and a storyteller or historian presence.",
    "College of Valor": "Emphasize heroic performance, battlefield inspiration, armor, weapons, and a bold warrior-poet mood.",
    "College of Glamour": "Emphasize enchanting beauty, fey-like charm, elegant clothing, and captivating stage presence.",

    "Way of the Open Hand": "Emphasize disciplined martial arts, calm posture, unarmed readiness, and balanced spiritual focus.",
    "Way of Shadow": "Emphasize stealth, darkness, silent movement, masked or hooded details, and shadowy martial discipline.",
    "Way of the Four Elements": "Emphasize elemental martial arts, with subtle fire, water, air, or earth energy around the hands or stance.",

    "Draconic Bloodline": "Emphasize draconic influence, subtle scales or dragon-like aura, elemental power, and noble sorcerous confidence.",
    "Wild Magic": "Emphasize unpredictable magical energy, colorful arcane sparks, whimsical danger, and unstable magical atmosphere.",
    "Divine Soul": "Emphasize celestial magic, gentle divine light, angelic undertones, and a sacred sorcerous presence.",

    "The Fiend": "Emphasize infernal influence, ember-like lighting, dark pact magic, horns or hellish motifs if appropriate, and dangerous charisma.",
    "The Archfey": "Emphasize fey mystery, otherworldly elegance, woodland magic, strange beauty, and enchanting presence.",
    "The Great Old One": "Emphasize eerie cosmic mystery, unsettling calm, strange symbols, distant eyes, and subtle eldritch atmosphere."
}

spellcasting_classes = {
    "Wizard": {
        "spellcasting_ability": "Intelligence",
        "cantrips": ["Fire Bolt", "Mage Hand", "Prestidigitation"],
        "level_1_spells": ["Magic Missile", "Shield", "Detect Magic"]
    },
    "Cleric": {
        "spellcasting_ability": "Wisdom",
        "cantrips": ["Sacred Flame", "Guidance", "Thaumaturgy"],
        "level_1_spells": ["Cure Wounds", "Bless", "Guiding Bolt"]
    },
    "Bard": {
        "spellcasting_ability": "Charisma",
        "cantrips": ["Vicious Mockery", "Mage Hand"],
        "level_1_spells": ["Healing Word", "Dissonant Whispers", "Charm Person"]
    },
    "Paladin": {
        "spellcasting_ability": "Charisma",
        "cantrips": [],
        "level_1_spells": []
    },
    "Ranger": {
        "spellcasting_ability": "Wisdom",
        "cantrips": [],
        "level_1_spells": []
    },
    "Sorcerer": {
        "spellcasting_ability": "Charisma",
        "cantrips": ["Fire Bolt", "Mage Hand", "Minor Illusion", "Prestidigitation"],
        "level_1_spells": ["Shield", "Magic Missile"]
    },
    "Warlock": {
        "spellcasting_ability": "Charisma",
        "cantrips": ["Eldritch Blast", "Mage Hand"],
        "level_1_spells": ["Hex", "Armor of Agathys"]
    }    
}

spell_slot_progression = {
    "full": {
        1: "2 level 1 slots",
        2: "3 level 1 slots",
        3: "4 level 1 slots, 2 level 2 slots",
        4: "4 level 1 slots, 3 level 2 slots",
        5: "4 level 1 slots, 3 level 2 slots, 2 level 3 slots",
        6: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots",
        7: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 1 level 4 slot",
        8: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 2 level 4 slots",
        9: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 3 level 4 slots, 1 level 5 slot",
        10: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 3 level 4 slots, 2 level 5 slots",
        11: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 3 level 4 slots, 2 level 5 slots, 1 level 6 slot",
        12: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 3 level 4 slots, 2 level 5 slots, 1 level 6 slot",
        13: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 3 level 4 slots, 2 level 5 slots, 1 level 6 slot, 1 level 7 slot",
        14: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 3 level 4 slots, 2 level 5 slots, 1 level 6 slot, 1 level 7 slot",
        15: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 3 level 4 slots, 2 level 5 slots, 1 level 6 slot, 1 level 7 slot, 1 level 8 slot",
        16: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 3 level 4 slots, 2 level 5 slots, 1 level 6 slot, 1 level 7 slot, 1 level 8 slot",
        17: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 3 level 4 slots, 2 level 5 slots, 1 level 6 slot, 1 level 7 slot, 1 level 8 slot, 1 level 9 slot",
        18: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 3 level 4 slots, 3 level 5 slots, 1 level 6 slot, 1 level 7 slot, 1 level 8 slot, 1 level 9 slot",
        19: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 3 level 4 slots, 3 level 5 slots, 2 level 6 slots, 1 level 7 slot, 1 level 8 slot, 1 level 9 slot",
        20: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 3 level 4 slots, 3 level 5 slots, 2 level 6 slots, 2 level 7 slots, 1 level 8 slot, 1 level 9 slot"
    },
    "half": {
        1: "No spell slots at level 1",
        2: "2 level 1 slots",
        3: "3 level 1 slots",
        4: "3 level 1 slots",
        5: "4 level 1 slots, 2 level 2 slots",
        6: "4 level 1 slots, 2 level 2 slots",
        7: "4 level 1 slots, 3 level 2 slots",
        8: "4 level 1 slots, 3 level 2 slots",
        9: "4 level 1 slots, 3 level 2 slots, 2 level 3 slots",
        10: "4 level 1 slots, 3 level 2 slots, 2 level 3 slots",
        11: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots",
        12: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots",
        13: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 1 level 4 slot",
        14: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 1 level 4 slot",
        15: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 2 level 4 slots",
        16: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 2 level 4 slots",
        17: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 3 level 4 slots, 1 level 5 slot",
        18: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 3 level 4 slots, 1 level 5 slot",
        19: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 3 level 4 slots, 2 level 5 slots",
        20: "4 level 1 slots, 3 level 2 slots, 3 level 3 slots, 3 level 4 slots, 2 level 5 slots"
    },
    "warlock": {
        1: "1 pact slot, level 1",
        2: "2 pact slots, level 1",
        3: "2 pact slots, level 2",
        4: "2 pact slots, level 2",
        5: "2 pact slots, level 3",
        6: "2 pact slots, level 3",
        7: "2 pact slots, level 4",
        8: "2 pact slots, level 4",
        9: "2 pact slots, level 5",
        10: "2 pact slots, level 5",
        11: "3 pact slots, level 5; Mystic Arcanum level 6",
        12: "3 pact slots, level 5; Mystic Arcanum level 6",
        13: "3 pact slots, level 5; Mystic Arcanum levels 6-7",
        14: "3 pact slots, level 5; Mystic Arcanum levels 6-7",
        15: "3 pact slots, level 5; Mystic Arcanum levels 6-8",
        16: "3 pact slots, level 5; Mystic Arcanum levels 6-8",
        17: "4 pact slots, level 5; Mystic Arcanum levels 6-9",
        18: "4 pact slots, level 5; Mystic Arcanum levels 6-9",
        19: "4 pact slots, level 5; Mystic Arcanum levels 6-9",
        20: "4 pact slots, level 5; Mystic Arcanum levels 6-9"
    }
}

class_spell_progression_type = {
    "Wizard": "full",
    "Cleric": "full",
    "Bard": "full",
    "Sorcerer": "full",
    "Paladin": "half",
    "Ranger": "half",
    "Warlock": "warlock"
}

MAX_CANTRIPS_TO_SHOW = 4
MAX_LEVEL_1_SPELLS_TO_SHOW = 4
MAX_HIGHER_LEVEL_SPELLS_TO_SHOW = 8

spell_examples_by_class = {
    "Wizard": {
        "cantrips": ["Fire Bolt", "Mage Hand", "Prestidigitation", "Ray of Frost"],
        1: ["Magic Missile", "Shield", "Detect Magic", "Sleep"],
        2: ["Misty Step", "Scorching Ray", "Invisibility"],
        3: ["Fireball", "Counterspell", "Fly"],
        4: ["Greater Invisibility", "Ice Storm"],
        5: ["Cone of Cold", "Wall of Force"],
        6: ["Chain Lightning", "Disintegrate"],
        7: ["Teleport", "Finger of Death"],
        8: ["Maze", "Power Word Stun"],
        9: ["Wish", "Meteor Swarm"]
    },
    "Cleric": {
        "cantrips": ["Sacred Flame", "Guidance", "Thaumaturgy"],
        1: ["Cure Wounds", "Bless", "Guiding Bolt"],
        2: ["Spiritual Weapon", "Lesser Restoration"],
        3: ["Spirit Guardians", "Revivify"],
        4: ["Death Ward", "Freedom of Movement"],
        5: ["Flame Strike", "Greater Restoration"],
        6: ["Heal", "Blade Barrier"],
        7: ["Resurrection", "Fire Storm"],
        8: ["Holy Aura", "Earthquake"],
        9: ["Mass Heal", "True Resurrection"]
    },
    "Bard": {
        "cantrips": ["Vicious Mockery", "Mage Hand", "Minor Illusion"],
        1: ["Healing Word", "Dissonant Whispers", "Charm Person"],
        2: ["Suggestion", "Invisibility"],
        3: ["Hypnotic Pattern", "Dispel Magic"],
        4: ["Greater Invisibility", "Dimension Door"],
        5: ["Mass Cure Wounds", "Dominate Person"],
        6: ["Mass Suggestion", "Otto's Irresistible Dance"],
        7: ["Forcecage", "Teleport"],
        8: ["Power Word Stun", "Glibness"],
        9: ["Power Word Heal", "Foresight"]
    },
    "Sorcerer": {
        "cantrips": ["Fire Bolt", "Mage Hand", "Minor Illusion", "Prestidigitation"],
        1: ["Shield", "Magic Missile", "Burning Hands"],
        2: ["Misty Step", "Scorching Ray"],
        3: ["Fireball", "Counterspell"],
        4: ["Greater Invisibility", "Ice Storm"],
        5: ["Cone of Cold", "Telekinesis"],
        6: ["Chain Lightning", "Disintegrate"],
        7: ["Teleport", "Finger of Death"],
        8: ["Power Word Stun", "Earthquake"],
        9: ["Meteor Swarm", "Wish"]
    },
    "Warlock": {
        "cantrips": ["Eldritch Blast", "Mage Hand", "Minor Illusion"],
        1: ["Hex", "Armor of Agathys", "Hellish Rebuke"],
        2: ["Misty Step", "Invisibility"],
        3: ["Counterspell", "Hunger of Hadar"],
        4: ["Banishment", "Shadow of Moil"],
        5: ["Hold Monster", "Synaptic Static"]
    },
    "Paladin": {
        "cantrips": [],
        1: ["Bless", "Cure Wounds", "Divine Favor"],
        2: ["Lesser Restoration", "Find Steed"],
        3: ["Aura of Vitality", "Revivify"],
        4: ["Death Ward", "Find Greater Steed"],
        5: ["Banishing Smite", "Holy Weapon"]
    },
    "Ranger": {
        "cantrips": [],
        1: ["Hunter's Mark", "Cure Wounds", "Goodberry"],
        2: ["Pass Without Trace", "Lesser Restoration"],
        3: ["Conjure Animals", "Lightning Arrow"],
        4: ["Freedom of Movement", "Stoneskin"],
        5: ["Swift Quiver", "Tree Stride"]
    }
}

species_ability_bonuses = {
    "Human": {
        "Strength": 1,
        "Dexterity": 1,
        "Constitution": 1,
        "Intelligence": 1,
        "Wisdom": 1,
        "Charisma": 1
    },
    "Elf": {
        "Dexterity": 2
    },
    "Dwarf": {
        "Constitution": 2
    },
    "Halfling": {
        "Dexterity": 2
    },
    "Half-Elf": {
        "Charisma": 2,
        "Dexterity": 1,
        "Constitution": 1
    },
    "Dragonborn": {
        "Strength": 2,
        "Charisma": 1
    },
    "Tiefling": {
        "Intelligence": 1,
        "Charisma": 2
    },
    "Gnome": {
        "Intelligence": 2
    },
    "Half-Orc": {
        "Strength": 2,
        "Constitution": 1
    }
}
