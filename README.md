<div align=center><img src="frontend/src/assets/logo.png" alt="logo" width="500"/></div>

# EasyLatex

This is the project for **IS305: Application Software Course Design** (SJTU，2021 Spring).

EasyLatex is an easy-to-use tool to **get Latex from OCR and edit the mathematical formulas**. The project is based on *Django+Vue+Element-UI*. 

Below is a demo.

<img src="界面.png" alt="界面" style="zoom:75%;" />

## Install

The back-end is developed with `python3.6`. Make sure you have an available environment. In your environment, install the required packages.

```sh
$ pip install -r requirements.txt
```

This project uses [npm](https://npmjs.com). Go check them out if you don't have them locally installed. Then execute the following commands.

```sh
$ cd frontend
$ npm install --save axios
$ npm install -g @vue/cli
$ npm install
$ npm run build
```

## Usage

Enter the home directory and execute the following commands.

```sh
$ cd IS305_EasyLatex_Web
$ python manage.py runserver
```

At this point, you can already access the page at http://127.0.0.1:8000.

## Code

The main code for frontend is [EasyLatex_Page.vue](frontend/src/components/EasyLatex_Page.vue) and [App.vue](frontend/src/App.vue). The main code for backend is [backend/views.py](backend/views.py).

## Related Work

 [XunFei API for FormulaRecognition](https://www.xfyun.cn/service/formula-discern)（科大讯飞公式识别API）

