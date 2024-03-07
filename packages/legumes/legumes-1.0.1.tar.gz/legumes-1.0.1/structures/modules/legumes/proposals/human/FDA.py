
'''
	import legumes.proposals.human.FDA as human_FDA_proposal
	proposal = human_FDA_proposal.retrieve ()
'''

def retrieve ():
    return {
		"label": "fda recommendations for humans of 4 or more years",
		
        "ingredients": [
            {
                "proposal": [
                    "2000",
                    "kcal"
                ],
                "labels": [
                    "calories"
                ]
            },
            {
                "proposal": [
                    "18",
                    "mg"
                ],
                "labels": [
                    "iron"
                ]
            },
            {
                "proposal": [
                    "150",
                    "mcg"
                ],
                "labels": [
                    "iodine"
                ]
            },
            {
                "proposal": [
                    "11",
                    "mg"
                ],
                "labels": [
                    "zinc"
                ]
            },
            {
                "proposal": [
                    "15",
                    "mg"
                ],
                "labels": [
                    "vitamin e"
                ]
            },
            {
                "proposal": [
                    "2.4",
                    "mcg"
                ],
                "labels": [
                    "vitamin b12"
                ]
            },
            {
                "proposal": [
                    "1.7",
                    "mg"
                ],
                "labels": [
                    "vitamin b6"
                ]
            },
            {
                "proposal": [
                    900,
                    "mcg"
                ],
                "labels": [
                    "vitamin a"
                ]
            },
            {
                "proposal": [
                    1.2,
                    "mg"
                ],
                "labels": [
                    "thiamin"
                ]
            },
            {
                "proposal": [
                    2300,
                    "mg"
                ],
                "labels": [
                    "sodium"
                ]
            },
            {
                "proposal": [
                    55,
                    "mcg"
                ],
                "labels": [
                    "selenium"
                ]
            },
            {
                "proposal": [
                    1.3,
                    "mg"
                ],
                "labels": [
                    "riboflavin"
                ]
            },
            {
                "proposal": [
                    5,
                    "mg"
                ],
                "labels": [
                    "pantothenic acid"
                ]
            },
            {
                "proposal": [
                    16,
                    "mg"
                ],
                "labels": [
                    "niacin"
                ],
                "notes": [
                    "milligrams of niacin equivalents"
                ]
            },
            {
                "proposal": [
                    45,
                    "mcg"
                ],
                "labels": [
                    "molybdenum"
                ]
            },
            {
                "proposal": [
                    30,
                    "mcg"
                ],
                "labels": [
                    "biotin"
                ]
            },
            {
                "proposal": [
                    2300,
                    "mg"
                ],
                "labels": [
                    "chloride"
                ]
            },
            {
                "proposal": [
                    0.9,
                    "mg"
                ],
                "labels": [
                    "copper"
                ]
            },
            {
                "proposal": [
                    35,
                    "mcg"
                ],
                "labels": [
                    "chromium"
                ]
            },
            {
                "proposal": [
                    300,
                    "mg"
                ],
                "labels": [
                    "cholesterol"
                ]
            },
            {
                "proposal": [
                    1300,
                    "mg"
                ],
                "labels": [
                    "calcium"
                ]
            },
            {
                "proposal": [
                    400,
                    "mcg"
                ],
                "labels": [
                    "folate",
                    "vitamin b9",
                    "folacin",
                    "folic acid"
                ]
            },
            {
                "proposal": [
                    420,
                    "mg"
                ],
                "labels": [
                    "magnesium"
                ]
            },
            {
                "proposal": [
                    4700,
                    "mg"
                ],
                "labels": [
                    "potassium"
                ]
            },
            {
                "proposal": [
                    90,
                    "mg"
                ],
                "labels": [
                    "vitamin c"
                ]
            },
            {
                "proposal": [
                    20,
                    "mcg"
                ],
                "labels": [
                    "vitamin d"
                ]
            },
            {
                "proposal": [
                    120,
                    "mcg"
                ],
                "labels": [
                    "vitamin k"
                ]
            },
            {
                "proposal": [
                    1250,
                    "mg"
                ],
                "labels": [
                    "phosphorous"
                ]
            },
            {
                "proposal": [
                    2.3,
                    "mg"
                ],
                "labels": [
                    "manganese"
                ]
            },
            {
                "proposal": [
                    50,
                    "g"
                ],
                "labels": [
                    "protein"
                ]
            },
            {
                "proposal": [
                    78,
                    "g"
                ],
                "includes": [
                    {
                        "proposal": [
                            20,
                            "g"
                        ],
                        "labels": [
                            "saturated fat"
                        ]
                    },
                    {
                        "proposal": [],
                        "labels": [
                            "polyunsaturated fat"
                        ]
                    },
                    {
                        "proposal": [
                            0,
                            "g"
                        ],
                        "labels": [
                            "trans fat"
                        ]
                    }
                ],
                "labels": [
                    "total fat",
                    "fat"
                ]
            },
            {
                "proposal": [
                    275,
                    "g"
                ],
                "includes": [
                    {
                        "proposal": [
                            28,
                            "g"
                        ],
                        "labels": [
                            "fiber",
                            "dietary fiber"
                        ]
                    },
                    {
                        "proposal": [
                            50,
                            "g"
                        ],
                        "labels": [
                            "sugars",
                            "total sugars"
                        ]
                    }
                ],
                "labels": [
                    "total carbohydrates",
                    "carbohydrates"
                ]
            },
            {
                "proposal": [
                    2300,
                    "mg"
                ],
                "labels": [
                    "sodium"
                ]
            }
        ],
        
        "limiters": [
            {
                "includes": [
                    "human"
                ],
                "label": "species"
            },
            {
                "includes": [
                    [
                        "4",
                        "eternity"
                    ]
                ],
                "kind": "slider--integer",
                "label": "age"
            },
            {
                "includes": [
                    "pregnant",
                    "breast feeding"
                ],
                "label": "exclusions"
            }
        ],
        "sources": [
            "https://www.fda.gov/food/new-nutrition-facts-label/daily-value-new-nutrition-and-supplement-facts-labels",
            "https://www.fda.gov/media/99069/download",
            "https://www.fda.gov/media/99059/download"
        ]
    }
