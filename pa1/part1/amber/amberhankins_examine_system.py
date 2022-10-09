#Amber Hankins  - 2/16/22
#CS446 PA 1     - Reading from /proc


#open text file
try:
    text = open('amberhankins_systemDetails.txt','w+')
except IOError as e:
    print('Error: could not open text file.')
    exit

#proc/cpuinfo
try:
    cpu = open('/proc/cpuinfo','r')
except IOError as e:
    print('Error: could not open file cpuinfo.')
    exit

for line in cpu:
    for word in line.split():
        if word == 'name':
            model = line

cpu.close()
text.write('1. CPU type and model:\n'+model)

#proc/version
try:
    version = open('/proc/version','r')
except IOError as e:
    print('Error: could not open file version.')
    exit

for line in version:
    for phrase in line.split('('):
        for word in phrase.split():
            if word == 'version':
                vers = phrase+'\n'

version.close()
text.write('\n2. Kernel version details:\n'+vers)

#proc/uptime
try:
    uptime = open('/proc/uptime','r')
except IOError as e:
    print('Error: could not open file uptime.')
    exit

for line in uptime:
    lastboot = line

uptime.close()
text.write('\n3. Amount of time since last boot:\n'+lastboot)

#proc/stat
try:
    stat = open('/proc/stat','r')
except IOError as e:
    print('Error: could not open file stat.')
    exit

for line in stat:
    for word in line.split():
        if word == 'btime':
            time = line
        if word == 'processes':
            proc = line


stat.close()
text.write('\n4. Time that the system was last booted:\n'+time)

#/proc/diskstats
text.write('\n5. Number of disk requests made:\n')

try:
    disk = open('/proc/diskstats','r')
except IOError as e:
    print('Error: could not open file diskstats.')
    exit

for line in disk:
    for word in line.split():
        if word == '7':
            text.write(line)

disk.close()
text.write('\n6. Number of processes created since last boot:\n'+proc)

#close text file
text.close()


        
