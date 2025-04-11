import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

def Title():
    st.markdown("""
        <div style="background-color:#8b0000; padding:10px; border-radius:8px;">
            <h1 style="color:#efefe9; text-align:center;">Review Analysis</h1>
        </div>
        """, unsafe_allow_html=True,
    )

def showReviews():

    try:
        with open("my_reviews.json", "r") as file:
            reviews = json.load(file)
            st.markdown(
            """
            <style>
            body {
                background-color: #f4f7fc;
                font-family: Arial, sans-serif;
            }
            .Container {
                background:  #ddedea;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                border: 1px solid #d1d9e6;
                padding: 20px;
                gap: 20px;
                margin-bottom: 20px;
                align-items: flex-start;
                display: flex;
                
            }
            
            .circle_Diner {
                width: 50px;
                height: 50px;
                background-color: #8b0000;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                font-weight: bold;
                align-items: center;
                color: white;
                font-size: 18px;
            }
            .Container:hover {
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
                transform: translateY(-5px);
            }
            .Diner_Name {
                text-align: center;
                margin-top: 8px;
                font-size: 14px;
                color: #33475b;
                font-weight: bold;
            }
            .review_meassage {
                flex: 1;
            }
            .top_of_review {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
            }
            .rating {
                display: inline-block;

            }
            .rating .star {
                width: 20px;
                height: 20px;
                display: inline-block;
                background-color: #8b0000;
                clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
                margin-right: 4px;
            }
            .rating .star.blank {
                background-color: #ffffff;
            }
            .date {
                font-size: 14px;
                color: #0c0c0c;
            }
            .review {
                margin-top: 10px;
                font-size: 16px;
                color: #4a5568;
            }
            .Rating {
                margin-top: 12px;
                font-size: 14px;
                color: #0c0c0c;
            }
            .Rating span {
                font-weight: bold;
                color: #8b0000;
            }
            .food {
                color: #044330;
                font-size: 14px;
            }
            .staff {
                color: #5a352c;
                font-size: 14px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )


        for r in reviews.values():
            firstAlpha = r['Name'][0].upper()
            stars = ""
            for i in range(5):
                if i < r['Overall_Rating']:
                    stars += '<div class="star"></div>'
                else:
                    stars += '<div class="star blank"></div>'

            html = f"""
            <div class="Container">
                <div>
                    <div class="circle_Diner">{firstAlpha}</div>
                    <div class="Diner_Name">{r['Name']}</div>
                </div>
                <div class="review_message">
                    <div class="top_of_review">
                        <div class="rating">{stars}</div>
                        <div class="date">Dined on {r['Date']}</div>
                    </div>
                    <div class="review">
                        <p class = "food"> {r['Food']}</p>
                        <p class = "staff"> {r['Staff']}</p>
                    </div>
                    <div class="Rating">
                        <strong>Ratings:</strong> 
                        Overall (<span>{r['Overall_Rating']}</span>), 
                        Food (<span>{r['Food_Rating']}</span>), 
                        Service (<span>{r['Service_Rating']}</span>), 
                        Ambience (<span>{r['Ambience_Rating']}</span>)
                    </div>
                </div>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)

            
    except FileNotFoundError:
        st.error("The file was not found.")
        return

    

        
Title()
showReviews()