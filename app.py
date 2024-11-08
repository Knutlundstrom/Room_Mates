
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

def calculate_compatibility(user1, user2):
    # Updated weights for higher priority factors (ensuring total weight sums to 10 for 0-10 scaling)
    personality_weight = 0.5
    confrontational_weight = 0.25
    religion_weight = 0.25
    sleep_schedule_weight = 0.5
    age_weight = 0.25
    drug_use_weight = 0.25
    social_preference_weight = 1.5  # Higher weight
    activities_weight = 1.5  # Higher weight
    busy_weight = 0.5
    significant_other_weight = 0.25
    major_weight = 0.5
    year_weight = 1.5  # Higher weight
    snore_weight = 0.25
    values_in_roommate_weight = 1.5  # Higher weight
    primary_focus_weight = 1.5  # Higher weight

    # Compatibility scores for each factor (1 if match, 0 if not)
    personality_score = 1 if user1.personality_type == user2.personality_type else 0
    confrontational_score = 1 if user1.confrontational_behavior == user2.confrontational_behavior else 0
    religion_score = 1 if user1.religion == user2.religion else 0
    sleep_schedule_score = 1 if user1.sleep_schedule == user2.sleep_schedule else 0
    age_score = 1 if abs(user1.age - user2.age) <= 10 else 0  # Similar age within a 10-year range
    drug_use_score = 1 if user1.drug_use == user2.drug_use else 0
    social_preference_score = 1 if user1.social_battery == user2.social_battery else 0
    activities_score = 1 if user1.activities == user2.activities else 0
    busy_score = 1 if user1.busy == user2.busy else 0
    significant_other_score = 1 if user1.significant_other == user2.significant_other else 0
    major_score = 1 if user1.major == user2.major else 0
    year_score = 1 if user1.year == user2.year else 0
    snore_score = 1 if user1.snore == user2.snore else 0
    values_in_roommate_score = 1 if user1.values_in_roommate == user2.values_in_roommate else 0
    primary_focus_score = 1 if user1.primary_focus == user2.primary_focus else 0

    # Calculate the weighted sum of all compatibility scores
    weighted_score = (
        (personality_score * personality_weight) +
        (confrontational_score * confrontational_weight) +
        (religion_score * religion_weight) +
        (sleep_schedule_score * sleep_schedule_weight) +
        (age_score * age_weight) +
        (drug_use_score * drug_use_weight) +
        (social_preference_score * social_preference_weight) +
        (activities_score * activities_weight) +
        (busy_score * busy_weight) +
        (significant_other_score * significant_other_weight) +
        (major_score * major_weight) +
        (year_score * year_weight) +
        (snore_score * snore_weight) +
        (values_in_roommate_score * values_in_roommate_weight) +
        (primary_focus_score * primary_focus_weight)
    )

    # Scale the compatibility score to a range of 0 to 100
    compatibility_score = weighted_score * 10  # since the total weight sums to 10

    return round(compatibility_score, 2)

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

def get_user_profile():
    st.title("Room_Mates/The Future of Roommate Matching")
    
    # Subtitle for Alpha test notice
    st.write("### This is an Alpha test")
    st.write("Feedback to kl608260@wne.edu very much appreciated.")
    st.write("If no matches are found due to a small number of users, try again in a few days.")
    
    # Collect user inputs
    name = st.text_input("What is your name?")
    email_or_instagram = st.text_input("Please type email, Instagram, or preferred way to be reached out to when matched:")

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

    age = st.number_input("Enter your age:", min_value=0, max_value=120)

    gender = st.selectbox("Enter your gender:", [1, 2], format_func=lambda x: "1: Male" if x == 1 else "2: Female")

    sleep_schedule = st.selectbox("What is your sleep schedule?", 
                                  [1, 2], 
                                  format_func=lambda x: "1: I have a set time I go to sleep and wake up always" if x == 1 else "2: I have no set routine, depends on how I am feeling and the day")

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

    social_battery = st.selectbox("What is your social preference?", 
                                  [1, 2, 3], 
                                  format_func=lambda x: {
                                      1: "1: No people over and don't seek out social interaction",
                                      2: "2: Occasionally people over and enjoy going out for dinner or drinks once a week",
                                      3: "3: Always people over and always wanting to go out no matter the day"
                                  }[x])

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
        # Step 2: Save the user profile to the database
        save_user_profile(user_profile)

        # Step 3: Retrieve all profiles from the database
        all_user_profiles = get_all_user_profiles()

        # Step 4: Exclude the current user from potential roommates
        potential_roommates = [user for user in all_user_profiles if user.email_or_instagram != user_profile.email_or_instagram]

        # Step 5: Find and display top matches
        find_and_display_top_matches(user_profile, potential_roommates)

# Ensure main() runs if the script is executed directly
if __name__ == "__main__":
    main()

