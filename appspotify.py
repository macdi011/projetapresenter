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

# Chargement des données à partir du fichier CSV
music = pd.read_csv('Spotify.csv')  # Assurez-vous que le chemin est correct

# Fonction pour récupérer les images d'albums et l'URL de la piste depuis Spotify
def get_track_info(track_name, artist_name):
    search_query = f"track:{track_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        track_url = track["external_urls"]["spotify"]
        return album_cover_url, track_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png", None  # Image par défaut si aucune n'est trouvée

# Fonction de recommandation basée sur le clustering
def recommend(song):
    try:
        index = music[music['track_name'] == song].index[0]
        recommended_music_names = []
        recommended_music_posters = []
        recommended_music_urls = []

        for i in range(index + 1, min(index + 6, len(music))):  # Remplacer la boucle avec votre propre logique de recommandation
            artist = music.iloc[i].artist_name
            album_cover_url, track_url = get_track_info(music.iloc[i].track_name, artist)
            recommended_music_posters.append(album_cover_url)
            recommended_music_names.append(music.iloc[i].track_name)
            recommended_music_urls.append(track_url)

        return recommended_music_names, recommended_music_posters, recommended_music_urls
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
                recommended_songs, recommended_posters, recommended_urls = recommend(song_name)
                if recommended_songs and recommended_posters and recommended_urls:
                    st.subheader('Chansons Recommandées:')

                    # Affichage des chansons recommandées avec leurs images d'album et lecteur audio
                    for i, song in enumerate(recommended_songs):
                        st.markdown('<hr>', unsafe_allow_html=True)
                        st.markdown(f'<div class="recommended-song"><p class="song-name">{i+1}. {song}</p><img src="{recommended_posters[i]}" class="song-image"></div>', unsafe_allow_html=True)
                        if recommended_urls[i]:
                            st.audio(recommended_urls[i], format='audio/ogg', start_time=0)

    elif choice == 'À propos':
        st.header('À propos de cette application')
        st.write('Cette application utilise Streamlit pour créer une interface de recommandation musicale basée sur le clustering. Elle se connecte à Spotify pour récupérer les images des albums et permet à l\'utilisateur d\'écouter des extraits de chansons.')

if __name__ == '__main__':
    main()
