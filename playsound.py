def playsound(m):
    #rm_define.media_sound_solmization_1A,
    # notes=[rm_define.media_sound_solmization_1A,
    #     rm_define.media_sound_solmization_1B,
    #     rm_define.media_sound_solmization_1C,
    #     rm_define.media_sound_solmization_1D,
    #     rm_define.media_sound_solmization_1E,
    #     rm_define.media_sound_solmization_1F,
    #     rm_define.media_sound_solmization_1G,
    #     rm_define.media_sound_solmization_2A,
    #     rm_define.media_sound_solmization_2B,
    #     rm_define.media_sound_solmization_2C,
    #     rm_define.media_sound_solmization_2D,
    #     rm_define.media_sound_solmization_2E,
    #     rm_define.media_sound_solmization_2F,
    #     rm_define.media_sound_solmization_2G,
    #     rm_define.media_sound_solmization_3A,
    #     rm_define.media_sound_solmization_3B,
    #     rm_define.media_sound_solmization_3C,
    #     rm_define.media_sound_solmization_3D,
    #     rm_define.media_sound_solmization_3E,
    #     rm_define.media_sound_solmization_3F,
    #     rm_define.media_sound_solmization_3G
    #     ]

    notes = ["rm_define.media_sound_solmization_1A",
             "rm_define.media_sound_solmization_1B",
             "rm_define.media_sound_solmization_1C",
             "rm_define.media_sound_solmization_1D",
             "rm_define.media_sound_solmization_1E",
             "rm_define.media_sound_solmization_1F",
             "rm_define.media_sound_solmization_1G",
             "rm_define.media_sound_solmization_2C",
             "rm_define.media_sound_solmization_2D",
             "rm_define.media_sound_solmization_2E",
             "rm_define.media_sound_solmization_2F",
             "rm_define.media_sound_solmization_2G",
             "rm_define.media_sound_solmization_2A",
             "rm_define.media_sound_solmization_2B",
             "rm_define.media_sound_solmization_3A",
             "rm_define.media_sound_solmization_3B",
             "rm_define.media_sound_solmization_3C",
             "rm_define.media_sound_solmization_3D",
             "rm_define.media_sound_solmization_3E",
             "rm_define.media_sound_solmization_3F",
             "rm_define.media_sound_solmization_3G"
             ]
    
    melody=[]
    for i in m:
        if i.isalpha():
            if i.islower():  #小写
                melody.append(int(ord(i)) - 97)
            else:
                melody.append(int(ord(i)) - 65+14)
        else:
            if int(i)==0:
                melody.append(-1)
            else:
                melody.append(int(ord(i)-49)+7)

    for i in melody:
        if i<0:
            print("0")
        else:
            print(notes[i])

m="565432111ggg13C76355500"
playsound(m)