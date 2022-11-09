from cx_Freeze import setup, Executable

# For Windows
setup(
    name="Jimanji_Rush",
    version="1.0.0",
    description="Pygame Game",
    author="ESIEE-IT",
    author_email="arthur.pellegrini@edu.esiee-it.fr",
    py_modules=[],
    options={'build_exe': {'include_files': [  # [SOURCE_DIR, DESTINATION_DIR],
        ['assets/background', 'assets/background'],
        ['assets/blue_gem', 'assets/blue_gem'],
        ['assets/cannonball', 'assets/cannonball'],
        ['assets/coin', 'assets/coin'],
        ['assets/egg', 'assets/egg'],
        ['assets/green_gem', 'assets/green_gem'],
        ['assets/heart', 'assets/heart'],
        ['assets/iddle', 'assets/iddle'],
        ['assets/medal', 'assets/medal'],
        ['assets/player', 'assets/player'],
        ['assets/ruby', 'assets/ruby'],
        ['assets/skull', 'assets/skull'],
        ['assets/star', 'assets/star'],
        ['assets/', 'assets/'],
        ['data/', 'data/'],
    ],
        'packages': ['pygame'],
    }
    },
    executables=[
        Executable(
            script="main.py",
            icon="icon.ico",
            base="Win32GUI",
            target_name="Jimanji_Rush.exe"
        )
    ]
)
