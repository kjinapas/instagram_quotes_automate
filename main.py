import requests
import random
import os
from PIL import Image, ImageDraw, ImageFont
from tkinter import simpledialog,messagebox
from key import access_key

import tkinter as tk

#select keyword
category = ['success','inspirational','life','faith','dreams','hope',]


#gen quotes
random_category = random.choice(category)
query=random_category#select query from catagory


#size image
width = height = 1080  # Size to crop the image to
size = (1080, 1080)


font_path = 'Font/Lora-VariableFont_wght.ttf'
font_size = 30
font = ImageFont.truetype(font_path, font_size)



class MyGUI:
   



    def __init__(self, master):
        self.master = master
        self.master.geometry("800x200")
        self.create_buttons()


    def create_buttons(self):
        self.button1 = tk.Button(self.master, text="Load img",command=lambda:self.load_images())
        self.button2 = tk.Button(self.master, text="Draw Quotes",command=lambda:self.load_text())
        self.button3 = tk.Button(self.master,text ="Open Images",command=lambda:self.open_directory("imgs"))
        self.button3_5 = tk.Button(self.master,text ="Open Final",command=lambda:self.open_directory("finals"))
        self.buttonall = tk.Button(self.master,text ="Load and Draw",command=lambda:self.load_and_draw())
        self.button4 = tk.Button(self.master, text="Delete img",command=lambda:self.delete_imgs('imgs'))
        self.button5 = tk.Button(self.master, text="delete draw Quotes",command=lambda:self.delete_imgs('finals'))
        self.button6 = tk.Button(self.master,text ="Delete All",command=lambda:self.delete_all())


        self.button1.place(x=50, y=50)
        self.button2.place(x=150, y=50)
        self.button3.place(x=300, y=50)
        self.button3_5.place(x=400, y=50)
        self.buttonall.place(x=500,y=50)
        self.button4.place(x=50, y=100)
        self.button5.place(x=150 ,y= 100)
        self.button6.place(x=300,y =100)


    def load_img(self,n):
       
        url = 'https://api.unsplash.com/photos/random?client_id={}&query={}&orientation=portrait&count={}'.format(access_key, query,n)
        response = requests.get(url)
        json_data = response.json()


        if not os.path.exists("imgs"):
            os.makedirs("imgs")
        for i, data in enumerate(json_data):
            image_url = data['urls']['regular']
            image_response = requests.get(image_url)
           
            with open('imgs/{}_{}.jpg'.format( query, i), 'wb') as f:
                f.write(image_response.content)
           
            # Resize the image
            # Open the downloaded image and crop it
            with Image.open('imgs/{}_{}.jpg'.format( query, i)) as img:
                w, h = img.size
                left = (w - width) / 2
                top = (h - height) / 2
                right = (w + width) / 2
                bottom = (h + height) / 2
                img_cropped = img.crop((left, top, right, bottom))
               
                # Save the cropped image
                img_cropped.save('imgs/{}_{}_crop.jpg'.format( query, i))
               
            # Remove the original image
            os.remove('imgs/{}_{}.jpg'.format( query, i))
           

    def delete_imgs(self,directory_path):
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        messagebox.showinfo("Delete", f"Delete All {directory_path}  successfully!")
   

    def draw_text(self,n):
# loop through all files in folder
        for filename in os.listdir("imgs"):
            api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(query)
            response = requests.get(api_url, headers={'X-Api-Key': 'pfBnVykGc1p7g7M1EiW05g==8tUIDmfrwKAvHcDu'})
            data= response.json()
            quote = data[0]['quote']
            author = data[0]['author']
       
            image = Image.open(os.path.join("imgs", filename))
            background_image = image.resize((width, height))


            image = Image.new('RGB', (width, height))
            image.paste(background_image, (0,0))
           
            quote_lines = []
            line = ''
            for word in quote.split():
                if len(line) + len(word) + 1 <= 50:
                    line += ' ' + word
                else:
                    quote_lines.append(line.lstrip())
                    line = word
            if line:
                quote_lines.append(line.lstrip())
            quote = '\n'.join(quote_lines)
            quote = f'{quote}\n({author})'
       


        # Set up the text drawing
            draw = ImageDraw.Draw(image)
            text_bbox = draw.textbbox((0, 0), quote, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_x = (width - text_width) / 2
            text_y = (height - text_height) / 2


        # Draw a rectangle behind the text
            padding = 20
            padding_y = 10
            background_x = text_x - padding
            background_y = text_y - padding_y
            background_width = text_width + padding*2
            background_height = text_height + padding*2
            draw.rounded_rectangle((background_x, background_y, background_x + background_width, background_y + background_height), radius=30, fill=(255, 255, 255,0))








        # Draw the quote on the image
            draw.multiline_text((text_x, text_y), quote, font=font, fill=(0, 0, 0), align='center')


        # Save the image
            image.save(f'finals/{filename}.png')
       
           
    def open_directory(self,path):
        os.startfile(path)




    def delete_all(self):
        for file_name in os.listdir("imgs"):
            file_path = os.path.join("imgs", file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        for file_name in os.listdir("finals"):
            file_path = os.path.join("finals", file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        messagebox.showinfo("Delete", "Delete All successfully!")




    def load_and_draw(self):
        n = simpledialog.askinteger("Input", "Enter a number : ")
        self.load_img(n)
        self.draw_text(n)
        messagebox.showinfo("Success", f"Load  and Draws {n} Images successfully!")




    def load_images(self):
        n = simpledialog.askinteger("Input", "Enter a number of images: ")
        self.load_img(n)
        messagebox.showinfo("Success", f"Load  {n} Images successfully!")
       
    def load_text(self):
        n = simpledialog.askinteger("Input", "Enter a number to Draw: ")
        self.draw_text(n)
        messagebox.showinfo("Success", f"Draw  {n} Images successfully!")


       


       




if __name__ == "__main__":
    root = tk.Tk()
    app = MyGUI(root)
    root.mainloop()

