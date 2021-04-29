from setuptools import setup

setup(
    name='camera-security-rpi',
    version='0.1.0',
    packages=['camera_security', 'camera_security.image',
              'camera_security.image.processing', 'camera_security.image.serializers', 'camera_security.program', 'camera_security.utility',
              'camera_security.utility.exceptions', 'camera_security.utility.serializers', 'camera_security.monitoring',
              'camera_security.monitoring.alerts', 'camera_security.monitoring.serializers',
              'camera_security.communication', 'camera_security.communication.requests', 'camera_security.communication.responses',
              'camera_security.communication.serializers', 'camera_security.authentication'],
    url='https://github.com/lzaromskis/camera-security-rpi',
    license='GNUv3',
    author='Lukas Žaromskis',
    author_email='lzaromskis@gmail.com',
    description='Camera security'
)
