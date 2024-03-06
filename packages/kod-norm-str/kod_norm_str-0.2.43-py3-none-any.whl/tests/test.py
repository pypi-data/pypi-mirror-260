from kod_normalize.normalize import normalize


# # #
print("Test Accents ... ")
print(normalize("Ryuichi Sakamoto - Sabiá"))  # no accents present (decomposed)
print(normalize("Ryuichi Sakamoto - Sabià"))  # accent is present but not the same, but same letter character
# #
print("Test Differences ... ")
print(normalize("Bizzy D - Symphony No.8 in F Major Op.93:Ⅳ (Remix)"))
print(normalize("Bizzy D - Symphony No.8 in F Major Op.93:Ⅱ (Remix)"))
#
#
print("Test Same ... ")
print(normalize("Leyla McCalla - Bon Appétit Messieurs"))  # this will always have mod
print(normalize("Leyla McCalla - Bon Appétit Messieurs"))  # this keeps failing
#
#
print("Test Same ... ")
print(normalize("Chlöe - How Does It Feel"))  # this will always have mod
print(normalize("Chlöe - How Does It Feel"))  # this keeps failing
#
#
print("Test Same ... ")
print(normalize("José José - El Amar y el Querer"))  # this will always have mod
print(normalize("José José - El Amar y el Querer"))  # this keeps failing
#

print("Test Same ... bb")
print(normalize("Bad Bunny - DÁKITI"))
print(normalize("Bad Bunny - DÁKITI"))

print("Test Same ... ")
print(normalize("Kraftwerk - Radioactivity (François Kervorkian 12” Remix)"))
print(normalize("Kraftwerk - Radioactivity (François Kervorkian 12” Remix)"))

print("Test Same ... ")
print(normalize("Öwnboss - Move Your Body"))
print(normalize("Öwnboss - Move Your Body"))

print("Test Same ... ")
print(normalize("Múm - Behind Two Hills…A Swimming Pool"))
print(normalize("Múm - Behind Two Hills…A Swimming Pool"))

print("Test Same ... ")
print(normalize("Psy - Gangnam Style (강남스타일)"))
print(normalize("Psy - Gangnam Style (강남스타일)"))

print("Test Same ... ")
print(normalize("Derya Yildirim & Grup Şimşek - Darıldım Darıldım"))
print(normalize("Derya Yildirim & Grup Şimşek - Darıldım Darıldım"))

print("Test Same ... ")
print(normalize("Alex Acuña - Chuncho (feat. Otmaro Ruiz, John Peńa, Lorenzo Ferrero, Ramón Stagnaro, Diana Acuńa & Regina Acuńa)"))
print(normalize("Alex Acuña - Chuncho (feat. Otmaro Ruiz, John Peńa, Lorenzo Ferrero, Ramón Stagnaro, Diana Acuńa & Regina Acuńa)"))


print("Test Same ... ")
print(normalize("CRÜPO - Feel Like Dancing"))
print(normalize("CRÜPO - Feel Like Dancing"))

print("Test Same ... ")
print(normalize("GORAN BREGOVIĆ - Duj Duj"))
print(normalize("GORAN BREGOVIĆ - Duj Duj"))

print("Test Same ... ")
print(normalize("Tinariwen - À l’Histoire"))
print(normalize("Tinariwen - À l’Histoire"))


print("Test Same ... ")
print(normalize("Jedi Mind Tricks - SÃ©ance Of Shamans"))
print(normalize("Jedi Mind Tricks - SÃ©ance Of Shamans"))

print("Test Same ... ")
print(normalize("RÜFÜS DU SOL - On My Knees (Cassian Remix)"))
print(normalize("RÜFÜS DU SOL - On My Knees (Cassian Remix)"))