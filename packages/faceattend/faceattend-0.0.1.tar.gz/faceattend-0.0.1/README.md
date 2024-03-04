# Face Attend
**An attendance system using face detection**

#### Whats working?
- Adding face data of a person to the database
- Detect face of known person using video feed
- Mark attendance of a valid person when detected
- Generating a csv file with attendance for a particalar date



## Instructions 📝
- **Create a virtual environment:**
     ```python3 -m venv .venv```
- **Activate the virtual environment:**
    ```source .venv/bin/activate```
- **Install the packages:**
    ```pip install -r requirements.txt```

>[!NOTE]
The above instructions are specific to macOS and Linux.</br>

### Windows specific instructions
- **Creating virtual environments see [here](https://docs.python.org/3/library/venv.html#creating-virtual-environments)**</br>
- **For issues with installation of the face-recognition package see [here](https://stackoverflow.com/questions/70001837/problem-in-installing-python-library-face-recognition-on-windows-10-11)**

   
## Database setup 🛢
### Create the database file
- Create a ```valid_persons.db``` file at the root of this folder

- Then import the required tables</br>
```cat schema.sql | sqlite3 valid_persons.db```

### Add valid faces in database
- Open the python interactive console</br>
```python3``` or ```python```

- Import the ```Face``` class from ```encode_face``` module</br>
```from encode_face import Face```

- Now use the ```Face``` class's add_face method to add face data and name of the person </br>
```Face.add_face("Person's Name","Path to the Person's image file")```

- If the face was added successfully it will display</br>
```Face Added```



## How to run?
```python3 detect.py``` or ```python detect.py```
