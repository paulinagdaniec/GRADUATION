import json
from collections import defaultdict
from streamlit_lottie import st_lottie
import streamlit as st
import pandas as pd
import base64
import os
import csv
import random



# streamlit intro 
def load_lottiefile(filepath:str):
    with open(filepath, "r") as f:
        return json.load(f)

hi = load_lottiefile("hi.json")

st_lottie(
    hi, 
    loop = True, 
    height=350, 
    key="hi")


st.write ("this is the second prototype of a font recommender system. Your input and feedback will be used for further developement. Thank you for your time and enjoy! 💙 ")



st.subheader(
    "We are here to help you find and manage suitable fonts that support the message and feel you want to convey in your design. No more scrolling through thousands of fonts to find the right one.")

# Ask user for name
col1, col2 = st.columns(2)

with col1:
    user_name = st.text_input("Please enter your name")
with col2:
    project_name = st.text_input("Please enter your project name")

hi = load_lottiefile("girl-selection.json")

st_lottie(
    hi, 
    loop = True, 
    height=350, 
    key= "selection")

# characteristic selection

st.subheader(" Review feels and select suitable category.")

st.markdown('###')

# Load the CSV file
csv_file = "avfonts_full2.csv"
df = pd.read_csv(csv_file)

feels_all = {
    'sans-serif': 'modern, clean, open, informal, progressive, simple, minimal, contemporary',
    'display': 'bold, creative, eye-catching, decorative, playful, attention-grabbing, unique',
    'serif': 'traditional, elegant, trustworthy, formal, classic, established, reliable',
    'handwriting': 'personal, friendly, whimsical, expressive, elegant, romantic, feminine',
    'monospace': 'technical, precise, retro, futuristic, minimal, structured',
}


col1, col2, col3, col4, col5 = st.columns(5)

# change pictures

with col1:
    st.image('sans serif.png',use_column_width=False,caption='Sans-Serif')

with col2:
    st.image('display.png',use_column_width=False, caption='Display')

with col3:
    st.image('serif.png',use_column_width=False, caption='Serif')

with col4:
    st.image('handwriting.png',use_column_width=False,caption='Handwriting')

with col5:
    st.image('monospace.png',use_column_width=False, caption='Monospace')

categories = ['sans-serif', 'display','serif', 'handwriting', 'monospace']


matched_character = st.selectbox("Most suitable category per feels", categories)

selected_feels = feels_all[matched_character]
 
st.write('Associated feels:', selected_feels)


font_list = []


# Filter the DataFrame based on the 'Category' column, the selected character, and the selected weights
filtered_df = df[(df['Category'] == matched_character)]
# Store the available fonts in font_list
font_list = filtered_df['available_fonts'].tolist()

# Add ".ttf" to each font in the 'available_fonts' column
df['available_fonts'] = df['available_fonts'].apply(lambda fonts: fonts.split(",")[0] + ".ttf")

# Filter the DataFrame based on the 'Category' column and the selected character
filtered_df = df[df['Category'] == matched_character]

# Store the available fonts in font_list
font_list = filtered_df['available_fonts'].tolist()


hi = load_lottiefile("arrow-blue.json")

st_lottie(
    hi, 
    loop = True, 
    height=200, 
    key="arrow")

st.subheader("Let's visualise it!")
st.write(
    "Here you can input a piece of text or simply a word you would like to try out. You can like, dislike and save fonts to your library. We will use your feedback to recommend fonts that you will like.")

# Define a CSS style with white text color
css = """
    <style>
        .mytext {
            color: {color};
            font-size: 50px;
            font-weight: {weight}
        }
    </style>
"""

# Display the CSS style
st.markdown(css, unsafe_allow_html=True)


# Define a function to generate a random font style but from the criteria user selected
def get_random_font(text=None):
    random_font = random.choice(font_list)
    font_dir = "/Users/paulinagdaniec/Desktop/State of the art tech/collectedttf"
    font_file = os.path.join(font_dir, random_font)
    font_data = open(font_file, "rb").read()
    font_b64 = base64.b64encode(font_data).decode()
    font_style = f"""
        <style>
            @font-face {{
                font-family: myfont;
                src: url('data:application/font-ttf;charset=utf-8;base64,{font_b64}');
            }}
            .mytext {{
                font-family: myfont;
                color: {color};
                font-size: 50px;
                font-weight: {weight}
            }}
        </style>
    """
    if text:
        # Generate a new font style with the input text
        font_style = f"""
            <style>
                @font-face {{
                    font-family: myfont;
                    src: url('data:application/font-ttf;charset=utf-8;base64,{font_b64}');
                }}
                .mytext {{
                    font-family: myfont;
                    color: {color};
                    font-size: 50px;
                    font-weight: {weight};
                }}
            </style>
        """
        # Display the input text with the custom font
        html = f'<span class="mytext">{text}</span>'
        return font_style, html, random_font

    return font_style, random_font


def show_font(font, text):
    font_dir = "/Users/paulinagdaniec/Desktop/State of the art tech/collectedttf"
    font_file = os.path.join(font_dir, font)
    font_data = open(font_file, "rb").read()
    font_b64 = base64.b64encode(font_data).decode()
    font_style = f"""
        <style>
            @font-face {{
                font-family: myfont;
                src: url('data:application/font-ttf;charset=utf-8;base64,{font_b64}');
            }}
            .mytext {{
                font-family: myfont;
                color: {color};
                font-size: 50px;
                font-weight: {weight}
            }}
        </style>
    """
    # Display the input text with the custom font
    html = f'<span class="mytext">{text}</span>'
    return font_style, html


def save_to_csv(user, project_name, font, feels, text, liked, disliked, skipped, saved, times_used, feedback=False):
    filename = "user_input3.csv"
    headers = ["User Name", "Project Name", "Selected Font", "Feels", "Text","Liked", "Disliked", "Skipped", "Saved", "Times Used"]
    mode = "a" if os.path.exists(filename) else "w"
    with open(filename, mode, newline="") as f:
        writer = csv.writer(f)
        if mode == "w":
            writer.writerow(headers)
        writer.writerow([user, project_name, font, feels, text, liked, disliked, skipped, saved, times_used])

    if liked or disliked:
        st.success("Thanks for the feedback!")
    elif skipped:
        st.success("Font skipped! You can revisit it later.")
    elif saved:
        st.success("Font saved successfully to your library!")




# Display the user inputted text with a random font
user_text = st.text_input("Enter your text & press enter")

color = st.color_picker("Pick a color", "#ffffff")

# only jump with values of 100 in the streamlit slider
weight = st.slider(
    'Select a prefered font weight',
    100, 900, (400, 600), step=100) 
    
st.write('Values:', weight)



# Now let's start font recommendations

df = filtered_df


def parse_designer(designer):
    try:
        return json.loads(designer.replace("'", '"'))
    except:
        return None


replace = str.maketrans("", "", "{}'")
df["keywords"] = df["keywords"].apply(lambda x: set(x.translate(replace).split(", ")))
df["weights"] = df["weights"].apply(lambda x: x.split(","))
df["styles"] = df["styles"].apply(lambda x: json.loads(x.replace("'", '"')))
df["connotations"] = df["connotations"].apply(lambda x: x.split(", "))
df["designer"] = df["designer"].astype(str).apply(parse_designer)


def rate_fonts(df, liked, disliked):
    keyword_ratings_factor = 10
    designer_ratings_factor = 1
    connotation_ratings_factor = 1.5
    year_factor = 0.1

    keyword_ratings = defaultdict(int)
    for entry in liked["keywords"]:
        for kw in entry:
            keyword_ratings[kw] += 1

    for entry in disliked["keywords"]:
        for kw in entry:
            keyword_ratings[kw] -= 1

    designer_ratings = defaultdict(int)
    for entry in liked["designer"]:
        if entry is None:
            continue
        for d in entry:
            designer_ratings[d] += 1

    for entry in disliked["designer"]:
        if entry is None:
            continue
        for d in entry:
            designer_ratings[d] -= 1

    connotation_ratings = defaultdict(int)
    for entry in liked["connotations"]:
        for c in entry:
            connotation_ratings[c] += 1

    for entry in disliked["connotations"]:
        for c in entry:
            connotation_ratings[c] -= 1

    liked_year_avg = liked["year"].mean()
    disliked_year_avg = disliked["year"].mean()
    middle_year = (liked_year_avg + disliked_year_avg) / 2

# diviiding by 1000 to make the ratings more reasonable and take into account user preferences rather than popularity of the font
    def rate_font(row):
        rating = 0
        for kw in row["keywords"]:
            rating += keyword_ratings[kw] * keyword_ratings_factor
        for d in row["designer"] if row["designer"] is not None else []:
            rating += designer_ratings[d] * designer_ratings_factor
        for c in row["connotations"]:
            rating += connotation_ratings[c] * connotation_ratings_factor

        rating += (row["year"] - middle_year) * year_factor

        rating -= row["rating"] / 1000
        return rating

    df["rating"] = df.apply(rate_font, axis=1)

    return df.sort_values("rating", ascending=False)

df1 = pd.read_csv("avfonts_full2.csv")

# Load ratings from the CSV file
user_input = pd.read_csv("user_input3.csv")
liked = user_input[user_input["Liked"] == True]["Selected Font"].str.replace(".ttf", "")
disliked = user_input[user_input["Disliked"] == True]["Selected Font"].str.replace(".ttf", "")
skipped = user_input[user_input["Skipped"] == True]["Selected Font"].str.replace(".ttf", "")


# set times_used to 0
times_used = 0

print(f"liked: {user_input}")

liked_entries = pd.DataFrame(columns=df.columns)
for font in liked:
    liked_entries = liked_entries.append(df.loc[df["available_fonts"].str.contains(font)])

disliked_entries = pd.DataFrame(columns=df.columns)
for font in disliked:
    disliked_entries = disliked_entries.append(df.loc[df["available_fonts"].str.contains(font)])

skipped_entries = pd.DataFrame(columns=df.columns)
for font in skipped:
    skipped_entries = skipped_entries.append(df.loc[df["available_fonts"].str.contains(font)])

r = rate_fonts(df, liked_entries, disliked_entries)


print(liked_entries)

# liked_entries to csv
liked_entries.to_csv("liked_entries.csv", index=False)

print(disliked_entries)
# Remove elements of r that are already in liked or disliked
if not liked_entries.empty:
    r = r[~r["family"].isin(liked_entries["family"])]
if not disliked_entries.empty:
    r = r[~r["family"].isin(disliked_entries["family"])]

if not skipped_entries.empty:
    r = r[~r["family"].isin(skipped_entries["family"])]


print(r["available_fonts"][r["available_fonts"].first_valid_index()])
next_font = r["available_fonts"][r["available_fonts"].first_valid_index()].split(",")[0]
font_name = next_font.replace(".ttf", "")

if user_text:
    # Generate a random font style ( filtered ) and display it
    font_style, text_html = show_font(next_font, user_text)
    st.markdown(font_style, unsafe_allow_html=True)

    # Display the font name and input text with the custom font
    st.write(f"Using font: {font_name}")
    st.markdown(text_html, unsafe_allow_html=True)


    # Create columns for the buttons
    col1, col2, col3, col4 = st.columns(4)

    # Add the "Like" button in the first column
    liked = col1.button("👍🏼 Like")

    # Add the "Dislike" button in the second column
    disliked = col2.button("👎🏼 Dislike")

    # Add the "Skip" button in the third column
    skipped = col3.button("⏭️ Skip")

    # If either "Like", "Dislike" or "Skipped" button is clicked, save the font to the CSV file
    if liked or disliked or skipped:
        save_to_csv(user_name, project_name, font_name, selected_feels, user_text, liked, disliked, skipped, False, times_used, feedback=True)


    # Add a "Save" button to store the input text and font to a CSV file in the third column
    if col4.button(" 🖤 Save to library"):
        save_to_csv(user_name,project_name, font_name,selected_feels, user_text,  False, False, False, True, times_used)



# Display the user's saved fonts

library = pd.read_csv("user_input3.csv")


# Filter the dataframe based on user's name
user_preferences = library[library["User Name"] == user_name]



# Filter for saved fonts where both Liked and Disliked columns are False

saved_fonts = user_preferences[(user_preferences["Liked"] == False) & (user_preferences["Disliked"] == False)]



# Create buttons to display saved fonts and preferences
show_saved = st.button("View your library & preferences", key="saved")


if show_saved:
    # Display the filtered dataframe - editable
    if not user_preferences.empty:
        edited_df = st.experimental_data_editor(user_preferences)
        favorite_font = edited_df.loc[edited_df["Times Used"].idxmax()]["Selected Font"]
        st.markdown(f"Your favorite font is **{favorite_font}** 🎈")
    else:
        st.write("No saved fonts yet.")


