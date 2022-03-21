class StdoutPrinter:
    """
    Prints results of a recommender script to standard output in a formatted
    way.
    """

    # ASCII text edit symbols
    PINK = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self, limit, verbose):
        self.limit = limit
        self.verbose = verbose
        self.__headers = ["IP ADDRESS", "DOMAIN(S)", "CONTACT(S)", "RISK"]
        self.__widths = [20, 0, 0, 10]

    def print_attacked_host(self, host):
        """
        Prints information about attacked host.
        :param host: Attacked host
        :return: None
        """
        print(self.BLUE + self.BOLD + "ATTACKED HOST:" + self.END)
        print(host)
        print()

    def print_number_of_hosts(self, number_of_hosts, max_distance):
        """
        Prints information about number of nearby hosts find and number
        of hosts actually given to stdout (in case limit option is used.
        :param number_of_hosts: Number of hosts found
        :param max_distance: Maximum distance in graph used during BFS search
        :return: None
        """

        print(self.BLUE +
              f"Found {number_of_hosts} hosts to maximum distance of "
              f"{max_distance}:")

        # Show how much hosts is actually being printed (defined by limit
        # given as a option)
        if self.limit is not None and self.limit < number_of_hosts:
            print(self.BLUE + f"Displaying {self.limit} hosts.")
        print()

    def print_host_list(self, host_list):
        """
        Prints given host list to stdout formatted in a table.
        :param host_list: List of hosts to print
        :return: None
        """

        # Get shortened list if limit is given
        list_slice = host_list[:self.limit]

        # Verbose print
        if self.verbose:
            self.__headers.append("SIMILARITIES")
            self.__widths.append(0)

        # Calculate width for variable size columns
        self.__calc_column_widths(host_list)

        table_color = self.YELLOW

        # Print table header
        self.__print_host_list_header(self.BLUE)

        # Print table
        self.__print_horizontal_separator(table_color)

        for host in list_slice:
            self.__print_host_in_table(host, table_color)
            self.__print_horizontal_separator(self.YELLOW)

    def __calc_column_widths(self, host_list):
        """
        Calculates width of all columns - it finds widest value in each
        column and adds 2 (value plus two spaces).
        :param host_list: List of hosts for printing
        :return: None
        """

        len_contact = 0
        len_domain = 0
        len_warning = 0

        for host in host_list:
            # Domain
            current_longest = len(max(host.domains, key=lambda x: len(x)))
            if current_longest > len_domain:
                len_domain = current_longest

            # Contact
            current_longest = len(max(host.contacts, key=lambda x: len(x)))
            if current_longest > len_contact:
                len_contact = current_longest

            # Warnings
            if self.verbose:
                if host.warnings:
                    current_longest = \
                        len(str(max(host.warnings, key=lambda x: len(str(x)))))
                    if current_longest > len_warning:
                        len_warning = current_longest

        # Set widths (+ 2 -> margin from a table, looks better)
        self.__widths[1] = len_domain + 2
        self.__widths[2] = len_contact + 2
        if self.verbose:
            self.__widths[4] = len_warning + 2

    def __print_horizontal_separator(self, color):
        """
        Prints horizontal separator of a table in given color.
        :param color: Color of a separator as ASCII edit symbol
        :return: None
        """
        print(color, end="")
        for width in self.__widths:
            print(f"+{width * '-'}", end="")
        print("+" + self.END)

    def __print_host_list_header(self, color):
        """
        Prints header of host list in given color.
        :param color: Header color as ASCII edit symbol
        :return: None
        """
        print(color + self.BOLD, end="")
        for header, width in zip(self.__headers, self.__widths):
            print(" " + str.center(header, width), end="")
        print(self.END)

    def __print_host_in_table(self, host, color):
        """
        Prints one host in a result table in given color.
        :param host: Host object to be printed
        :param color: Color of a row with host as ASCII edit symbol
        :return: None
        """

        print(color + "|", end="")

        print_items = [str(host.ip), host.domains[0], host.contacts[0],
                       str(round(host.risk, 4))]

        if self.verbose and host.warnings:
            print_items.append(str(host.warnings[0]))
        elif self.verbose:
            print_items.append("")

        for item, width in zip(print_items, self.__widths):
            print(self.YELLOW + str.center(item, width) + "|", end="")

        # Print domains and warnings, which can take more rows
        if len(host.domains) > 1 or len(host.contacts) or \
                (len(host.warnings) > 1 and self.verbose):
            print()

            # One row is already printed -> minus one
            if self.verbose:
                rows = max(max(len(host.domains), len(host.warnings)),
                           len(host.contacts)) - 1
            else:
                rows = max(len(host.domains), len(host.contacts)) - 1

            for i in range(1, rows + 1):
                # IP
                print("|" + self.__widths[0] * " " + "|", end="")

                # DOMAIN
                if i < len(host.domains):
                    print(str.center(host.domains[i], self.__widths[1]) + "|",
                          end="")
                else:
                    print(self.__widths[1] * " " + "|", end="")

                # CONTACT
                if i < len(host.contacts):
                    print(str.center(host.contacts[i], self.__widths[2]) + "|",
                          end="")
                else:
                    print(self.__widths[2] * " " + "|", end="")

                # RISK
                print(self.__widths[3] * " " + "|", end="")

                # WARNINGS
                if self.verbose and i < len(host.warnings):
                    print(str.center(str(host.warnings[i]),
                                     self.__widths[4]) + "|")
                elif self.verbose:
                    print(self.__widths[4] * " " + "|")
                else:
                    print()
        else:
            print()

        print(self.END, end="")