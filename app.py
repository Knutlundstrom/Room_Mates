
import psycopg2
import psycopg2.extras
import streamlit as st

import os
import psycopg2

def connect_db():
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://RoomMates_owner:7CKkMTds5Yqy@ep-young-cell-a531avz2.us-east-2.aws.neon.tech/RoomMates?sslmode=require") 
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Test the database connection in main()
conn = connect_db()
if conn:
    st.write("Database connection successful.")
    conn.close()
else:
    st.write("Failed to connect to the database.")


# Define UserProfile class
class UserProfile:
    def __init__(self, name, email_or_instagram, cleanliness, age, gender, sleep_schedule,
                 personality_type, social_battery, confrontational_behavior, religion,
                 drug_use, activities, busy, significant_other, major, year, snore,
                 values_in_roommate, primary_focus):
        self.name = name
        self.email_or_instagram = email_or_instagram
        self.cleanliness = cleanliness
        self.age = age
        self.gender = gender
        self.sleep_schedule = sleep_schedule
        self.personality_type = personality_type
        self.social_battery = social_battery
        self.confrontational_behavior = confrontational_behavior
        self.religion = religion
        self.drug_use = drug_use
        self.activities = activities
        self.busy = busy
        self.significant_other = significant_other
        self.major = major
        self.year = year
        self.snore = snore
        self.values_in_roommate = values_in_roommate
        self.primary_focus = primary_focus


def save_user_profile(user1):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO User_Profiles (
            name, email_or_instagram, cleanliness, age, gender, sleep_schedule,
            personality_type, social_battery, confrontational_behavior, religion,
            drug_use, activities, busy, significant_other, major, year, snore,
            values_in_roommate, primary_focus
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (
            user1.name,
            user1.email_or_instagram,
            user1.cleanliness,
            user1.age,
            user1.gender,
            user1.sleep_schedule,
            user1.personality_type,
            user1.social_battery,
            user1.confrontational_behavior,
            user1.religion,
            user1.drug_use,
            user1.activities,
            user1.busy,
            user1.significant_other,
            user1.major,
            user1.year,
            user1.snore,
            user1.values_in_roommate,
            user1.primary_focus
        )
        cursor.execute(insert_query, data)
        conn.commit()
        st.write("Your profile has been saved to the database.")
    except Exception as e:
        st.write(f"An error occurred while saving user profile: {e}")
    finally:
        cursor.close()
        conn.close()

def get_all_user_profiles():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        select_query = "SELECT * FROM User_Profiles"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        user_profiles = []
        for row in rows:
            user_profile = UserProfile(
                name=row[1],
                email_or_instagram=row[2],
                cleanliness=row[3],
                age=row[4],
                gender=row[5],
                sleep_schedule=row[6],
                personality_type=row[7],
                social_battery=row[8],
                confrontational_behavior=row[9],
                religion=row[10],
                drug_use=row[11],
                activities=row[12],
                busy=row[13],
                significant_other=row[14],
                major=row[15],
                year=row[16],
                snore=row[17],
                values_in_roommate=row[18],
                primary_focus=row[19]
            )
            user_profiles.append(user_profile)
        return user_profiles
    except Exception as e:
        st.write(f"An error occurred while retrieving user profiles: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
def get_weights(max_attempts=3):
    """Prompts the user to enter weights for each criterion with a better user experience."""
    default_weights = {
        "personality": 0.25, "confrontational": 0.25, "religion": 0.25, "sleep_schedule": 0.5,
        "age": 0.0, "drug_use": 0.25, "social_preference": 1.25, "activities": 1.25,
        "busy": 0.5, "significant_other": 0.25, "major": 0.5, "year": 1.25,
        "snore": 0.25, "values_in_roommate": 0.75, "primary_focus": 0.75
    }
    
    criteria = list(default_weights.keys())
    print("Assign a weight to each question (total must sum to 10). Suggested defaults shown in parentheses.")
    
    for attempt in range(max_attempts):
        weights = {}
        total_weight = 0.0
        remaining_weight = 10.0  # Start with 10 as the total weight

        for criterion in criteria:
            while True:
                print(f"\nCurrent total: {total_weight}, Remaining: {remaining_weight}")
                try:
                    weight = input(f"Enter weight for {criterion} (default: {default_weights[criterion]}): ")
                    weight = float(weight) if weight else default_weights[criterion]  # Use default if blank
                    
                    if weight < 0:
                        print("Weight must be a non-negative number.")
                    elif weight > remaining_weight:
                        print(f"Weight exceeds remaining limit. You can only assign up to {remaining_weight}.")
                    else:
                        weights[criterion] = weight
                        total_weight += weight
                        remaining_weight -= weight  # Update remaining weight
                        break
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")
        
        # Check if the total weight is exactly 10
        if round(total_weight, 2) == 10:
            return weights
        else:
            print(f"\nAttempt {attempt + 1} of {max_attempts} failed. Total weight was {total_weight}. Please try again.\n")
    
    print("Max attempts reached. Reverting to default weights.")
    return default_weights

def calculate_compatibility(user1, user2, weights=None):
    """
    Calculates compatibility score between two users based on various criteria.
    Uses provided weights if available, otherwise defaults to pre-defined weights.
    """
    # Default weights if none are provided
    default_weights = {
        "personality": 0.25, "confrontational": 0.25, "religion": 0.25, "sleep_schedule": 0.5,
        "age": 0.0, "drug_use": 0.25, "social_preference": 1.25, "activities": 1.25,
        "busy": 0.5, "significant_other": 0.25, "major": 0.5, "year": 1.25,
        "snore": 0.25, "values_in_roommate": 0.75, "primary_focus": 0.75
    }
    
    # Use default weights if none are provided
    weights = weights if weights else default_weights

    # Compatibility score for each attribute comparison
    scores = {
        "personality": 1 if user1.personality_type == user2.personality_type else 0,
        "confrontational": 1 if user1.confrontational_behavior == user2.confrontational_behavior else 0,
        "religion": 1 if user1.religion == user2.religion else 0,
        "sleep_schedule": 1 if user1.sleep_schedule == user2.sleep_schedule else 0,
        "age": 1 if abs(user1.age - user2.age) <= 10 else 0,
        "drug_use": 1 if user1.drug_use == user2.drug_use else 0,
        "social_preference": 1 if user1.social_battery == user2.social_battery else 0,
        "activities": 1 if user1.activities == user2.activities else 0,
        "busy": 1 if user1.busy == user2.busy else 0,
        "significant_other": 1 if user1.significant_other == user2.significant_other else 0,
        "major": 1 if user1.major == user2.major else 0,
        "year": 1 if user1.year == user2.year else 0,
        "snore": 1 if user1.snore == user2.snore else 0,
        "values_in_roommate": 1 if user1.values_in_roommate == user2.values_in_roommate else 0,
        "primary_focus": 1 if user1.primary_focus == user2.primary_focus else 0,
    }

    # Calculate the weighted compatibility score
    weighted_score = sum(scores[key] * weights[key] for key in scores)
    compatibility_score = (weighted_score / sum(weights.values())) * 100  # Normalize by total weight for percentage

    return round(compatibility_score, 2)  # Return the score rounded to two decimal places

def find_and_display_top_matches(current_user, potential_roommates, top_n=5):
    matches = []
    for roommate in potential_roommates:
        compatibility_score = calculate_compatibility(current_user, roommate)
        matches.append((roommate, compatibility_score))

    # Sort matches by compatibility score in descending order
    matches.sort(key=lambda x: x[1], reverse=True)

    # Display the top N matches
    st.subheader("Top Matches")
    if matches:
        for roommate, score in matches[:top_n]:
            st.write(f"Name: {roommate.name}")
            st.write(f"Contact: {roommate.email_or_instagram}")
            st.write(f"Compatibility Score: {score}")
            st.write("---")
    else:
        st.write("No matches currently.")




import streamlit as st

# Define UserProfile class
class UserProfile:
    def __init__(self, name, email_or_instagram, cleanliness, age, gender, sleep_schedule, personality_type, social_battery, confrontational_behavior, religion, drug_use, activities, busy, significant_other, major, year, snore, values_in_roommate, primary_focus):
        self.name = name
        self.email_or_instagram = email_or_instagram
        self.cleanliness = cleanliness
        self.age = age
        self.gender = gender
        self.sleep_schedule = sleep_schedule
        self.personality_type = personality_type
        self.social_battery = social_battery
        self.confrontational_behavior = confrontational_behavior
        self.religion = religion
        self.drug_use = drug_use
        self.activities = activities
        self.busy = busy
        self.significant_other = significant_other
        self.major = major
        self.year = year
        self.snore = snore
        self.values_in_roommate = values_in_roommate
        self.primary_focus = primary_focus

import streamlit as st
import re

def get_user_profile():
    st.title("Room_Mates/The Future of Roommate Matching")
    
    # Subtitle for Alpha test notice
    st.write("### This is an Alpha test")
    st.write("Feedback to kl608260@wne.edu very much appreciated.")
    st.write("If no matches are found due to a small number of users, try again in a few days.")
    
    # Collect user inputs
    name = st.text_input("What is your name?")
    email_or_instagram = st.text_input("Please type email to be reached out to when matched:")

    # Validate email
    if email_or_instagram:
        if not re.match(r"^[a-zA-Z0-9._%+-]+@(gmail\.com|outlook\.com|.+\.edu)$", email_or_instagram):
            st.error("Please enter a valid email address ending with .edu, @gmail.com, or @outlook.com.")
            return None  # Exit the function if the email is invalid

    # Collect cleanliness preference
    cleanliness = st.selectbox(
        "How clean are you?", 
        options=[1, 2, 3], 
        format_func=lambda x: {
            1: "1: I have an assigned day weekly for deep cleaning, dishes are never in the sink, and my cleaning routine is set",
            2: "2: I take care of my room that's it and leave dishes when I am tired",
            3: "3: I clean when I feel like it or seems to be time"
        }[x]
    )

    # Collect additional user inputs
    age = st.number_input("Enter your age:", min_value=0, max_value=120)
    gender = st.selectbox("Enter your gender:", [1, 2], format_func=lambda x: "1: Male" if x == 1 else "2: Female")

    # Sleep schedule selectbox
    sleep_schedule = st.selectbox(
        "What is your sleep schedule?", 
        [1, 2], 
        format_func=lambda x: "1: I have a set time I go to sleep and wake up always" 
        if x == 1 else "2: I have no set routine, depends on how I am feeling and the day"
    )

    # Personality type dropdown with labels
    personality_type = st.selectbox(
        "Enter your Myers-Briggs personality type:",
        options=range(1, 17),
        format_func=lambda x: [
            "1: ENTJ", "2: ENTP", "3: ESFJ", "4: ESFP",
            "5: ESTJ", "6: ESTP", "7: INFJ", "8: INFP",
            "9: INTP", "10: ISFP", "11: ENFJ", "12: ENFP",
            "13: INTJ", "14: ISFJ", "15: ISTP", "16: ISTJ"
        ][x - 1]
    )

    # Social battery selectbox
    social_battery = st.selectbox(
        "What is your social preference?", 
        [1, 2, 3], 
        format_func=lambda x: {
            1: "1: No people over and don't seek out social interaction",
            2: "2: Occasionally people over and enjoy going out for dinner or drinks once a week",
            3: "3: Always people over and always wanting to go out no matter the day"
        }[x]
    )

    confrontational_behavior = st.selectbox("What is your conflict tolerance?", 
                                            [1, 2], 
                                            format_func=lambda x: "1: Confrontational" if x == 1 else "2: Non-confrontational")

    religion = st.selectbox("What is your religious influence?", 
                            [1, 2], 
                            format_func=lambda x: "1: Actively practicing" if x == 1 else "2: No impact")

    drug_use = st.selectbox("What is your stance on drug use?", 
                            [1, 2], 
                            format_func=lambda x: "1: Yes" if x == 1 else "2: No")

    activities = st.selectbox("What activities do you prefer?", 
                              [1, 2], 
                              format_func=lambda x: "1: Movement-based" if x == 1 else "2: Video games/TV")

    busy = st.selectbox("Do you plan your day?", 
                        [1, 2], 
                        format_func=lambda x: "1: Always planned" if x == 1 else "2: Go with the flow")

    significant_other = st.selectbox("Do you have a significant other?", 
                                     [1, 2], 
                                     format_func=lambda x: "1: Yes" if x == 1 else "2: No")

    major = st.selectbox("What is your major?", 
                         [1, 2, 3, 4], 
                         format_func=lambda x: {
                             1: "1: Business/Management",
                             2: "2: STEM",
                             3: "3: Health/Medicine",
                             4: "4: Arts/Humanities"
                         }[x])

    year = st.selectbox("What year are you?", 
                        [1, 2, 3, 4, 5], 
                        format_func=lambda x: {
                            1: "1: Freshman",
                            2: "2: Sophomore",
                            3: "3: Junior",
                            4: "4: Senior",
                            5: "5: Grad Student or Other"
                        }[x])

    snore = st.selectbox("Do you snore?", 
                         [1, 2], 
                         format_func=lambda x: "1: Yes" if x == 1 else "2: No")

    values_in_roommate = st.selectbox("What do you value in a roommate?", 
                                      [1, 2, 3], 
                                      format_func=lambda x: {
                                          1: "1: Supportive",
                                          2: "2: Honest/Direct",
                                          3: "3: Joint Activities"
                                      }[x])

    primary_focus = st.selectbox("What is your primary focus?", 
                                 [1, 2], 
                                 format_func=lambda x: "1: School" if x == 1 else "2: Sports/Other")

    # Place the Submit Profile button at the end
    if st.button("Submit Profile"):
        # Create and return the UserProfile object
        return UserProfile(
            name, email_or_instagram, cleanliness, age, gender, sleep_schedule,
            personality_type, social_battery, confrontational_behavior, religion,
            drug_use, activities, busy, significant_other, major, year,
            snore, values_in_roommate, primary_focus
        )
    return None

# Main function to collect profile and display compatibility results
def main():
    # Step 1: Collect user profile
    user_profile = get_user_profile()

    # Only proceed if the user has submitted the profile
    if user_profile:
        # Step 2: Retrieve all profiles from the database
        all_user_profiles = get_all_user_profiles()

        # Step 3: Check if there's already a user with the same email
        user_exists = any(user.email_or_instagram == user_profile.email_or_instagram for user in all_user_profiles)

        # Step 4: Save the profile only if it doesn't already exist
        if not user_exists:
            save_user_profile(user_profile)
        else:
            print("User profile already exists, skipping save to prevent duplication.")

        # Step 5: Exclude the current user from potential roommates
        potential_roommates = [user for user in all_user_profiles if user.email_or_instagram != user_profile.email_or_instagram]

        # Step 6: Find and display top matches
        find_and_display_top_matches(user_profile, potential_roommates)

# Ensure main() runs if the script is executed directly
if __name__ == "__main__":
    main()