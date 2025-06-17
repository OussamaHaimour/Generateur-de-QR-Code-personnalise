import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import streamlit as st


colors = [
    "Red", "Blue", "Green", "Yellow", "Orange", "Purple", "Pink", "Brown", "Gray", "Black", "White"
]



def create_qr_sans_logo(link, nom, colour):
    backgrounds = "White"
    if colour == "White":
        backgrounds = "Black"
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(link)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color=colour, back_color=backgrounds).convert("RGBA")

    qr_width, qr_height = qr_img.size


    font_size = 30
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    bbox = font.getbbox(nom)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    new_height = qr_height + text_height + 20
    final_img = Image.new("RGBA", (qr_width, new_height), "White")
    final_img.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(final_img)
    text_x = (qr_width - text_width) // 2
    text_y = qr_height -20

    draw.text((text_x, text_y), nom, font=font, fill=colour)

    file_name = f"{nom}_QRCode.png".replace(" ", "_")
    final_img.save(file_name)

    st.image(final_img, caption="QR Code généré", use_container_width=True)

    with open(file_name, "rb") as file:
        st.download_button("⬇️ Télécharger l'image", file, file_name=file_name)


def create_qr_code(link,nom,save_path,colour,logo_path):
    backgrounds = "White"
    if colour == "White":
        backgrounds = "Black"
    if not os.path.exists(save_path):
        print("le path ca marche pas")
        save_path = os.getcwd()

    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )

    qr.add_data(link)
    qr.make(fit=True)


    qr_img = qr.make_image(fill_color=colour, back_color=backgrounds).convert("RGBA")




    logo = Image.open(logo_path).convert("RGBA")
    logo_size = 70
    logo = logo.resize((logo_size, logo_size))

    qr_width, qr_height = qr_img.size
    logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

    square_size = logo_size + 20
    square_position = ((qr_width - square_size) // 2, (qr_height - square_size) // 2)

    draw = ImageDraw.Draw(qr_img)
    corner_radius = square_size // 5

    draw.rounded_rectangle(
        [square_position[0], square_position[1],
         square_position[0] + square_size, square_position[1] + square_size],
        fill="white",
        radius=corner_radius
    )


    qr_img.paste(logo, logo_position, mask= logo)

    



    font_size = 30
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    bbox = font.getbbox(nom)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    new_height = qr_height + text_height + 10

    final_img = Image.new("RGBA", (qr_width, new_height), backgrounds)
    final_img.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(final_img)
    text_x = (qr_width - text_width) // 2
    text_y = qr_height -20

    draw.text((text_x, text_y), nom, font=font, fill=colour)

    file_name = f"{nom}_QRCode.png".replace(" ", "_")


    file_path = os.path.join(save_path, file_name)

    final_img.save(file_path)

    return final_img, file_path


def main():
    st.title("🖼️ Générateur de QR Code personnalisé")

    link = st.text_input('🔗 Entrez le lien à transformer en QR Code:')
    logo_path = st.text_input("📂 Entrez le chemin du logo (optionnel):")
    nom = st.text_input('🏢 Entrez le nom de la société:')
    save_path = st.text_input('💾 Entrez le chemin pour enregistrer le fichier:')
    choix_colour = st.selectbox("🎨 Choisissez la couleur de votre QR Code:", colors)

    if st.button("🚀 Générer QR Code"):
        if not link or not nom or not save_path:
            st.error("Veuillez remplir tous les champs obligatoires !")

        else:
            if not logo_path:
                create_qr_sans_logo(link,nom,choix_colour)
                return

            if not os.path.exists(logo_path):
                st.error("❌ Votre chemin est incorrect. Veuillez vérifier et réessayer.")
                return

            final_img, file_path = create_qr_code(link, nom, save_path, choix_colour, logo_path)
            st.image(final_img, caption="QR Code généré", use_container_width=True)
            

            with open(file_path, "rb") as file:
                st.download_button("⬇️ Télécharger l'image", file, file_name=os.path.basename(file_path))

    

main()
