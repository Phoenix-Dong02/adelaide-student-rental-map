# Adelaide Student Rental Map

A Streamlit-based rental map platform designed for Chinese students in Adelaide.

---
## 🚨 Problem

Most rental platforms are property-centric.  
Although they provide map views, listings are often expensive due to agency fees.

As a result, many students turn to free platforms such as AdelaideBBS.

However, these platforms have major limitations:
- Listings are post-based and sorted by time, not relevance
- Older but still available properties are easily buried
- Users must manually search and filter through large volumes of posts
- No clear visualization of location or price distribution

---

## 💡 Insight

Budget-sensitive students care more about **location and price distribution**  
than browsing individual listings one by one.

However, existing free platforms do not support efficient location-based exploration.

---

## 🚀 Solution

This project introduces a **map-first rental platform** that:

- Visualizes all available listings directly on a map
- Allows users to quickly understand price distribution across locations
- Surfaces low-cost listings that would otherwise be buried in post-based platforms
- Eliminates the need for manual searching through fragmented posts

---

## 🎯 Value

- Transforms rental search from **time-based browsing → location-based decision-making**
- Makes hidden affordable housing easier to discover
- Significantly reduces search effort for students
---

## ✨ Features

- Interactive rental map using Folium
- Filters for price, room type, suburb, furniture, and bills
- Listing cards with detailed property information
- Image browsing for each property
- Summary table for filtered results

---

## 🛠 Tech Stack

- Python
- Streamlit
- Pandas
- Folium

---

## 👥 Target Users

Chinese international students in Adelaide who want a more visual and efficient way to compare rental options.

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
