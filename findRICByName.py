import dbManipulator

name = 'Sber'

bank_RICs = dbManipulator.findRICByName(name)
print(bank_RICs)
#ban_names - список кортжей (рик, имя) всех анйденных банков
