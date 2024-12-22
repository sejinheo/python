from fastapi import FastAPI
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = FastAPI()

DATA_PATH = "data/food_orders.csv"
data = pd.read_csv(DATA_PATH)

# 홈 화면
@app.get("/")
async def read_root():
    return {"message": "배달 음식 소비 트렌드 분석 API입니다!"}

# 시간대별 주문량 분석
@app.get("/orders-by-time/")
async def orders_by_time():
    data['order_time'] = pd.to_datetime(data['order_time'])
    data['hour'] = data['order_time'].dt.hour
    hourly_orders = data['hour'].value_counts().sort_index()

    plt.figure(figsize=(10, 5))
    hourly_orders.plot(kind='bar', color='skyblue')
    plt.title('시간대별 음식 주문량')
    plt.xlabel('시간대')
    plt.ylabel('주문 수')
    graph_path = 'static/orders_by_time.png'
    plt.savefig(graph_path)
    plt.close()

    return {"message": "시간대별 주문량 분석 완료", "graph": f"/{graph_path}"}

# 인기 메뉴 분석
@app.get("/popular-menu/")
async def popular_menu():
    popular_menu = data['menu'].value_counts().head(5)
    
    plt.figure(figsize=(10, 5))
    sns.barplot(x=popular_menu.index, y=popular_menu.values, palette='coolwarm')
    plt.title('인기 메뉴 TOP 5')
    plt.xlabel('메뉴')
    plt.ylabel('주문 수')
    graph_path = 'static/popular_menu.png'
    plt.savefig(graph_path)
    plt.close()

    return {"message": "인기 메뉴 분석 완료", "graph": f"/{graph_path}"}
