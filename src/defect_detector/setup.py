from setuptools import find_packages, setup

package_name = 'defect_detector'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shivanshmishra',
    maintainer_email='shivanshmishra@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'inference_node = defect_detector.inference_node:main',
             'decision_node = defect_detector.decision_node:main',
            'actuator_node = defect_detector.actuator_node:main',
             ],
    },
)
