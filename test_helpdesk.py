import io
import os
import unittest
import datetime
import importlib.util
from contextlib import redirect_stdout
from unittest.mock import patch


def load_helpdesk_module():
    file_path = os.path.join(os.path.dirname(__file__), "helpdesk-system.py")
    spec = importlib.util.spec_from_file_location("helpdesk_system", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HelpdeskTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h = load_helpdesk_module()

    def setUp(self):
        self.h.initialize_starter_data()

    def test_create_ticket(self):
        initial_len = len(self.h.tickets)
        initial_counter = self.h.ticket_counter

        inputs = [
            "New VPN issue",
            "Cannot connect to VPN",
            "High",
            "2",
        ]

        with patch("builtins.input", side_effect=inputs):
            with patch("builtins.print"):
                self.h.create_ticket()

        self.assertEqual(len(self.h.tickets), initial_len + 1)
        new_ticket = self.h.tickets[-1]
        self.assertEqual(new_ticket["id"], initial_counter)
        self.assertEqual(new_ticket["title"], "New VPN issue")
        self.assertEqual(new_ticket["description"], "Cannot connect to VPN")
        self.assertEqual(new_ticket["status"], "Open")
        self.assertEqual(new_ticket["assigned_to"], "Unassigned")
        self.assertEqual(new_ticket["priority"], "High")
        self.assertEqual(new_ticket["category"], "Software")
        self.assertIsInstance(new_ticket["created_at"], datetime.datetime)
        self.assertEqual(self.h.ticket_counter, initial_counter + 1)

    def test_assign_ticket(self):
        ticket_id = 1
        staff = "Alice Johnson"
        ticket = self.h.find_ticket_by_id(ticket_id)

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket["status"], "Open")

        with patch("builtins.print"):
            self.h.assign_ticket(ticket_id, staff)

        updated = self.h.find_ticket_by_id(ticket_id)
        self.assertEqual(updated["assigned_to"], staff)
        self.assertEqual(updated["status"], "In Progress")
        self.assertTrue(any("Ticket assigned to Alice Johnson" in c for c in updated["comments"]))

    def test_close_ticket(self):
        ticket_id = 2
        ticket = self.h.find_ticket_by_id(ticket_id)
        self.assertIsNotNone(ticket)
        self.assertNotEqual(ticket["status"], "Closed")

        with patch("builtins.print"):
            self.h.close_ticket(ticket_id)

        updated = self.h.find_ticket_by_id(ticket_id)
        self.assertEqual(updated["status"], "Closed")
        self.assertTrue(any("Ticket closed" in c for c in updated["comments"]))

    def test_search_tickets(self):
        query = "printer"
        buf = io.StringIO()

        with redirect_stdout(buf):
            self.h.search_tickets(query)

        output = buf.getvalue().lower()
        self.assertIn("search results", output)
        self.assertIn("printer", output)
        self.assertIn("found 1 matching tickets", output)


if __name__ == "__main__":
    unittest.main()

