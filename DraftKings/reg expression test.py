import re
line = "C Vincent Trocheck C Jack Roslovic W Oliver Bjorkstrand W Teuvo Teravainen UTIL Cam Atkinson W Jesperi Kotkaniemi D Jake Bean D Ryan Ellis G Frederik Andersen"

startReg = re.compile('\s(C|C|W|UTIL|D|G)\s')

line2 = startReg.split(line)

print(line2)

# middleReg = re.compile('\s[CWDG]\s')
#
# util = re.compile('\sUTIL\s')
#
# for x in middleReg.split(line2[1]):\
#     print(util.split(x))