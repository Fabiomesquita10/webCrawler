
from controllers.analyticsController import analyticsRouter
from controllers.productController import productRouter
from controllers.userController import userRouter
from controllers.cartController import cartRouter
from controllers.scraperController import scraperRouter
from fastapi import FastAPI
import uvicorn

app = FastAPI()
app.include_router(productRouter)
app.include_router(analyticsRouter)
app.include_router(userRouter)
app.include_router(cartRouter)
app.include_router(scraperRouter)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
