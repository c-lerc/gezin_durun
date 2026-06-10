@echo off
echo ====================================================
echo Yapay Zeka Destekli Gezi Rehberi - Baslatici
echo ====================================================

echo 1. Strapi calisiyor mu kontrol ediliyor... (Lutfen baska bir terminalde "npm run dev" ile Strapi'nin calistigindan emin olun)

echo 2. Python bagimliliklari yukleniyor...
cd python_engine
pip install -r requirements.txt
echo Python AI ve Web Scraping Motoru baslatiliyor...
python main.py
cd ..

echo 3. Streamlit Arayuzu baslatiliyor...
cd frontend
pip install -r requirements.txt
streamlit run app.py
cd ..

echo Islem tamamlandi.
pause
