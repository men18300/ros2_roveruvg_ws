from setuptools import setup

package_name = 'odometry_pkg'

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
    maintainer='diego',
    maintainer_email='77988142+men18300@users.noreply.github.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'hardware_arduino_odometry = odometry_pkg.hardware_arduino_wheels:main',
        'dwm1001_odometry = odometry_pkg.node_dwm1001:main',
        'optitrack_odometry = odometry_pkg.optitrack_client:main',
        ],
    },
)
