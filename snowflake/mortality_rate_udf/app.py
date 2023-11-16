def calculate_mortality_rate():
    try:
        # Hardcode the total_cases value
        total_cases = 52000  # You can replace this with your desired fixed value
        
        # Prompt the user for the number of deaths
        deaths = input("Enter the number of deaths in your area: ")
        
        # Convert the input to a float
        deaths = float(deaths)
        
        mortality_rate = deaths / total_cases if total_cases > 0 else 0.0
        print(f"The calculated mortality rate is: {mortality_rate:.4f}")
    except ValueError as e:
        print(f"Error: {e}")

# Call the function
calculate_mortality_rate()

