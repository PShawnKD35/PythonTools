import iDeskAPI
import getpass

print("Please enter your iDesk user name:")
username = input()
password = getpass.getpass()
idesk = iDeskAPI.iDesk(username,password)
# idesk.BulkGetInfo(idesk.getFullName, "network ID")
idesk.BulkGetInfo(idesk.getOwner, "Incident Number")