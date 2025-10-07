def is_prime(num):
    if num <= 2:
        return False
    for i in range(2, num):
        if num % i == 0:
            return False
    return True

def chk_prime_day(date_str):
    from datetime import datetime
    
    # Convert string date to datetime object
    try:
        date = datetime.strptime(date_str, "%m-%d-%Y")
        day = date.day
        print(f"Day of the month: {day}")
        
        if is_prime(day):
            print(f" {date_str} is a Prime Day!")
        else:
            print(f" {date_str} is NOT a Prime Day.")
    except ValueError:
        print("Invalid date format. Please use MM-DD-YYYY.")

# user input format MM-DD-YYYY
date_input = input("Enter a date (MM-DD-YYYY): ")
chk_prime_day(date_input)