import os
import random
import tkinter as tk

from PIL import Image, ImageTk

import image_requestor as imgr
import image_scraper as img
import quinsectz as qi

species_name = ""

family = ""

other_choices = []

# Main Tkinter window setup
root = tk.Tk()
root.title("Taxon Selection")

import tkinter as tk

from PIL import Image, ImageTk


# Main question GUI setup
def show_question(image_path, choices, correct_family):
    quiz = tk.Tk()
    quiz.title("Family Identification Quiz")

    # Create frames for image and choices
    image_frame = tk.Frame(quiz)
    image_frame.pack(side="left", padx=10, pady=10)

    choices_frame = tk.Frame(quiz)
    choices_frame.pack(side="right", padx=10, pady=10)

    # Load and display the image on the left
    img = Image.open(image_path)
    img.thumbnail((900, 900))  # Resize to fit within 900x900
    img_tk = ImageTk.PhotoImage(img)
    img_label = tk.Label(image_frame, image=img_tk)
    img_label.image = img_tk  # Keep a reference to avoid garbage collection
    img_label.pack()

    # Function to check the answer
    def check_answer(selected_family):
        if selected_family == correct_family:
            result_label.config(text="Correct!", fg="green")
        else:
            result_label.config(text="Wrong, try again!", fg="red")

    # Display the choices on the right
    for choice in choices:
        button = tk.Button(
            choices_frame, text=choice, command=lambda c=choice: check_answer(c)
        )
        button.pack(pady=5, anchor="w")

    # Label to show result below the choices
    result_label = tk.Label(choices_frame, text="", font=("Helvetica", 16))
    result_label.pack(pady=10)

    # Function to load a new question
    def load_new_question():
        quiz.destroy()  # Close the current quiz window
        quiz_logic(
            name, taxonomic_level
        )  # Reload quiz logic with the same taxon selection

    # Button to load a new question, aligned below result label
    new_question_button = tk.Button(
        choices_frame, text="New Question", command=load_new_question
    )
    new_question_button.pack(pady=20)

    # Function to label the image
    def label_image_with(tag):
        imgr.label_image(species_name, image_path, tag)

    # Label buttons
    label_frame = tk.Frame(choices_frame)
    label_frame.pack(pady=20)
    tk.Button(label_frame, text="Good", command=lambda: label_image_with("good")).pack(side="left", padx=5)
    tk.Button(label_frame, text="Medium", command=lambda: label_image_with("medium")).pack(side="left", padx=5)
    tk.Button(label_frame, text="Bad", command=lambda: label_image_with("bad")).pack(side="left", padx=5)
    tk.Button(label_frame, text="Unusable", command=lambda: label_image_with("unusable")).pack(side="left", padx=5)
    
    # Start the tkinter main loop for the quiz window
    quiz.mainloop()


def quiz_logic(name="Insecta", taxonomic_level="class"):
    global species_name, family, other_choices
    # Main loop
    species_name = ""
    while species_name == "":

        family_list = qi.families_in_taxon(name=name, rank=taxonomic_level)

        genus_list = []

        while genus_list == []:

            # Select random family
            random_family = random.choice(family_list)
            family = random_family

            # Print the randomly selected family's name
            print("Randomly selected family:", random_family["scientificName"])

            genus_list = qi.genus_in_family(random_family["scientificName"])

        random_genus = random.choice(genus_list)

        print("Randomly selected genus:", random_genus["scientificName"])

        # Get Image
        usage_key = random_genus["key"]
        print("Taxon key:", usage_key)
        image_info = imgr.select_random_image(usage_key)
        if image_info:
            species_name = image_info[0]
            imgr.save_image(image_info)

    print(
        "Species name is: ------------------------------ "
        + species_name
        + "-------------------------------------------------------s"
    )

    family_siblings = qi.sibling_families(family["scientificName"])

    if len(family_siblings) >= 3:
        other_choices = random.sample(family_siblings, 3)
    else:
        other_choices = family_siblings

    choices = [family["scientificName"]] + [
        choice["scientificName"] for choice in other_choices
    ]
    random.shuffle(choices)  # Shuffle the options

    # Assuming the image was saved in worker.py
    image_path = os.path.join("images", species_name.replace(" ", "_") + ".jpg")

    # Display the GUI
    show_question(image_path, choices, family["scientificName"])


# Function to start the quiz by using the entered class
def start_quiz():
    global name, taxonomic_level
    name = name_entry.get()  # Get the class from the entry box
    taxonomic_level = level_entry.get()
    # if class_name:  # Only proceed if a class is entered
    root.destroy()  # Close the class selection window
    quiz_logic(
        name=name, taxonomic_level=taxonomic_level
    )  # Call the main quiz function
    # else:
    #    error_label.config(text="Please enter a class name.")


# Set up the class selection window
tk.Label(root, text="Enter a desired taxon name (Default is 'Insecta'").pack(pady=10)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

tk.Label(root, text="Enter the taxonomic level (Default is 'Class'):").pack(pady=10)
level_entry = tk.Entry(root)
level_entry.pack(pady=5)

error_label = tk.Label(root, text="", fg="red")
error_label.pack()

start_button = tk.Button(root, text="Start Quiz", command=start_quiz)
start_button.pack(pady=10)

# Run the class selection window
root.mainloop()
