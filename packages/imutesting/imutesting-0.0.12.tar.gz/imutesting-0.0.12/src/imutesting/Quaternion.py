import numpy as np


class Quater:
    def __init__(self):
        pass

    # 四元数乘法-Quaternion Multiplication
    @staticmethod
    def multiply(Q1, Q2, scalar_first=True):
        if scalar_first:
            w1, x1, y1, z1 = Q1
            w2, x2, y2, z2 = Q2
            w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
            x = x1 * w2 + w1 * x2 - z1 * y2 + y1 * z2
            y = y1 * w2 + z1 * x2 + w1 * y2 - x1 * z2
            z = z1 * w2 - y1 * x2 + x1 * y2 + w1 * z2
            multiply_result = np.array([w, x, y, z])
        else:
            x1, y1, z1, w1 = Q1
            x2, y2, z2, w2 = Q2
            w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
            x = x1 * w2 + w1 * x2 - z1 * y2 + y1 * z2
            y = y1 * w2 + z1 * x2 + w1 * y2 - x1 * z2
            z = z1 * w2 - y1 * x2 + x1 * y2 + w1 * z2
            multiply_result = np.array([x, y, z, w])

        return multiply_result

    # 四元数加法-Quaternion Addition
    @staticmethod
    def add(Q1, Q2):
        a1, b1, c1, d1 = Q1
        a2, b2, c2, d2 = Q2
        a = a1 + a2
        b = b1 + b2
        c = c1 + c2
        d = d1 + d2
        add_result = np.array([a, b, c, d])

        return add_result

    # 四元数减法-Quaternion Subtraction
    @staticmethod
    def substract(Q1, Q2):
        a1, b1, c1, d1 = Q1
        a2, b2, c2, d2 = Q2
        a = a1 - a2
        b = b1 - b2
        c = c1 - c2
        d = d1 - d2
        substract_result = np.array([a, b, c, d])

        return substract_result

    # 四元数范数-Quaternion Norm
    @staticmethod
    def norm(Quat):
        norm_result = np.linalg.norm(Quat)
        return norm_result

    # 四元数归一化-Quaternion Normalize
    @staticmethod
    def normalize(Quat):
        norm = np.linalg.norm(Quat)
        normalize_result = Quat / norm
        return normalize_result

    # 四元数共轭-Quaternion Conjugate
    @staticmethod
    def conjugate(Quat, scalar_first=True):
        if scalar_first:
            # Quat[w,x,y,z] 实部在前
            w, x, y, z = np.array(Quat)
            conjugate_result = np.array([w, -x, -y, -z])

        else:
            # Quat[x,y,z,w] 实部在后
            x, y, z, w = np.array(Quat)
            conjugate_result = np.array([-x, -y, -z, w])

        return conjugate_result

    # 四元数的逆-Quaternion Inverse
    @staticmethod
    def inverse(Quat, scalar_first=True):
        if scalar_first:
            # Quat[w,x,y,z] 实部在前
            w, x, y, z = np.array(Quat)
            conjugate = np.array([w, -x, -y, -z])
            norm = np.linalg.norm(Quat)
            inverse_result = conjugate / norm
        else:
            # Quat[x,y,z,w] 实部在后
            x, y, z, w = np.array(Quat)
            conjugate = np.array([-x, -y, -z, w])
            norm = np.linalg.norm(Quat)
            inverse_result = conjugate / norm

        return inverse_result

    @staticmethod  # 从地面坐标系到传感器坐标系
    def ground_to_sensor(ground_vector, Quat, scalar_first=True):
        if scalar_first:
            # Quat[w,x,y,z] 实部在前
            w, x, y, z = np.array(Quat)
        else:
            # Quat[x,y,z,w] 实部在后
            x, y, z, w = np.array(Quat)

        ground_to_sensor = np.array([
            [1 - 2 * y ** 2 - 2 * z ** 2, 2 * x * y + 2 * w * z, 2 * x * z - 2 * w * y],
            [2 * x * y - 2 * w * z, 1 - 2 * x ** 2 - 2 * z ** 2, 2 * y * z + 2 * w * x],
            [2 * x * z + 2 * w * y, 2 * y * z - 2 * w * x, 1 - 2 * x ** 2 - 2 * y ** 2]
        ])
        sensor_vector = np.dot(ground_to_sensor, ground_vector)
        return sensor_vector

    @staticmethod  # 从传感器坐标系到地面坐标系
    def sensor_to_ground(sensor_vector, Quat, scalar_first=True):
        if scalar_first:
            # Quat[w,x,y,z] 实部在前
            w, x, y, z = np.array(Quat).squeeze()
        else:
            # Quat[x,y,z,w] 实部在后
            x, y, z, w = np.array(Quat).squeeze()

        sensor_to_ground = np.array([
            [1 - 2 * y ** 2 - 2 * z ** 2, 2 * x * y - 2 * w * z, 2 * x * z + 2 * w * y],
            [2 * x * y + 2 * w * z, 1 - 2 * x ** 2 - 2 * z ** 2, 2 * y * z - 2 * w * x],
            [2 * x * z - 2 * w * y, 2 * y * z + 2 * w * x, 1 - 2 * x ** 2 - 2 * y ** 2]
        ])

        ground_vector = np.dot(sensor_to_ground, sensor_vector)
        return ground_vector

    @staticmethod  # 这是从载体系到地面系的旋转矩阵
    def rotation_matrix(Quat, scalar_first=True):
        if scalar_first:
            # Quat[w,x,y,z] 实部在前
            w, x, y, z = np.array(Quat).squeeze()
        else:
            # Quat[x,y,z,w] 实部在后
            x, y, z, w = np.array(Quat).squeeze()
        R = np.zeros((3, 3))
        R[0, 0] = 1 - 2 * (y * y + z * z)
        R[0, 1] = 2 * (x * y - w * z)
        R[0, 2] = 2 * (x * z + w * y)

        R[1, 0] = 2 * (x * y + w * z)
        R[1, 1] = 1 - 2 * (x * x + z * z)
        R[1, 2] = 2 * (y * z - w * x)

        R[2, 0] = 2 * (x * z - w * y)
        R[2, 1] = 2 * (y * z + w * x)
        R[2, 2] = 1 - 2 * (x * x + y * y)

        return R

    @staticmethod  # 独立的欧拉角函数，传入四元数参数进行计算
    def eulerangle(Quat, scalar_first=True):
        if scalar_first:
            # Quat[w,x,y,z] 实部在前
            w, x, y, z = np.array(Quat)
        else:
            # Quat[x,y,z,w] 实部在后
            x, y, z, w = np.array(Quat)

        roll = np.arctan2(2 * (w * x + y * z), 1 - 2 * (x ** 2 + y ** 2))
        pitch = -np.arcsin(2 * (z * x - w * y))
        yaw = np.arctan2(2 * (w * z + x * y), 1 - 2 * (y ** 2 + z ** 2))

        # 弧度制转换为角度制
        roll = np.degrees(roll)
        pitch = np.degrees(pitch)
        yaw = np.degrees(yaw)

        eulerangle_result = np.array([roll, pitch, yaw])

        return eulerangle_result
