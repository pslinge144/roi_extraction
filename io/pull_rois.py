import os
import shutil
from osgeo import gdal


DATA_ROOT_DIR = "/media/phil/My Passport/Phil/Data"


def extract_all_compressed_files_from_site(site_name):
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


def store_poi_chips(site_name, poi, chip_size=(256, 256)):
    site_dir = os.path.join(DATA_ROOT_DIR, site_name)
    for sensor_name in os.listdir(site_dir):
        print("\nReading from", sensor_name, "\n")
        sensor_dir = os.path.join(site_dir, sensor_name)
        image_dirs = [os.path.join(sensor_dir, f) for f in os.listdir(sensor_dir) if
                os.path.isdir(os.path.join(sensor_dir, f))]
        for image_dir in image_dirs:
            band_8 = [f for f in os.listdir(image_dir) if f.endswith("B8.TIF")]
            band_8 = band_8[0]
            image_path = os.path.join(sensor_dir, image_dir, band_8)
            img_ds = gdal.Open(image_path)
            img_gt = img_ds.GetGeoTransform()

            inv_gt = gdal.InvGeoTransform(img_gt)
            
            offset_center = gdal.ApplyGeoTransform(
                    inv_gt, poi["utm"]["center_x"],
                    poi["utm"]["center_y"])
            off_cx, off_cy = map(int, offset_center)

            gtiff_driver = gdal.GetDriverByName('GTiff')
            out_ds = gtiff_driver.Create("CHIPPED_" + band_8, chip_size[0],
                    chip_size[1], 1)
            out_ds.SetProjection(img_ds.GetProjection())
            subset_cx, subset_cy = gdal.ApplyGeoTransform(
                    img_gt, off_cx, off_cy)
            subset_cx -= chip_size[0] // 2
            subset_cy -= chip_size[1] // 2
            out_gt = list(img_gt)
            out_gt[0] = subset_cx
            out_gt[3] = subset_cy
            out_ds.SetGeoTransform(out_gt)

            in_band = img_ds.GetRasterBand(1)
            out_band = out_ds.GetRasterBand(1)
            data = in_band.ReadAsArray(
                    off_cx - chip_size[0] // 2,
                    off_cy - chip_size[1] // 2,
                    chip_size[0],
                    chip_size[1])
            out_band.WriteArray(data)
        del out_ds



if __name__ == "__main__":
    site_names = ["Puri-Odisha", "Geoje, South Korea"]

    pois = [{"name": "puri",
            "utm": {"center_x": 377589, "center_y": 2191230}},
            {"name": "geoje",
                "utm": {"center_x": 465350, "center_y": 3859863}}]
    for i in range(len(pois)):
        poi = pois[i]
        site_name = site_names[i]

        print(poi["name"])
        extract_all_compressed_files_from_site(site_name)

        store_poi_chips(site_name, poi, chip_size=(1024, 1024))



