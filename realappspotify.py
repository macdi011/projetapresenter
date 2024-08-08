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
music = pd.read_csv('spotify-2023_2.csv')  # Assurez-vous que le chemin est correct

# Fonction pour récupérer les images d'albums, l'URL de la piste audio et l'URL Spotify depuis Spotify
def get_track_info(track_name, artist_name):
    search_query = f"track:{track_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        track_url = track["external_urls"]["spotify"]
        audio_preview_url = track["preview_url"]  # URL de prévisualisation audio au format mp3
        return album_cover_url, track_url, audio_preview_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png", None, None  # Image par défaut si aucune n'est trouvée

# Fonction de recommandation basée sur le clustering
def recommend(song):
    try:
        index = music[music['Track'] == song].index[0]
        recommended_music_names = []
        recommended_music_posters = []
        recommended_music_urls = []
        recommended_youtube_urls = []
        recommended_titles = []
        recommended_views = []

        for i in range(index + 1, min(index + 6, len(music))):  
            artist = music.iloc[i].Artist
            album_cover_url, track_url, audio_preview_url = get_track_info(music.iloc[i].Track, artist)
            recommended_music_posters.append(album_cover_url)
            recommended_music_names.append(music.iloc[i].Track)
            recommended_music_urls.append(audio_preview_url)
            recommended_youtube_urls.append(music.iloc[i].Url_youtube)
            recommended_titles.append(music.iloc[i].Title)
            recommended_views.append(music.iloc[i].Views)

        return recommended_music_names, recommended_music_posters, recommended_music_urls, recommended_youtube_urls, recommended_titles, recommended_views
    except IndexError:
        st.error(f"Aucune chanson trouvée avec le nom '{song}'. Veuillez essayer avec un autre nom de chanson.")

# Fonction pour afficher les statistiques et l'EDA
def show_statistics_and_eda():
    st.header('Statistiques et Analyse Exploratoire des Données (EDA)')
    
    # Affichage des statistiques descriptives
    st.subheader('Statistiques Descriptives')
    st.write(music.describe())

    # Nombre de colonnes
    st.subheader('Nombre de Colonnes')
    st.write(f"Le dataset contient {len(music.columns)} colonnes.")

    # Répartition des types d'albums
    st.subheader('Répartition des Types d\'Albums')
    if 'Album_Type' in music.columns:
        album_types = music['Album_Type'].value_counts()
        st.bar_chart(album_types)
    else:
        st.write("Colonne 'Album_Type' non trouvée dans le dataset.")

    # Artistes les plus présents
    st.subheader('Artistes les Plus Présents')
    top_artists = music['Artist'].value_counts().head(10)
    st.bar_chart(top_artists)

    # Chansons les plus streamées
    st.subheader('Chansons les Plus Streamées')
    if 'Streams' in music.columns:
        top_songs = music[['Track', 'Streams']].sort_values(by='Streams', ascending=False).head(10)
        st.write(top_songs)
    else:
        st.write("Colonne 'Streams' non trouvée dans le dataset.")

# Fonction principale pour l'application Streamlit
def main():
    st.title('Cellou Spotube Recommendations')
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
    menu = ['Accueil', 'Statistiques', 'À propos']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Accueil':
        st.markdown('<hr>', unsafe_allow_html=True)
        st.header('Accueil')

        # Formulaire pour saisir une chanson
        st.subheader('Recherche de chanson')
        song_name = st.text_input('Nom de la chanson')

        if st.button('Rechercher'):
            if song_name:
                recommended_songs, recommended_posters, recommended_urls, recommended_youtube, recommended_titles, recommended_views = recommend(song_name)
                if recommended_songs and recommended_posters and recommended_urls:
                    st.subheader('Chansons Recommandées:')

                    # Affichage des chansons recommandées avec leurs images d'album et lecteur audio
                    for i, song in enumerate(recommended_songs):
                        st.markdown('<hr>', unsafe_allow_html=True)
                        st.markdown(f'<div class="recommended-song"><p class="song-name">{i+1}. {song}</p><img src="{recommended_posters[i]}" class="song-image"></div>', unsafe_allow_html=True)
                        st.write(f"Titre: {recommended_titles[i]}")
                        st.write(f"Nombre de vues sur YouTube: {recommended_views[i]}")
                        if recommended_urls[i]:
                            st.audio(recommended_urls[i], format='audio/mpeg', start_time=0)
                        if recommended_youtube[i]:
                            st.write(f"Lien YouTube: {recommended_youtube[i]}")

    elif choice == 'Statistiques':
        show_statistics_and_eda()

    elif choice == 'À propos':
        st.header('À propos de cette application')
        st.write(
            """
            Cette application de recommandation musicale Spotify, appelée **Cellou Spotube Recommendations**, fournit des liens YouTube pour les pistes recommandées. Elle a été développée dans le cadre d'un travail de laboratoire du bootcamp en Data Science de **GOMYCODE**. Elle utilise les données de Spotify pour proposer des recommandations musicales et offre des fonctionnalités telles que l'affichage des images d'album et des extraits audio.
            """
        )

if __name__ == '__main__':
    main()
