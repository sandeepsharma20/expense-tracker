import sys
import random
from datetime import datetime, timedelta
from database.db import get_db

def main():
    if len(sys.argv) != 4:
        print("Usage: /seed-expenses <user_id> <count> <months>")
        print("Example: /seed-expenses 1 50 6")
        sys.exit(1)

    try:
        user_id = int(sys.argv[1])
        count = int(sys.argv[2])
        months = int(sys.argv[3])
    except ValueError:
        print("Usage: /seed-expenses <user_id> <count> <months>")
        print("Example: /seed-expenses 1 50 6")
        sys.exit(1)

    conn = get_db()
    try:
        # Verify user exists
        cursor = conn.execute('SELECT 1 FROM users WHERE id = ?', (user_id,))
        if cursor.fetchone() is None:
            print(f"No user found with id {user_id}.")
            sys.exit(1)

        # Define categories with amounts ranges and description templates
        categories = [
            ('Food', 50, 800, [
                'Lunch at restaurant', 'Groceries for week', 'Dinner with family',
                'Snacks and beverages', 'Breakfast cafe', 'Food delivery',
                'Vegetables and fruits', 'Milk and dairy', 'Rice and lentils'
            ]),
            ('Transport', 20, 500, [
                'Bus ticket', 'Auto rickshaw fare', 'Metro recharge',
                'Fuel for bike', 'Parking fees', 'Taxi ride',
                'Vehicle maintenance', 'Toll charges', 'Car service'
            ]),
            ('Bills', 200, 3000, [
                'Electricity bill', 'Water bill', 'Internet recharge',
                'Mobile phone bill', 'Gas cylinder', 'DTH recharge',
                'Laundry service', 'House maintenance', 'Garbage collection'
            ]),
            ('Health', 100, 2000, [
                'Pharmacy purchase', 'Doctor consultation', 'Medical test',
                'Vitamins supplements', 'Dental checkup', 'Eye checkup',
                'Traditional medicine', 'Fitness class', 'Yoga session'
            ]),
            ('Entertainment', 100, 1500, [
                'Movie tickets', 'Concert pass', 'Amusement park',
                'Streaming subscription', 'Gaming zone', 'Theatre play',
                'Sports event', 'Museum entry', 'Picnic supplies'
            ]),
            ('Shopping', 200, 5000, [
                'Clothing purchase', 'Footwear', 'Electronics accessory',
                'Home decor', 'Gift for friend', 'Personal grooming',
                'Kitchen utensils', 'Books and stationery', 'Festival shopping'
            ]),
            ('Other', 50, 1000, [
                'Miscellaneous expense', 'Donation', 'Postage stamps',
                'Printer recharge', 'Tool purchase', 'Umbrella',
                'Raincoat', 'Battery', 'Light bulb'
            ])
        ]

        # Define weights for category selection (Food most common, Health and Entertainment least)
        weights = [0.3, 0.2, 0.15, 0.15, 0.1, 0.05, 0.05]  # corresponds to categories order above
        category_list = [c[0] for c in categories]

        # Calculate date range: today minus months months (approx 30 days per month)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months*30)

        expenses_to_insert = []
        for _ in range(count):
            # Choose category based on weights
            cat_idx = random.choices(range(len(categories)), weights=weights)[0]
            cat_name, min_amt, max_amt, descriptions = categories[cat_idx]
            amount = round(random.uniform(min_amt, max_amt), 2)
            description = random.choice(descriptions)
            # Random date within range
            days_offset = random.randint(0, (end_date - start_date).days)
            expense_date = start_date + timedelta(days=days_offset)
            date_str = expense_date.strftime('%Y-%m-%d')
            expenses_to_insert.append((
                user_id,
                amount,
                cat_name,
                date_str,
                description
            ))

        # Insert all expenses in a single transaction
        cursor = conn.executemany('''
            INSERT INTO expenses (user_id, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
        ''', expenses_to_insert)
        conn.commit()

        inserted = cursor.rowcount
        # Get date range of inserted expenses for confirmation
        cursor = conn.execute('''
            SELECT MIN(date), MAX(date) FROM expenses WHERE user_id = ?
        ''', (user_id,))
        min_date, max_date = cursor.fetchone()

        # Get a sample of 5 inserted records (most recent)
        cursor = conn.execute('''
            SELECT id, amount, category, date, description FROM expenses
            WHERE user_id = ?
            ORDER BY date DESC, id DESC
            LIMIT 5
        ''', (user_id,))
        sample = cursor.fetchall()

        print(f"Inserted {inserted} expenses for user {user_id}.")
        print(f"Date range: {min_date} to {max_date}")
        print("Sample of 5 inserted records:")
        for row in sample:
            print(f"  ID: {row[0]}, Amount: Rs.{row[1]}, Category: {row[2]}, Date: {row[3]}, Description: {row[4]}")

    finally:
        conn.close()

if __name__ == '__main__':
    main()