import sys
import os
import pydicom


def check_dicom_compression_in_folder(folder_path):
    compressed_count = 0
    uncompressed_count = 0
    i = 0

    # Loop through files in the folder
    for file_name in os.listdir(folder_path):
        i += 1
        file_path = os.path.join(folder_path, file_name)

        # Check if the file is a DICOM image
        if os.path.isfile(file_path) and file_path.lower().endswith(".dcm"):
            # Load the DICOM image
            dicom_image = pydicom.dcmread(file_path)

            # Check image dimensions
            try:
                rows = dicom_image.Rows
                columns = dicom_image.Columns
                print(f"{i} File: {file_name}, Resolution: {columns}x{rows}")
            except AttributeError:
                print(f"{i} File: {file_name} does not have resolution information.")
                continue

            # Check if compression information is available
            is_compressed = (
                dicom_image.file_meta.TransferSyntaxUID
                and dicom_image.file_meta.TransferSyntaxUID.is_compressed
            )
            print(dicom_image.file_meta.TransferSyntaxUID, is_compressed)
            if is_compressed:
                uid_compression = dicom_image.file_meta.TransferSyntaxUID
                print(f"{i} File: {file_name}, Compression UID: {uid_compression}")
                compressed_count += 1
            else:
                print(f"{i} File: {file_name}, NOT COMPRESSED")
                uncompressed_count += 1
        else:
            print(f"The file {file_name} is not a DICOM image.")

    print(f"\nTotal files with compression: {compressed_count}")
    print(f"Total files without compression: {uncompressed_count}")


# Example usage: specify the path to the folder containing DICOM images
if __name__ == "__main__":
    folder_path = sys.argv[1]
    check_dicom_compression_in_folder(folder_path)
