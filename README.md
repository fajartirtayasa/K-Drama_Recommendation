

# Laporan Proyek Machine Learning Terapan : Recommendation System



## [Project Overview]

*MyDramaList.com* adalah proyek berbasis komunitas yang  menyediakan drama & film Asia. Di situs web ini, penggemar dapat  membuat daftar pantauan drama mereka sendiri, menilai drama dan film, hingga menulis ulasan.

Proyek yang dirancang kali ini merupakan proyek membuat sistem rekomendasi K-Drama berdasarkan genre menggunakan data **Top 100 K-Drama MyDramaList** yang didownload dari kaggle. Dengan adanya sistem rekomendasi ini, pelanggan akan dapat dengan mudah mendapatkan rekomendasi K-Drama berdasarkan genre dari judul yang dicari atau yang telah diinput sebelumnya.



## [Business Understanding]

#### Problem Statement

Berdasarkan *project overview* di atas, maka diperoleh *problem statement* pada proyek ini, yaitu:

*"Bagaimana memberikan rekomendasi judul K-Drama berdasarkan genre pada setiap judul K-Drama yang diinput pengguna sehingga dapat memberikan referensi yang sesuai dengan minatnya?"*

#### Goals

Berdasarkan *problem statement* di atas, maka diperoleh tujuan dari proyek ini, yaitu:

*"Untuk membantu pengguna agar lebih mudah menemukan judul K-Drama berdasarkan genre dengan bantuan sistem rekomendasi."*

#### Solution Approach

Berdasarkan *problem statement* dan *goals* di atas, maka berikut solusi yang dapat dilakukan untuk mencapai tujuan dari proyek  ini, yaitu:

Menggunakan metode ***Content Based Filtering*** untuk merekomendasikan judul K-Drama berdasarkan kecocokan genre. Lebih jelasnya, *Content Based Filtering* merupakan metode rekomendasi berbasis konten yang merekomendasikan item yang memiliki kemiripan dengan item yang disukai/dipilih pengguna sebelumnya. Adapun kemiripan item dihitung berdasarkan fitur-fitur yang ada pada item yang dibandingkan [1]. Lebih lanjut, proses perhitungan kemiripan item akan dilakukan dengan ***Cosine Similarity***.

Kelebihan dari *Content Based Filtering* adalah *User Independence*, artinya metode ini tidak bergantung pada situasi apakah item tersebut merupakan item baru (yang belum pernah dipilih oleh pengguna manapun) maupun bukan item baru [2]. Misalnya, jika seorang pengguna telah memesan suatu menu hidangan pada kategori tertentu maka sistem akan mencoba merekomendasikan menu hidangan dengan kategori serupa yang juga tersedia di restoran lain yang mungkin akan disukai oleh pengguna tersebut.

Sedangkan kekurangan dari *Content Based Filtering* adalah terbatasnya rekomendasi yang hanya pada item-item yang mirip sehingga tidak ada kesempatan untuk mendapatkan item yang tidak terduga. [2]



## [Data Understanding]

Data yang digunakan dalam *recommendation system* ini merupakan data yang bersumber dari kaggle. Dataset ini berisikan detail informasi dari 100 drama korea teratas berdasarkan rating yang diberikan pengguna di situs web *MyDramaList.com*.

*Source Dataset*: [Top 100 Korean Drama](https://www.kaggle.com/datasets/chanoncharuchinda/top-100-korean-drama-mydramalist)

#### Variabel-Variabel pada Dataset Top 100 Korean Drama

- **Name**: nama drama korea.
- **Year of release**: tahun rilis drama.
- **Aired Date**: tanggal penayangan (mulai-selesai).
- **Aired On**: hari penayangan.
- **Number of Episode**: banyaknya episode.
- **Network**: jaringan/saluran media penayangan drama.
- **Duration**: durasi tiap episode.
- **Content Rating**: tingkatan konten (sesuai usia).
- **Synopsis**: sinopsis drama korea.
- **Cast**: aktor atau aktris dalam drama.
- **Genre**: genre drama korea.
- **Tags**: tag yang terdapat pada drama.
- **Rank**: peringkat di situs web.
- **Rating**: nilai rating untuk drama korea (1-10).

#### Descriptive Statistic

Tabel 1. Descriptive Statistic Data Numerikal

|       | Year of release | Number of Episode |   Rating   |
| :---: | :-------------: | :---------------: | :--------: |
| count |   100.000000    |    100.000000     | 100.000000 |
| mean  |   2017.970000   |     19.070000     |  8.723000  |
|  std  |    2.869044     |     12.378096     |  0.174573  |
|  min  |   2003.000000   |     6.000000      |  8.500000  |
|  25%  |   2017.000000   |     16.000000     |  8.600000  |
|  50%  |   2019.000000   |     16.000000     |  8.700000  |
|  75%  |   2020.000000   |     20.000000     |  8.800000  |
|  max  |   2021.000000   |    100.000000     |  9.200000  |



Tabel 2. Descriptive Statistic Data Kategorikal

|        |  Name   |  Aired Date  |    Aired On     | Network | Duration |     Content Rating      |              Synopsis              |             Cast              |                  Genre                   |                       Tags                        | Rank |
| :----: | :-----: | :----------: | :-------------: | :-----: | :------: | :---------------------: | :--------------------------------: | :---------------------------: | :--------------------------------------: | :-----------------------------------------------: | :--: |
| count  |   100   |     100      |       100       |   100   |   100    |           100           |                100                 |              100              |                   100                    |                        100                        | 100  |
| unique |   99    |     100      |        9        |   13    |    26    |            3            |                100                 |              99               |                    86                    |                        100                        | 100  |
|  top   | Kingdom | May 14, 2021 | Monday, Tuesday |   tvN   | 60 min.  | 15+ - Teens 15 or older | Geu Roo is a young autistic man... | Jo Jung Suk, Yoo Yeon Seok... | Psychological,  Comedy,  Romance,  Drama | Autism, Uncle-Nephew Relationship, Death, Sava... |  #1  |
|  freq  |    2    |      1       |       24        |   19    |    20    |           88            |                 1                  |               2               |                    4                     |                         1                         |  1   |

Beberapa informasi yang dapat diperoleh dari tahapan Descriptive Statistic berdasarkan Tabel 1 dan Tabel 2 di atas adalah:

- Dataset ini terdiri atas 100 baris dan 14 kolom (3 kolom dengan tipe data numerik, dan 11 kolom dengan tipe data object).
- Tidak terdapat *missing value* pada data. Dengan demikian, proses *handling missing value* tidak diperlukan.
- Tidak terdapat data yang duplikat pada dataset. Adapun judul yang sama pada kolom 'Name' mengartikan bahwa serial K-Drama tersebut dibagi  ke dalam 2 season yang dirilis pada waktu berbeda.
- Terdapat beberapa kolom yang memiliki *multiple value*, seperti kolom 'Aired On', 'Network', 'Genre', dan 'Tags'.

#### Univariate Analysis

<img src='https://drive.google.com/uc?export=view&id=1fz4R0vOuupM7e5ovx-uZHtJBpMFgE8be'>

Gambar 1. Banyak K-Drama Favorit berdasarkan Content Rating





<img src='https://drive.google.com/uc?export=view&id=1qLmqU3wPRFl6fVrkCe6dPOI6DuhRMLSF'>

Gambar 2. Banyak Penyedia Network untuk K-Drama Favorit





<img src='https://drive.google.com/uc?export=view&id=1IzwjicnIWSHwZv8NNwEgE7fO_OEyGjKT'>

Gambar 3. Banyak Setiap Genre untuk K-Drama Favorit



<img src='https://drive.google.com/uc?export=view&id=1e-qBxS5sO_NydeabePIbP5ZNojD5VclN'>

Gambar 4. 10 Tag dengan Kemunculan Terbanyak



<img src='https://drive.google.com/uc?export=view&id=1pI421MEKwTKPcnFKnLhkiHtGwUPoMr-d'>

Gambar 5. Banyak K-Drama Favorit yang Rilis Setiap Tahun





<img src='https://drive.google.com/uc?export=view&id=1tw3icz-0vRiYJGATQ2ZB5zdBy37Va-Wi'>

Gambar 6. Banyak Total Episode yang Digunakan K-Drama Favorit



<img src='https://drive.google.com/uc?export=view&id=1RU6GTjTiUs_OyCPvCzdURDuxkfmvowL-'>

Gambar 7. Distribusi Rating K-Drama Favorit



Beberapa informasi yang dapat diperoleh dari tahapan Univariate Analysis di atas adalah:

- Berdasarkan Gambar 1, dapat diketahui bahwa hampir seluruh data top 100 drama korea mensyaratkan penikmatnya berusia di atas 15 tahun. Sebagai kategori film yang khas dengan drama-drama dan alur percintaannya, adalah hal yang wajar apabila tontonan tersebut hanya boleh dikonsumsi oleh kalangan remaja hingga dewasa.
- Berdasarkan Gambar 2, dalam proses penayangan serial drama korea--tvN, Netflix, dan SBS berhasil menjadi network/penyedia layanan siaran yang paling banyak menggaet drama-drama korea terbaik untuk tayang pada platformnya.
- Berdasarkan Gambar 3, terdapat 5 genre yang mendominasi data top 100 drama korea, di antaranya adalah Drama, Romance, Comedy, Mistery, dan Thriller. Sementara itu genre Military, School, dan Food yang belum banyak tersentuh sepertinya dapat menjadi opsi bagi para pembuat drama korea untuk berupaya menyajikan tontonan drama korea dengan suasana dan alur cerita yang tidak biasa.
- Berdasarkan Gambar 4, dapat diketahui bahwa 3 tags terbanyak yang muncul pada mayoritas top 100 drama korea adalah 'Strong Female Lead', 'Smart Female Lead', dan 'Bromance'. Selain karena alur percintaannya, ternyata penonton drama korea juga cenderung menyukai karakter pemeran wanita yang kuat dan cerdas.
- Berdasarkan Gambar 5, apabila dilihat dari trennya, banyak drama korea terbaik di setiap tahun cenderung mengalami kenaikan seiring dengan berjalannya waktu. Hal ini menandakan bahwa industri ini memang berkembang dan terus melakukan *improvement* agar dapat diterima dengan baik oleh masyarakat. Dalam sudut pandang lain, hal ini bisa juga menandakan bahwa penikmat K-Drama lebih menyukai drama korea dengan tahun rilis terbaru untuk menghindari kejenuhan yang mungkin disajikan di drama korea dengan tahun rilis lama.
- Berdasarkan Gambar 6, dapat diketahui bahwa mayoritas top 100 drama korea membagi keseluruhan ceritanya ke dalam 12, 16, atau 20 episode. Hal ini menandakan drama korea yang ideal bagi penikmatnya tidak perlu memiliki puluhan ataupun ratusan episode.
- Berdasarkan Gambar 7, dapat diketahui bahwa data top 100 drama korea memiliki interval rating antara 8.5 hingga 9.2, dengan rata-rata rating sebesar 8.72 (pada *Descriptive Statistic*).



## [Data Preparation]

Teknik yang digunakan pada tahapan Data Preparation ini adalah vektorisasi fungsi CountVectorizer dari library scikit-learn. CountVectorizer digunakan untuk mengubah teks yang diberikan menjadi vektor berdasarkan frekuensi (jumlah) setiap kata yang muncul di seluruh teks.

CountVectorizer membuat matriks di mana setiap kata unik diwakili oleh kolom matriks, dan setiap sampel teks dari dokumen adalah baris dalam matriks. Nilai setiap sel tidak lain adalah jumlah kata  dalam sampel teks tertentu. [3]

Pada proses vektorisasi ini, digunakan beberapa metode sebagai berikut.

- **fit()**, berfungsi untuk melakukan perhitungan idf pada data.
- **get_feature()**, berfungsi untuk melakukan mapping array dari fitur index integer ke fitur nama.
- **fit_transform()**, berfungsi untuk mempelajari kosa kata dan Inverse Document Frequency (IDF) dengan memberikan nilai *return* berupa *document-term matrix*.
- **todense()**, berfungsi untuk mengubah vektor TF-IDF dalam bentuk matriks.



## [Modelling and Results]

Sistem rekomendasi yang digunakan pada proyek ini menggunakan metode ***Content Based Filtering*** dengan penerapan ***Cosine Similarity***  sebagai teknik untuk menghitung kesamaan antar item.

Model *Content Based Filtering* bekerja dengan mempelajari profil minat pengguna berdasarkan data dari objek yang telah dinilai pengguna. Metode ini dapat memberi saran item yang serupa dengan yang pernah disukai sebelumnya atau sedang dilihat sekarang berdasarkan kategori tertentu. Lebih lanjut, *Cosine Similarity* merupakan salah satu teknik untuk mengukur kesamaan--yang bekerja dengan menghitung sudut cosinus antara dua buah vektor. Semakin kecil sudut cosinus, maka semakin besar nilai *Cosine Similarity*.



<img src='https://latex.codecogs.com/svg.image?cos(\Theta&space;)=\frac{\vec{a}.&space;\vec{b}}{\left|&space;\vec{a}\right|.\left|&space;\vec{b}\right|}'>

Gambar 8. Fungsi *Cosine Similarity*



Berikut adalah nilai *cosine similarity* dari 5 contoh judul K-Drama berdasarkan beberapa kumpulan Genre.



Tabel 3. Nilai *Cosine Similarity* untuk 5 Contoh Judul K-Drama

|          JUDUL K-DRAMA          | Friendship,  Comedy,  Life,  Drama | Business,  Comedy,  Crime,  Drama | Thriller,  Mystery,  Horror,  Supernatural | Drama,  Sports,  Melodrama | Thriller,  Mystery,  Drama,  Political | Thriller,  Mystery,  Law,  Drama | Comedy,  Romance,  Drama | Action,  Comedy,  Romance,  Melodrama | Action,  Thriller,  Mystery,  Crime | Historical,  Romance,  Fantasy,  Political |
| :-----------------------------: | :--------------------------------: | :-------------------------------: | :----------------------------------------: | :------------------------: | :------------------------------------: | :------------------------------: | :----------------------: | :-----------------------------------: | :---------------------------------: | :----------------------------------------: |
|              Mouse              |              0.000000              |             0.000000              |                  0.577350                  |          0.000000          |                0.577350                |             0.577350             |         0.000000         |               0.000000                |              0.577350               |                  0.000000                  |
|           Racket Boys           |              0.500000              |             0.250000              |                  0.000000                  |          0.288675          |                0.000000                |             0.000000             |         0.288675         |               0.250000                |              0.000000               |                  0.000000                  |
| What's Wrong with Secretary Kim |              0.500000              |             0.500000              |                  0.000000                  |          0.000000          |                0.000000                |             0.000000             |         0.577350         |               0.500000                |              0.000000               |                  0.250000                  |
|      Hometown Cha-Cha-Cha       |              0.577350              |             0.288675              |                  0.000000                  |          0.000000          |                0.000000                |             0.000000             |         0.666667         |               0.577350                |              0.000000               |                  0.288675                  |
|    Strong Woman Do Bong Soon    |              0.408248              |             0.408248              |                  0.408248                  |          0.235702          |                0.408248                |             0.408248             |         0.707107         |               0.612372                |              0.408248               |                  0.204124                  |

Nilai *cosine similarity* berkisar antara 0 hingga 1. Semakin besar nilai *cosine similarity*, artinya semakin erat pula kesamaan antara genre suatu judul K-Drama dengan kumpulan genre tertentu. Selanjutnya, pemanggilan rekomendasi judul K-Drama menggunakan fungsi yang dibuat dengan kode sebagai berikut.

``` python
#indikasi judul K-Drama berdasarkan urutan data
indices = pd.Series(index = content_df['Name'], data = content_df.index)

#membuat fungsi untuk memanggil 10 rekomendasi K-Drama berdasarkan judul yang diinput
def get_recommendations(judul, cosine_sim = cosine_sim, 
                        items = content_df[['Name', 'Year of release', 'Genre']]):
    idx = indices[judul]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key = lambda x : x[1], reverse = True)
    sim_scores = sim_scores[1:11]
    drama_indices = [i[0] for i in sim_scores]
    return pd.DataFrame(content_df['Name'][drama_indices]).merge(items)
```

Tahapan yang dilakukan pada fungsi `get_recommendations` di atas adalah:

1. Mengambil indeks dari judul K-Drama yang telah didefinisikan dalam variabel `indices`,
2. Mengambil skor kemiripan dengan semua judul,
3. Mengurutkan K-Drama berdasarkan skor kemiripan,
4. Mengambil 10 data dengan skor kemiripan tertinggi (indeks 1-11), dan
5. Menampilkan dataframe rekomendasi 10 K-Drama.



Tabel 4. Contoh K-Drama yang akan diuji.

|      |           Name            | Year of release |          Genre           |
| :--: | :-----------------------: | :-------------: | :----------------------: |
|  90  | Dali and the Cocky Prince |      2021       | Comedy,  Romance,  Drama |



Tabel 5. Top 10 Rekomendasi K-Drama dengan Genre Serupa pada 'Dali and the Cocky Prime'

|      |             Name              | Year of release |                       Genre                       |
| :--: | :---------------------------: | :-------------: | :-----------------------------------------------: |
|  0   |   It's Okay to Not Be Okay    |      2020       |     Psychological,  Comedy,  Romance,  Drama      |
|  1   |       Kill Me, Heal Me        |      2015       |     Psychological,  Comedy,  Romance,  Drama      |
|  2   |    It's Okay, That's Love     |      2014       |     Psychological,  Comedy,  Romance,  Drama      |
|  3   |     My Father is Strange      |      2017       |         Comedy,  Romance,  Drama,  Family         |
|  4   |     My Love from the Star     |      2013       |      Comedy,  Romance,  Drama,  Supernatural      |
|  5   |          Once Again           |      2020       |         Comedy,  Romance,  Drama,  Family         |
|  6   |         Yumi's Cells          |      2021       |     Psychological,  Comedy,  Romance,  Drama      |
|  7   | Because This Is My First Life |      2017       |          Comedy,  Romance,  Life,  Drama          |
|  8   |   When the Camellia Blooms    |      2019       |   Thriller,  Comedy,  Romance,  Drama,  Family    |
|  9   |   Strong Woman Do Bong Soon   |      2017       | Action,  Thriller,  Comedy,  Romance,  Drama, ... |

Berdasarkan Tabel 4 dan Tabel 5 di atas, dapat dilihat bahwa seseorang yang mencari, menonton, ataupun menyukai K-Drama 'Dali and the Cocky Prime' dengan genre Comedy, Romance, dan Drama; diberikan 10 rekomendasi K-Drama lain yang mengandung genre serupa.



## [Evaluation]

*Metric* yang digunakan pada sistem rekomendasi K-Drama berdasarkan genre ini adalah ***precision***. *Precision* adalah metrik yang membandingkan rasio prediksi benar atau positif dengan keseluruhan hasil yang diprediksi positif. Pada penerapannya, *metric* ini akan membandingkan antara banyaknya rekomedasi K-Drama yang memiliki genre mirip atau serupa, dengan keseluruhan rekomendasi K-Drama yang diberikan.



Berikut adalah perhitungan *metric Precision*.

```python
TP = 10 #jumlah prediksi benar untuk genre yang mirip atau serupa
FP = 0 #jumlah prediksi salah untuk genre yang mirip atau serupa

Precision = TP / (TP+FP)
print("{0:.0%}".format(Precision))
```

Hasil perhitungan *Presicision* di atas adalah `100%`. Hal ini menunjukkan bahwa rekomendasi dari metode *Content Based Filtering* yang diberikan untuk K-Drama 'Dali and the Cocky Prime' sudah memiliki performa yang baik karena berhasil merekomendasikan beberapa K-Drama lain yang mengandung genre Comedy, Romance, dan Drama.



#### **Kesimpulan dan Rekomendasi**

Metode *Content Based Filtering* cocok untuk digunakan ketika ingin membuat sistem rekomendasi berdasarkan kemiripan fitur-fitur pada objek pengamatan. Berdasarkan hasil analisis dan pemodelan untuk kasus ini, metode *Content Based Filtering* memiliki performa yang cukup baik ketika merekomendasikan top-N K-Drama berdasarkan kemiripan genre-genre tertentu. Namun meskipun demikian, masih perlu adanya *improvement* lanjutan untuk memperkaya opsi rekomendasi lainnya.

Berikut adalah beberapa saran *improvement* yang dapat dieksplorasi:

- Gunakan variabel kategorik lain sebagai acuan rekomendasi, contohnya adalah variabel 'Tags'.
- Gunakan metode ***Collaborative Filtering*** untuk membuat sistem rekomendasi berdasarkan pendapat pengguna lain, contohnya adalah rating dari K-Drama.



## **[Daftar Referensi]**

[1] F. Ricci, et.al., “Introduction to Recommender Systems Handbook”. MA: Springer,  US, pp. 1–35, 2011.

[2] Rhesa. H. M, et al., "Recommendation System with Content-Based Filtering Method for Culinary Tourism in Mangan Application". ITSMART: Jurnal Ilmiah Teknologi dan Informasi, Vol 8, No.2. 65-72, 2019.

[3] Khushali, V. "Using CountVectorizer to Extracting Features from Text". https://www.geeksforgeeks.org/using-countvectorizer-to-extracting-features-from-text/ [accesed Dec. 6 2022]
