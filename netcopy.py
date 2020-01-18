import netmiko,argparse,csv

from getpass import getpass  

 

 

 

def upload (args,rl):

                print ('Uploading license files')

                for row in rl:

                                print (row)

                               

                                net_connect = netmiko.ConnectHandler(device_type='cisco_ios', ip=row['DEVICE'], username=args.username, password=args.password, ssh_config_file='~/.ssh/config.bak', verbose=True)

                                net_connect.config_mode() 

                                net_connect.send_command('ip scp server enable')

                                net_connect.exit_config_mode()

                                transfer_dict = netmiko.file_transfer (net_connect, source_file=row['LICENSE'], direction='put', dest_file=row['LICENSE'], file_system='bootflash:')

                                net_connect.config_mode()

                                net_connect.send_command('no ip scp server enable')

                                net_connect.exit_config_mode()

                                print (transfer_dict)

                print ('License upload completed')

 

def apply_lic(args,rl):

                print ('Applying license files')

                for row in rl:

                                print (row)

 

                                net_connect = netmiko.ConnectHandler(device_type='cisco_ios', ip=row['DEVICE'], username=args.username, password=args.password, ssh_config_file='~/.ssh/config.bak', verbose=True)

                                result = net_connect.send_command('license install bootflash:{}'.format(row['LICENSE']))

                                print (result)

                print ('License apply completed')

 

 

def check (args,rl):

                print ('Running checks')

                fields = ['Device', 'Command', 'Output']

                with open(args.output_file,'w') as csvfile:

                                csvwriter = csv.writer(csvfile)

                                csvwriter.writerow(fields)

                                for row in rl:

                                                net_connect = netmiko.ConnectHandler(device_type='cisco_ios', ip=row['DEVICE'], username=args.username, password=args.password, ssh_config_file='~/.ssh/config.bak', verbose=True)

                                                ip = row['DEVICE']

                                                result = net_connect.send_command('show license')

                                                csvwriter.writerow([ip,'show license',result])

                                                result = net_connect.send_command('show run | sec license')

                                                csvwriter.writerow([ip,'show run | sec license',result])

                                                result = net_connect.send_command('show platform hardware throughput level')

                                                csvwriter.writerow([ip,'show platform hardware throughput level',result])

 

def main():

                creds = argparse.ArgumentParser(description='Script to upload and apply Cisco lic files')

                creds.add_argument('-i','--hosts', help='CSV format host_ip_address,lic_file_name', required=True)

                creds.add_argument('-l','--username', help='TACACS or local username', required=True)

                creds.add_argument('-p','--password', help='TACACS or local password', required=True)

                creds.add_argument('-u','--upload', action='store_true', default=False, help='Upload only')

                creds.add_argument('-a','--apply_lic', action='store_true', default=False, help='Apply only')

                creds.add_argument('-c','--check', action='store_true', default=False, help='Check only')

                creds.add_argument('-o','--output_file', help='File path for logs ')

                args = creds.parse_args()

                rl = []

                with open (args.hosts) as hf:

                                rd = csv.DictReader(hf)

                                for row in rd:

                                                rl.append(row)

                for row in rl:

                                print (row)

                if args.check:

                                check(args,rl)                    

                if args.upload:

                                upload(args,rl)

                if args.apply_lic:

                                apply_lic(args,rl)                              

                if args.check:

                                check(args,rl)

               

 

if __name__ == "__main__":

    main()
