import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Clés d'API Spotify (remplacez-les par vos propres clés)
CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialisation du client Spotify
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Chargement des données à partir du fichier CSV avec spécification de l'encodage
try:
    music = pd.read_csv('spotify-2023.csv', encoding='utf-8')  # Assurez-vous que le chemin est correct et spécifiez l'encodage approprié
except UnicodeDecodeError:
    st.error("Erreur de décodage Unicode lors de la lecture du fichier CSV.")

# Fonction pour récupérer les images d'albums depuis Spotify
def get_song_album_cover_url(track_name, artist_name):
    search_query = f"track:{track_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"  # Image par défaut si aucune n'est trouvée

# Fonction de recommandation basée sur le clustering
def recommend(song, music):
    try:
        index = music[music['track_name'] == song].index[0]
        recommended_music_names = []
        recommended_music_posters = []
        
        # Ici, vous pouvez effectuer votre logique de recommandation
        
        for i in range(index + 1, min(index + 6, len(music))):  
            artist = music.iloc[i].artist_name
            recommended_music_posters.append(get_song_album_cover_url(music.iloc[i].track_name, artist))
            recommended_music_names.append(music.iloc[i].track_name)

        return recommended_music_names, recommended_music_posters
    except IndexError:
        st.error(f"Aucune chanson trouvée avec le nom '{song}'. Veuillez essayer avec un autre nom de chanson.")

# Fonction principale pour l'application Streamlit
def main():
    st.title('Application de Recommandation Musicale')
    st.markdown(
        """
        <style>
        .title {
            font-size: 32px;
            font-weight: bold;
            color: #FF5733;
            text-align: center;
            margin-bottom: 20px;
        }
        .input-container {
            margin-bottom: 20px;
        }
        .recommended-song {
            margin-top: 30px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .song-name {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .song-image {
            width: 200px;
            height: auto;
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Menu de navigation
    menu = ['Accueil', 'À propos']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Accueil':
        st.markdown('<hr>', unsafe_allow_html=True)
        st.header('Accueil')

        # Formulaire pour saisir une chanson
        st.subheader('Recherche de chanson')
        song_name = st.text_input('Nom de la chanson')

        if st.button('Rechercher'):
            if song_name:
                recommended_songs, recommended_posters = recommend(song_name, music)
                if recommended_songs and recommended_posters:
                    st.subheader('Chansons Recommandées:')
                    
                    # Affichage des chansons recommandées avec leurs images d'album
                    for i, song in enumerate(recommended_songs):
                        st.markdown('<hr>', unsafe_allow_html=True)
                        st.markdown(f'<div class="recommended-song"><p class="song-name">{i+1}. {song}</p><img src="{recommended_posters[i]}" class="song-image"></div>', unsafe_allow_html=True)

    elif choice == 'À propos':
        st.header('À propos de cette application')
        st.write('Cette application utilise Streamlit pour créer une interface de recommandation musicale basée sur le clustering. Elle se connecte à Spotify pour récupérer les images des albums.')

if __name__ == '__main__':
    main()
