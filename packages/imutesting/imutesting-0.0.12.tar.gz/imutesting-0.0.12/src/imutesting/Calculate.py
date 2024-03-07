import numpy as np
from Quaternion import Quater


class EKF_AHRS:
    def __init__(self, sample_dt, g_vector, Q_noise=0.1 * np.eye(4), R1_noise=3.8 * np.eye(3),
                 R2_noise=0.5 * np.eye(3)):
        # 状态量初始值 先验误差协方差矩阵
        self.x_k_minus_1 = np.array([1.0, 0.0, 0.0, 0.0]).reshape(-1, 1)
        self.P_k_minus_1 = 0.001 * np.eye(4)

        # 先验估计
        self.P_k_prior = 0
        self.x_k_prior = 0
        # 后验估计
        self.x_k_posterior = 0
        self.P_k_posterior = 0

        # 过程噪声协方差矩阵
        # self.Q_noise = 0.1 * np.eye(4)
        self.Q_noise = Q_noise
        # 观测噪声协方差矩阵 R1加速度计 R2磁力计
        # self.R1_noise = 3.8 * np.eye(3)
        self.R1_noise = R1_noise
        # self.R2_noise = 0.5 * np.eye(3)
        self.R2_noise = R2_noise

        # 所用imu输出频率200Hz
        self.dt = sample_dt
        # self.dt = 1 / 200
        self.g_vector = np.array(g_vector).reshape(-1, 1)

    # EKF 预测阶段
    def ekf_prior(self, gyro):
        # 陀螺仪
        gyro = np.array(gyro, dtype=np.float64)
        wx, wy, wz = gyro

        # 陀螺仪 Ω矩阵
        omega = np.array([
            [0, -wx, -wy, -wz],
            [wx, 0, wz, -wy],
            [wy, -wz, 0, wx],
            [wz, wy, -wx, 0]
        ])
        # 状态转移矩阵A
        A_k = np.eye(4) + 0.5 * self.dt * omega
        '''1.状态量 先验估计 '''
        self.x_k_prior = A_k @ self.x_k_minus_1
        '''2.误差协方差矩阵 先验估计 '''
        self.P_k_prior = A_k @ self.P_k_minus_1 @ A_k.T + self.Q_noise

    # EKF 更新阶段
    def ekf_posterior(self, accel, mag):
        # 此处四元数应为k时刻状态量先验估计的值
        q0, q1, q2, q3 = self.x_k_prior[0:4].squeeze()

        # 观测量 加速度计、磁力计
        accel = np.array(accel, dtype=np.float64).reshape(-1, 1)
        mag = np.array(mag, dtype=np.float64).reshape(-1, 1)

        # 单位化
        accel = accel / np.linalg.norm(accel)
        mag = accel / np.linalg.norm(mag)

        # # 载体系到地面系的四元数旋转矩阵
        # b_to_g = np.array([
        #     [1 - 2 * q2 ** 2 - 2 * q3 ** 2, 2 * q1 * q2 - 2 * q0 * q3, 2 * q1 * q3 + 2 * q0 * q2],
        #     [2 * q1 * q2 + 2 * q0 * q3, 1 - 2 * q1 ** 2 - 2 * q3 ** 2, 2 * q2 * q3 - 2 * q0 * q1],
        #     [2 * q1 * q3 - 2 * q0 * q2, 2 * q2 * q3 + 2 * q0 * q1, 1 - 2 * q1 ** 2 - 2 * q2 ** 2]
        # ])
        #
        # '''加速度计 阶段1'''
        # g_vector = np.array([0, 0, 1]).reshape(-1, 1)
        # # 加速度计观测方程h1
        # h1 = b_to_g.T @ g_vector
        '''加速度计 阶段1'''
        h1 = Quaternion.sensor_to_ground(self.g_vector, self.x_k_prior)
        # 雅克比矩阵H1
        H1 = np.array([
            [-2 * q2, 2 * q3, -2 * q0, 2 * q1],
            [2 * q1, 2 * q0, 2 * q3, 2 * q2],
            [2 * q0, -2 * q1, -2 * q2, 2 * q3],
        ])

        '''3.卡尔曼增益 Kk1'''
        Kk1 = self.P_k_prior @ H1.T @ np.linalg.inv(H1 @ self.P_k_prior @ H1.T + self.R1_noise)

        # 加速度计观测量 残差
        r_k1 = accel - h1
        state1 = Kk1 @ r_k1

        # 不影响偏航角 将q3置为0
        state1[3][0] = 0

        '''4.状态量 后验估计1'''
        self.x_k_posterior = self.x_k_prior + state1
        '''5.误差协方差矩阵 后验估计1'''
        self.P_k_posterior = (np.eye(4) - Kk1 @ H1) @ self.P_k_prior

        '''磁力计 阶段2'''
        # 磁力计观测方程h2
        # h_ground = b_to_g @ mag
        h_ground = Quaternion.sensor_to_ground(mag, self.x_k_prior)
        b_ground = np.array([
            [np.sqrt(h_ground[0][0] ** 2 + h_ground[1][0] ** 2)],
            [0],
            [h_ground[2][0]],
        ])
        bx, by, bz = b_ground.squeeze()
        # h2 = b_to_g.T @ b_ground
        h2 = Quaternion.sensor_to_ground(b_ground, self.x_k_prior)
        # 雅克比矩阵H2
        H2 = np.array([
            [2 * q0 * bx - 2 * q2 * bz, 2 * q1 * bx + 2 * q3 * bz, -2 * q2 * bx - 2 * q0 * bz,
             -2 * q3 * bx + 2 * q1 * bz],
            [-2 * q3 * bx + 2 * q1 * bz, 2 * q2 * bx + 2 * q0 * bz, 2 * q1 * bx + 2 * q3 * bz,
             -2 * q0 * bx + 2 * q2 * bz],
            [2 * q2 * bx + 2 * q0 * bz, 2 * q3 * bx - 2 * q1 * bz, 2 * q0 * bx - 2 * q2 * bz, 2 * q1 * bx + 2 * q3 * bz]
        ])

        '''3.卡尔曼增益 Kk2'''
        Kk2 = self.P_k_prior @ H2.T @ np.linalg.inv(H2 @ self.P_k_prior @ H2.T + self.R2_noise)

        # 磁力计观测量 残差
        r_k2 = mag - h2
        state2 = Kk2 @ r_k2
        # 不影响俯仰角、翻滚角 将q1 q2置为0
        state2[1][0] = 0
        state2[2][0] = 0
        '''4.状态量 后验估计2'''
        self.x_k_posterior = self.x_k_posterior + state2
        # 对状态量四元数归一化
        # self.x_k_posterior = Normalize.ekf_q(self.x_k_posterior)
        self.x_k_posterior = Quaternion.normalize(self.x_k_posterior)
        '''5.误差协方差矩阵 后验估计2'''
        self.P_k_posterior = (np.eye(4) - Kk2 @ H2) @ self.P_k_posterior

    # 姿态角
    def updata_angle(self):
        # 取出四元数
        # q0, q1, q2, q3 = self.x_k_posterior.squeeze()
        eulerangle = Quaternion.eulerangle(self.x_k_posterior)
        return eulerangle

    # EKF 应用
    def ekf_apply(self, accel, gyro, mag):
        # 预测
        self.ekf_prior(gyro)
        # 更新
        self.ekf_posterior(accel, mag)
        # 姿态角
        eulerangle = self.updata_angle()
        roll, pitch, yaw = eulerangle.squeeze()
        '''将更新的状态量以及误差协方差矩阵 后验值作为k-1时刻的值，以便下一次EKF过程'''
        self.x_k_minus_1 = self.x_k_posterior
        self.P_k_minus_1 = self.P_k_posterior
        q0, q1, q2, q3 = self.x_k_posterior[0:4].squeeze()
        quat = np.array([q0, q1, q2, q3])
        return roll, pitch, yaw, quat
