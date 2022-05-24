from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians


class Camera:
    def __init__(self):
        self.camera_pos = Vector3([0.0, 3.0, 12.0])
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])
        self.mouse_sensitivity = 0.25
        self.normal_angle = -90
        self.pitch = 0

    def get_view_matrix(self):
        return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.normal_angle += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 80:
                self.pitch = 80
            if self.pitch < -80:
                self.pitch = -80
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.normal_angle)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.normal_angle)) * cos(radians(self.pitch))

        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0])))
        self.camera_up = vector.normalise(vector3.cross(self.camera_right, self.camera_front))

    def process_keyboard(self, direction, velocity):
        if direction == "W":
            self.camera_pos += self.camera_front * velocity
        if direction == "S":
            self.camera_pos -= self.camera_front * velocity
        if direction == "A":
            self.camera_pos -= self.camera_right * velocity
        if direction == "D":
            self.camera_pos += self.camera_right * velocity