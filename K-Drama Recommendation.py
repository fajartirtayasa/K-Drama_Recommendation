#!/usr/bin/env python
# coding: utf-8

# # **[K-Drama Recommendation]**

# ### Proyek Machine Learning Terapan: Recommendation System
# by Fajar Tirtayasa

# <img src='https://drive.google.com/uc?export=view&id=1ZBtA_o080zjskyfQdckf_gq5LuUgFmSA'>

# ## **[Business Understanding]**
# *MyDramaList.com* adalah proyek berbasis komunitas yang menyediakan drama & film Asia. Di situs web ini, penggemar dapat membuat daftar pantauan drama mereka sendiri, menilai drama dan film, hingga menulis ulasan. Dataset ini memeringkat 100 Drama Korea teratas yang diberikan oleh pengguna di situs web.

# ## **[Data Understanding]**
# 
# Source Dataset: https://www.kaggle.com/datasets/chanoncharuchinda/top-100-korean-drama-mydramalist

# In[247]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from collections import Counter


# In[248]:


#loading data
df = pd.read_csv('/Data Science/Dicoding/K-Drama Recommendation/top100_kdrama.csv')
df.head(3)


# Informasi mengenai kolom dataframe:
# - **Name**: nama drama korea.
# - **Year of release**: tahun rilis drama.
# - **Aired Date**: tanggal penayangan (mulai-selesai).
# - **Aired On**: hari penayangan.
# - **Number of Episode**: banyaknya episode.
# - **Network**: jaringan/saluran media penayangan drama.
# - **Duration**: durasi tiap episode.
# - **Content Rating**: tingkatan konten (sesuai usia).
# - **Synopsis**: sinopsis drama korea.
# - **Cast**: aktor atau aktris dalam drama.
# - **Genre**: genre drama korea.
# - **Tags**: tag yang terdapat pada drama.
# - **Rank**: peringkat di situs web.
# - **Rating**: nilai rating untuk drama korea (1-10).

# ### Exploratory Data Analysis: Descriptive Statistic

# In[249]:


#melihat banyaknya baris dan kolom pada dataframe
df.shape


# In[250]:


#mengecek banyaknya Non-Null value dan tipe data di setiap kolom
df.info()


# In[251]:


#melihat banyaknya Null value di setiap kolom
df.isna().sum()


# In[252]:


#mengecek ada tidaknya data yang duplikat
df[df.duplicated()]


# In[253]:


#melihat statistik deskriptif untuk kolom dengan tipe data numerik
df.describe()


# In[254]:


#melihat statistik deskriptif untuk kolom dengan tipe data object
df.describe(include='object')


# In[255]:


#mengecek data yang sama pada kolom 'Name'
df[df['Name']=='Kingdom']


# In[256]:


#mengganti K-Drama berjudul 'Kingdom' yang rilis tahun 2020 menjadi 'Kingdom_2'
df.loc[16, 'Name'] = 'Kingdom_2'


# Beberapa informasi yang dapat diperoleh dari tahapan Descriptive Statistic di atas adalah:
# - Dataset ini terdiri atas 100 baris dan 14 kolom (3 kolom dengan tipe data numerik, dan 11 kolom dengan tipe data object).
# - Tidak terdapat *missing value* pada data. Dengan demikian, proses *handling missing value* tidak diperlukan.
# - Tidak terdapat data yang duplikat pada dataset. Adapun judul yang sama pada kolom 'Name' mengartikan bahwa serial K-Drama tersebut dibagi ke dalam 2 season yang dirilis pada waktu berbeda.
# - Terdapat beberapa kolom yang memiliki *multiple value*, seperti kolom 'Aired On', 'Network', 'Genre', dan 'Tags'.

# ### Exploratory Data Analysis: Univariate Analysis

# #### **Categorical Data**

# In[257]:


#banyaknya K-Drama berdasarkan Content Rating
count = df['Content Rating'].value_counts().sort_index(ascending=False)
#membuat count plot untuk kolom 'Content Rating'
sns.set_style('whitegrid')
sns.countplot(x='Content Rating', data=df, palette='ocean')
for i, v in enumerate(count):
    plt.text(i-0.01, v+2, str(v), fontweight='bold')
plt.title('Banyak K-Drama berdasarkan Content Rating', pad=20, fontsize=20)
plt.ylim(ymax=100)
plt.gcf().set_size_inches(12,8)
plt.savefig('cat_1.png', quality=95)
plt.show()


# In[258]:


#menampung semua data network yang muncul ke dalam list
network_list = []
for networks in df['Network'].to_list():
    networks = networks.strip().split(",  ")
    for network in networks:
        network_list.append(network)
#membuat dataframe yang berisi banyak setiap network
network_df = pd.DataFrame.from_dict(Counter(network_list), orient='index').rename(columns={0:'Count'})
network_df.sort_values(by='Count', ascending = False, inplace = True)
print(network_df.T)

#membuat barplot untuk melihat banyak setiap network
sns.set_style('whitegrid')
sns.barplot(x=network_df.index, y=network_df['Count'], palette='ocean')
for i, v in enumerate(network_df['Count']):
    plt.text(i-0.03, v+0.5, str(v), fontweight='bold')
plt.ylim(ymax=40)
plt.title('Banyak Penyedia Network untuk K-Drama', pad=20, fontsize=20)
plt.gcf().set_size_inches(12,8)
plt.savefig('cat_2.png', quality=95)
plt.show()


# In[259]:


#menampung semua data genre yang muncul ke dalam list
genre_list = []
for genre in df['Genre'].to_list():
    genre = genre.strip().split(",  ")
    for gen in genre:
        genre_list.append(gen)
#membuat dataframe yang berisi banyak setiap genre
genre_df = pd.DataFrame.from_dict(Counter(genre_list), orient='index').rename(columns={0:'Count'})
genre_df.sort_values(by='Count', ascending = False, inplace = True)
print('Total Genre unik: ', len(genre_df))
print('5 Genre yang Paling Sering Diadopsi:\n', genre_df.head())

#membuat barplot untuk melihat banyak setiap genre
sns.set_style('whitegrid')
sns.barplot(x=genre_df.index, y=genre_df['Count'], palette='ocean')
for i, v in enumerate(genre_df['Count']):
    plt.text(i-0.1, v+0.5, str(v), fontweight='bold')
plt.ylim(ymax=60)
plt.title('Banyak Setiap Genre untuk K-Drama', pad=20, fontsize=20)
plt.xticks(rotation=90)
plt.gcf().set_size_inches(12,8)
plt.savefig('cat_3.png', quality=95)
plt.show()


# In[260]:


#menampung semua data tags yang muncul ke dalam list
tags_list = []
for tags in df['Tags'].to_list():
    tags = tags.strip().split(", ")
    for tag in tags:
        tags_list.append(tag)
#membuat dataframe yang berisi banyak setiap tag
tags_df = pd.DataFrame.from_dict(Counter(tags_list), orient='index').rename(columns={0:'Count'})
tags_df.sort_values(by='Count', ascending = False, inplace = True)
top_tags_df = tags_df.head(10)
print('10 Tag dengan kemunculan tebanyak:\n',top_tags_df)

#membuat barplot untuk melihat 10 tag dengan kemunculan terbanyak
sns.set_style('whitegrid')
sns.barplot(x=top_tags_df.index, y=top_tags_df['Count'], palette='ocean')
for i, v in enumerate(top_tags_df['Count']):
    plt.text(i-0.03, v+0.5, str(v), fontweight='bold')
plt.ylim(ymax=45)
plt.title('10 Tag dengan Kemunculan Terbanyak', pad=20, fontsize=20)
plt.xticks(rotation=90)
plt.gcf().set_size_inches(12,8)
plt.savefig('cat_4.png', quality=95)
plt.show()


# #### **Numerical Data**

# In[261]:


#banyaknya K-Drama yang rilis di setiap tahun
count = df['Year of release'].value_counts().sort_index()
#membuat count plot untuk kolom 'Year of release'
sns.set_style('whitegrid')
sns.countplot(x='Year of release', data=df, palette='ocean_r')
for i, v in enumerate(count):
    plt.text(i-0.03, v+0.5, str(v), fontweight='bold')
plt.ylim(ymax=25)
plt.title('Banyak K-Drama yang Rilis di Setiap Tahun', pad=20, fontsize=20)
plt.gcf().set_size_inches(12,8)
plt.savefig('num_1.png', quality=95)
plt.show()


# In[262]:


#banyaknya total episode yang digunakan K-Drama
count_each_episode = df['Number of Episode'].value_counts().sort_values()
#visualisasi count_each_episode
count_each_episode.plot(kind='barh', figsize=(12,8), color='darkblue')
plt.grid(False)
plt.title('Banyak Total Episode yang Digunakan K-Drama', pad=30, fontsize=25)
plt.xlabel('Number of K-Drama')
plt.ylabel('Total Episode')
for i, v in enumerate(count_each_episode):
    plt.text(v+0.5, i-0.15, str(v), fontweight='bold')
plt.tight_layout()
plt.savefig('num_2.png', quality=95)
plt.show()


# In[263]:


#membuat histogram untuk melihat distribusi data pada kolom 'Rating'
sns.set_style('whitegrid')
sns.histplot(data=df, x='Rating', kde=True, bins=7, color='darkblue')
plt.gcf().set_size_inches(12,8)
plt.title('Distribusi Rating', pad=20, fontsize=20)
plt.savefig('num_3.png', quality=95)
plt.show()


# Beberapa informasi yang dapat diperoleh dari tahapan Univariate Analysis di atas adalah:
# - 5 genre terbanyak yang muncul pada data top 100 drama korea adalah Drama, Romance, Comedy, Mistery, dan Thriller. Dengan kentalnya genre Drama dan Romance pada industri perfilman ini, menjadikan hampir seluruh drama korea mensyaratkan penikmatnya berusia di atas 15 tahun. Adapun dalam proses penayangannya--tvN, Netflix, dan SBS berhasil menjadi network/penyedia layanan siaran yang paling banyak menggaet drama-drama korea terbaik untuk tayang pada platformnya.
# - Apabila dilihat dari trennya, banyak drama korea terbaik di setiap tahun cenderung mengalami kenaikan seiring dengan waktu berlalu. Hal ini menandakan bahwa industri ini memang berkembang dan terus melakukan *improvement* agar dapat diterima dengan baik oleh masyarakat.
# - Mayoritas pembuat drama korea membagi keseluruhan cerita drama korea ke dalam 12, 16, atau 20 episode.
# - Data top 100 drama korea memiliki interval rating antara 8.5 hingga 9.2, dengan rata-rata rating sebesar 8.72.

# ## **[Data Preparation]**

# #### **Mengambil Kolom yang Diperlukan**

# In[264]:


content_df = df[['Name', 'Year of release', 'Genre']]
content_df


# #### **Menghilangkan Karakter Strip (-) Sebelum Vectorizer**

# In[265]:


#menghilangkan string strip (-)
content_df['Genre'] = content_df['Genre'].apply(lambda x: x.replace('-', ''))
content_df['Genre']


# #### **TF-IDF Vectorizer**

# In[266]:


from sklearn.feature_extraction.text import CountVectorizer 
#inisialisasi CountVectorizer
tf = CountVectorizer()
#melakukan perhitungan idf pada data genre
tf.fit(content_df['Genre']) 
#mapping array dari fitur index integer ke fitur nama
tf.get_feature_names()


# #### **Fit dan Transform ke Bentuk Matriks**

# In[267]:


#melakukan fit lalu ditransformasikan ke bentuk matrix
tfidf_matrix = tf.fit_transform(content_df['Genre'])
#melihat ukuran matrix tf-idf
tfidf_matrix.shape


# #### **Mengubah Vektor TF_IDF dalam Bentuk Matriks**

# In[268]:


#mengubah vektor tf-idf dalam bentuk matriks dengan fungsi todense()
tfidf_matrix.todense()


# #### **Melihat Matriks TF-IDF untuk Beberapa K-Drama dan Genre**

# In[269]:


pd.DataFrame(tfidf_matrix.todense(),
             columns=tf.get_feature_names(),
             index=content_df['Name']).sample(26, axis=1).sample(10, axis=0)


# ## **[Modelling]**

# #### **Latih Model dengan Cosine Similarity**

# In[270]:


from sklearn.metrics.pairwise import cosine_similarity
 
#menghitung cosine similarity pada matrix tf-idf
cosine_sim = cosine_similarity(tfidf_matrix) 
cosine_sim


# In[271]:


#membuat dataframe dari variabel cosine_sim dengan baris dan kolom berupa nama K-Drama
cosine_sim_df = pd.DataFrame(cosine_sim,
                             index=content_df['Name'],
                             columns=content_df['Genre'])
print('Shape:', cosine_sim_df.shape)

#melihat similarity matrix pada babarapa K-Drama
cosine_sim_df.sample(10, axis=1).sample(5, axis=0)


# #### **Uji Model**

# In[272]:


#indikasi judul K-Drama berdasarkan urutan data
indices = pd.Series(index = content_df['Name'], data = content_df.index)
indices.head()


# In[273]:


#membuat fungsi untuk memanggil 10 rekomendasi K-Drama berdasarkan judul yang diinput
def get_recommendations(judul, cosine_sim = cosine_sim, 
                        items = content_df[['Name', 'Year of release', 'Genre']]):
    #mengambil indeks dari judul K-Drama yang telah didefinisikan sebelumnnya
    idx = indices[judul]
    #mengambil skor kemiripan dengan semua judul
    sim_scores = list(enumerate(cosine_sim[idx]))
    #mengurutkan K-Drama berdasarkan skor kemiripan
    sim_scores = sorted(sim_scores, key = lambda x : x[1], reverse = True)
    #mengambil 10 skor kemiripan dari 1-11 (0 tidak dimasukan, karena adalah data yang diinput)
    sim_scores = sim_scores[1:11]
    #mengambil judul K-Drama dari skor kemiripan
    drama_indices = [i[0] for i in sim_scores]
    #mengembalikan 10 rekomendasi judul K-Drama
    return pd.DataFrame(content_df['Name'][drama_indices]).merge(items)


# In[274]:


#mengambil salah satu data K-Drama untik diuji
content_df[content_df['Name'] == "Dali and the Cocky Prince"]


# In[275]:


#menampilkan 10 rekomendasi K-Drama yang sesuai dengan data uji
rekomendasi = pd.DataFrame(get_recommendations("Dali and the Cocky Prince"))
rekomendasi


# ## **[Evaluation]**

# In[276]:


#melihat persebaran genre hasil rekomendasi
count = pd.DataFrame(rekomendasi['Genre'].value_counts().reset_index().values,
                     columns = ['Genre', 'Count'])
count.head()


# In[277]:


TP = 10 #jumlah prediksi benar untuk genre yang mirip atau serupa
FP = 0 #jumlah prediksi salah untuk genre yang mirip atau serupa

Precision = TP/(TP+FP)
print("{0:.0%}".format(Precision))

