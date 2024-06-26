import csv
from pyVmomi import vmodl, vim
from tools import cli, service_instance  # Import external modules for parsing command line arguments and connecting to vCenter

def print_vm_info_to_csv(virtual_machine, csv_writer):
    """
    Extracts and writes information to the provided CSV writer.
    """
    summary = virtual_machine.summary

    # Check if guestFullName exists and is not blank 
    if summary.config.guestFullName is not None and summary.config.guestFullName != "":
        # Check for "Red Hat" or "RHEL" in guestFullName, exclude "TMPL" in the name
        if ("Red Hat" in summary.config.guestFullName or "RHEL" in summary.config.guestFullName) and "TMPL" not in summary.config.name:
            csv_writer.writerow([summary.config.name, summary.config.guestFullName, summary.guest.ipAddress])

def main():
    """
    Simple command-line program for listing VM information in a CSV file.
    """

    parser = cli.Parser()  # Create a command-line argument parser
    parser.add_argument('-O', '--output', required=True, help='Path to the output CSV file')
    args = parser.get_args()  # Parse the command-line arguments
    si = service_instance.connect(args)  # Connect to the vCenter server

    try:
        content = si.RetrieveContent()  # Get the root content object from vCenter

        container = content.rootFolder  # Get the root folder
        view_type = [vim.VirtualMachine]  # Specify we want to view VirtualMachine objects
        recursive = True  # Search recursively through the inventory
        container_view = content.viewManager.CreateContainerView(container, view_type, recursive) 
        children = container_view.view  # Get the list of virtual machines

        with open(args.output, 'w', newline='') as csvfile: 
            csv_writer = csv.writer(csvfile)  # Create a CSV writer object
            csv_writer.writerow(['VM Name', 'Guest OS', 'IP Address'])  # Write the header row
            for child in children:  # Iterate over each virtual machine
                print_vm_info_to_csv(child, csv_writer)  # Process VM information

    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)  # Handle errors during API calls 
        return -1  # Indicate failure

    return 0  # Indicate success 

# Start program
if __name__ == "__main__":
    main()
