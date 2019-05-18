import os
import shutil
from osgeo import gdal


DATA_ROOT_DIR = "/media/phil/My Passport/Phil/Data"


if __name__ == "__main__":
    site_name = "Puri-Odisha"
    site_dir = os.path.join(DATA_ROOT_DIR, site_name)
    for sensor_name in os.listdir(site_dir):
        print("\nReading from", sensor_name, "\n")
        sensor_dir = os.path.join(site_dir, sensor_name)
        filenames = [f for f in os.listdir(sensor_dir) if
                not os.path.isdir(os.path.join(sensor_dir, f))]
        for filename in filenames:
            sensor_file = os.path.join(sensor_dir, filename)
            out_sensor_dir = os.path.splitext(sensor_file)[0]
            if not os.path.exists(out_sensor_dir):
                print("\t" + filename)
                try:
                    sensor_file_extracted = shutil.unpack_archive(sensor_file,
                            out_sensor_dir)
                except EOFError:
                    print("\t\t-----SKIPPED------")

