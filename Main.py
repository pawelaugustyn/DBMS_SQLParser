from Parser import Parser


if __name__ == "__main__":
    parser = Parser()
    parser.parse_query("""select r.roomNo, r.type, r.price
                       from Room r, Hotel h, Booking b
                       where r.roomNo = 5 and b.hotelNo = h.hotelNo""")

    parser.parse_query("""select g.guestNo, g.guestName from Room r, Hotel h, Booking b, Guest g
                          where h.hotelNo = 5 and g.guestNo = b.guestNo and h.hotelNo = r.hotelNo
                          and h.hotelName = 'Grosvenor Hotel'
        """)