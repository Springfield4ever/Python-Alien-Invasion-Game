import cx_Freeze

executables = [cx_Freeze.Executable(script="options.py",icon= 'icon.ico',targetName= 'Alien Invasion.exe', base= 'Win32GUI')]

cx_Freeze.setup(
    name="Alien Invasion",
    options={"build_exe": {"packages":["pygame", "pygame.sprite" , "time", "tkinter", "tkinter.messagebox" ,"os", "sys" ,"json", "webbrowser"],
                           "include_files":[
                               ".\\fonts\\ARCADE_I.TTF",
                               ".\\fonts\\ARCADE_N.TTF",
                               ".\\fonts\\ARCADE_R.TTF",
                               ".\\images\\frame_apngframe1.png",
                               ".\\images\\frame_apngframe2.png",
                               ".\\images\\frame_apngframe3.png",
                               ".\\images\\frame_apngframe4.png",
                               ".\\images\\frame_apngframe5.png",
                               ".\\images\\frame_apngframe6.png",
                               ".\\images\\pygame_logo.png",
                               ".\\images\\ship.png",
                               ".\\sounds\\fail.wav",
                               ".\\sounds\\laser.wav",
                               ".\\sounds\\level_up.wav",
                               ".\\sounds\\main_title.mp3",
                               ".\\sounds\\score.wav"
                                ]}},
    executables = executables

    )