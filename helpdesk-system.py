#!/usr/bin/env python3
"""
Helpdesk System - Service Desk Ticket Management
Simple terminal application for Part V Kanban practice

This system demonstrates an "existing codebase" scenario where basic
functionality already works, but needs ongoing maintenance and enhancements.
Students will apply Kanban practices to manage continuous flow of work items.
"""

import datetime
from typing import List, Dict, Optional
import csv

# Global data structures
tickets: List[Dict] = []
ticket_counter = 1
categories = ['Hardware', 'Software', 'Network', 'Other']
staff_members = ['Alice Johnson', 'Bob Smith', 'Charlie Lee', 'Dana White']

# Simple user store for login simulation
users = {
    "admin": {"password": "admin123", "role": "Admin"},
    "suzanna": {"password": "helpdesk1", "role": "Support"},
    "yulia": {"password": "helpdesk2", "role": "Support"},
    "fuad": {"password": "helpdesk3", "role": "Support"},
    "ira": {"password": "helpdesk4", "role": "Support"}
}

current_user = None


def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Check whether username/password are valid"""
    username = username.strip().lower()
    password = password.strip()

    if not username or not password:
        return None

    user = users.get(username)
    if not user:
        return None

    if user["password"] != password:
        return None

    return {"username": username, "role": user["role"]}

def login() -> bool:
    """Prompt user to log in before accessing the system"""
    global current_user

    print("\n" + "=" * 60)
    print("  HELPDESK SYSTEM LOGIN")
    print("=" * 60)

    attempts = 3

    while attempts > 0:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        user = authenticate_user(username, password)

        if user:
            current_user = user
            print(f"\n✓ Login successful. Welcome, {current_user['username']} ({current_user['role']})")
            return True

        attempts -= 1
        print(f"Error: Invalid username or password. Attempts left: {attempts}")

    print("\nAccess denied. Too many failed login attempts.")
    return False

# Starter tickets (demonstrates existing system with some data)
def initialize_starter_data():
    """Initialize system with 3 existing tickets to demonstrate 'existing codebase' concept"""
    global tickets, ticket_counter

    tickets = [
        {
            'id': 1,
            'title': 'Cannot access shared drive',
            'description': 'User reports unable to connect to //fileserver/shared. Getting "access denied" error.',
            'status': 'Open',
            'assigned_to': 'Support Team',
            'created_at': datetime.datetime.now() - datetime.timedelta(days=2),
            'comments': ['Initial report received from user@example.com'], 
            'priority': 'High',
            'category': 'Network'
        },
        {
            'id': 2,
            'title': 'Printer not working in Room 301',
            'description': 'HP LaserJet in Room 301 showing error code 49. Paper jams frequently.',
            'status': 'In Progress',
            'assigned_to': 'Alice Johnson',
            'created_at': datetime.datetime.now() - datetime.timedelta(days=1),
            'comments': ['Ticket assigned to Alice', 'Alice: Checked printer, ordered replacement parts'],
            'priority': 'Medium',
            'category': 'Hardware'
        },
        {
            'id': 3,
            'title': 'Email not syncing on mobile device',
            'description': 'User cannot receive emails on iPhone. Webmail works fine.',
            'status': 'Closed',
            'assigned_to': 'Bob Smith',
            'created_at': datetime.datetime.now() - datetime.timedelta(days=3),
            'comments': ['Bob: Reset mobile sync settings', 'Bob: Issue resolved, user confirmed emails working'],
            'priority': 'Low',
            'category': 'Software'
        }
    ]
    ticket_counter = 4  # Next ticket will be ID 4


def create_ticket() -> None:
    """Create a new support ticket"""
    global ticket_counter

    print("\n=== Create New Ticket ===")
    title = input("Ticket title: ").strip()
    if not title:
        print("Error: Title cannot be empty")
        return

    description = input("Description: ").strip()
    if not description:
        print("Error: Description cannot be empty")
        return
    
    priority = input("Priority (Low/Medium/High) [default: Medium]: ")

    if not priority:
        priority = "Medium"

    priority = priority.strip().title()

    if priority not in ["Low", "Medium", "High"]:
        print("Invalid priority. Defaulting to Medium.")
        priority = "Medium"

    # Category selection 
    print("\nSelect category:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")

    try:
        cat_choice = int(input("Choose category (number): "))
        category = categories[cat_choice - 1]
    except (ValueError, IndexError):
        print("Invalid category. Defaulting to 'Other'")
        category = 'Other'

    # Create new ticket
    new_ticket = {
        'id': ticket_counter,
        'title': title,
        'description': description,
        'status': 'Open',
        'assigned_to': 'Unassigned',
        'created_at': datetime.datetime.now(),
        'comments': [],
        'priority': priority,
        'category': category
    }

    tickets.append(new_ticket)
    print(f"\n✓ Ticket #{ticket_counter} created successfully")
    ticket_counter += 1


def view_tickets(filter_status: Optional[str] = None) -> None:
    """
    View all tickets or filtered by status

    Args:
        filter_status: Optional status filter ('Open', 'In Progress', 'Closed')
    """
    print("\n=== Ticket List ===")

    # Normalize status values to avoid mismatches caused by case/extra spaces.
    normalize = lambda s: str(s).strip().lower()

    ticket_stream = (t for t in tickets)
    if filter_status:
        target_status = normalize(filter_status)
        ticket_stream = (t for t in ticket_stream if normalize(t.get('status', '')) == target_status)
        print(f"Filter: {filter_status} tickets only")

    page_size = 20
    page_number = 1
    shown_total = 0

    while True:
        page = []
        for _ in range(page_size):
            try:
                page.append(next(ticket_stream))
            except StopIteration:
                break

        if not page:
            if shown_total == 0:
                print("No tickets found")
            break

        print(
            f"\n{'ID':<5} {'Title':<25} {'Category':<12} {'Status':<15} {'Assigned To':<20} {'Created':<12}"
        )
        print("-" * 85)

        for ticket in page:
            created_str = ticket['created_at'].strftime('%Y-%m-%d')
            title_truncated = ticket['title'][:28] + '..' if len(ticket['title']) > 30 else ticket['title']

            print(
                f"{ticket['id']:<5} {title_truncated:<25} {ticket['category']:<12} {ticket['status']:<15} "
                f"{ticket['assigned_to']:<20} {created_str:<12}"
            )

        shown_total += len(page)

        if len(page) < page_size:
            break

        prompt = f"\nPage {page_number} shown ({shown_total} tickets). Type 'Next' for more or press Enter to stop: "
        if input(prompt).strip().lower() != 'next':
            break
        page_number += 1

    print(f"\nTotal: {shown_total} tickets")


def view_ticket_details(ticket_id: int) -> None:
    """View full details of a specific ticket"""
    ticket = find_ticket_by_id(ticket_id)
    if not ticket:
        print(f"Error: Ticket #{ticket_id} not found")
        return

    print("\n" + "=" * 60)
    print(f"Ticket #{ticket['id']}: {ticket['title']}")
    print("=" * 60)
    print(f"Status: {ticket['status']}")
    print(f"Priority: {ticket.get('priority', 'Medium')}")
    print(f"Assigned To: {ticket['assigned_to']}")
    print(f"Created: {ticket['created_at'].strftime('%Y-%m-%d %H:%M')}")
    print(f"\nDescription:\n{ticket['description']}")
    print(f"\nCategory: {ticket.get('category', 'Other')}")

    if ticket['comments']:
        print(f"\nComments ({len(ticket['comments'])}):")
        for i, comment in enumerate(reversed(ticket['comments']), 1):
            print(f"  {i}. {comment}")
    else:
        print("\nNo comments yet")
    print("=" * 60)


def assign_ticket(ticket_id: int, staff_name: str) -> None:
    ticket = find_ticket_by_id(ticket_id)
    if not ticket:
        print(f"Error: Ticket #{ticket_id} not found")
        return

    # Check if staff member exists
    if staff_name not in staff_members:
        print("Error: Staff member does not exist")
        print("Available staff:", ", ".join(staff_members))
        return

    # Check if ticket is already assigned to the same staff member
    if ticket['assigned_to'] == staff_name:
        print(f"Ticket already assigned to {staff_name}")
        return

    # Check if ticket is closed
    if ticket['status'] == 'Closed':
        print("Error: Cannot assign a closed ticket")
        return

    ticket['assigned_to'] = staff_name
    ticket['comments'].append(f"Ticket assigned to {staff_name}")

    if ticket['status'] == 'Open':
        ticket['status'] = 'In Progress'

    print(f"\n✓ Ticket #{ticket_id} assigned to {staff_name}")


def add_comment(ticket_id: int, comment: str) -> None:
    ticket = find_ticket_by_id(ticket_id)

    if not ticket:
        print(f"Error: Ticket #{ticket_id} not found")
        return

    if not comment.strip():
        print("Error: Comment cannot be empty")
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    ticket['comments'].append(f"[{timestamp}] {comment}")

    print(f"\n✓ Comment added to ticket #{ticket_id}")


def close_ticket(ticket_id: int) -> None:
    ticket = find_ticket_by_id(ticket_id)

    if not ticket:
        print(f"Error: Ticket #{ticket_id} not found")
        return

    if ticket['status'] == 'Closed':
        print(f"Warning: Ticket #{ticket_id} already closed")
        return

    ticket['status'] = 'Closed'
    ticket['comments'].append("Ticket closed")

    print(f"\n✓ Ticket #{ticket_id} closed successfully")

def search_tickets(query: str) -> None:
    """
    Search tickets by ID or title/description

    Args:
        query: Search query (ticket ID number or keywords)
    """
    query = query.strip()
    print(f"\n=== Search Results for '{query}' ===")

    # Search by ticket ID
    if query.isdigit():
        ticket_id = int(query)
        ticket = find_ticket_by_id(ticket_id)

        if ticket:
            view_ticket_details(ticket_id)
            return
        else:
            print(f"No ticket found with ID #{ticket_id}")
            return

    # Search by title/description (case-insensitive)
    query_lower = query.lower()
    matching_tickets = [
        t for t in tickets
        if query_lower in t['title'].lower()
        or query_lower in t['description'].lower()
    ]

    if not matching_tickets:
        print("No tickets found matching query")
        return

    print(f"\n{'ID':<5} {'Title':<30} {'Status':<15} {'Assigned To':<20}")
    print("-" * 70)

    for ticket in matching_tickets:
        title_truncated = ticket['title'][:28] + '..' if len(ticket['title']) > 30 else ticket['title']
        print(f"{ticket['id']:<5} {title_truncated:<30} {ticket['status']:<15} {ticket['assigned_to']:<20}")

    print(f"\nFound {len(matching_tickets)} matching tickets")

def find_ticket_by_id(ticket_id: int) -> Optional[Dict]:
    """
    Find ticket by ID

    Args:
        ticket_id: Ticket ID to search for

    Returns:
        Ticket dictionary if found, None otherwise
    """
    for ticket in tickets:
        if ticket['id'] == ticket_id:
            return ticket
    return None

def export_tickets_to_csv(filename: str = "tickets_export.csv") -> None:
    """Export all tickets to CSV file"""
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Header row
            writer.writerow([
                "ID",
                "Title",
                "Status",
                "Assigned To",
                "Created Date",
                "Category",
                "Priority"
            ])

            # Ticket rows
            for ticket in tickets:
                writer.writerow([
                    ticket.get('id', ''),
                    ticket.get('title', ''),
                    ticket.get('status', ''),
                    ticket.get('assigned_to', ''),
                    ticket.get('created_at').strftime('%Y-%m-%d %H:%M') if ticket.get('created_at') else '',
                    ticket.get('category', 'Other'),
                    ticket.get('priority', 'Medium')
                ])

        print(f"\n✓ Tickets successfully exported to {filename}")

    except Exception as e:
        print(f"Error exporting tickets: {e}")

def main_menu() -> None:
    """Main menu loop"""
    print("\n" + "=" * 60)
    print("  HELPDESK SYSTEM - Service Desk Ticket Management")
    print("=" * 60)
    print("  Part V Kanban Practice - Existing Codebase Scenario")
    print("=" * 60)
    print(f"Logged in as: {current_user['username']} ({current_user['role']})")

    while True:
        print("\n--- Main Menu ---")
        print("1. View all tickets")
        print("2. View open tickets only")
        print("3. View ticket details")
        print("4. Create new ticket")
        print("5. Assign ticket")
        print("6. Add comment to ticket")
        print("7. Close ticket")
        print("8. Search tickets")
        print("9. Export tickets to CSV")
        print("0. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == '1':
            view_tickets()

        elif choice == '2':
            view_tickets(filter_status='Open')

        elif choice == '3':
            try:
                ticket_id = int(input("Enter ticket ID: "))
                view_ticket_details(ticket_id)
            except ValueError:
                print("Error: Invalid ticket ID")

        elif choice == '4':
            create_ticket()

        elif choice == '5':
            try:
                ticket_id = int(input("Enter ticket ID: "))

                print("\nAvailable staff:")
                for i, s in enumerate(staff_members, 1):
                    print(f"{i}. {s}")

                try:
                    staff_choice = int(input("Select staff (number): "))
                    staff_name = staff_members[staff_choice - 1]
                except (ValueError, IndexError):
                    print("Error: Invalid selection")
                continue

                assign_ticket(ticket_id, staff_name)

            except ValueError:
                print("Error: Invalid ticket ID")

        elif choice == '6':
            try:
                ticket_id = int(input("Enter ticket ID: "))
                comment = input("Comment: ").strip()
                if comment:
                    add_comment(ticket_id, comment)
            except ValueError:
                print("Error: Invalid ticket ID")

        elif choice == '7':
            try:
                ticket_id = int(input("Enter ticket ID: "))
                close_ticket(ticket_id)
            except ValueError:
                print("Error: Invalid ticket ID")

        elif choice == '8':
            query = input("Search query (ID or keywords): ").strip()
            if query:
                search_tickets(query)

        elif choice == '9':
            export_tickets_to_csv()

        elif choice == '0':
            print("\n👋 Thank you for using Helpdesk System!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    # Initialize with starter data
    initialize_starter_data()

    # Run main menu
    if login():
        main_menu()
