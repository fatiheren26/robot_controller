from setuptools import setup

package_name = 'automatic_mover'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='fatih',
    maintainer_email='fatih@todo.todo',
    description='Robotu hedefe götüren basit node',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'move_node = automatic_mover.move_node:main',
        ],
    },
)
