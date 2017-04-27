import re


class NoKeywordsInQuery(Exception):
    pass


class NotSupportedPredicate(Exception):
    pass


class Parser(object):
    def __init__(self):
        pass

    def parse_query(self, query):
        if not self._is_string(query):
            raise TypeError("Not a string")
        if not self._keywords_in_query(query):
            raise NoKeywordsInQuery


        # print("\u22c8")

        self._print_data(query)
        print("")

    def _print_data(self, query):
        select, from_part, where, query_show = self._get_content(query)

        print("Prompted query:\n" + query_show)

        table_names = self._get_table_names(from_part)
        tables = ""
        separator = ""
        spaces = " " * (len(table_names)) * 2
        for table, shortcut in table_names:
            tables += separator + table
            separator = " x "


        where_spaces_amount = " " * (len(select)+4)
        where_spaces = re.sub(" and ", " and\n{}".format(where_spaces_amount), where)

        print("\nRelational algebra form:")
        print("\N{GREEK CAPITAL LETTER PI}" + " "+ " "*len(select) +
              " \N{GREEK SMALL LETTER SIGMA} " + " "+" "*int(len(where)/(where_spaces.count("\n")+1)) +
              "(" + tables + ")")
        print(" " + select + " "*3 + where_spaces)
        print("\nTree")
        print(spaces[:len(spaces) - 1] + "\N{GREEK CAPITAL LETTER PI}\n" + spaces + select)
        print(spaces[:len(spaces) - 1] + "|")
        print(spaces[:len(spaces) - 1] + "\N{GREEK SMALL LETTER SIGMA}\n" + spaces + where)
        print(spaces[:len(spaces) - 1] + "|\n" + spaces[:len(spaces) - 1] + "x")
        for i in range(0, len(table_names) - 1):
            last_table = table_names.pop()
            if len(table_names) > 1:
                left = "x"
            else:
                left = table_names[0][1]
            print(spaces[:len(spaces) - 2 - i * 2] + "/" + " " + "\\")
            print(spaces[:len(spaces) - 3 - i * 2] + left + "   " + last_table[1])

    @staticmethod
    def _get_content(query):
        query = re.sub("SELECT", "select", query)
        query = re.sub("FROM", "from", query)
        query = re.sub("WHERE", "where", query)
        query = re.sub(" +", " ", query)
        query = re.sub("\n", "", query)
        query = re.sub("from", "\nfrom", query)
        query = re.sub("where", "\nwhere", query)
        query_show = query

        query = query.splitlines()
        for i in range(0, len(query)):
            query[i] = query[i].strip(' \t\n\r')

        select = re.sub("select ", "", query[0])
        from_part = re.sub("from ", "", query[1])
        where = re.sub("where ", "", query[2])
        return select, from_part, where, query_show

    @staticmethod
    def _get_table_names(from_part):
        from_part = re.sub(",[ ]+", ",", from_part)
        list_f = from_part.split(",")
        output = []
        for elem in list_f:
            elem = elem.split(" ")
            output.append((elem[0], elem[1]))
        return output

    @staticmethod
    def _is_string(query):
        return isinstance(query, str)

    @staticmethod
    def _keywords_in_query(query):
        if "SELECT" not in query.upper():
            return False
        if "FROM" not in query.upper():
            return False
        return True
