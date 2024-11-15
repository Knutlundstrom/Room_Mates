
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


import streamlit as st
import re

# Define UserProfile class with new fields for enhanced matching
class UserProfile:
    def __init__(self, name, email_or_instagram, cleanliness, age, gender, sleep_schedule,
                 personality_type, social_battery, confrontational_behavior, religion,
                 drug_use, activities, busy, significant_other, major, year, snore,
                 values_in_roommate, primary_focus, communication_style, privacy_level, pets, temperature_preference):
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
        self.communication_style = communication_style
        self.privacy_level = privacy_level
        self.pets = pets
        self.temperature_preference = temperature_preference

# Function to gather user input for profile creation
def get_user_profile():
    st.title("Roommates Matching Service")
    
    # Basic Info
    name = st.text_input("What is your name?")
    email_or_instagram = st.text_input("Enter preferred contact (email, Instagram, etc.):")

    # Questions with standardized numeric responses
    cleanliness = st.selectbox("How clean are you?", [1, 2, 3], format_func=lambda x: {
        1: "Very clean, routine",
        2: "Moderate, clean when needed",
        3: "Minimal cleaning"
    }[x])

    age = st.number_input("Enter your age:", min_value=0, max_value=120)
    gender = st.selectbox("Gender:", [1, 2], format_func=lambda x: "Male" if x == 1 else "Female")

    sleep_schedule = st.selectbox("What is your sleep schedule?", [1, 2], format_func=lambda x: {
        1: "Consistent bedtime/wake time",
        2: "Flexible, varies by day"
    }[x])

    personality_type = st.selectbox("Myers-Briggs personality type:", range(1, 17), format_func=lambda x: [
        "ENTJ", "ENTP", "ESFJ", "ESFP", "ESTJ", "ESTP", "INFJ", "INFP", "INTP", "ISFP",
        "ENFJ", "ENFP", "INTJ", "ISFJ", "ISTP", "ISTJ"
    ][x - 1])

    social_battery = st.selectbox("Social preference?", [1, 2, 3], format_func=lambda x: {
        1: "Minimal interaction, no guests",
        2: "Occasional social gatherings",
        3: "Very social, frequent guests"
    }[x])

    confrontational_behavior = st.selectbox("Conflict tolerance?", [1, 2], format_func=lambda x: "Direct" if x == 1 else "Avoids confrontation")

    religion = st.selectbox("Religious influence?", [1, 2], format_func=lambda x: "Actively practicing" if x == 1 else "No impact")

    drug_use = st.selectbox("Drug use?", [1, 2, 3], format_func=lambda x: {
        1: "Comfortable with frequent use",
        2: "Occasionally okay",
        3: "Not comfortable"
    }[x])

    activities = st.selectbox("Preferred activities?", [1, 2], format_func=lambda x: "Active" if x == 1 else "Relaxed")

    busy = st.selectbox("Daily planning?", [1, 2], format_func=lambda x: "Planned" if x == 1 else "Spontaneous")

    significant_other = st.selectbox("Significant other visits?", [1, 2, 3], format_func=lambda x: {
        1: "Yes, frequently",
        2: "Occasionally",
        3: "No"
    }[x])

    major = st.selectbox("What is your major?", [1, 2, 3, 4], format_func=lambda x: {
        1: "Business/Management",
        2: "STEM",
        3: "Health/Medicine",
        4: "Arts/Humanities"
    }[x])

    year = st.selectbox("School year?", [1, 2, 3, 4, 5], format_func=lambda x: {
        1: "Freshman",
        2: "Sophomore",
        3: "Junior",
        4: "Senior",
        5: "Graduate"
    }[x])

    snore = st.selectbox("Do you snore?", [1, 2], format_func=lambda x: "Yes" if x == 1 else "No")

    values_in_roommate = st.selectbox("Values in roommate?", [1, 2, 3], format_func=lambda x: {
        1: "Supportive",
        2: "Honest/Direct",
        3: "Shared activities"
    }[x])

    primary_focus = st.selectbox("Primary focus?", [1, 2], format_func=lambda x: "School" if x == 1 else "Sports/Other")

    # Additional preference questions
    communication_style = st.selectbox("Communication style?", [1, 2], format_func=lambda x: "Direct" if x == 1 else "Indirect")

    privacy_level = st.selectbox("Privacy level?", [1, 2, 3], format_func=lambda x: {
        1: "Very private",
        2: "Moderately private",
        3: "Open"
    }[x])

    pets = st.selectbox("Comfortable with pets?", [1, 2, 3], format_func=lambda x: {
        1: "Comfortable with pets",
        2: "No preference",
        3: "Not comfortable"
    }[x])

    temperature_preference = st.selectbox("Temperature preference?", [1, 2, 3], format_func=lambda x: {
        1: "Cooler",
        2: "Warmer",
        3: "No preference"
    }[x])

    # Submit profile creation
    if st.button("Submit Profile"):
        return UserProfile(
            name, email_or_instagram, cleanliness, age, gender, sleep_schedule,
            personality_type, social_battery, confrontational_behavior, religion,
            drug_use, activities, busy, significant_other, major, year,
            snore, values_in_roommate, primary_focus,
            communication_style, privacy_level, pets, temperature_preference
        )
    return None

# Compatibility calculation with additional attributes
def calculate_compatibility(user1, user2, weights=None):
    # Default weights with new attributes included
    default_weights = {
    "personality": 0.25, 
    "confrontational": 0.25, 
    "religion": 0.25, 
    "sleep_schedule": 0.75,  # Increased from 0.5 to 0.75
    "age": 0.0, 
    "drug_use": 0.25, 
    "social_preference": 1.25, 
    "activities": 1.25,
    "busy": 0.5, 
    "significant_other": 0.25, 
    "major": 0.5, 
    "year": 1.25,
    "snore": 0.25, 
    "values_in_roommate": 0.75, 
    "primary_focus": 0.75,
    "communication_style": 0.5, 
    "privacy_level": 0.5, 
    "pets": 0.0,  # Set to 0
    "temperature_preference": 0.5
}


    # Use provided weights or default
    weights = weights if weights else default_weights

    # Compatibility for each attribute
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
        "communication_style": 1 if user1.communication_style == user2.communication_style else 0,
        "privacy_level": 1 if user1.privacy_level == user2.privacy_level else 0,
        "pets": 1 if user1.pets == user2.pets else 0,
        "temperature_preference": 1 if user1.temperature_preference == user2.temperature_preference else 0
    }

    # Calculate weighted compatibility score
    weighted_score = sum(scores[key] * weights[key] for key in scores)
    compatibility_score = (weighted_score / sum(weights.values())) * 100  # Normalize to percentage

    return round(compatibility_score, 2)  # Rounded to 2 decimal places



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
import re

# Define UserProfile class with new fields
class UserProfile:
    def __init__(self, name, email_or_instagram, cleanliness, age, gender, sleep_schedule, 
                 personality_type, social_battery, confrontational_behavior, religion,
                 drug_use, activities, busy, significant_other, major, year, snore,
                 values_in_roommate, primary_focus, communication_style, privacy_level, pets, temperature_preference):
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
        self.communication_style = communication_style
        self.privacy_level = privacy_level
        self.pets = pets
        self.temperature_preference = temperature_preference


def get_user_profile():
    st.title("Room_Mates/The Future of Roommate Matching")
    
    # Basic Info
    name = st.text_input("What is your name?")
    email_or_instagram = st.text_input("Please type your contact info for matches:")

    # Email validation
    if email_or_instagram and not re.match(r"^[a-zA-Z0-9._%+-]+@(gmail\.com|outlook\.com|.+\.edu)$", email_or_instagram):
        st.error("Please enter a valid email address ending with .edu, @gmail.com, or @outlook.com.")
        return None  # Exit function if email invalid

    # Roommate Preference Questions
    cleanliness = st.selectbox("How clean are you?", [1, 2, 3], 
                               format_func=lambda x: {1: "Very clean", 2: "Moderate", 3: "Minimal"}[x])

    age = st.number_input("Enter your age:", min_value=0, max_value=120)
    gender = st.selectbox("Enter your gender:", [1, 2], format_func=lambda x: "Male" if x == 1 else "Female")
    sleep_schedule = st.selectbox("What is your sleep schedule?", [1, 2], 
                                  format_func=lambda x: {1: "Consistent", 2: "Flexible"}[x])
    personality_type = st.selectbox("Myers-Briggs personality type:", range(1, 17), 
                                    format_func=lambda x: [
                                        "ENTJ", "ENTP", "ESFJ", "ESFP", "ESTJ", "ESTP", "INFJ", "INFP", 
                                        "INTP", "ISFP", "ENFJ", "ENFP", "INTJ", "ISFJ", "ISTP", "ISTJ"
                                    ][x - 1])
    social_battery = st.selectbox("Social preference?", [1, 2, 3], 
                                  format_func=lambda x: {1: "Minimal", 2: "Occasional gatherings", 3: "Very social"}[x])
    confrontational_behavior = st.selectbox("Conflict tolerance?", [1, 2], 
                                            format_func=lambda x: "Direct" if x == 1 else "Avoids conflict")
    religion = st.selectbox("Religious influence?", [1, 2], 
                            format_func=lambda x: "Practicing" if x == 1 else "No impact")
    drug_use = st.selectbox("Drug use?", [1, 2, 3], 
                            format_func=lambda x: {1: "Comfortable with frequent use", 2: "Occasionally okay", 3: "Not comfortable"}[x])
    activities = st.selectbox("Preferred activities?", [1, 2], 
                              format_func=lambda x: "Active" if x == 1 else "Relaxed")
    busy = st.selectbox("Daily planning?", [1, 2], format_func=lambda x: "Planned" if x == 1 else "Spontaneous")
    significant_other = st.selectbox("Significant other visits?", [1, 2, 3], 
                                     format_func=lambda x: {1: "Frequently", 2: "Occasionally", 3: "No"}[x])
    major = st.selectbox("What is your major?", [1, 2, 3, 4], 
                         format_func=lambda x: {1: "Business", 2: "STEM", 3: "Health", 4: "Arts"}[x])
    year = st.selectbox("Year in school?", [1, 2, 3, 4, 5], 
                        format_func=lambda x: {1: "Freshman", 2: "Sophomore", 3: "Junior", 4: "Senior", 5: "Graduate"}[x])
    snore = st.selectbox("Do you snore?", [1, 2], format_func=lambda x: "Yes" if x == 1 else "No")
    values_in_roommate = st.selectbox("Values in roommate?", [1, 2, 3], 
                                      format_func=lambda x: {1: "Supportive", 2: "Direct", 3: "Shared activities"}[x])
    primary_focus = st.selectbox("Primary focus?", [1, 2], format_func=lambda x: "School" if x == 1 else "Sports/Other")
    communication_style = st.selectbox("Communication style?", [1, 2], format_func=lambda x: "Direct" if x == 1 else "Indirect")
    privacy_level = st.selectbox("Privacy level?", [1, 2, 3], 
                                 format_func=lambda x: {1: "Very private", 2: "Moderate", 3: "Open"}[x])
    pets = st.selectbox("Comfortable with pets?", [1, 2, 3], 
                        format_func=lambda x: {1: "Comfortable", 2: "No preference", 3: "Not comfortable"}[x])
    temperature_preference = st.selectbox("Temperature preference?", [1, 2, 3], 
                                          format_func=lambda x: {1: "Cool", 2: "Warm", 3: "No preference"}[x])

    if st.button("Submit Profile"):
        return UserProfile(
            name, email_or_instagram, cleanliness, age, gender, sleep_schedule,
            personality_type, social_battery, confrontational_behavior, religion,
            drug_use, activities, busy, significant_other, major, year,
            snore, values_in_roommate, primary_focus, 
            communication_style, privacy_level, pets, temperature_preference
        )

if st.button("Submit Profile"):
    # Create the UserProfile instance
    user_profile = UserProfile(
        name, email_or_instagram, cleanliness, age, gender, sleep_schedule,
        personality_type, social_battery, confrontational_behavior, religion,
        drug_use, activities, busy, significant_other, major, year,
        snore, values_in_roommate, primary_focus, 
        communication_style, privacy_level, pets, temperature_preference
    )

    # Save the profile to the database directly here
    try:
        # Establish a database connection
        conn = connect_db()
        cursor = conn.cursor()

        # SQL Insert query
        insert_query = """
        INSERT INTO user_profiles (
            name, email_or_instagram, cleanliness, age, gender, sleep_schedule,
            personality_type, social_battery, confrontational_behavior, religion,
            drug_use, activities, busy, significant_other, major, year, snore,
            values_in_roommate, primary_focus, communication_style, privacy_level, pets, temperature_preference
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        # Execute the query with user profile data
        cursor.execute(insert_query, (
            user_profile.name, user_profile.email_or_instagram, user_profile.cleanliness, user_profile.age,
            user_profile.gender, user_profile.sleep_schedule, user_profile.personality_type,
            user_profile.social_battery, user_profile.confrontational_behavior, user_profile.religion,
            user_profile.drug_use, user_profile.activities, user_profile.busy,
            user_profile.significant_other, user_profile.major, user_profile.year,
            user_profile.snore, user_profile.values_in_roommate, user_profile.primary_focus,
            user_profile.communication_style, user_profile.privacy_level, user_profile.pets,
            user_profile.temperature_preference
        ))

        # Commit changes to the database
        conn.commit()
        st.success("Your profile has been saved successfully.")

    except Exception as e:
        # Handle any exceptions during database operations
        st.error(f"Error saving user profile: {e}")

    finally:
        # Ensure resources are properly closed
        cursor.close()
        conn.close()

# If the profile was not submitted, return None
return None


# Updated function to find and display top matches with new fields
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

def calculate_compatibility(user1, user2, weights=None):
    default_weights = {
        "personality": 0.25, "confrontational": 0.25, "religion": 0.25, "sleep_schedule": 0.5,
        "age": 0.0, "drug_use": 0.25, "social_preference": 1.25, "activities": 1.25,
        "busy": 0.5, "significant_other": 0.25, "major": 0.5, "year": 1.25,
        "snore": 0.25, "values_in_roommate": 0.75, "primary_focus": 0.75,
        "communication_style": 0.5, "privacy_level": 0.5, "pets": 0.5, "temperature_preference": 0.5
    }

    weights = weights if weights else default_weights
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
        "communication_style": 1 if user1.communication_style == user2.communication_style else 0,
        "privacy_level": 1 if user1.privacy_level == user2.privacy_level else 0,
        "pets": 1 if user1.pets == user2.pets else 0,
        "temperature_preference": 1 if user1.temperature_preference == user2.temperature_preference else 0
    }

    # Calculate weighted compatibility score
    weighted_score = sum(scores[key] * weights[key] for key in scores)
    compatibility_score = (weighted_score / sum(weights.values())) * 100  # Normalize to percentage

    return round(compatibility_score, 2)

# Main function to collect profile and display compatibility results
def main():
    # Step 1: Collect user profile
    user_profile = get_user_profile()

    if user_profile:
        # Step 2: Retrieve all profiles from the database
        all_user_profiles = get_all_user_profiles()

        # Step 3: Exclude the current user from potential roommates
        potential_roommates = [user for user in all_user_profiles if user.email_or_instagram != user_profile.email_or_instagram]

        # Step 4: Find and display top matches
def get_all_user_profiles():
    # Establish a database connection
    conn = connect_db()
    cursor = conn.cursor()
    
    # Execute a query to retrieve all user profiles
    query = """
    SELECT name, email_or_instagram, cleanliness, age, gender, sleep_schedule,  
           personality_type, social_battery, confrontational_behavior, religion,
           drug_use, activities, busy, significant_other, major, year, snore,
           values_in_roommate, primary_focus, communication_style, privacy_level, pets, temperature_preference
    FROM user_profiles;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Close the database connection
    cursor.close()
    conn.close()

    # Map database rows to UserProfile instances
    user_profiles = [UserProfile(*row) for row in rows]
    return user_profiles

def main():
    # Step 1: Collect user profile
    user_profile = get_user_profile()

    if user_profile:
        # Step 2: Retrieve all profiles from the database
        all_user_profiles = get_all_user_profiles()

        # Step 3: Exclude the current user from potential roommates
        potential_roommates = [user for user in all_user_profiles if user.email_or_instagram != user_profile.email_or_instagram]

        # Step 4: Find and display top matches
        find_and_display_top_matches(user_profile, potential_roommates)

if __name__ == "__main__":
    main()
