import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


# ============================================================
# BUS RESERVATION SYSTEM
# Single Python Script
# ============================================================

class BusReservationSystem:

    def __init__(self, root):
        self.root = root
        self.root.title("🚌 Bus Reservation System")
        self.root.geometry("1050x700")
        self.root.minsize(900, 600)
        self.root.configure(bg="#F4F7FB")

        # Database
        self.db = sqlite3.connect("bus_reservation.db")
        self.cursor = self.db.cursor()

        self.create_database()
        self.insert_default_buses()

        self.selected_bus = None
        self.selected_seat = None

        self.home_screen()

    # ========================================================
    # DATABASE
    # ========================================================

    def create_database(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS buses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bus_number TEXT UNIQUE,
                bus_name TEXT,
                source TEXT,
                destination TEXT,
                departure TEXT,
                fare REAL,
                total_seats INTEGER
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id TEXT UNIQUE,
                passenger_name TEXT,
                phone TEXT,
                bus_number TEXT,
                source TEXT,
                destination TEXT,
                travel_date TEXT,
                seat_number INTEGER,
                fare REAL,
                booking_time TEXT
            )
        """)

        self.db.commit()

    def insert_default_buses(self):

        buses = [
            (
                "BUS101",
                "Express Travels",
                "Hyderabad",
                "Vijayawada",
                "08:00 AM",
                550,
                20
            ),
            (
                "BUS102",
                "City Express",
                "Vijayawada",
                "Hyderabad",
                "09:30 AM",
                550,
                20
            ),
            (
                "BUS103",
                "Super Deluxe",
                "Visakhapatnam",
                "Vijayawada",
                "07:00 AM",
                650,
                20
            ),
            (
                "BUS104",
                "Royal Travels",
                "Vijayawada",
                "Visakhapatnam",
                "10:00 AM",
                650,
                20
            ),
            (
                "BUS105",
                "Green Line",
                "Hyderabad",
                "Visakhapatnam",
                "06:30 AM",
                900,
                20
            )
        ]

        for bus in buses:
            try:
                self.cursor.execute("""
                    INSERT INTO buses
                    (bus_number, bus_name, source, destination,
                     departure, fare, total_seats)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, bus)
            except sqlite3.IntegrityError:
                pass

        self.db.commit()

    # ========================================================
    # COMMON UI
    # ========================================================

    def clear_screen(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    def header(self, title, subtitle=""):

        frame = tk.Frame(
            self.root,
            bg="#2563EB",
            height=95
        )

        frame.pack(fill="x")
        frame.pack_propagate(False)

        tk.Label(
            frame,
            text=title,
            bg="#2563EB",
            fg="white",
            font=("Arial", 25, "bold")
        ).pack(pady=(15, 0))

        if subtitle:
            tk.Label(
                frame,
                text=subtitle,
                bg="#2563EB",
                fg="white",
                font=("Arial", 10)
            ).pack()

    def button(
        self,
        parent,
        text,
        command,
        color="#2563EB",
        width=18
    ):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=width,
            height=2
        )

    # ========================================================
    # HOME SCREEN
    # ========================================================

    def home_screen(self):

        self.clear_screen()

        self.header(
            "🚌 BUS RESERVATION SYSTEM",
            "Book your journey quickly and easily"
        )

        main = tk.Frame(
            self.root,
            bg="#F4F7FB"
        )

        main.pack(
            expand=True,
            fill="both"
        )

        tk.Label(
            main,
            text="🚌",
            bg="#F4F7FB",
            font=("Arial", 65)
        ).pack(pady=(35, 5))

        tk.Label(
            main,
            text="Welcome!",
            bg="#F4F7FB",
            fg="#172033",
            font=("Arial", 30, "bold")
        ).pack()

        tk.Label(
            main,
            text="Plan your journey and reserve your seat",
            bg="#F4F7FB",
            fg="#64748B",
            font=("Arial", 13)
        ).pack(pady=5)

        card = tk.Frame(
            main,
            bg="white",
            padx=40,
            pady=30
        )

        card.pack(pady=25)

        self.button(
            card,
            "🔍 SEARCH BUSES",
            self.search_buses,
            "#2563EB",
            25
        ).pack(pady=8)

        self.button(
            card,
            "🎫 MY RESERVATIONS",
            self.view_bookings,
            "#16A34A",
            25
        ).pack(pady=8)

        self.button(
            card,
            "❌ CANCEL RESERVATION",
            self.cancel_booking,
            "#DC2626",
            25
        ).pack(pady=8)

        self.button(
            main,
            "🚪 EXIT",
            self.close_application,
            "#172033",
            15
        ).pack(pady=5)

    # ========================================================
    # SEARCH BUSES
    # ========================================================

    def search_buses(self):

        self.clear_screen()

        self.header(
            "🔍 Search Buses",
            "Select your source and destination"
        )

        form = tk.Frame(
            self.root,
            bg="#F4F7FB"
        )

        form.pack(pady=25)

        tk.Label(
            form,
            text="From:",
            bg="#F4F7FB",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=0, padx=10)

        source = ttk.Combobox(
            form,
            width=25,
            state="readonly"
        )

        sources = self.cursor.execute(
            "SELECT DISTINCT source FROM buses"
        ).fetchall()

        source["values"] = [x[0] for x in sources]
        source.grid(row=0, column=1, padx=10)

        tk.Label(
            form,
            text="To:",
            bg="#F4F7FB",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=2, padx=10)

        destination = ttk.Combobox(
            form,
            width=25,
            state="readonly"
        )

        destinations = self.cursor.execute(
            "SELECT DISTINCT destination FROM buses"
        ).fetchall()

        destination["values"] = [x[0] for x in destinations]
        destination.grid(row=0, column=3, padx=10)

        results_frame = tk.Frame(
            self.root,
            bg="white"
        )

        results_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=15
        )

        columns = (
            "bus",
            "name",
            "source",
            "destination",
            "departure",
            "fare",
            "seats"
        )

        tree = ttk.Treeview(
            results_frame,
            columns=columns,
            show="headings",
            height=12
        )

        headings = [
            ("bus", "Bus No."),
            ("name", "Bus Name"),
            ("source", "From"),
            ("destination", "To"),
            ("departure", "Departure"),
            ("fare", "Fare"),
            ("seats", "Seats")
        ]

        for column, heading in headings:

            tree.heading(
                column,
                text=heading
            )

            tree.column(
                column,
                width=120
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        def search():

            for item in tree.get_children():
                tree.delete(item)

            src = source.get()
            dst = destination.get()

            if not src or not dst:

                messagebox.showwarning(
                    "Selection Required",
                    "Please select source and destination."
                )

                return

            buses = self.cursor.execute("""
                SELECT
                    b.bus_number,
                    b.bus_name,
                    b.source,
                    b.destination,
                    b.departure,
                    b.fare,
                    b.total_seats -
                    (
                        SELECT COUNT(*)
                        FROM bookings bk
                        WHERE bk.bus_number = b.bus_number
                    )
                FROM buses b
                WHERE b.source = ?
                AND b.destination = ?
            """, (src, dst)).fetchall()

            if not buses:

                messagebox.showinfo(
                    "No Buses",
                    "No buses found for this route."
                )

                return

            for bus in buses:

                tree.insert(
                    "",
                    tk.END,
                    values=bus
                )

        self.button(
            form,
            "SEARCH",
            search,
            "#16A34A",
            15
        ).grid(row=0, column=4, padx=15)

        def select_bus():

            selected = tree.selection()

            if not selected:

                messagebox.showwarning(
                    "Select Bus",
                    "Please select a bus first."
                )

                return

            values = tree.item(
                selected[0]
            )["values"]

            self.selected_bus = values

            self.seat_selection()

        self.button(
            self.root,
            "💺 SELECT BUS & SEAT",
            select_bus,
            "#2563EB",
            22
        ).pack(pady=10)

        self.button(
            self.root,
            "← BACK",
            self.home_screen,
            "#172033",
            15
        ).pack(pady=(0, 15))

    # ========================================================
    # SEAT SELECTION
    # ========================================================

    def seat_selection(self):

        self.clear_screen()

        bus = self.selected_bus

        self.header(
            "💺 Select Your Seat",
            f"{bus[0]} - {bus[1]}"
        )

        tk.Label(
            self.root,
            text=f"{bus[2]} → {bus[3]}    |    Fare: ₹{bus[5]}",
            bg="#F4F7FB",
            fg="#172033",
            font=("Arial", 14, "bold")
        ).pack(pady=15)

        seats_frame = tk.Frame(
            self.root,
            bg="#F4F7FB"
        )

        seats_frame.pack(pady=10)

        booked_seats = self.cursor.execute("""
            SELECT seat_number
            FROM bookings
            WHERE bus_number = ?
        """, (bus[0],)).fetchall()

        booked = [x[0] for x in booked_seats]

        selected_var = tk.IntVar(value=0)

        for seat in range(1, 21):

            row = (seat - 1) // 4
            col = (seat - 1) % 4

            if seat in booked:

                btn = tk.Button(
                    seats_frame,
                    text=f"💺 {seat}\nBOOKED",
                    bg="#DC2626",
                    fg="white",
                    width=12,
                    height=3,
                    state="disabled"
                )

            else:

                def select(
                    s=seat
                ):
                    selected_var.set(s)

                    for child in seats_frame.winfo_children():

                        if child["state"] != "disabled":
                            child.configure(
                                bg="#CBD5E1",
                                fg="#172033"
                            )

                    current = seats_frame.grid_slaves(
                        row=(s - 1) // 4,
                        column=(s - 1) % 4
                    )[0]

                    current.configure(
                        bg="#16A34A",
                        fg="white"
                    )

                btn = tk.Button(
                    seats_frame,
                    text=f"💺 {seat}\nAVAILABLE",
                    command=select,
                    bg="#CBD5E1",
                    fg="#172033",
                    font=("Arial", 9, "bold"),
                    width=12,
                    height=3,
                    cursor="hand2"
                )

            btn.grid(
                row=row,
                column=col,
                padx=10,
                pady=10
            )

        def continue_booking():

            seat = selected_var.get()

            if seat == 0:

                messagebox.showwarning(
                    "Select Seat",
                    "Please select an available seat."
                )

                return

            self.selected_seat = seat

            self.passenger_details()

        self.button(
            self.root,
            "CONTINUE →",
            continue_booking,
            "#2563EB",
            20
        ).pack(pady=15)

        self.button(
            self.root,
            "← BACK",
            self.search_buses,
            "#172033",
            15
        ).pack()

    # ========================================================
    # PASSENGER DETAILS
    # ========================================================

    def passenger_details(self):

        self.clear_screen()

        self.header(
            "👤 Passenger Details",
            "Enter passenger information"
        )

        frame = tk.Frame(
            self.root,
            bg="#F4F7FB"
        )

        frame.pack(pady=30)

        tk.Label(
            frame,
            text="Passenger Name",
            bg="#F4F7FB",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=0, pady=10)

        name_entry = tk.Entry(
            frame,
            width=35,
            font=("Arial", 12)
        )

        name_entry.grid(
            row=0,
            column=1,
            padx=15
        )

        tk.Label(
            frame,
            text="Phone Number",
            bg="#F4F7FB",
            font=("Arial", 11, "bold")
        ).grid(row=1, column=0, pady=10)

        phone_entry = tk.Entry(
            frame,
            width=35,
            font=("Arial", 12)
        )

        phone_entry.grid(
            row=1,
            column=1,
            padx=15
        )

        tk.Label(
            frame,
            text="Travel Date",
            bg="#F4F7FB",
            font=("Arial", 11, "bold")
        ).grid(row=2, column=0, pady=10)

        date_entry = tk.Entry(
            frame,
            width=35,
            font=("Arial", 12)
        )

        date_entry.insert(
            0,
            datetime.now().strftime("%d-%m-%Y")
        )

        date_entry.grid(
            row=2,
            column=1,
            padx=15
        )

        def confirm():

            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            date = date_entry.get().strip()

            if not name or not phone or not date:

                messagebox.showwarning(
                    "Missing Information",
                    "Please fill all fields."
                )

                return

            if not phone.isdigit() or len(phone) != 10:

                messagebox.showwarning(
                    "Invalid Phone",
                    "Enter a valid 10-digit phone number."
                )

                return

            bus = self.selected_bus

            booking_id = (
                "BR"
                + datetime.now().strftime("%Y%m%d%H%M%S")
            )

            try:

                self.cursor.execute("""
                    INSERT INTO bookings
                    (
                        booking_id,
                        passenger_name,
                        phone,
                        bus_number,
                        source,
                        destination,
                        travel_date,
                        seat_number,
                        fare,
                        booking_time
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    booking_id,
                    name,
                    phone,
                    bus[0],
                    bus[2],
                    bus[3],
                    date,
                    self.selected_seat,
                    bus[5],
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                ))

                self.db.commit()

                messagebox.showinfo(
                    "Booking Successful",
                    f"Your bus has been booked successfully!\n\n"
                    f"Booking ID: {booking_id}\n"
                    f"Passenger: {name}\n"
                    f"Bus: {bus[0]}\n"
                    f"Seat: {self.selected_seat}\n"
                    f"Fare: ₹{bus[5]}"
                )

                self.home_screen()

            except sqlite3.IntegrityError:

                messagebox.showerror(
                    "Booking Error",
                    "This seat may have just been booked."
                )

        self.button(
            self.root,
            "🎫 CONFIRM BOOKING",
            confirm,
            "#16A34A",
            22
        ).pack(pady=20)

        self.button(
            self.root,
            "← BACK",
            self.seat_selection,
            "#172033",
            15
        ).pack()

    # ========================================================
    # VIEW BOOKINGS
    # ========================================================

    def view_bookings(self):

        self.clear_screen()

        self.header(
            "🎫 My Reservations",
            "View all booked tickets"
        )

        frame = tk.Frame(
            self.root,
            bg="white"
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        columns = (
            "booking",
            "name",
            "bus",
            "route",
            "date",
            "seat",
            "fare"
        )

        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        headings = [
            ("booking", "Booking ID"),
            ("name", "Passenger"),
            ("bus", "Bus"),
            ("route", "Route"),
            ("date", "Date"),
            ("seat", "Seat"),
            ("fare", "Fare")
        ]

        for col, heading in headings:

            tree.heading(
                col,
                text=heading
            )

            tree.column(
                col,
                width=130
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        bookings = self.cursor.execute("""
            SELECT
                booking_id,
                passenger_name,
                bus_number,
                source || ' → ' || destination,
                travel_date,
                seat_number,
                fare
            FROM bookings
            ORDER BY id DESC
        """).fetchall()

        for booking in bookings:

            tree.insert(
                "",
                tk.END,
                values=booking
            )

        if not bookings:

            messagebox.showinfo(
                "No Reservations",
                "There are no reservations yet."
            )

        self.button(
            self.root,
            "← BACK",
            self.home_screen,
            "#172033",
            15
        ).pack(pady=15)

    # ========================================================
    # CANCEL BOOKING
    # ========================================================

    def cancel_booking(self):

        self.clear_screen()

        self.header(
            "❌ Cancel Reservation",
            "Enter your booking ID"
        )

        frame = tk.Frame(
            self.root,
            bg="#F4F7FB"
        )

        frame.pack(pady=50)

        tk.Label(
            frame,
            text="Booking ID:",
            bg="#F4F7FB",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, padx=10)

        entry = tk.Entry(
            frame,
            width=30,
            font=("Arial", 13)
        )

        entry.grid(
            row=0,
            column=1,
            padx=10
        )

        def cancel():

            booking_id = entry.get().strip()

            if not booking_id:

                messagebox.showwarning(
                    "Required",
                    "Enter a booking ID."
                )

                return

            booking = self.cursor.execute("""
                SELECT
                    passenger_name,
                    bus_number,
                    seat_number
                FROM bookings
                WHERE booking_id = ?
            """, (booking_id,)).fetchone()

            if not booking:

                messagebox.showerror(
                    "Not Found",
                    "Booking ID not found."
                )

                return

            confirm = messagebox.askyesno(
                "Confirm Cancellation",
                f"Cancel booking {booking_id}?"
            )

            if confirm:

                self.cursor.execute(
                    "DELETE FROM bookings WHERE booking_id = ?",
                    (booking_id,)
                )

                self.db.commit()

                messagebox.showinfo(
                    "Cancelled",
                    "Reservation cancelled successfully."
                )

                self.home_screen()

        self.button(
            frame,
            "CANCEL BOOKING",
            cancel,
            "#DC2626",
            18
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            pady=25
        )

        self.button(
            self.root,
            "← BACK",
            self.home_screen,
            "#172033",
            15
        ).pack()

    # ========================================================
    # CLOSE
    # ========================================================

    def close_application(self):

        self.db.close()
        self.root.destroy()


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = BusReservationSystem(root)

    root.mainloop()