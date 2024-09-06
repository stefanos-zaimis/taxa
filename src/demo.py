import quinsectz as qi
import image_scraper as img
import random
import threading
import queue
import tkinter as tk
from PIL import Image, ImageTk
import os

url_queue = queue.Queue()
species_queue = queue.Queue()

img_scraper_thread = threading.Thread(target=img.scrape_random_species_text_dynamic, args=(url_queue, species_queue), daemon = True)
img_scraper_thread.start()

species_name = ""

family = ""

other_choices = []

# GUI setup
def show_question(image_path, choices, correct_family):
    # Set up the tkinter root
    root = tk.Tk()
    root.title("Family Identification Quiz")

    # Load the image
    img = Image.open(image_path)
    img.thumbnail((400, 400))  # Resize to fit within 400x400 while keeping aspect ratio
    img_tk = ImageTk.PhotoImage(img)

    # Display the image
    img_label = tk.Label(root, image=img_tk)
    img_label.pack()

    # Display the choices
    def check_answer(selected_family):
        if selected_family == correct_family:
            result_label.config(text="Correct!", fg="green")
        else:
            result_label.config(text="Wrong, try again!", fg="red")

    # Add buttons for multiple choices
    for choice in choices:
        button = tk.Button(root, text=choice, command=lambda c=choice: check_answer(c))
        button.pack(pady=10)

    # Label to show result
    result_label = tk.Label(root, text="", font=("Helvetica", 16))
    result_label.pack()

    # Start the tkinter main loop
    root.mainloop()


# Main loop
while species_name == "":

    # Define the class name
    class_name = "Mammalia"

    # Get the family list
    family_list = qi.families_in_class(class_name)

    genus_list = []

    while genus_list == []:

        # Select random family
        random_family = random.choice(family_list)
        family = random_family

        # Print the randomly selected family's name
        print("Randomly selected family:", random_family['scientificName'])
        
        genus_list = qi.genus_in_family(random_family['scientificName'])

    random_genus = random.choice(genus_list)

    print("Randomly selected genus:", random_genus['scientificName'])

    #Get Image
    usage_key = random_genus['key']
    print("Taxon key:",usage_key)
    url = "https://www.gbif.org/occurrence/gallery?taxon_key=" + str(usage_key) + "&occurrence_status=present"
    url_queue.put(url)

    species_name = species_queue.get()
    print("Got the stuff")

print("Species name is: ------------------------------ " + species_name + "-------------------------------------------------------s")

family_siblings = qi.sibling_families(family['scientificName'])

if len(family_siblings) >= 3:
    other_choices = random.sample(family_siblings, 3)
else:
    other_choices = family_siblings

choices = [family['scientificName']] + [choice['scientificName'] for choice in other_choices]
random.shuffle(choices)  # Shuffle the options

# Assuming the image was saved in worker.py
image_path = os.path.join("images", species_name + ".png")

# Display the GUI
show_question(image_path, choices, family['scientificName'])