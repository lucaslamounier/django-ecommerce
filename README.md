# Django Ecommerce
Loja virtual - Projeto utilizado para fins de aprendizagem.

![image](https://cloud.githubusercontent.com/assets/5832193/17952257/3ee3156e-6a3f-11e6-8add-6eeccbf68e3c.png)

## Instalação

### Clone o projeto
```
git clone https://github.com/gileno/djangoecommerce
cd djangoecommerce
```

### virtualenv
```
virtualenv env -p python3
```
Linux
```
source env/bin/activate
```
Windows
```
env\Scripts\activate.bat
```



## Instale as dependencias
```
pip install -r requirements.txt
python manage.py runserver
```
# install watson
```
python manage.py installwatson

register models for works with watson
in your_app/apps.py

python manage.py buildwatson

create cache

python manage.py createcachetable
```
