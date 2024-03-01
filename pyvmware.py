import csv
from pyVmomi import vmodl, vim
from tools import cli, service_instance


def print_vm_info_to_csv(virtual_machine, csv_writer):
    """
    Extracts and writes information to the provided CSV writer.
    """
    summary = virtual_machine.summary

    # Check for None or empty string in guestFullName
    if summary.config.guestFullName is not None and summary.config.guestFullName != "":
        if ("Red Hat" in summary.config.guestFullName or "RHEL" in summary.config.guestFullName) and "TMPL" not in summary.config.name:
            csv_writer.writerow([summary.config.name, summary.config.guestFullName, summary.guest.ipAddress])


def main():
    """
    Simple command-line program for listing VM information in a CSV file.
    """

    parser = cli.Parser()
    parser.add_custom_argument('-O', '--output', required=True,
                        help='Path to the output CSV file')
    args = parser.get_args()
    si = service_instance.connect(args)

    try:
        content = si.RetrieveContent()

        container = content.rootFolder
        view_type = [vim.VirtualMachine]
        recursive = True
        container_view = content.viewManager.CreateContainerView(
            container, view_type, recursive)

        children = container_view.view

        with open(args.output, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['VM Name', 'Guest OS', 'IP Address'])
            for child in children:
                print_vm_info_to_csv(child, csv_writer)

    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1

    return 0


# Start program
if __name__ == "__main__":
    main()
