# Face Attend
<p align="center">
    <img width = "300" height = "300" src="https://raw.githubusercontent.com/AkashMondal1998/FaceAttend/main/face_attend.png">
</p>



## Whats working?
- [x] Adding face data of a person to the database
- [x] Detect face of known person using video feed
- [x] Provide audio feedback when attendance marked successfully 
- [x] Mark attendance of a valid person when detected
- [x] Generating a csv file with attendance for a particular date or a particular employee

## Todo
- [ ] Further improve the face recognition model

## Built with
- [face-recognition](https://github.com/ageitgey/face_recognition)
- [opencv-python](https://github.com/opencv/opencv-python)
- [gTTS](https://github.com/pndurette/gTTS)
- [pygame](https://github.com/pygame/pygame)
- [python-email-validator](https://github.com/JoshData/python-email-validator)

## Instructions 📝
- Create a virtual environment:</br>
     ```python3 -m venv .venv```
- Activate the virtual environment:</br>
    ```source .venv/bin/activate``` or ```.\.venv\Scripts\Activate.ps1```

- On Windows make sure to set this environment variable using powershell
```[Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User")```
- Install the package:</br>
    ```pip install faceattend```


### Windows specific issues 
- **Creating virtual environments see [here](https://docs.python.org/3/library/venv.html#creating-virtual-environments)**</br>
- **For issues with installation of the face-recognition package see [here](https://stackoverflow.com/questions/70001837/problem-in-installing-python-library-face-recognition-on-windows-10-11)**

   
## Database setup 🛢
### Create the database
```
>>> from faceattend.create_database import create_database
>>> create_database()
'Database created!'
```

### Add valid faces in database
```
>>> from faceattend.face import Face
>>> Face.add_face("Akash","Akash.jpg")
'Face added for Akash with employee id 7277962575'
```

### Remove face data from database
```
>>> from faceattend.face import Face
>>> Face.delete_face("1894559876")
'Person with emp_id 1894559876 has been removed!'
```

### Generating CSV file 
#### For a particular date
```
>>> from faceattend.attendance import Attendance
>>> Attendance.generate_csv_date("2024-03-04")
'CSV file generated!'
```
#### For a particular employee
```
>>> from faceattend.attendance import Attendance
>>> Attendance.generate_csv_emp("7277962575")
'CSV file generated!'
```
#### Employee list
```
>> from faceattend.face import Face
>>> Face.generate_emp_list()
'CSV file generated!'
```

## How to run?
```
>>> from faceattend.detect import detect_face
>>> detect_face()
```
