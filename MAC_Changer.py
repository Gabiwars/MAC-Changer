import subprocess
import optparse #Allow us to get arguments from the user
import re #Regex

def get_arguments():
    parser = optparse.OptionParser()  # Object that can handle unser input using arguments
    parser.add_option('-i', '--interface', dest='interface', help='Interface to change its MAC address')  # Teaching parser that the user can enter 2 options (-i or --interface) and it will be stored in 'interface'. Help is to explain what the argument is
    parser.add_option('-m', '--mac', dest='new_mac', help='New MAC address')  # Teaching parser that the user can enter 2 options (-m or --mac) and it will be stored in 'new_mac'. Help is to explain what the argument is
    (options, arguments) = parser.parse_args() #Return to the place where this function is being called from  # Allows the object to understand what the user entered and hadles it
    if not options.interface: #If options.interface does not hold a value
        parser.error('Please specify an interface, use -- help for more info') #It will display the message and exit

    elif not options.new_mac: #If options.new_mac does not hold a value
        parser.error('Please specify a new MAC, use --help for more info')
    return options #If everything is correct


def change_mac(interface, new_mac):
    subprocess.run(['ifconfig', interface, 'down'])  # Put the interface down
    subprocess.run(['ifconfig', interface, 'hw', 'ether', new_mac]) # Mudar o MAC para oq a gente quiser, (ether eh o MAC)
    subprocess.run(['ifconfig', interface, 'up'])  # Put the interface up again

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface])  # To return the output
    search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', str(ifconfig_result))  # To get the search
    if search_result:
        return search_result.group(0)
    else:  # If there is not a MAC
        print('Sorry, I could not read MAC address')

options = get_arguments()
current_mac = get_current_mac(options.interface)
print('Current MAC: ' + str(current_mac)) #Transforma current_mac em string
change_mac(options.interface, options.new_mac)
if current_mac == options.new_mac:
    print('MAC address did not change ' + str(current_mac))
    print('Please enter a different MAC address')
else:
    print('Changing MAC address for ' + (options.interface) + ' to ' + (options.new_mac))
    print('MAC address successfully changed to ' + options.new_mac)