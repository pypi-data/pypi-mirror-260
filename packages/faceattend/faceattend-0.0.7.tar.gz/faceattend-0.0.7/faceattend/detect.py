import face_recognition
import cv2
import numpy as np
from faceattend.face import Face
from faceattend.attendance import Attendance


def detect_face():

    # Get the valid face data from database
    known_face_encodings, known_face_names = Face.load_faces()

    # Initialize variables
    face_names = []
    face_locations = []
    face_encodings = []
    process_this_frame = True

    # start video capture
    video_capture = cv2.VideoCapture(0)

    while True:
        # Grab a single frame of video
        _, frame = video_capture.read()

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations, 1
            )

            face_names = []
            attendance_face_encodings = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding, tolerance=0.5
                )
                name = "Stranger"

                # the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding
                )
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    encoding = known_face_encodings[best_match_index]
                if name in face_names:
                    continue
                face_names.append(name)
                if name != "Stranger":
                    attendance_face_encodings.append(encoding)

        Attendance.mark_attendance(attendance_face_encodings)
        process_this_frame = not process_this_frame
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a red box around the unknown face and green box around the known face
            if name == "Stranger":
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label  below the face
                cv2.rectangle(
                    frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
                )
            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                cv2.rectangle(
                    frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED
                )
            # Add the name to the label
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 1)

        # Display the resulting image
        cv2.imshow("Attendance", frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_face()
