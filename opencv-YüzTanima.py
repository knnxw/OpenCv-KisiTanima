import cv2
import cv2
import os
import time
from simple_facerec import SimpleFacerec

# Yüz tanıma için gerekli dosyaları yükle
sfr = SimpleFacerec()

# Kamera başlat
cap = cv2.VideoCapture(0)
ascii_art="""
 _  __    ___   _
| |/ / \ | | \ | |
| ' /|  \| |  \| |
| . \| |\  | |\  |
|_|\_\_| \_|_| \_|"""
def listele_kisiler():
    kisiler = [f.replace('.jpg', '') for f in os.listdir("images") if os.path.isfile(os.path.join("images", f))]
    if not kisiler:  # Eğer liste boşsa
        print("Kimse ekli değil.Lütfen yeni kişiler ekleyin.")
        time.sleep(2)
        return []
    for idx, kisi in enumerate(kisiler, 1):
        print(f"{idx}-{kisi}")
    return kisiler


try:
    while True:
        print(ascii_art)
        time.sleep(0.5)
        print(" ")
        print("OPENCV - YÜZ TANIMA SİSTEMİ 1.0")
        print("_______________________________")
        print("                               |")
        print("[1] Yüz Tanıma.                |")
        print("[2] Yeni Kişi Ekleme.          |")
        print("[3] Kişi Silme.                |")
        print("                               |")
        print("[4] İnfo.                      |")
        print("[99] Çıkış.                    |")
        print("_______________________________|")
        print(" ")
        mod = input("Seçeneğinizi seçin:  ")
        print("                               ")
        print("                               ")
        print("                               ")

        if mod == "1":
             print("Yüz Tanıma Modu")
             time.sleep(0.5)
               # Diğer işlemler

             sfr.load_encoding_images("images/") 
                # Yüz tanıma modu
             while True:
                    ret, cerceve = cap.read()
                    if not ret:
                        print("Kamera görüntüsü alınamıyor.")
                        break

                    yuz_konumlar, yuz_isimler = sfr.detect_known_faces(cerceve)
                    if not yuz_isimler:  # Eğer hiçbir yüz tanınmadıysa
                        print("Hiçbir yüz bulunamadı.")

                    for yuz_konum, isim in zip(yuz_konumlar, yuz_isimler):
                        y1, x2, y2, x1 = yuz_konum
                        cv2.putText(cerceve, isim, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                        cv2.rectangle(cerceve, (x1, y1), (x2, y2), (0, 0, 200), 4)

                        if isim != "Bilinmeyen":
                            print(isim + " Tanındı.")
                        else:
                            print("Kişi sisteme ekli değil.")

                    cv2.imshow("Cerceve", cerceve)

                    if cv2.waitKey(1) == 27:
                        cv2.destroyAllWindows()
                        # ESC tuşu ile çıkış
                        break

        elif mod == "2":
            print("Yeni kişi ekleme modu")
            time.sleep(0.5)
            # Yeni kişi ekleme modu
            print("Boşluk tuşuna basıldığında fotoğraf kaydedilecek.")
            while True:
                ret, cerceve = cap.read()
                cv2.imshow("Cerceve", cerceve)

                tus = cv2.waitKey(1)
                if tus == 32:  # Boşluk tuşu ile fotoğraf çek
                    cv2.destroyAllWindows()
                    img_isim = input("Kaydedilecek kişinin ismini girin: ")
                    if not img_isim.strip():
                        print("Geçersiz isim. Lütfen geçerli bir isim girin.")
                        continue
                    img_yol = os.path.join("images", img_isim + ".jpg")
                    cv2.imwrite(img_yol, cerceve)
                    print(f"{img_yol} olarak fotoğraf kaydedildi.")
                    cv2.destroyAllWindows()
                    break
                elif tus == 27:  # ESC tuşu ile çıkış ve çerçeveyi kapat
                    cv2.destroyAllWindows()
                    break
        elif mod == "3":
            kisiler = listele_kisiler()
            if kisiler:  # Sadece liste boş değilse kullanıcıdan girdi al
                silinecek_kisiler_num = input("Silmek istediğiniz kişilerin numaralarını aralarına virgül koyarak girin: ")
                silinecek_kisiler_num = [int(num) - 1 for num in silinecek_kisiler_num.split(',') if num.isdigit()]

                for num in silinecek_kisiler_num:
                    if 0 <= num < len(kisiler):
                        silinecek_kisi = kisiler[num]
                        os.remove(os.path.join("images", silinecek_kisi + ".jpg"))
                        print(f"{silinecek_kisi} silindi.")
                    else:
                        print(f"Geçersiz seçim: {num + 1}. Lütfen listedeki bir numarayı girin.")
        elif mod == "4":
              print("""
    OPENCV - YÜZ TANIMA SİSTEMİ 1.0

    Bu program, OpenCV ve simple_facerec kütüphanelerini kullanarak geliştirilmiş,
    temel düzeyde bir yüz tanıma sistemini içerir.
    
    Kullanım:
    1. Programı başlatın.
    2. Menüden istediğiniz işlemi seçin:
       - [1] Yüz Tanıma: Tanıdığı kişileri gösterir.
       - [2] Yeni Kişi Ekleme: Yeni kişiler eklemenizi sağlar.
       - [3] Kişi Silme: Sisteme ekli kişileri silebilirsiniz.
       - [99] Çıkış: Programı kapatır.

    Proje Bilgileri:
    - Versiyon: 1.0
    - Geliştirici: Kenan OZAN ♥ Azra TURAN

    """)
              time.sleep(5)
        elif mod == "99":
            print("Good by :)")
            break

        else:
            print("Geçersiz seçenek. Lütfen 1, 2, 3 veya 4 giriniz.")

except Exception as e:
  print(f"Hata: İsimsiz dosya & Kimse ekli değil. Lütfen kontrol edin")

finally:
    cap.release()
    cv2.destroyAllWindows()
