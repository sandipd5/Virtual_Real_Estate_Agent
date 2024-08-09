from typing import Dict, List, Union, Callable
import pandas as pd

class RealEstateChatbot:
    def __init__(self, filter_properties_func: Callable[[Dict, pd.DataFrame], List[Dict]]):
        self.matching_properties = []
        self.filter_properties = filter_properties_func
        self.selected_option_number = None
        self.property_details = None
        self.visit_availability = None
        self.house_price = None
        self.vist_date = None

    def compose_answer(self, intent: str, entities: Dict, property_df: pd.DataFrame) -> str:
        if intent == "Greetings":
            return "Hello! Welcome to our real estate chatbot. How can I assist you with your property search today?"

        elif intent == "Property_inquiries":
            self.matching_properties = self.filter_properties(entities, property_df)

            if not self.matching_properties:
                return "No properties found matching your criteria."

            # Sort properties by price (optional)
            self.matching_properties = sorted(self.matching_properties, key=lambda x: x['Price'])

            # Select top 3 properties
            top_properties = self.matching_properties[:3]

            # Format the answer
            response_lines = [
                "These are the top property listings for your requirements. Select one to know the details by writing the option number or type 'exit':"
            ]
            for idx, prop in enumerate(top_properties):
                response_lines.append(
                    f"{idx + 1}. Price: ${prop['Price']}, City: {prop['City']}, "
                    f"Bedrooms: {prop['Bedroom']}, Bathrooms: {prop['Bathroom']}, "
                    f"House Type: {prop['House Type']}, House Size: {prop['House Size']}"
                )

            return "\n".join(response_lines)

        elif intent == "Details":
            option_number = entities.get('option_number')
            if option_number is not None and 1 <= option_number <= len(self.matching_properties):
                self.selected_option_number = option_number
                property_details = self.matching_properties[option_number - 1]
                self.property_details = property_details
                details = "This is the detailed description for the property you chose:\n"
                for key, value in property_details.items():
                    details += f"{key}: {value}\n"
                details += "Do you want to schedule an appointment to  visit this house ?"    
                return details
            else:
                return "Invalid option number. Please select a valid option."
        elif intent == "Finance_DB":
            property_details = self.property_details
            house_price = property_details['Price']
            self.house_price = house_price
            min_down = float(house_price) * 0.2
            response = "The monthly payment or a mortgage will be calculated based on your down payment.Please provide your down payment and loan term. Loan term is the number of years you would like to pay the mortgage.\n The downpayment should be greater than 20% of the house price i.e greater than {min_down}."
            return response
        elif intent == "monthly_mortgage":
            house_price = self.house_price
            down_payment = entities.get('down_payment')
            loan_term = entities.get('loan_term')

            if down_payment and loan_term:
                down_payment = float(down_payment)
                loan_term = int(loan_term)
                interest_rate = 0.065
                monthly_payment = self.calculate_monthly_payment(house_price, down_payment, interest_rate, loan_term)  
                return (f"Based on a house price of ${house_price:,}, a down payment of ${down_payment:,}, " f"and a loan term of {loan_term} years at an interest rate of {interest_rate * 100:.2f}%, "f"your estimated monthly mortgage payment would be ${monthly_payment:,.2f}.")
            else:
             return ("To calculate your monthly mortgage payment, please provide the down payment amount and the loan term in years.")

        elif intent == "Visit_schedule":
                if self.selected_option_number is not None and 1 <= self.selected_option_number <= len(self.matching_properties):
                    property_details = self.matching_properties[self.selected_option_number - 1]
                    visit_availability = property_details.get('Visit availability date time', 'No visit dates available')
                    self.visit_availability = visit_availability
                return (
                    "These are the available dates to view the property. "
                    "If you want to schedule the appointment for a visit, choose one date from below:\n"
                    f"{visit_availability}"
                )
        elif intent == "Visit_confirmed":
                visit_dates = [date.strip() for date in self.visit_availability.split('\n')]
                if entities.get('visit_date') in visit_dates:
                    self.visit_date = entities.get('visit_date')
                    return f"Okay, your visit appointment is confirmed for this house on {self.visit_date}."
                else:
                    return "Sorry, the chosen date is not available. Please try again."
        
                   
        else:
            return "Please provide your requirements, I will help you chose and schedule a visit to the  house"


    def calculate_monthly_payment(self, house_price, down_payment, interest_rate, loan_term):
        principal = house_price - down_payment
        monthly_interest_rate = interest_rate / 12
        number_of_payments = loan_term * 12
        monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / ((1 + monthly_interest_rate) ** number_of_payments - 1)
        return monthly_payment
            