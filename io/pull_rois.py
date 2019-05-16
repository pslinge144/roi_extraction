import os
from osgeo import gdal


DATA_ROOT_DIR = "/media/phil/My Passport/Phil/Data"


if __name__ == "__main__":
    site_name = "Puri-Odisha"
    site_dir = os.path.join(DATA_ROOT_DIR, site_name)
    for sensor_name in os.listdir(site_dir):
        print("\nReading from", sensor_name, "\n")
        sensor_dir = os.path.join(site_dir, sensor_name)
        for filename in os.listdir(sensor_dir):
            sensor_file = os.path.join(sensor_dir, filename)
            print(gdal.Open(sensor_file).getProjection())

