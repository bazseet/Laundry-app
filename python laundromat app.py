import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table, select
import stripe

# Set your Stripe API key
stripe.api_key = "your_stripe_secret_key"

# Create an SQLite database
engine = create_engine('sqlite:///laundry_app.db', echo=True)
metadata = MetaData()

# Define the 'orders' table
orders_table = Table('orders', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('quantity', Integer),
                     Column('type', String),
                     Column('total_cost', Float),
                     Column('status', String)
                     )

metadata.create_all(engine)

class LaundryApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Widgets
        self.quantity_label = QLabel('Quantity:')
        self.quantity_input = QLineEdit(self)

        self.types_label = QLabel('Types of Clothes:')
        self.types_input = QLineEdit(self)

        self.calculate_button = QPushButton('Calculate', self)
        self.result_label = QLabel('Total Cost: $0.00')

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_input)
        layout.addWidget(self.types_label)
        layout.addWidget(self.types_input)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

        # Connect the button click to the calculate function
        self.calculate_button.clicked.connect(self.calculate_cost)

        # Window settings
        self.setWindowTitle('Laundry App')
        self.setGeometry(300, 300, 300, 200)

    def calculate_cost(self):
        try:
            quantity = int(self.quantity_input.text())
            selected_type = self.types_input.text()

            # Check if the selected type is valid
            if selected_type in ["Agbada", "Jalabiya", "Abaya", "Natives", "Others"]:
                price_per_item = self.get_price(selected_type)
                total_cost = quantity * price_per_item

                # Store order in the database
                with engine.connect() as connection:
                    ins = orders_table.insert().values(
                        quantity=quantity,
                        type=selected_type,
                        total_cost=total_cost,
                        status='Pending'
                    )
                    result = connection.execute(ins)

                self.result_label.setText(f'Total Cost: ${total_cost:.2f}')
                print("Order placed. Order ID:", result.inserted_primary_key[0])

                # Process payment
                payment_status = self.process_payment(total_cost)

                if payment_status:
                    # Update order status to 'Paid'
                    with engine.connect() as connection:
                        connection.execute(
                            orders_table.update().where(orders_table.c.id == result.inserted_primary_key[0]).values(
                                status='Paid')
                        )
                    print("Payment processed successfully.")
                else:
                    print("Payment failed.")

            else:
                self.result_label.setText('Invalid type. Please choose from the provided types.')

        except ValueError:
            self.result_label.setText('Invalid input. Please enter numbers.')

    def get_price(self, cloth_type):
        # Retrieve price from the predefined prices
        prices = {
            'Agbada': 500,
            'Jalabiya': 300,
            'Abaya': 300,
            'Natives': 350,
            'Others': 200
        }
        return prices.get(cloth_type, 0)

    def process_payment(self, amount):
        try:
            # Simulate payment processing using Stripe
            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Amount is in cents
                currency='naira',
            )
            return payment_intent.status == 'succeeded'

        except stripe.error.CardError as e:
            print(f"Payment failed: {e.error.message}")
            return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    laundry_app = LaundryApp()
    laundry_app.show()
    sys.exit(app.exec_())