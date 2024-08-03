from typing import Dict, List, Union, Callable
import pandas as pd

class RealEstateChatbot:
    def __init__(self, filter_properties_func: Callable[[Dict, pd.DataFrame], List[Dict]]):
        self.matching_properties = []
        self.filter_properties = filter_properties_func
        self.selected_option_number = None

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
                details = "This is the detailed description for the property you chose:\n"
                for key, value in property_details.items():
                    details += f"{key}: {value}\n"
                return details
            else:
                return "Invalid option number. Please select a valid option."

        elif intent == "Visit_schedule":
           if self.selected_option_number is not None and 1 <= self.selected_option_number <= len(self.matching_properties):
                property_details = self.matching_properties[self.selected_option_number - 1]
                visit_availability = property_details.get('Visit availability date time', 'No visit dates available')
                return (
                    "These are the available dates to view the property. "
                    "If you want to schedule the appointment for a visit, choose one date from below:\n"
                    f"{visit_availability}"
                )
        else:
                return "Please select a property first by inquiring about property details."


