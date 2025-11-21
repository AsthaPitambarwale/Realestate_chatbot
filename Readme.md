## 🏢 Real Estate AI



Real Estate Market Analysis with AI-Powered Insights



Analyze real estate datasets, generate professional summaries, compare areas, and visualize trends in price and demand with a sleek web interface.



#### 🌟 Features



📊 **AI-Powered Query Analysis:** Ask questions in natural language and get market summaries.



📈 **Trend Visualization:** Interactive charts showing price \& demand trends.



🏘 **Area Comparison:** Compare multiple localities with insights on demand and sales trends.



💾 **Dataset Upload:** Upload Excel files and instantly analyze your data.



📁 **CSV Export:** Download filtered data for offline use.



🌙 **Dark/Light Mode:** Sleek UI with theme toggle.



📚 **Professional Summaries:** Market overview with multi-year insights.



#### ⚙️ Tech Stack



**Backend:** Django, Django REST Framework, Pandas, NumPy



**Frontend:** React, Chart.js, TailwindCSS, Lucide Icons



**Optional:** OpenAI API for enhanced query processing



#### 🚀 Installation



##### Backend Setup



1. git clone <repo\_url>
2. cd realestate-chatbot
3. python -m venv venv
4. source venv/bin/activate  # Linux/Mac
5. venv\\Scripts\\activate     # Windows
6. pip install -r requirements.txt
7. python manage.py migrate
8. python manage.py runserver



##### Frontend Setup



1. cd frontend
2. npm install
3. npm start





Open http://localhost:3000 in your browser to access the app.



#### 🔍 Queries Supported



1️⃣ **Single Area Market Summary**



Example: Show market summary for Pimpri



Outputs:



* Demand \& sales trends



* Pricing insights



* Supply overview



* Professional summary



* Trend chart (price \& demand)



2️⃣ **Area Comparison**



Example: Compare Akurdi vs Chinchwad



Outputs:



* Comparative demand trend summary



* Trend chart showing both areas



* Insights on differences in sales \& prices



3️⃣ **Price Growth**



Example: Show price growth for Akurdi over the last 3 years



Outputs:



* Year-wise average price



* Interactive trend chart for last 3 years



#### 🗂 Project Structure



real-estate-ai/

│

├─ backend/

│   ├─ api/

│   │   ├─ views.py

│   │   ├─ utils.py          # Data processing, chart generation, summaries

│   │   └─ urls.py

│   └─ manage.py

│

├─ frontend/

│   ├─ src/

│   │   ├─ components/

│   │   │   ├─ Sidebar.js

│   │   │   ├─ TrendChart.js

│   │   ├─ pages/

│   │   │   ├─ Dashboard.js

│   │   │   ├─ Upload.js

│   │   │   ├─ Analysis.js

│   │   └─ App.js

│   └─ package.json

│

└─ README.md



#### 🖥 Frontend Components



Sidebar.js – Navigation links with dark/light toggle.



TrendChart.js – Interactive line chart for price \& demand trends.



Pages:



Dashboard.js – Overview of datasets.



Upload.js – Excel dataset upload.



Analysis.js – AI query interface with summaries \& charts.



#### 💡 Notes



* Dataset Columns: Area, Year, Flat Sold - IGR, Shop Sold - IGR, Flat - Weighted Average Rate, etc.



* Chart.js: Ensure datasets object contains price and demand arrays for chart rendering.



* Caching: Dataset is stored in memory (DATA\_CACHE) for faster queries.



* Dark Mode: TailwindCSS dark classes toggle on Sidebar.



* OpenAI Integration: Optional; configure OPENAI\_API\_KEY in settings.py.



#### 📬 Contact



For issues or feature requests, open an issue or contact the developer.

