# # AI for Rural Fires Detection

This project was developed for the ""Projeto-Estágio de Inteligência Artificial e Ciência de Dados"" course and aims to develop AI models capable of detecting wildfires in images and to generalize well on unseen data.
Second Semester of the Third Year of the Bachelor's Degree in Artificial Intelligence and Data Science.

<br>

## Programming Language:

<div style = "display: inline_block"><br/>
  <img align="center" alt="python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</div><br/>

<br>

## Requirements:

	- python: 3.10.14
	- Tensorflow: 2.13.0
	- Numpy == 1.32.5
	- Pandas == 1.5.3
	- Matplotlib == 3.7.1

You can use other versions of these libraries as long as they are compatible with each other.

<br>

## About the Repository

The repository is divided as follows:

```
RuralFiresReport_MagdCosta.pdf

Project_code
├── Phase_1
│   ├── *.ipynb
├── Phase_2
│   ├── *.ipynb
├── Phase_3
│   ├── *.ipynb
├── Phase_4
│   ├── *.ipynb
├── Criar_Mixed_Datasets-ipynb
├── _Criar_Datasets_.ipynb
├── requirements.txt

WebApp
├── ImageSamples
│   ├── *.png
│   ├── *.jpg
├── Models
│   ├── *.h4
├── public
│   ├── index.html
│   ├── styles.css
│   ├── scripts.js
├── model_loader.py
├── app.py
├── requirements.txt

```

The `RuralFiresReport_MagdCosta.pdf`is an extensive report of the work developed.
The `Project_code` has the jupyter notebooks created and used in order to develop this project. The corresponding jupyters of each model and phase are divided in 4 folders. There are also two jupyters that I used to create the csv files to use the images from the three datasets and to create de combined datasets.
The `WebApp` has the code of a web app used to test several images, even uploaded from your computer on the models developed in this project.
Both `Project_code` and `WebApp` folders have a `requirements.txt` file, since I used two different virtual environments to run the respective codes.


## Setting up to run the Project

In order to facilitate the use of our code, we provide the requiremts.txt of the virtual environments we used for the project. If you want to use it to facilitate the installation of libraries and dependencies, you should do the following:

1. We recommend the creaton of an enviroment, if you don't want to do this, skip to step [3]

You can create an environment by typing this on your terminal:
```bash
python3.10 -m venv project
```
This code allows you to create an environment called `webots-env`.
If you don't have `venv` installed you can do this:

```bash
sudo apt install python3.10 python3.10-venv python3.10-dev
```
2. Once you have your virtual environment you need to activate it by typing:

```bash
source project/bin/activate
```
We are considering that you created the virtual environment at `~`. If that's not the case you need to write the correct path or move to the correct folder.

3. When you are ready to install the requirements, download the file `requirements.txt` and type this:

```bash
pip install -r requirements.txt
```

Note: For this project I used the WSL (Windows Subsystem for Linux) as it enabled GPU use.

<br>

## Link to the course: 

This course is part of the **<u>second semester</u>** of the **<u>third year</u>** of the **<u>Bachelor's Degree in Artificial Intelligence and Data Science</u>** at **<u>FCUP</u>** and **<u>FEUP</u>** in the academic year 2024/2025. You can find more information about this course at the following link:

<div style="display: flex; flex-direction: column; align-items: center; gap: 10px;">
  <a href="https://sigarra.up.pt/fcup/pt/UCURR_GERAL.FICHA_UC_VIEW?pv_ocorrencia_id=546538">
    <img alt="Link to Course" src="https://img.shields.io/badge/Link_to_Course-0077B5?style=for-the-badge&logo=logoColor=white" />
  </a>

  <div style="display: flex; gap: 10px; justify-content: center;">
    <a href="https://sigarra.up.pt/fcup/pt/web_page.inicial">
      <img alt="FCUP" src="https://img.shields.io/badge/FCUP-808080?style=for-the-badge&logo=logoColor=grey" />
    </a>
    <a href="https://sigarra.up.pt/feup/pt/web_page.inicial">
      <img alt="FEUP" src="https://img.shields.io/badge/FEUP-808080?style=for-the-badge&logo=logoColor=grey" />
    </a>
  </div>
</div>
