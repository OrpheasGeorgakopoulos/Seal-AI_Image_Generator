from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import openai
import os
import base64
from PIL import Image, ImageTk

client = openai.OpenAI(api_key = 'YOUR_OPENAI_KEY')

OUTPUT_DIR = "outputs"

window = ThemedTk(theme="equilux")
window.configure(themebg="equilux")
window.geometry("500x800")
window.title("Seal")
window.resizable(False, False)

image_paths = []
cIndex = 0

title = ttk.Label(window, text="Seal", font=("Agency FB Bold", 35))
title.place(x=210, y=30)

subTitle = ttk.Label(
    window,
    text ="Seal, Idea Gen Engine for 3D Designs.",
    font=("Agency FB", 15)
)
subTitle.place(x=140, y=89)

def generate_ideas(user_text, n):
    prompt = f"Give me {n} creative wallpaper 4k ideas about: {user_text}\n" \
             f"Return ONLY  {n} lines, no numbering, no bullets."

    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )

    ideas = []
    for line in resp.choices[0].message.content.splitlines():
        print(line)
        line = line.strip()
        if line != "":
            ideas.append(line)
    return ideas[:n]

def generate_images_from_ideas(ideas):
    paths = []

    for i in range(len(ideas)):
        idea = ideas[i]

        img = client.images.generate(
            model="dall-e-3",
            prompt=idea,
            size="1024x1024",
            n=1
        )

        url = img.data[0].url
        print(url)


#MAIN
def generate_images_from_ideas2(ideas):
    paths = []

    for i in range(len(ideas)):
        idea = ideas[i]

        img = client.images.generate(
            model="gpt-image-1.5",
            prompt=ideas[i],
            size="1536x1024",
            n=1,
            output_format = "jpeg"
        )

        filepath = os.path.join(OUTPUT_DIR, f"request_{i+1}.jpg")

        b64 = img.data[0].b64_json
        print(b64)

        with open(filepath, "wb") as f:
            f.write(base64.b64decode(b64))

        paths.append(filepath)

    return paths



def showImage(ind):
    global imagePreview

    img = Image.open(image_paths[ind])
    img = img.resize((200,200), Image.Resampling.LANCZOS)
    imagePreview = ImageTk.PhotoImage(img)
    image_label.configure(image = ImagePreview)



def process(event=None):
    global image_paths

    user = text_widget.get()
    if rb.get() == "Choice15":
        n = 3
    else:
        n = 1

    ideas = generate_ideas(user, n)
    image_paths = generate_images_from_ideas2(ideas)

    cIndex = 0
    showImage(0)

def showImage(ind):
    global ImagePreview
    img = Image.open(image_paths[ind])
    img = img.resize((400,400), Image.Resampling.LANCZOS)
    ImagePreview = ImageTk.PhotoImage(img)
    image_label.config(image=ImagePreview)

def nextImg(event=None):
    global cIndex

    cIndex = (cIndex + 1) % len(image_paths)
    showImage(cIndex)

def prevImg(event=None):
    global cIndex

    if not image_paths:
        return
    cIndex = (cIndex - 1) % len(image_paths)
    showImage(cIndex)

def preview_first():
    if image_paths == True:
        os.startfile(image_paths[0])

window.bind("<Left>", prevImg)
window.bind("<Right>", nextImg)


rb = StringVar(value="Choice5")

rad1 = ttk.Radiobutton(window, text="Short [1 Variants]", value="Choice5",variable=rb)
rad1.place(x=110, y=135)

rad2 = ttk.Radiobutton(window, text="Long [3 Variants]", value="Choice15",variable=rb)
rad2.place(x=260, y=135)

text_widget = ttk.Entry(window,width=35,font=("Segoe UI", 15))
text_widget.place(x=50, y=200)

enter_button = ttk.Button(window, text="Enter", command = process)
enter_button.place(x=310, y=290, height=40,width=140)

preview_button = ttk.Button(window, text ="Preview") # , command = preview_first
preview_button.place(x=50, y=290, height =40,width=140)

image_label = ttk.Label(window)
image_label.place(x=50,y=330,width=400,height=400)

window.mainloop()
