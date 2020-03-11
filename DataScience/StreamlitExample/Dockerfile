FROM python:3.7-slim
COPY iris_model_app.py rf_model.pkl requirements.txt config.toml credentials.toml /app/
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
RUN mkdir ~/.streamlit
RUN cp config.toml ~/.streamlit/config.toml
RUN cp credentials.toml ~/.streamlit/credentials.toml
##COPY config.toml ~/.streamlit/config.toml
##COPY credentials.toml ~/.streamlit/credentials.toml
WORKDIR /app
ENTRYPOINT ["streamlit", "run"]
CMD ["iris_model_app.py"]
